# Troubleshooting

Start with a backup, [installation checks](install.md) and
[safety/recovery](safety.md). Do not treat a successful offline test, model
label or manifest comparison as proof of physical behavior.

| Symptom | Check and next action |
|---|---|
| No ZHA coordinator | Configure ZHA with its own supported coordinator; do not reuse the radio owned by Zigbee2MQTT |
| Quirks do not load | All 15 files must be flat in the directory configured by `custom_quirks_path`; inspect startup import errors; fully restart after changes |
| Existing custom quirks stop working | Restore the prior path and files; never redirect ZHA away from an existing custom directory |
| Remote stays unknown | Confirm updated quirks loaded after a full restart, wake the remote, and inspect discovery logs; identification requires the real model attribute, not just the address prefix. Reconfigure an incomplete interview; use the documented manual fallback only for a confirmed SR-260 |
| Files are in the wrong directory | Move the package files into the existing configured directory, keeping other quirks intact |
| `BUTTON_7` / `BUTTON_8` import error | Check that this package's `c4_helpers.py`, including its compatibility fallback, is installed; do not mix versions |
| Keys produce no events | Listen to `zha_event`, wake the remote and press a key; confirm Control4 / C4-SR260 and active quirk/key triggers, not only a cache entry. Rebuild errors need investigation before resets |
| Automatic identity was learned but activation failed | Check the explicit lifecycle error in ZHA logs; supported zigpy/ZHA rebuild APIs are required. A restart after model learning is a fallback; don't repeatedly delete/rejoin |
| Recognized remote still sends only Device Announce | Model/class matching is not application registration. Install the current response-first quirks and fully restart once, then check actual events and registration errors; a blueprint-only update or repeated resets will not establish the missing handshake |
| Model cache cannot be read or saved | Preserve it and its backup, inspect JSON/permissions, and restart after a deliberate repair. Automatic persistence refuses to overwrite an unreadable cache |
| Events arrive but no action | Inspect automation enabled state, chosen remote, target entities and trace; make sure only the intended automation owns that remote |
| Key events arrive for a different device than the automation | Select the replacement remote in that automation while preserving its other inputs; discovery does not migrate old device references |
| List works but the room-name header seems blank | Let the screen go completely dark, wait a few seconds, then pick up without pressing a key. Check the wake-text/header settings and a real wake event; pressing keys on an already-awake remote is not that test |
| TV key does nothing | Verify the target `remote` entity and its integration-specific command names; Roku defaults are not universal |
| Screen misses an update | The radio sleeps; test immediately after a remote event, not an arbitrary delayed push; reduce avoidable delays |
| Wrong menu opens or selection runs wrong row | Use distinct menu titles and unique short row labels; compare saved inputs and automation trace |
| List shows state but every selection is ignored with a padded menu title | Update the blueprint: configured/output/incoming titles now share trimming and quote/newline handling. Saved titles need not be rewritten. Duplicate normalized titles/labels still reject explicitly |
| Fan only used to toggle, or a control is missing | Updated fan rows open a capability-driven submenu. Oscillation/presets/direction require the fan to be on and supported; direction must be reported. Missing/invalid speed step uses generic percentage choices, not invented speed levels |
| Fan selection says stale/ambiguous | Reopen List after state/capabilities/layout changed; keep preset labels unambiguous after truncation. No action is sent on a mismatch |
| Thermostat only shows read-only targets | Confirm the entity reports valid targets, minimum/maximum and a positive temperature step, and is not off/unavailable; supported mode choices can turn an off thermostat back on |
| Thermostat displays H/C but does not seem to heat or cool | H/C is the configured Heat/Cool mode, not active HVAC action; the package does not invent missing active-heating/cooling status |
| Set/Heat/Cool picker has fewer than eleven rows | Bounds, the opposite range endpoint or unrepresentable values remove alternatives without clamping/duplication/backfill; the marked current row is read-only and initially selected |
| Choosing the marked current row does nothing | Intentional: it reopens the same picker without a thermostat command. Choose another numeric row to change the target |
| Single thermostat still shows Warmer/Cooler | Update the blueprint and reload automations while preserving saved inputs; the consistent picker uses Set. No quirk restart is needed for this blueprint-only update |
| Temperature numbers look right but the unit is wrong | Set Room controls > Temperature unit to match HA in each automation. Celsius is the default; labels are manual, not detection or conversion. Fahrenheit installs must select Fahrenheit explicitly |
| Degree symbol is absent or wrong | The updated climate labels intentionally use ASCII space F/C; no numeric conversion. Older blueprint paths still produce their own old label text |
| Physical picker order differs from sorted HA rows | The experimental helper returns one complete row per request; one Cool picker now has owner-confirmed correct ordering/ASCII labels. Update matching helper/restart once, but verify your own display. Do not sort the already-sorted source again or select a dubious row |
| A thermostat selection refreshes without changing the target | Its target/mode/step/limits or room layout may have changed. Reopen with List; do not reuse an old picker. Room names must be unique; new clean-title menus require hidden context from the matching updated quirks |
| Fan/thermostat menu title shows a hash | An older blueprint is still in use. The clean-title revision moves routing into optional local metadata; install matching display/button quirks and fully restart before switching its blueprint |
| Chosen Room row remains on screen | Check that blueprint and all quirks match v0.1 and `room_feedback` is off; the silent-choice implementation still needs physical confirmation |
| Battery is unknown | The native Battery diagnostic waits for a valid passive `c4.zr.bl` report; no fake initial value or active poll is used. Other status attributes are not substituted |
| Battery entity is missing | Load all matching updated quirks and fully restart; known SR-260 power classification is corrected so native ZHA can discover it. Check whether the entity was disabled manually |
| LQI/RSSI is empty | Diagnostic values can remain empty and are not by themselves proof the remote is offline |
| Media-key scene/automation repeats unexpectedly | Overrides run on short press only; inspect traces for duplicate automations or multiple real press events. Hold-only events do not repeat overrides |
| A key no longer sends its remote command | A selected optional scene/automation override takes priority. Clear it to restore the command and its existing repeats |
| `quirk_applied: false` despite working events | That flag was misleading in the reported setup; inspect actual device behavior, class/loading evidence and event flow |
| No signal-bars icon | Its behavior is unresolved; use received events instead of the remote's icon as the connectivity check |
| Update broke startup | Restore the prior known-good quirk files and configuration, then fully restart; see recovery before changing the Zigbee network |

