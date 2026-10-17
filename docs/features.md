# Behavior and limits

These are implemented v0.1 features, not a claim of completed physical testing.
See the [evidence limits in the README](../README.md).

## Automatic identity learning

After pairing and waking, a verified SR-260 model attribute can activate the
remote quirk and refresh ZHA without routine manual cache edits or a second
restart. Already-paired unknown devices use the same path. This relies on actual
identity traffic and supported zigpy/ZHA lifecycle APIs, not an IEEE-prefix
guess. One already-paired unknown remote was physically recognized after wake,
with its model cached automatically and quirk/key triggers exposed. Brand-new
first joins remain offline-tested; physical keys/menus are a separate check.
Validated Device Announce traffic can start a bounded query for an unknown
Control4-prefix device; that announcement alone never classifies it.
See [installation limits and fallback](install.md#3-check-automatic-recognition).
Verified/cached SR-260s also use experimental bounded controller registration
(identity response, report, then network-wide MTORR route advertisement),
including after reset/rejoin.
This is separate from learning a model. Actual key/motion/menu operation must be
checked. List/Room Off and menus were captured working on one cache-preserved
replacement; its wake room-name header was confirmed by the owner after sleep/
pickup. That does not establish every v0.1 feature or a truly uncached first join.

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
  temperature/mode choices, and covers open/close/stop. Switches and fans can
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

### Thermostats

The Room row shows **measured temperature and configured mode**, for example
`Thermostat Now73 H/C`. `H/C` means Heat/Cool mode, not that heating or cooling
is currently running. Long thermostat names are shortened to keep this row
within 22 characters. No active-heating/cooling status is invented.

For a Heat/Cool thermostat with targets 69 and 76, the submenu contains:

```text
Heat 69
Cool 76
Now 73
* Heat/Cool
Off
```

Select **Heat 69** to open a temperature picker. With a reported step of 1,
its ten choices are **64, 65, 66, 67, 68, 70, 71, 72, 73, 74**: five steps
below and five above, omitting the current 69. A step of 0.5 offers
66.5-68.5 and 69.5-71.5. Signed and fractional temperatures are supported.

Limits and the opposite endpoint can leave **fewer than ten choices**; invalid
values are removed, never clamped, duplicated or backfilled. An empty range
shows a read-only **No valid temperatures** row. Opening a picker, selecting
`Now`, or pressing **Cancel** does not change the thermostat. Cancel returns
from picker to thermostat menu, then from thermostat to Room.

Choosing a value changes only the selected target. Range service calls include
both endpoints, preserving the opposite endpoint's current live reported value.
The existing safety contract is low <= high; no unreported minimum gap is
invented. Single-target thermostats retain **Warmer (set N)** and
**Cooler (set N)**, unchanged.
After the menu refresh delay, targets/mode/limits/step are read again immediately
before the service call. A conflicting change cancels the write and logs a
warning; a still-valid opposite endpoint is preserved at its latest value.

`Now` is read-only. `*` marks the configured mode; only modes reported as
supported are offered. An off thermostat keeps targets read-only while allowing
a supported mode to be selected. Missing/invalid targets, limits or a positive
step disable temperature adjustments rather than guessing values. Unknown or
unavailable thermostats cannot be controlled from these menus. Stale or
unrecognized choices are rejected/logged without a thermostat write; reopen
with List if the entity or room layout changed. Compact routing tags in
thermostat titles bind each menu to its entity/layout and picker snapshot,
within the 22-character title budget. Keep room names unique.
For example, the picker caption can look like `Heat#12345678.90abcdef`;
the visible suffix is a routing tag, not a temperature. Choices are the numeric rows.

A changed selected target, mode, step or limits invalidates an old picker.
Measured-temperature updates do not invalidate it; a changed opposite target
is rechecked live. After choosing a target, allow the integration to report its
new state before opening another picker. Numeric choices that cannot be
represented safely in the display format are omitted rather than rounded
into an unintended command.

Values use the thermostat's reported temperature units. Refreshed adjustment
rows show the requested target, not confirmation that the device accepted it.
This menu revision is offline-checked but still needs physical verification.

## TV and volume

Navigation, transport, digit, channel and color keys call the selected `remote`
entity. Defaults use Roku command strings; edit them for your integration.
Roku Play and Pause both use `play` (toggle), Skip Back uses `replay`, and
unmapped keys are ignored. Home Assistant must already control the target;
this package does not pair an IR device or supply vendor codes.

The three optional media-action sections cover 28 navigation, playback and
channel/page/color keys. Digits 0-9 keep the editable command template, without
scene/automation overrides. Select a scene or automation to replace a non-digit
key's command on short press, even without a remote entity. Empty keeps the
existing command. An override runs **once per press**: held events do not
repeat it or send the underlying command. Existing command-only hold behavior,
dedicated menus/shortcut/volume controls and menu-owned Select/Cancel remain.
Invalid manual overrides are logged and ignored rather than sent to a different
domain. See the [manual command-name reference](remote-commands.md) for current
official Roku/Apple TV sources; there are no platform dropdowns or runtime downloads.

Vol + / - / Mute use the selected media player. Held volume and selected
navigation keys repeat. The header can show a number, a text bar or both.
It uses the media player's reported state; a sleeping/off target or delayed
state reporting can limit the result. The text bar is not the native Control4
bottom-of-screen volume overlay.

In **TV / streamer control > Volume display**, four additional ASCII styles
show a ten-position indicator followed by the percentage:

| Style | At 9% |
|---|---|
| Hash | `[#---------] 9%` |
| Equals | `[=.........] 9%` |
| Star | `[*---------] 9%` |
| Marker | `[>.........] 9%` |

Positions round to the nearest 10% of the displayed percentage. Filled bars
are empty at 0% and full at 100%. Marker shows one position instead of filling:
all dots at 0%, the first position at 9%, and the last position at 100%.
Existing Number and bar, Bar only and Number only styles are unchanged;
Number and bar remains the default.

**Volume percentage precision** defaults to whole percentages. Choose
**One decimal** to show values such as `35.5%`, `35.0%`, `0.0%` and `100.0%`
where a style includes a number. Bar only remains a bar without a number.
The percentage comes from the media player's normalized volume, clamped to
0-100%; it is not a receiver-scale value or dB, and does not change volume steps.
It is not a promise that a receiver's half-step corresponds to half a percent.
Fractional reporting and the new glyphs have not been physically confirmed.
The volume displays fit within 22 ASCII characters, including 100.0%.

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
backlight/keypad brightness controls or native
bottom volume bar are provided.

## Battery diagnostics

Each resolved SR-260 exposes ZHA's **native Battery sensor**, enabled by default
with battery device class and Diagnostic category. It uses the passive
`c4.zr.bl` battery-percent announcement only: valid hexadecimal 0-100% is
converted to the standard Power Configuration half-percent units
(`battery_percentage_remaining`, attribute `0x0021`). For example, `5f` is
95%, stored as 190. No report means **unknown**, not an assumed 100%.

Invalid/sentinel/out-of-range reports do not invent or replace values. Vendor
status attribute 6, signal strength and unrelated telemetry are not battery
sources. No aggressive polling or extra battery commands are added; values can
remain unknown until the next legitimate announcement and stale while asleep.
Existing Zigbee attribute caching retains the last valid report through restart.

The SR-260's advertised mains-power flag is corrected only on its resolved
host-side quirk so ZHA can discover the battery entity. The original descriptor,
other Control4 devices, receiver-on-idle flag and firmware are untouched.
This corrects ZHA's battery-device classification/availability policy; it is
not a change to radio configuration. The protocol units are supported by the
[upstream Battery Level gauge notes](https://github.com/naisbitt/zha-device-handlers/blob/2fe087c3edf64678015159716380f02dfafbbaf7/zhaquirks/control4/documentation/control4-sr260-remote-protocol.md).
Native entity creation/enabled Diagnostic metadata was confirmed after restart
on three remotes; values remained unknown without passive reports. Percentage
updates/cache behavior are offline-verified, while physical reporting/
calibration and newly selected key overrides remain separate checks.

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
