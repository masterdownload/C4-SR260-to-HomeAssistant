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
An unknown manufacturer/model initially is expected.

Copy the device's eight-byte IEEE address from its device information.
Use that address, not a controller's six-byte MAC.

C4 four times is the confirmed identification sequence. SR-150/SR-250 reset
recipes are **unverified for the SR-260**. This package does not provide a
confirmed factory-reset procedure.

## 3. Set the model

The SR-260 needs a manual model-cache entry.

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

The running quirk keeps a cache in memory; editing while Core runs can lose
your changes. After startup, confirm the entries remain and the devices show
**Control4 / C4-SR260**.

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

Under **TV / streamer control**, choose **Volume display** for the optional
Hash, Equals, Star or Marker styles. **Volume percentage precision** can show
one decimal; its default is whole percentages. Existing choices stay unchanged.

Test one harmless action while present. Check the remote, target device and
automation trace. The full new blueprint behavior is not physically verified
by the package's development checks.

For upgrades, preserve the whole `use_blueprint.input` mapping and change only
`use_blueprint.path` when needed. Avoid UI **Re-assign**: input loss was
observed, with its cause unconfirmed. See [safety and recovery](safety.md).
