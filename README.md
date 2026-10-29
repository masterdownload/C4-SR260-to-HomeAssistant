# C4-SR260-to-HomeAssistant

**Experimental v0.3.4.** Use a Control4 SR-260 remote with Home Assistant **ZHA**,
without a Control4 controller.

**Build tracking:** `VERSION` is shared by the package and blueprint. Every
subsequent published blueprint or quirk change/fix increments the patch:
**v0.3.5, v0.3.6, ...**, even while experimental. Minor/major checkpoints
are chosen explicitly; documentation/tests-only updates do not change
deployable versions. This v0.3.4 update adds wake/first-use display preparation.
The version distinguishes it from intervening experimental builds; no stable
release/tag or complete physical acceptance is implied.

Watch/Listen menus, room controls, TV keys, volume, screen text and clock.
Optional scene/automation media-key actions and a native ZHA Battery diagnostic
are included; empty action selections preserve the existing remote commands.
The full new blueprint behavior has **not yet been physically verified**.
Reported testing: Home Assistant 2026.9.4, SONOFF ZBDongle-E / EZSP,
channel 15, three remotes. Other setups are unverified.

**Take a full Home Assistant backup first.** These community quirks affect the
ZHA process, not the remote's firmware. ZHA needs its own coordinator; it
cannot share one with Zigbee2MQTT. [Safety and recovery](docs/safety.md).

## Download

- [Download the package ZIP](https://github.com/masterdownload/C4-SR260-to-HomeAssistant/archive/refs/heads/main.zip)
- [Download the blueprint YAML](https://raw.githubusercontent.com/masterdownload/C4-SR260-to-HomeAssistant/main/blueprint/c4_sr260_room_remote.yaml)

## New installation

**1. Copy the quirk files.** Unzip the package and copy **all 15 files** from
`quirks` directly into `/config/custom_zha_quirks/` in Home Assistant.
Do not put them inside another subfolder.

Already have a `custom_quirks_path`? Keep that path and put the files there
instead, alongside your existing quirks. Back up and compare any filename
collisions; do not overwrite local changes blindly. Existing package users
should follow the [upgrade instructions](docs/install.md#first-use-display-update)
rather than copy the whole package over their customizations.

**2. Add this to `configuration.yaml`**, then check configuration and fully
restart Home Assistant:

```yaml
zha:
  custom_quirks_path: /config/custom_zha_quirks
```

If `zha:` already exists, add only the indented line. If it already has a
custom-quirks path, keep it unchanged.

**3. Pair the remote.** In ZHA, choose **Add device**, then press the remote's
**C4 button four times**. Keep it awake near the coordinator. It may initially
show an unknown model while its identity is being learned.

**4. Check recognition.** The device should become **Control4 / C4-SR260**
automatically after its actual identity exchange. No routine manual cache entry
or second restart is needed on the supported lifecycle. Listen for `zha_event`
and press a key to check it. Already paired but unknown? Wake it after the
quirk update and full restart; deletion/re-pairing is not the first step.

Automatic recognition is experimental and needs real device traffic; a sleeping
remote cannot identify itself. If it stays unknown, follow
[recognition checks and manual fallback](docs/install.md#3-check-automatic-recognition).
Recognition without manual seeding or re-pairing was physically confirmed on
one already-paired unknown remote; brand-new first joins remain offline-tested.
Recognition alone does not prove keys or menus work. Controller registration
uses an experimental bounded identity-response/report/route-advertisement
exchange; see the
[operational check](docs/install.md#controller-registration-and-operational-check).

**5. Install the blueprint.** Copy the downloaded YAML to:

```text
/config/blueprints/automation/control4/c4_sr260_room_remote.yaml
```

Open **Settings > Automations & scenes > Blueprints**, select it and create
one automation per remote. Pick the remote and the room's entities. Start
with one harmless action and check it at the physical remote.

Optional media-key action sections let a scene/automation replace a key's
command **once per press**; leaving it empty keeps the command and hold repeats.
For Roku, Apple TV or another target, edit command text using the
[command-name reference](docs/remote-commands.md). Nothing is downloaded or
updated automatically. Battery appears under the ZHA device's diagnostics and
stays unknown until a valid passive report arrives.

For a key that runs several commands, follow the
[multi-command, System Bridge and IR guide](docs/remote-commands.md#multiple-commands-system-bridge-and-ir).

**Acceptance:** check the model, then actual key events, the List menu and the
room name after the screen goes dark and you pick the remote up without a key.
List, Room Off and the wake header were physically confirmed on one replacement
with a preserved model cache. A truly uncached first join is not yet physically
verified. Existing installs need the updated quirks plus one full HA restart;
replacing only the blueprint cannot fix missing radio events.

**First-use display update:** install the matching `c4_display_cluster.py`
before the v0.3.4 blueprint and perform **one full HA restart**. Automation
reload alone is insufficient. No new helpers, input migration, model-cache
edits or routine re-pairing are required. The next usable pickup/short press
prepares the enabled room header and color ahead of the clock; the same key
still runs its existing action. No Loading splash or startup model label is
sent. Pending settings use bounded event-driven retries and successful settings
are deduplicated. For an existing matching public package, only the display
module and blueprint need updating; preserve every other installed module.
If the display file has local changes, merge the update rather than replace
those changes. See [installation and physical checks](docs/install.md#first-use-display-update).

No installer or helper tools are required. Users need not run tests or
command-line Python.
[Installation details](docs/install.md) · [Features](docs/features.md) ·
[Inputs](docs/blueprint-reference.md) · [Troubleshooting](docs/troubleshooting.md).

## License

[Apache-2.0](LICENSE), only to the extent contributors are authorized to license
their contributions. Original contributions are attributed to **masterdownload**;
upstream rights and credits are retained. [Attribution and scope](docs/attribution.md)
· [NOTICE](NOTICE). **AS IS, without warranty.**

Independent community project, not affiliated with or endorsed by Control4,
Snap One, Home Assistant or SONOFF. Trademarks belong to their owners.
