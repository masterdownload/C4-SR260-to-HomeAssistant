# Installation details

The short instructions and downloads are in the [README](../README.md).
No helper tools, tests or command-line Python are required.

Take a full backup first. These experimental quirks load into the ZHA process
and may affect other devices. They do not change remote firmware.

## 1. Copy and enable the quirks

Download and unzip the package. Using your usual file-access method, copy all
15 files from `quirks` directly into `/config/custom_zha_quirks/`.

If you already have a `custom_quirks_path`, use **that directory** instead.
Preserve its other files and configuration. Back up any filename collisions
before replacing them. All 15 modules are needed because they import each other;
do not create an extra `control4` subfolder.

If you have no existing ZHA YAML block, add:

```yaml
zha:
  custom_quirks_path: /config/custom_zha_quirks
```

If `zha:` exists, add only the indented setting. Never duplicate `zha:` or
replace an existing path blindly.

Check configuration in Home Assistant, then perform a **full restart**.
If ZHA fails to load, restore your backup before continuing.

Examples use `/config`, as seen inside Home Assistant. Some file-access
add-ons show the same directory as `/homeassistant`.

## 2. Pair one remote

ZHA must own its coordinator. It cannot share a radio with Zigbee2MQTT or
another stack. Follow the [official ZHA guide](https://www.home-assistant.io/integrations/zha/)
if you have not set it up.

Choose **Add device** in ZHA, keep the remote close, and press **C4 four times**.
Keep it awake while it exchanges identity information. An unknown model can
appear temporarily during the interview.

Copy the device's eight-byte IEEE address from its device information.
Use that address, not a controller's six-byte MAC.

C4 four times is the confirmed identification sequence. SR-150/SR-250 reset
recipes are **unverified for the SR-260**. This package does not provide a
confirmed factory-reset procedure.

## 3. Check automatic recognition

The quirks now learn the exact SR-260 model identity from validated Control4
traffic and apply the remote quirk through ZHA's device-rebuild lifecycle.
The address prefix alone is **not** identification. After a successful exchange
the device should show **Control4 / C4-SR260**, with its key triggers available.
Listen to `zha_event` and press a key. The model mapping is saved automatically
in `/config/.storage/c4_quirk_data.json`; keep existing mappings and back it up.

Some unclassified remotes initially send only a Zigbee Device Announce and
advertise a generic endpoint. After normal Zigbee join handling, a validated
announcement from an unknown Control4-prefix device may trigger the bounded
controller/model query. The prefix permits that query only; it never supplies
the model. Without a valid identity response the remote remains unknown.

For an already-paired unknown remote, install the updated files and perform the
required full Home Assistant restart, then wake the remote. It can be recognized
without deleting or rejoining. No additional restart is normally needed once a
valid identity arrives on the tested zigpy/ZHA lifecycle.

This is not zero-step discovery: ZHA pairing, a loaded quirk set and awake radio
traffic are required. Probes are bounded (three per device/process, at least
30 seconds apart), as are rebuild attempts (two, at least 60 seconds apart).
If it stays unknown, inspect the ZHA logs, wake it again, and use ZHA reconfigure
if its interview is incomplete. Missing lifecycle APIs, exhausted retries or an
unreadable cache require explicit recovery; do not loop resets or delete the
network. A restart after learning a model is a fallback on unsupported versions,
not the normal new-remote workflow.

Offline coverage uses zigpy 2.2.0 and ZHA/zha-quirks 2.2.2. It checks strict
unwrapped ZCL identity frames on profile `0xC25D`, cluster 1, endpoint 2,
including the actual model-read response captured during a successful physical
check. One already-paired unknown SR-260 was identified, cached and activated
after waking, without manual seeding, delete/rejoin or a restart after identity
learning. A brand-new first join remains offline-tested, not physically proven.
Other wrappers, firmware and lifecycle versions remain unverified.

The discovery parser also accepts the captured Control4 manufacturer-specific
identity form (`0x1040`, cluster command 1, status-free attribute records).
This is identity coverage only: it does not add controller provisioning, prove
key traffic, or resolve a remote that still sends only network announcements.

Recognition does not transfer an old remote's automation settings to a different
IEEE/device. Select the intended device when creating or updating an automation.

### Manual fallback

Only if automatic recognition has failed and you have independently confirmed
the device is an SR-260, the earlier manual cache method remains available:

1. Arrange access to the configuration files that works while Home Assistant
   Core is stopped, then stop Core. If your only file editor stops with Core,
   arrange another access method before continuing.
2. Open or create `/config/.storage/c4_quirk_data.json`.
3. Add your remote as shown below, replacing the synthetic example IEEE.
   Preserve other entries. The file is a flat JSON object, with commas between
   entries and no trailing comma.
4. Save the file and start Home Assistant.

One remote:

```json
{
  "00:0f:ff:00:00:00:00:01": "C4-SR260"
}
```

Two remotes:

```json
{
  "00:0f:ff:00:00:00:00:01": "C4-SR260",
  "00:0f:ff:00:00:00:00:02": "C4-SR260"
}
```

The running quirk keeps a cache in memory; manual editing while Core runs can lose
your changes. After startup, confirm the entries remain and the devices show
**Control4 / C4-SR260**.

### Controller registration and operational check

The experimental verified/cached SR-260 registration sequence sends an
unsolicited controller identity Read Attributes Response, then the controller
identity Report Attributes, then the existing Zigbee Many-to-One
Route Request (MTORR) helper. This is an explicitly experimental message-form
variation, not a claim that every SR-260 accepts this sequence. MTORR is a
**network-wide route advertisement**, not a firmware change or a thermostat/
media action. Unknown Control4-prefix devices do not trigger MTORR merely from
their address or an announcement. Their model must be verified first.

Registration has a separate bound from model queries: one in-flight exchange,
at least 60 seconds between attempts, and at most two attempts for the same
IEEE/network address per process. A changed network address can get a new
bounded attempt after the cooldown. Cached SR-260 reset/rejoins can register
without exhausting or depending on the unknown-model query budget.

This sequence follows the upstream author's
[documented registration finding](https://community.home-assistant.io/t/control4-sw2-zx-with-zha/844219/12).
The unsolicited response is a separately investigated form from an
[upstream SR-260 fixes proposal](https://github.com/pvanbaren/zha-device-handlers/pull/1);
the existing helper's values/endpoints are kept, not the proposal's other
features or inferred protocol changes. Logs mark the sequence EXPERIMENTAL.
Each send must finish before the next; actual radio return-status failures
are logged and stop the sequence. A successful send, recognized model, or exposed trigger list
does **not** prove the remote accepted registration. Check actual `motion_wake`
and key press/release events, then menus/header at the physical remote.
This registration revision is offline-tested; physical operational acceptance
was subsequently observed on one already-identified replacement with its model
cache preserved: real List/Room Off key traffic and menus worked, and the owner
confirmed the room-name header after sleep/pickup. This is not a physically
verified fully uncached first join or a guarantee for every remote/firmware.

If a recognized remote still sends only Device Announce and no Control4 key/
motion frames, stop repeating reset/re-pair operations. Its Zigbee interview
has succeeded, but application registration is not confirmed. Preserve logs
and the known-good backup; do not guess new attribute values or firmware steps.

Check acceptance in order:

1. Device shows Control4 / C4-SR260 with the active remote quirk.
2. Real presses produce `zha_event` press/release commands; a trigger dropdown
   alone does not prove the remote transmits them.
3. List opens the configured Room menu and one harmless action works.
4. Let the screen go fully dark, wait a few seconds, then pick it up without
   pressing a key. Confirm the configured room-name header appears.

The header is wake-driven; repeatedly pressing keys while already awake is not
the same test. Select the correct device in each automation when replacing a
remote. These quirks do not migrate an old device reference automatically.
Keep all automation inputs when updating the blueprint path.

### Why one remote needed the response-first form

On the observed replacement, model reads succeeded but it sent only network
announcements, not Control4 keys. Report-only and Report -> MTORR attempts did
not enable key traffic. With the same existing controller values/endpoints,
adding the identity-response form immediately produced vendor identity/status
and then key events. Both that remote and the working comparison reported
firmware 2.2.50. That supports a controller-registration/message-handling
difference, not a proven firmware or hardware difference. Why their initial
controller state differed remains unknown.

## 4. Copy the blueprint

[Download the YAML](https://raw.githubusercontent.com/masterdownload/C4-SR260-to-HomeAssistant/main/blueprint/c4_sr260_room_remote.yaml)
and put it here, creating the folders if necessary:

```text
/config/blueprints/automation/control4/c4_sr260_room_remote.yaml
```

Use the blueprint and quirk files from the same package version.

In **Settings > Automations & scenes > Blueprints**, create one automation
per remote. Select the remote, then the entities you want to control.
Keep menu names short and unique. Roku command names are defaults; other
remote integrations may need different names.

The optional media-key action sections accept a scene/automation instead of
that key's command. Overrides run once on short press, never while held;
empty preserves the command, and no remote entity is needed for an override.
Use the [command reference](remote-commands.md) for integration-specific text.

The native ZHA Battery diagnostic appears after the updated quirks load.
It remains unknown until a valid passive battery report; do not treat unknown
as empty or full. No battery polling/setup automation is required.

Under **TV / streamer control**, choose **Volume display** for the optional
Hash, Equals, Star or Marker styles. **Volume percentage precision** can show
one decimal; its default is whole percentages. Existing choices stay unchanged.

Thermostat rows show measured temperature and mode. Heat/Cool thermostats have
separate Heat and Cool `+`/`-` target rows; single-target thermostats keep
Warmer/Cooler. `*` marks the configured mode. See [thermostat controls](features.md#thermostats).

Test one harmless action while present. Check the remote, target device and
automation trace. The full new blueprint behavior is not physically verified
by the package's development checks.

For upgrades, preserve the whole `use_blueprint.input` mapping and change only
`use_blueprint.path` when needed. Avoid UI **Re-assign**: input loss was
observed, with its cause unconfirmed. See [safety and recovery](safety.md).
