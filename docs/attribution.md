# Attribution, licensing and provenance

## Scope of the Apache-2.0 license

The [Apache License 2.0](../LICENSE) applies to original contributions only to
the extent their contributors are authorized to license them and relevant
rights exist. Original contributions are publicly attributed to
**masterdownload**. This is not a claim of exclusive ownership of upstream
code, firmware, protocol facts, or purely AI-generated output. Third-party
authors retain their applicable rights and credits.

This package is a fresh public-oriented distribution, not a copy of the private
development repository's history. The blueprint and user documentation use
generic examples and synthetic identifiers. Tests, helper/development tools,
personal automation instances and deployment records are not distributed here.

## Upstream sources and license evidence

| Source | Material and license evidence |
|---|---|
| [pvanbaren/zha-device-handlers, exact commit](https://github.com/pvanbaren/zha-device-handlers/tree/5c04d09852916d60137681c695af4245a88337ba/zhaquirks/control4) | All 15 modules in `quirks/`, from branch `control4`, commit `5c04d09852916d60137681c695af4245a88337ba`; a fork of [zigpy/zha-device-handlers](https://github.com/zigpy/zha-device-handlers) |
| [Pinned upstream license](https://github.com/pvanbaren/zha-device-handlers/blob/5c04d09852916d60137681c695af4245a88337ba/LICENSE.md) | Apache-2.0; a copy is retained [here](third-party/zha-device-handlers-LICENSE-Apache-2.0.txt) |
| [defjam903/control4-zha-quirk-fixes, pinned README](https://github.com/defjam903/control4-zha-quirk-fixes/blob/44a386bcd61acc2f06cbd88dbce6126705d20d20/README.md#license) | `BUTTON_7` / `BUTTON_8` import fallback in `c4_helpers.py`; README explicitly states: **"Same as upstream (Apache-2.0)."** |

Checked on 2026-10-14: the full tree at the pinned pvanbaren commit contains
`LICENSE.md` and no `NOTICE` file. No copyright/license header was present in
the 15 upstream Python modules. Their original content and applicable notices
are retained; the project's [NOTICE](../NOTICE) adds attribution rather than
purporting to reproduce a nonexistent upstream NOTICE.

The defjam903 repository has no root `LICENSE` file and GitHub's metadata
reports `license: null`. Neither fact alone establishes permission, but the
explicit license statement in its pinned README does. On that evidence, the
borrowed fallback is retained under Apache-2.0 with attribution. No permission
is inferred merely from public accessibility. Its other fixes and patch files
are not copied. This is a documented licensing assessment, not a legal
clearance opinion.

## Modified quirk files

Compared with the pinned pvanbaren source after normalizing CRLF to LF:

| File | Changes |
|---|---|
| `c4_helpers.py` | defjam903 button fallback; raw-frame/length/sequence helpers; strict identity parsing and atomic persistence; identity-send/radio status checking; experimental single-row menu replies; prominent source/modification notice |
| `c4_hooks.py` | Strict pre-quirk SR-260 discovery, validated announce probing, safe raw-device lifecycle promotion and ZHA refresh; response-first registration with expiring recovery budget, cooldown and active-status suppression; preserve other-device/normal initialization routing; prominent modification notice |
| `c4_button_cluster.py` | Diagnostics, bounded probing, silent selection/display announcements and passive battery reports; echo local context only for matching list IDs and ignore replaced-list events; prominent modification notice |
| `c4_display_cluster.py` | Raw-send/display settings; `show_selection`; bounded optional local-only menu context and list-owned failure cleanup; prominent modification notice |
| `control4_remote.py` | Clone the resolved SR-260 node descriptor and clear only its incorrect mains-power bit for native battery diagnostics; preserve raw descriptor and other flags; prominent modification notice |

The other 10 modules are unchanged apart from checkout line-ending
normalization: `c4_basic_cluster.py`, `c4_led_cluster.py`,
`c4_ramp_cluster.py`, `c4_z2io_zp.py`, `control4_dimmer.py`,
`control4_fan.py`, `control4_outlet.py`,
`control4_scene_controller.py`, `control4_switch.py`, `control4_z2io_zp.py`.
They are included because the modules import each other, not as a claim of
physical testing or support for all those device types.

Public-package changes to the other distributed source files are licensing
notices, blueprint author attribution and generic documentation examples.
The private installation is not modified by this distribution.

## External references and dependencies

[Home Assistant ZHA documentation](https://www.home-assistant.io/integrations/zha/)
describes supported radios and integration setup.
[Upstream SR-260 protocol notes](https://github.com/pvanbaren/zha-device-handlers/blob/5c04d09852916d60137681c695af4245a88337ba/zhaquirks/control4/documentation/control4-sr260-remote-protocol.md)
are factual community background, not firmware or a vendor manual.

Home Assistant, ZHA, zigpy and zha-quirks are separate dependencies with
their own licenses; their distributions are not bundled or relicensed here.
In particular, the installed zigpy 2.2.0 metadata identifies GPL-3.0, ZHA and
zha-quirks identify Apache-2.0. Consult each exact
dependency's license when using or redistributing it.

No Control4 firmware, manual PDFs, logos or artwork are included. Control4,
SR-260, Snap One, Home Assistant and SONOFF names identify factual compatibility
or origin only. Trademarks belong to their respective owners. This project is
not affiliated with, endorsed by or sponsored by those owners.

## Warranty and contributions

The software is **AS IS, without warranty**, subject to the full license and
applicable law. Read [safety and recovery](safety.md); take a full backup before
use. Neither a license nor this document promises legal immunity.

Contribute only material you are authorized to submit under Apache-2.0.
Preserve third-party credits, license terms and any applicable NOTICE. Put
prominent change notices in modified upstream files. Do not submit credentials,
personal device identifiers, proprietary firmware, manual PDFs or copied code
without an applicable redistribution license.
