# Remote command names

Type command text in **Key command names** in the blueprint. There are no
platform presets, command dropdowns or runtime downloads. This page is a
manual reference; your saved text does not change when this page is updated.

## Scene or automation instead

Open one of the **Optional navigation/playback/channel-color actions**
sections and select a scene or automation for a key. That selection wins over
its command text and works without a `remote` entity.

- Selected override: runs **once per short press**. Holding does not repeat
  the scene/automation or fall through to its remote command.
- Empty override: keeps the current command and its existing hold-repeat policy.
- Digits have no action overrides; they use the existing editable
  **Digits 0-9 (template)** field.
- Watch, Listen, List, Room Off, I / II / III, Prev, DVR and volume keep their
  existing dedicated controls. Menu-owned navigation/Select/Cancel stays local.
- Automation selections use `automation.trigger`, like the existing shortcut
  keys, rather than simulating an automation's normal trigger. Scenes use
  `scene.turn_on`.

## Examples

Verified against the official integration documentation on **2026-10-17**.
Commands depend on the integration, device and app; the same spelling is not
universal. Blank a field when that platform has no suitable command.

| SR-260 command field | Roku example | Apple TV example |
|---|---|---|
| Up / Down / Left / Right | `up` / `down` / `left` / `right` | `up` / `down` / `left` / `right` |
| Select | `select` | `select` |
| Cancel / Back | `back` | `menu` |
| Control4 / Home | `home` | `home` |
| Menu (optional) | leave blank unless your device supports an appropriate command | `top_menu` |
| Play | `play` (play/pause toggle) | `play` |
| Pause | `play` (same toggle) | `pause` |
| Skip back / forward | `replay` / leave blank | `skip_backward` / `skip_forward` |
| Rewind / Fast forward | `reverse` / `forward` | `skip_backward` / `skip_forward` are jumps, not continuous rewind |
| Info | `info` | leave blank unless the integration supports an appropriate command |
| Channel up / down | `channel_up` / `channel_down` (device-dependent) | leave blank |
| Digits template | `Lit_{n}` | leave blank; Apple TV does not document digit remote commands |
| Star / Hash | `Lit_*` / `Lit_#` | leave blank |

Roku `Lit_` sends text. Apple TV text entry uses its keyboard actions, not Roku
`Lit_` commands; use a separate automation if that is the intended behavior.
Apple TV also documents `previous` and `next`, which are distinct from skip
jumps. Choose the behavior your app supports rather than assuming equivalence.
Volume still goes to the blueprint's selected media player, not these fields.

## Official sources and updates

- [Home Assistant Roku - Remote](https://www.home-assistant.io/integrations/roku/#remote):
  supported names, device-dependent commands and `Lit_STRING`.
- [Home Assistant Apple TV - Remote](https://www.home-assistant.io/integrations/apple_tv/#remote):
  supported names, command examples and version limitations.
- Tested-release implementation references:
  [Roku remote.py, HA 2026.9.4](https://github.com/home-assistant/core/blob/2026.9.4/homeassistant/components/roku/remote.py)
  and [Apple TV remote.py, HA 2026.9.4](https://github.com/home-assistant/core/blob/2026.9.4/homeassistant/components/apple_tv/remote.py).

The live official pages can change independently of this package. To update
your mapping, check the documentation for your installed integration, then edit
the blueprint's text fields yourself. For another integration, start with its
official `remote.send_command` examples; do not copy Roku or Apple TV names
blindly. No downloaded data, executable configuration or credentials are used.

Try one harmless key at the actual target and inspect its automation trace
before mapping the rest. This reference is not a physical verification of
every integration/device combination.