## File versions

Keep the 15 quirks and blueprint from the same package version. Compare
unexpected changes with your backup before replacing files.
`MANIFEST.sha256` records checksums for those files with CRLF normalized to LF.
It is an optional integrity reference, not something you need to run to install.
Checksums detect differences, not author identity or a trustworthy download.

Automatic discovery sends a bounded controller-identity exchange and model
attribute query while the remote is awake. It does not identify a sleeping
device or infer its model from `00:0f:ff`. Limits and compatibility are in
[recognition checks](install.md#3-check-automatic-recognition). This also does
not migrate an automation from an old remote to a newly paired replacement.

If a capture shows only Device Announce and no private-profile identity poll,
use the updated announce-trigger hook; the first discovery implementation
missed this cold-start path. Normal Zigbee join processing still runs first,
and a model response is required before activation. A transmitted query alone
is not evidence of successful recognition.

The experimental registration sequence adds an unsolicited controller identity
response before the identity report and bounded global MTORR for verified/cached
SR-260s. The earlier report/MTORR-only physical attempt did not restore key
traffic. Response/report delivery errors, non-success MTORR statuses and
unsupported radio backends are explicit in logs. No new attribute values,
firmware or undocumented ASCII settings are part of this variation.
The response-first form enabled actual keys/menus on one observed replacement,
and its wake header was owner-confirmed. Do not confuse that scoped acceptance
with a guarantee of uncached first joins or all v0.1 behavior.

If a recognized remote later emits only Device Announce, an earlier hook's
two-attempt process-lifetime registration cap could suppress recovery for
hours at the same network address. The recovery revision keeps the 60-second
cooldown and two-attempt burst, but renews eligibility after 15 quiet minutes
on a later valid announcement. It does not run a retry timer or register on
every key/status packet. Back up and install the updated quirk, then perform
one full HA restart; changing the blueprint alone cannot fix missing events.
This gap is reproduced offline; actual later physical recovery must be checked
separately. Do not assume it explains every radio or reachability failure.

## Pairing and reset uncertainty

C4 pressed four times is the confirmed identify sequence. Reset recipes for
SR-150/SR-250 are not verified for the SR-260. A used remote may need its
vendor-documented leave/reset procedure, but this package does not provide a
confirmed recipe. Avoid repeated factory resets or deleting the network.

## Asking for help without exposing your home

Describe package version, Home Assistant/ZHA versions, radio type, symptom and
minimal redacted traceback. Do **not** post access tokens, backups, full device
registry/config entries, real IEEE/device IDs, entity inventories, internal
hostnames/IPs or unredacted capture logs. Replace identifiers consistently with
synthetic placeholders. State separately what was checked offline and what was
observed on the actual remote.
