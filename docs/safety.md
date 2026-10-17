# Safety, upgrades and recovery

**Experimental v0.1; AS IS, without warranty.** Make a full Home Assistant
backup before installation or upgrade. Keep a separate recovery-accessible
copy of configuration, custom quirks, blueprint and automation inputs.

The custom quirks install process-wide ZHA/zigpy hooks. Although intended to
handle Control4 traffic, they sit in shared paths and can affect other devices
or integration startup. They do not modify remote firmware. Backup and offline
tests reduce risk, not eliminate it.

## Evidence limits

Reported development testing used Home Assistant 2026.9.4, SONOFF ZBDongle-E
with EZSP, channel 15 and three remotes. The full new blueprint behavior has
not been physically verified. At the source handoff, configuration had been
loaded but no remote event had exercised the new full behavior. This package
does not claim a later physical result.

ZHA only; no Zigbee2MQTT support or shared coordinator. Automatic SR-260
identity learning needs a paired, awake remote and validated identity traffic;
manual cache seeding is a fallback, not a normal onboarding step.
Other custom-quirk layouts, devices, networks and
Home Assistant updates require cautious evaluation.

## Preserve existing quirks

ZHA reads one `custom_quirks_path`. Keep an existing path and its contents.
Copy the files into that existing directory. Check collisions before replacing files.
Do not disable unrelated quirks by redirecting ZHA to a new empty directory.

## Safe upgrades

Back up each automation's full YAML, especially the **`use_blueprint.input`**
mapping. Keep quirk files and blueprint from the same version together.

When adopting a blueprint at a new path, change `use_blueprint.path` while
preserving the entire `input` mapping. Compare the resulting YAML before
reloading or enabling it. Avoid UI **Re-assign** as an upgrade method: input
loss was observed, but its cause has not been confirmed.

Reload automations when only their blueprint/YAML changes. Perform a **full
Home Assistant restart** when quirk code changes or you manually edit the model
cache. Automatic learning/rebuild does not normally need a second restart.

## Recovery

1. Disable the affected automation if it causes unexpected actions. Test only
   while present and against equipment where an unintended action is safe.
2. For an automation-only problem, restore the prior blueprint and complete
   automation input block. Reload automations and inspect the saved targets.
3. For a quirk/startup problem, restore the previous quirk files and
   configuration. Remove only files added by this installation and keep other
   custom quirks intact. Use the copies you saved before installation.
4. Restore the previous model-cache backup if necessary, preserving unrelated
   mappings. Prefer editing while Home Assistant is stopped; otherwise a
   running in-memory copy can overwrite your changes.
5. Check configuration and fully restart Home Assistant. If it cannot start,
   use your installation's supported recovery access or restore the full
   backup. Do not delete ZHA's device database, factory-reset every remote or
   reset the Zigbee network as a first troubleshooting step.

Only the **C4 button pressed four times** identification sequence is confirmed
here. SR-150/SR-250 reset or reboot sequences are **unverified for the SR-260**;
do not treat them as confirmed recovery instructions.
