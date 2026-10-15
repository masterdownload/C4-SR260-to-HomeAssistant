# Blueprint reference: Control4 SR-260 Room Remote v0.1 (menus, room controls, full remote, clock, volume)

> Input reference for `blueprint/c4_sr260_room_remote.yaml` (sha256 `c423eec7b59b`). No tools or tests need to be run to install the blueprint.

Requires Home Assistant 2025.9.0 or newer. Run mode: `parallel` (up to 10 runs at once; extra runs are dropped silently).

## Events the blueprint reacts to

Every trigger is a `zha_event` from the chosen remote.

| Trigger id | `zha_event` command | Extra filter |
|---|---|---|
| `press` | `remote_button_short_press` |   |
| `hold` | `remote_button_long_press` |   |
| `release` | `remote_button_short_release` | button: volume_up |
| `release` | `remote_button_short_release` | button: volume_down |
| `release` | `remote_button_short_release` | button: volume_mute |
| `wake` | `motion_wake` |   |
| `menu` | `menu_select` |   |
| `menu_cancel` | `menu_cancel` |   |

## Top-level inputs

| Input | Name | Default | Type | What it does |
|---|---|---|---|---|
| `remote` | SR-260 remote | *required* | device (ZHA, Control4 C4-SR260) | The Control4 SR-260 in this room. |
| `wake_text` | Header, line 1 (room name) | *(empty)* | text | The room name shown on the remote's screen whenever it is picked up (the status bar with the clock and battery stays visible). Templates are allowed. Leave blank to use the remote's area name in Home Assistant. |
| `header_line2` | Header, line 2 | *(empty)* | text | Optional second line under the room name, e.g. {{ states('sensor.room_temperature') }} F. It is replaced by the volume while a volume target is set (see "TV / streamer control"). |
| `room_off_target` | Room Off key | *(empty)* | entity (scene, script, automation) |   |
| `show_header` | Show the header when the remote is picked up | on | on / off | Off leaves the screen as it is. The clock and text colour below are still sent. |

## Screen look and clock (`screen_section`)

Sent to the remote each time it is picked up.

| Input | Name | Default | Type | What it does |
|---|---|---|---|---|
| `sync_clock` | Set the remote's clock | on | on / off | The top bar then shows the time, taken from Home Assistant's clock and time zone. |
| `set_text_color` | Set the text colour | off | on / off | Off leaves the remote's own colour. On, the colour and brightness below are used for all text and menus. |
| `text_color` | Text colour | `[176, 208, 224]` | color_rgb | The remote can show 256 colours (8 levels of red and green, 4 of blue), so the result is the nearest of those. |
| `text_brightness` | Text brightness | `100` | number | 100 is the colour as picked; lower values make the text dimmer. |

## Watch menu (`watch_section`)

Opened by the Watch key. Add one row per item.

| Input | Name | Default | Type | What it does |
|---|---|---|---|---|
| `watch_title` | Menu title | `Watch` | text |   |
| `watch_items` | Items | *(no rows)* | list of rows: `label` = text, `target` = entity (scene, script, automation) | Each row has a name (shown on the remote) and the scene, script or automation it runs. |

## Listen menu (`listen_section`)

Opened by the Listen key. Add one row per item.

| Input | Name | Default | Type | What it does |
|---|---|---|---|---|
| `listen_title` | Menu title | `Listen` | text |   |
| `listen_items` | Items | *(no rows)* | list of rows: `label` = text, `target` = entity (scene, script, automation) | Each row has a name (shown on the remote) and the scene, script or automation it runs. |

## Room controls (List key) (`room_section`)

Opened by the List key. Switches and fans toggle when chosen. Lights, thermostats and blinds open a small menu (Cancel goes back). Thermostats show measured temperature and supported modes; range targets adjust independently. Scenes, scripts and automations run.

| Input | Name | Default | Type | What it does |
|---|---|---|---|---|
| `room_title` | Menu title | `Room` | text |   |
| `room_items` | Items | *(no rows)* | list of rows: `label` = text, `entity` = entity (light, switch, input_boolean, fan, cover, climate, humidifier, valve, media_player, scene, script, automation) | Each row has a name (shown on the remote) and the thing it controls. |
| `show_states` | Show the state after each name | on | on / off | e.g. "Floor Lamp 60%" or "Thermostat Now73 H/C". Climate names are shortened to fit the measured temperature and configured mode. |
| `room_feedback` | Show a result message after a Room action | off | on / off | Off (default): the remote stays quiet and you see the light, fan or thermostat change. On: the screen also shows a short message such as "Floor Lamp: On", or "Running: Movie" for a scene. |

