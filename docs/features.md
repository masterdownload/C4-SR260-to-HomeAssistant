# Behavior and limits

These are implemented v0.1 features, not a claim of completed physical testing.
See the [evidence limits in the README](../README.md).

## Events and keys

The quirk exposes 50 key names through `zha_event` and device triggers.

| Event command | Meaning / useful `args` |
|---|---|
| `remote_button_short_press` | Key down; `button` |
| `remote_button_short_release` | Key up; `button` |
| `remote_button_long_press` | Repeated while held; `button`; cadence varies |
| `motion_wake` | Pickup / wake |
| `menu_select` | Choice in a package-opened menu; `list_id`, `selected_index`, `item`, `title` |
| `menu_cancel` | Cancel in such a menu; `list_id`, `selected_index`, `title` |

While a menu is open the remote handles highlight movement locally; Select and
Cancel can arrive as menu events instead of ordinary key events. Do not assume
every held key repeats at a fixed 100 ms interval.

## Room controller

- Watch and Listen open menus of scenes, scripts or automations.
- List opens Room controls. Lights can offer on/off and dim levels, thermostats
  warmer/cooler/mode choices, and covers open/close/stop. Switches and fans can
  toggle. Other supported domains follow the blueprint's implementation.
- Room Off, I / II / III, Prev and DVR can each run a target. Leave empty inputs
  empty to ignore those actions.
  Room Off is always visible directly below Header, line 2; the other shortcut
  keys remain in the collapsed Other keys section.
- Labels must be unique and short; Watch, Listen and Room titles must differ.
  Selections are matched using menu title/index. Avoid duplicate room entities.
- Room actions are silent by default. The optional feedback setting shows a
  result message instead. Cancel inside a submenu returns to Room.

Every input and supported selector domain is listed in the
[blueprint reference](blueprint-reference.md).

## TV and volume

Navigation, transport, digit, channel and color keys call the selected `remote`
entity. Defaults use Roku command strings; edit them for your integration.
Roku Play and Pause both use `play` (toggle), Skip Back uses `replay`, and
unmapped keys are ignored. Home Assistant must already control the target;
this package does not pair an IR device or supply vendor codes.

Vol + / - / Mute use the selected media player. Held volume and selected
navigation keys repeat. The header can show a number, a text bar or both.
It uses the media player's reported state; a sleeping/off target or delayed
state reporting can limit the result. The text bar is not the native Control4
bottom-of-screen volume overlay.

## Display and timing

The remote sleeps; commands generally need to be sent immediately after it
transmits. Earlier testing indicated a roughly half-second receive window,
not a guaranteed timing budget. A held key can keep it reachable. Arbitrary
unsolicited screen updates will often miss it.

The blueprint sends the header, optional color and clock on wake, and refreshes
the volume line on volume actions. Whether the full sequence reaches a real
remote within its listening window remains an end-to-end physical test.

Expect roughly 17-20 visible characters across and only a few menu rows at
once. Use labels around 12 characters so appended states fit. Menus page as
you scroll; no universal supported row count is claimed. The blueprint
sanitizes delimiter characters that cannot safely appear in remote text.

Color is quantized to the remote's palette (8 red levels, 8 green, 4 blue).
**Text brightness scales the text color, not the LCD backlight.** No
backlight/keypad brightness controls, Home Assistant battery sensor or native
bottom volume bar are provided.

The automation runs in `parallel` mode, at most 10 concurrent runs. Additional
runs beyond that bound are silently dropped by its configured mode settings.
Avoid unnecessary duplicate automations for one remote.

## Advanced interface

The virtual display cluster is `0xFC47` on endpoint 1. Its implemented commands
are `show_list` (0), `close_list` (1), `send_raw` (2), `set_header` (3),
`set_clock` (4) and `set_text_color` (5). Inspect
[`c4_display_cluster.py`](../quirks/c4_display_cluster.py) for the exact schemas.
These are host-side virtual commands, not claims about native ZCL support.

`send_raw` and diagnostic/probe events are advanced interfaces, not required
for onboarding. Do not experiment with unknown commands or settings on
equipment you cannot recover. No private captures or probe harness are shipped.
Factual community protocol background is linked in [attribution](attribution.md).
