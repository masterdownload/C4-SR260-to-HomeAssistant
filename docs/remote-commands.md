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

## Multiple commands, System Bridge and IR

One key can run an ordered sequence of Home Assistant actions, including
commands from different integrations. No virtual `remote` entity is needed
just to hold the sequence.

1. Open **Settings > Automations & scenes > Create automation > Create new
   automation**. Give it a name such as **Media key sequence** and leave
   **When** (triggers) empty.
2. Under **Then do**, use **Add action** for each step, in order. Add a
   **Delay / Wait for time to pass** block between commands that need time.
   Choose actions actually available for your installed integrations:
   [System Bridge](https://www.home-assistant.io/integrations/system_bridge/)
   can provide computer actions such as keyboard input; an IR integration
   sends commands through its separately configured transmitter.
3. Save and test a harmless sequence with **Run actions**. Start with
   **Single** mode to avoid overlapping runs from separate presses. Inspect
   its trace if a step fails; an action returning does not prove the target
   device has finished responding.
4. Edit your SR-260 blueprint automation, find the desired optional media-key
   override, and select **Media key sequence**. Save. The selector accepts
   **scene or automation**, not scripts; a short press runs the automation.

Example structure: **supported System Bridge action -> delay -> learned IR
command**. Replace every step with an action/command your equipment supports;
this is not a universal command preset or a physically tested combination.

**Conditions:** this blueprint calls
[`automation.trigger`](https://www.home-assistant.io/actions/automation.trigger/)
without changing its default: automation-level **And if** conditions are
skipped. Put required checks as **Condition** steps inside **Then do**, and do
not rely on data from a normal trigger event.

For a reusable sequence, create a [script](https://www.home-assistant.io/docs/script/)
and call it from that automation. In **Add action**, select the script's own
named action when subsequent steps must wait for it to finish.
`script.turn_on` starts it in the background instead; add an explicit wait
before dependent steps if using that form. Keep the automation wrapper for
the media override; this does not add a direct script selector.

**IR needs hardware:** use a supported transmitter such as
[Broadlink](https://www.home-assistant.io/integrations/broadlink/#remote), with
learned codes sent using
[`remote.send_command`](https://www.home-assistant.io/integrations/remote/).
An [ESPHome IR transmitter](https://esphome.io/components/remote_transmitter/)
must expose its configured commands to Home Assistant, for example through
[user-defined API actions](https://esphome.io/components/api/#user-defined-actions).
ESPHome's low-level transmit actions are not generic Home Assistant
`remote.send_command` commands. System Bridge is not itself an IR transmitter,
and this quirk does **not** expose the physical SR-260's IR emitter.

Official references checked 2026-10-17:
[ordered actions and building blocks](https://www.home-assistant.io/docs/automation/building-blocks/),
[delays](https://www.home-assistant.io/building-blocks/delay/) and
[script waiting behavior](https://www.home-assistant.io/docs/script/#waiting-for-a-script-to-finish).

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
