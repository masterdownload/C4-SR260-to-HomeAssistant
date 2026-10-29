# SPDX-License-Identifier: Apache-2.0
# Original contributions attributed to masterdownload; see docs/attribution.md.
"""Offline first-use checks using real ZHA conversion and a fake radio."""

import asyncio
import os
from pathlib import Path
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, os.environ.get(
    "C4_QUIRK_DIR", str(Path(__file__).resolve().parents[1] / "quirks"),
))

from jinja2 import StrictUndefined
from jinja2.nativetypes import NativeEnvironment
import yaml
import zigpy.exceptions
from zha.application.helpers import convert_to_zcl_values
from zigpy.quirks import CustomCluster

import c4_button_cluster as B
import c4_display_cluster as D
import c4_helpers as H


class FakeDevice:
    ieee = "00:0f:ff:00:00:aa:bb:cc"

    def __init__(self):
        self.endpoints = {}
        self.sent = []
        self.calls = 0
        self.fail_on = set()
        self.delay = 0

    def get_sequence(self):
        return self.calls & 0xFF

    async def request(self, **kwargs):
        self.calls += 1
        if self.calls in self.fail_on:
            raise zigpy.exceptions.DeliveryError("fake sleeping radio")
        await asyncio.sleep(self.delay)
        self.sent.append(kwargs["data"])


def rig():
    device = FakeDevice()
    endpoint = SimpleNamespace(
        device=device, endpoint_id=1, in_clusters={}, out_clusters={},
    )
    device.endpoints[1] = endpoint
    display = D.C4SR260DisplayCluster(endpoint, is_server=True)
    endpoint.in_clusters[H.C4_DISPLAY_CLUSTER_ID] = display
    return device, display


class FirstUseTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.device, self.display = rig()
        self.now = 100.0
        self.clock_patch = patch.object(
            D, "time", SimpleNamespace(monotonic=lambda: self.now),
        )
        self.clock_patch.start()
        self.addCleanup(self.clock_patch.stop)

    async def prepare(self, **overrides):
        params = dict(
            room="Test Room", line2="Vol 35", show_header=1, color=224,
            sync_clock=1, hour=12, minute=34, second=56, weekday=4, wake=0,
        )
        params.update(overrides)
        schema = self.display.server_commands[6].schema
        converted = convert_to_zcl_values(params, schema)
        await self.display.prepare_display(**converted)

    def namespaces(self):
        return [data.split()[1].decode("ascii") for data in self.device.sent]

    async def test_first_button_prioritizes_header_and_color_before_clock(self):
        await self.prepare()
        self.assertEqual(self.namespaces(), ["c4.ln.ri", "c4.zr.tc", "c4.zr.tm"])
        self.assertIn(b'"Test Room" "Vol 35"', self.device.sent[0])
        self.assertTrue(all(len(data) <= 70 for data in self.device.sent))
        self.assertEqual(self.display._setup_done, {"header", "color", "clock"})

    async def test_successful_setup_does_not_repeat_on_keys_or_volume_changes(self):
        await self.prepare()
        self.now += 2
        await self.prepare(line2="Vol 50", second=58)
        await self.prepare()
        self.assertEqual(len(self.device.sent), 3)

    async def test_changed_room_color_and_enable_flags_initialize_on_next_key(self):
        await self.prepare()
        await self.prepare(room="Other Room", color=28)
        self.assertEqual(len(self.device.sent), 6)
        self.assertIn(b'"Other Room"', self.device.sent[3])
        await self.prepare(room="Other Room", color=-1, sync_clock=0)
        self.assertEqual(len(self.device.sent), 7)

    async def test_disabled_settings_and_header_opt_out_are_respected(self):
        await self.prepare(show_header=0, color=-1, sync_clock=0)
        self.assertEqual(self.device.sent, [])
        await self.prepare(show_header=0)
        self.assertEqual(self.namespaces(), ["c4.zr.tc", "c4.zr.tm"])

    async def test_wake_refreshes_but_nearby_press_and_duplicate_wake_deduplicate(self):
        await asyncio.gather(self.prepare(wake=1), self.prepare(), self.prepare(wake=1))
        self.assertEqual(len(self.device.sent), 3)
        self.now += 10
        await self.prepare(wake=1)
        self.assertEqual(len(self.device.sent), 6)

    async def test_first_press_then_immediate_wake_does_not_leave_spurious_pending_work(self):
        await self.prepare()
        self.now += 0.1
        await self.prepare(wake=1)
        self.now += 2
        await self.prepare()
        self.assertEqual(len(self.device.sent), 3)

    async def test_failure_retains_only_unsent_settings_and_waits_for_later_event(self):
        self.device.fail_on = {2}
        with self.assertLogs(D.__name__, level="WARNING"):
            await self.prepare()
        self.assertEqual(self.display._setup_done, {"header"})
        await self.prepare()
        self.assertEqual(self.device.calls, 2)
        self.now += 1
        await self.prepare()
        self.assertEqual(self.namespaces(), ["c4.ln.ri", "c4.zr.tc", "c4.zr.tm"])

    async def test_three_failed_attempts_stop_until_next_wake_or_configuration_change(self):
        self.device.fail_on = set(range(1, 100))
        with self.assertLogs(D.__name__, level="WARNING"):
            for _ in range(10):
                await self.prepare()
                self.now += 1
        self.assertEqual(self.device.calls, 3)
        with self.assertLogs(D.__name__, level="WARNING"):
            await self.prepare(wake=1)
            await self.prepare(room="Reassigned")
        self.assertEqual(self.device.calls, 5)

    async def test_no_retry_timer_is_created(self):
        self.device.fail_on = {1}
        with self.assertLogs(D.__name__, level="WARNING"):
            await self.prepare()
        self.now += 10
        await asyncio.sleep(0.02)
        self.assertEqual(self.device.calls, 1)

    async def test_radio_timeout_is_bounded_and_leaves_settings_pending(self):
        self.device.delay = 10
        started = time.monotonic()
        with self.assertLogs(D.__name__, level="WARNING"):
            await self.prepare()
        self.assertLess(time.monotonic() - started, 0.65)
        self.assertEqual(self.display._setup_done, set())
        self.assertFalse(self.display._display_lock.locked())
        await asyncio.sleep(0)
        self.device.delay = 0
        self.now += 1
        await self.prepare()
        self.assertEqual(len(self.device.sent), 3)

    async def test_waiting_for_a_menu_lock_is_also_bounded(self):
        await self.display._display_lock.acquire()
        started = time.monotonic()
        try:
            with self.assertLogs(D.__name__, level="WARNING"):
                await self.prepare()
            self.assertLess(time.monotonic() - started, 0.65)
            self.assertEqual(self.device.calls, 0)
        finally:
            self.display._display_lock.release()
        await self.prepare()
        self.assertEqual(len(self.device.sent), 3)

    async def test_active_menu_is_never_closed_or_replaced_by_initialization(self):
        await self.display.show_list("Watch", "Movie|TV", 1, context="watch#test")
        menu = self.display._active_menu
        self.device.sent.clear()
        await self.prepare()
        self.assertIs(self.display._active_menu, menu)
        self.assertEqual(self.namespaces(), ["c4.zr.tc", "c4.zr.tm"])
        self.assertNotIn("header", self.display._setup_done)

    async def test_first_menu_keys_open_the_menu_after_setup_without_equipment_actions(self):
        for title in ("Watch", "Listen", "Room"):
            device, display = rig()
            await display.prepare_display("Test", "", 1, 224, 1, 12, 0, 0, 4, 0)
            await display.show_list(title, "First|Second", 0, context="root#test")
            self.assertEqual(display._active_menu["title"], title)
            self.assertEqual(
                [data.split()[1] for data in device.sent],
                [b"c4.ln.ri", b"c4.zr.tc", b"c4.zr.tm", b"c4.ln.sl"],
            )

    async def test_simultaneous_menu_open_and_setup_never_write_header_after_menu(self):
        await asyncio.gather(
            self.display.show_list("Room", "Lamp|Fan", 0, show_selection=0),
            self.prepare(wake=1),
        )
        self.assertEqual(self.namespaces(), ["c4.ln.sl", "c4.zr.tc", "c4.zr.tm"])
        self.assertEqual(self.display._active_menu["title"], "Room")

    async def test_devices_have_independent_pending_state(self):
        await self.prepare()
        device, display = rig()
        await display.prepare_display("Test Room", "", 1, 224, 1, 12, 0, 0, 4, 0)
        self.assertEqual(len(device.sent), 3)
        self.assertIsNot(self.display._setup_done, display._setup_done)

    async def test_invalid_parameters_do_not_touch_state_or_radio(self):
        for overrides in ({"color": 256}, {"hour": 24}, {"weekday": 7}):
            with self.assertRaises(ValueError):
                await self.prepare(**overrides)
        self.assertIsNone(self.display._setup_fingerprint)
        self.assertEqual(self.device.calls, 0)

    async def test_headers_keep_existing_normalization_and_frame_limit(self):
        await self.prepare(room='Caf\u00e9 "Room"\\x', line2="L" * 50)
        self.assertIn(b'"Cafe Room/x"', self.device.sent[0])
        self.assertIn(b'"' + b"L" * 22 + b'"', self.device.sent[0])
        self.assertLessEqual(len(self.device.sent[0]), 70)

    async def test_startup_never_sends_model_or_cached_splash(self):
        async def initialize(cluster, from_cache=False):
            pass

        with patch.object(CustomCluster, "async_initialize", initialize, create=True):
            await self.display.async_initialize()
            self.display._update_attribute(0, "Old splash")
            await self.display.async_initialize(from_cache=True)
        self.assertEqual(self.device.sent, [])

    async def test_existing_menu_selection_and_cancel_context_are_preserved(self):
        endpoint = SimpleNamespace(
            device=self.device, endpoint_id=197, in_clusters={}, out_clusters={},
        )
        self.device.endpoints[197] = endpoint
        button = B.C4RemoteButtonCluster(endpoint, is_server=True)
        events = []
        recorder = SimpleNamespace(zha_send_event=lambda *args: events.append(args))
        button.add_listener(recorder)
        await self.display.show_list("Fan", "Off|High", 0, 0, "fan#abc")
        menu_id = self.display._active_menu["list_id"]
        button._fire_menu_select(menu_id, 1)
        await asyncio.sleep(0.01)
        self.assertEqual(events[0][0], "menu_select")
        self.assertEqual(events[0][1]["context"], "fan#abc")
        self.assertEqual(events[0][1]["item"], "High")
        await self.display.show_list("Heat", "19 C|20 C", 0, 0, "Heat#abc")
        button._fire_menu_cancel(self.display._active_menu["list_id"], 0)
        await asyncio.sleep(0.01)
        self.assertEqual(events[1][0], "menu_cancel")
        self.assertEqual(events[1][1]["context"], "Heat#abc")

    async def test_existing_command_ids_stay_stable(self):
        self.assertEqual(
            {key: command.name for key, command in self.display.server_commands.items()},
            {0: "show_list", 1: "close_list", 2: "send_raw", 3: "set_header",
             4: "set_clock", 5: "set_text_color", 6: "prepare_display"},
        )

    async def test_single_row_paging_keeps_request_sequence_and_later_offsets(self):
        endpoint = SimpleNamespace(
            device=self.device, endpoint_id=197, in_clusters={}, out_clusters={},
        )
        self.device.endpoints[197] = endpoint
        button = B.C4RemoteButtonCluster(endpoint, is_server=True)
        await self.display.show_list("Watch", "Alpha|Beta", 0, context="watch#test")
        list_id = self.display._active_menu["list_id"]
        self.device.sent.clear()
        await button._answer_gi_request(list_id, 0, 2, "0123")
        await button._answer_gi_request(list_id, 1, 2, "0124")
        self.assertEqual(self.device.sent, [
            b'0r0123 000 "\x01Alpha"\r\n',
            b'0r0124 000 "\x01Beta"\r\n',
        ])

    async def test_unexpected_errors_propagate_and_external_cancellation_releases_lock(self):
        with patch.object(self.device, "request", side_effect=RuntimeError("fake defect")):
            with self.assertRaises(RuntimeError):
                await self.prepare()
        self.assertFalse(self.display._display_lock.locked())
        self.now += 1
        self.device.delay = 10
        task = asyncio.create_task(self.prepare())
        await asyncio.sleep(0.01)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertFalse(self.display._display_lock.locked())

    async def test_cancellation_resistant_transport_blocks_late_menu_clobbering(self):
        release = asyncio.Event()

        async def resistant_request(**kwargs):
            try:
                await release.wait()
            except asyncio.CancelledError:
                await release.wait()
            self.device.sent.append(kwargs["data"])

        started = time.monotonic()
        with patch.object(self.device, "request", resistant_request):
            with self.assertLogs(D.__name__, level="WARNING"):
                await self.prepare()
            self.assertLess(time.monotonic() - started, 0.65)
            self.assertFalse(self.display._setup_send_task.done())
            with self.assertRaises(RuntimeError):
                await self.display.show_list("Watch", "TV", 0)
            release.set()
            await self.display._setup_send_task
        self.assertEqual(self.namespaces(), ["c4.ln.ri"])
        await self.display.show_list("Watch", "TV", 0)
        self.assertEqual(self.namespaces(), ["c4.ln.ri", "c4.ln.sl"])

class BlueprintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class Loader(yaml.SafeLoader):
            pass

        Loader.add_constructor(
            "!input", lambda loader, node: "input:" + loader.construct_scalar(node),
        )
        path = Path(os.environ.get(
            "C4_BLUEPRINT_PATH",
            str(Path(__file__).resolve().parents[1] / "blueprint" / "c4_sr260_room_remote.yaml"),
        ))
        cls.blueprint = yaml.load(path.read_text(encoding="utf-8"), Loader=Loader)
        cls.templates = NativeEnvironment(undefined=StrictUndefined)

    def context(self, trigger="press", button="watch"):
        return dict(
            trigger=SimpleNamespace(id=trigger), button=button,
            show_header=True, sync_clock=True, set_text_color=True,
            watch_list=[{"label": "TV", "target": "scene.test"}],
            listen_list=[{"label": "Radio", "target": "scene.test"}],
            room_list=[{"text": "Lamp", "entity": "light.test"}],
            key_target="", media_key_target="", volume_target="",
            remote_target="remote.test", cmd="", media_key_valid=True,
            menu_titles_valid=True, room_titles_valid=True,
            watch_title="Watch", listen_title="Listen", room_title="Room",
            room_feedback=False, run_entity="", pick_entity="",
        )

    def render(self, name, context):
        value = self.templates.from_string(self.blueprint["variables"][name]).render(context)
        return value.strip() if isinstance(value, str) else ("" if value is None else value)

    def test_first_menu_press_routes_to_only_its_existing_menu(self):
        for button, expected in (("watch", "Watch"), ("listen", "Listen"), ("list", "Room")):
            with self.subTest(button=button):
                context = self.context(button=button)
                context["situation"] = self.render("situation", context).strip()
                self.assertEqual(self.render("menu_title", context).strip(), expected)
                self.assertEqual(self.render("svc", context).strip(), "")
                self.assertEqual(self.render("screen_text", context).strip(), "")
                self.assertTrue(self.templates.from_string(
                    self.blueprint["actions"][0]["if"][0],
                ).render(context))

    def test_unmapped_first_key_still_prepares_without_equipment_actions(self):
        context = self.context(button="digit_1")
        context["remote_target"] = ""
        context["situation"] = self.render("situation", context).strip()
        self.assertEqual(context["situation"], "none")
        self.assertEqual(self.render("svc", context).strip(), "")
        self.assertTrue(self.templates.from_string(
            self.blueprint["actions"][0]["if"][0],
        ).render(context))

    def test_preparation_does_not_run_on_hold_release_or_menu_events(self):
        condition = self.templates.from_string(self.blueprint["actions"][0]["if"][0])
        for trigger in ("hold", "release", "menu", "menu_cancel"):
            self.assertFalse(condition.render(self.context(trigger=trigger)))
        context = self.context()
        context.update(show_header=False, set_text_color=False, sync_clock=False)
        self.assertFalse(condition.render(context))

    def test_wake_has_no_equipment_or_menu_action(self):
        context = self.context(trigger="wake")
        context["situation"] = self.render("situation", context).strip()
        self.assertEqual(context["situation"], "wake")
        self.assertEqual(self.render("svc", context).strip(), "")
        self.assertEqual(self.render("menu_title", context).strip(), "")

    def test_new_service_failure_cannot_abort_existing_key_action(self):
        prepare = self.blueprint["actions"][0]
        self.assertEqual(prepare["then"][-1]["data"]["command"], 6)
        self.assertTrue(prepare["then"][-1]["continue_on_error"])
        self.assertNotIn("stop", prepare)
        self.assertEqual(self.blueprint["actions"][2]["then"][-1]["data"]["command"], 0)

    def test_header_and_post_volume_refresh_share_the_existing_templates(self):
        prepare_values = self.blueprint["actions"][0]["then"][0]["variables"]
        refresh_values = self.blueprint["actions"][-1]["then"][1]["variables"]
        self.assertIs(prepare_values, refresh_values)
        level = [0.35]
        context = dict(
            volume_target="media_player.test", show_volume=True,
            volume_precision="decimal", volume_style="number", header_line2="",
            states=lambda entity: "on",
            state_attr=lambda entity, key: level[0] if key == "volume_level" else None,
            is_state_attr=lambda *args: False,
        )
        for value, expected in ((0.35, "Vol 35.0%"), (0.50, "Vol 50.0%")):
            level[0] = value
            for name, template in prepare_values.items():
                rendered = self.templates.from_string(template).render(context)
                context[name] = rendered.strip() if isinstance(rendered, str) else rendered
            self.assertEqual(context["vol_line"].strip(), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