## Other keys (scene, script or automation) (`keys_section`)

Each key runs the scene, script or automation you pick. Leave empty to ignore the key.

| Input | Name | Default | Type | What it does |
|---|---|---|---|---|
| `i_target` | I key | *(empty)* | entity (scene, script, automation) |   |
| `ii_target` | II key | *(empty)* | entity (scene, script, automation) |   |
| `iii_target` | III key | *(empty)* | entity (scene, script, automation) |   |
| `prev_target` | Prev key | *(empty)* | entity (scene, script, automation) |   |
| `dvr_target` | DVR key | *(empty)* | entity (scene, script, automation) |   |

## TV / streamer control (full remote) (`media_section`)

Where the navigation, transport, digit and volume keys are sent. Leave empty to ignore those keys.

| Input | Name | Default | Type | What it does |
|---|---|---|---|---|
| `remote_target` | Remote entity | *(empty)* | entity (remote) | A `remote` entity (Roku, Android TV, Apple TV, Harmony ...). Receives D-pad, transport, digit, channel and colour keys. |
| `volume_target` | Volume target | *(empty)* | entity (media_player) | The media player controlled by Vol + / Vol - / Mute. |
| `show_volume` | Show the volume on the remote's screen | on | on / off | The volume of the target above is shown on the second line of the header: when the remote is picked up, and again after every Vol + / Vol - / Mute. A device that is off shows "Vol: device off". |
| `volume_style` | Volume display | `number_bar` | select | How the level is drawn on the header's second line. Hash, Equals, Star and Marker use 10 positions, rounded to the nearest 10% of the displayed level. Marker shows one position, not a filled bar. |
| `volume_precision` | Volume percentage precision | `whole` | select | Whole percentages keep the existing display. One decimal uses the fractional percentage reported by the media player, not receiver-scale units or dB. This changes the display only, not volume steps. |
| `volume_settle_ms` | Wait for the receiver (ms) | `300` | number | After a volume key, how long to wait for the receiver to report its new level before the screen is updated. The remote can only receive for about half a second after a key event, so keep this below 450. |

## Key command names (default = Roku) (`commands_section`)

The command string sent to the remote entity for each key. The defaults are the key names of Home Assistant's Roku integration (up, select, back, home, reverse, forward, replay, channel_up ...). Leave a field empty to ignore that key. Other platforms use other spellings, e.g. Android TV DPAD_UP / MEDIA_PLAY.

| Input | Name | Default | Type | What it does |
|---|---|---|---|---|
| `up_command` | Up | `up` | text |   |
| `down_command` | Down | `down` | text |   |
| `left_command` | Left | `left` | text |   |
| `right_command` | Right | `right` | text |   |
| `select_command` | Select / OK | `select` | text |   |
| `cancel_command` | Cancel / Back | `back` | text |   |
| `home_command` | Control4 key (Home) | `home` | text |   |
| `menu_command` | Menu | *(empty)* | text |   |
| `info_command` | Info | `info` | text |   |
| `guide_command` | Guide | *(empty)* | text |   |
| `play_command` | Play | `play` | text |   |
| `pause_command` | Pause | `play` | text | Roku has no separate Pause; play toggles. |
| `stop_command` | Stop | *(empty)* | text |   |
| `skip_back_command` | Skip back | `replay` | text |   |
| `skip_forward_command` | Skip forward | *(empty)* | text |   |
| `rewind_command` | Rewind | `reverse` | text |   |
| `fast_forward_command` | Fast forward | `forward` | text |   |
| `record_command` | Record | *(empty)* | text |   |
| `page_up_command` | Page up | *(empty)* | text |   |
| `page_down_command` | Page down | *(empty)* | text |   |
| `channel_up_command` | Channel up | `channel_up` | text |   |
| `channel_down_command` | Channel down | `channel_down` | text |   |
| `red_command` | Red | *(empty)* | text |   |
| `green_command` | Green | *(empty)* | text |   |
| `yellow_command` | Yellow | *(empty)* | text |   |
| `blue_command` | Blue | *(empty)* | text |   |
| `digit_command_template` | Digits 0-9 (template) | `Lit_{n}` | text | The text {n} is replaced by the digit. Roku example Lit_{n}. Android TV / LG example {n}. |
| `star_command` | Star (*) | `Lit_*` | text |   |
| `hash_command` | Hash (#) | `Lit_#` | text |   |
