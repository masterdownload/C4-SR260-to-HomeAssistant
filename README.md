# C4-SR260-to-HomeAssistant

**Experimental v0.1.** Use a Control4 SR-260 remote with Home Assistant **ZHA**,
without a Control4 controller.

Watch/Listen menus, room controls, TV keys, volume, screen text and clock.
The full new blueprint behavior has **not yet been physically verified**.
Reported testing: Home Assistant 2026.9.4, SONOFF ZBDongle-E / EZSP,
channel 15, three remotes. Other setups are unverified.

**Take a full Home Assistant backup first.** These community quirks affect the
ZHA process, not the remote's firmware. ZHA needs its own coordinator; it
cannot share one with Zigbee2MQTT. [Safety and recovery](docs/safety.md).

## Download

- [Download the package ZIP](https://github.com/masterdownload/C4-SR260-to-HomeAssistant/archive/refs/heads/main.zip)
- [Download the blueprint YAML](https://raw.githubusercontent.com/masterdownload/C4-SR260-to-HomeAssistant/main/blueprint/c4_sr260_room_remote.yaml)

## Install

**1. Copy the quirk files.** Unzip the package and copy **all 15 files** from
`quirks` directly into `/config/custom_zha_quirks/` in Home Assistant.
Do not put them inside another subfolder.

Already have a `custom_quirks_path`? Keep that path and put the files there
instead, alongside your existing quirks. Back up any files you would replace.

**2. Add this to `configuration.yaml`**, then check configuration and fully
restart Home Assistant:

```yaml
zha:
  custom_quirks_path: /config/custom_zha_quirks
```

If `zha:` already exists, add only the indented line. If it already has a
custom-quirks path, keep it unchanged.

**3. Pair the remote.** In ZHA, choose **Add device**, then press the remote's
**C4 button four times**. Copy its eight-byte IEEE address from the device
information. An unknown model at this stage is expected.

**4. Set the model.** Stop Home Assistant Core before editing
`/config/.storage/c4_quirk_data.json`, using file access that remains available.
Add the following, replacing the example address with your remote's IEEE:

```json
{"00:0f:ff:00:00:00:00:01": "C4-SR260"}
```

Preserve any entries already in that file. Start Home Assistant again.
The device should now show **Control4 / C4-SR260**. More detail:
[model-cache step](docs/install.md#3-set-the-model).

**5. Install the blueprint.** Copy the downloaded YAML to:

```text
/config/blueprints/automation/control4/c4_sr260_room_remote.yaml
```

Open **Settings > Automations & scenes > Blueprints**, select it and create
one automation per remote. Pick the remote and the room's entities. Start
with one harmless action and check it at the physical remote.

No installer, helper tools or tests to run. No command-line Python required.
[Installation details](docs/install.md) · [Features](docs/features.md) ·
[Inputs](docs/blueprint-reference.md) · [Troubleshooting](docs/troubleshooting.md).

## License

[Apache-2.0](LICENSE), only to the extent contributors are authorized to license
their contributions. Original contributions are attributed to **masterdownload**;
upstream rights and credits are retained. [Attribution and scope](docs/attribution.md)
· [NOTICE](NOTICE). **AS IS, without warranty.**

Independent community project, not affiliated with or endorsed by Control4,
Snap One, Home Assistant or SONOFF. Trademarks belong to their owners.
