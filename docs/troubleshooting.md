# Troubleshooting

Start with a backup, [installation checks](install.md) and
[safety/recovery](safety.md). Do not treat a successful offline test, model
label or manifest comparison as proof of physical behavior.

| Symptom | Check and next action |
|---|---|
| No ZHA coordinator | Configure ZHA with its own supported coordinator; do not reuse the radio owned by Zigbee2MQTT |
| Quirks do not load | All 15 files must be flat in the directory configured by `custom_quirks_path`; inspect startup import errors; fully restart after changes |
| Existing custom quirks stop working | Restore the prior path and files; never redirect ZHA away from an existing custom directory |
| Remote stays unknown | Confirm the actual eight-byte IEEE and `C4-SR260` cache mapping, valid flat JSON, and a full restart; check that the mapping survived |
| Files are in the wrong directory | Move the package files into the existing configured directory, keeping other quirks intact |
| `BUTTON_7` / `BUTTON_8` import error | Check that this package's `c4_helpers.py`, including its compatibility fallback, is installed; do not mix versions |
| Keys produce no events | Listen to `zha_event`, wake the remote and press a key; confirm model-cache onboarding and loaded quirks before attempting resets |
| Events arrive but no action | Inspect automation enabled state, chosen remote, target entities and trace; make sure only the intended automation owns that remote |
| TV key does nothing | Verify the target `remote` entity and its integration-specific command names; Roku defaults are not universal |
| Screen misses an update | The radio sleeps; test immediately after a remote event, not an arbitrary delayed push; reduce avoidable delays |
| Wrong menu opens or selection runs wrong row | Use distinct menu titles and unique short row labels; compare saved inputs and automation trace |
| Thermostat only shows read-only targets | Confirm the entity reports valid targets, minimum/maximum and a positive temperature step, and is not off/unavailable; supported mode choices can turn an off thermostat back on |
| Thermostat displays H/C but does not seem to heat or cool | H/C is the configured Heat/Cool mode, not active HVAC action; the package does not invent missing active-heating/cooling status |
| Chosen Room row remains on screen | Check that blueprint and all quirks match v0.1 and `room_feedback` is off; the silent-choice implementation still needs physical confirmation |
| No battery/LQI/RSSI value | Battery sensing is not implemented; diagnostic values can remain empty and are not by themselves proof the remote is offline |
| `quirk_applied: false` despite working events | That flag was misleading in the reported setup; inspect actual device behavior, class/loading evidence and event flow |
| No signal-bars icon | Its behavior is unresolved; use received events instead of the remote's icon as the connectivity check |
| Update broke startup | Restore the prior known-good quirk files and configuration, then fully restart; see recovery before changing the Zigbee network |

## File versions

Keep the 15 quirks and blueprint from the same package version. Compare
unexpected changes with your backup before replacing files.
`MANIFEST.sha256` records checksums for those files with CRLF normalized to LF.
It is an optional integrity reference, not something you need to run to install.
Checksums detect differences, not author identity or a trustworthy download.

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
