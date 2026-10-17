# Public package changelog

## v0.1

Experimental initial standalone package, not a stable release.

- Corrected the automatic-discovery cold-start trigger to handle validated
  Device Announce traffic before private-profile identity polls exist.
  Announcement/prefix only permits a bounded query, never model inference.
  Recognition still requires a validated identity response; physical acceptance
  is not claimed from a query or successful restart alone. One already-paired
  unknown remote subsequently supplied that response and was automatically
  recognized with its quirk/key triggers exposed, without manual seeding or
  re-pairing. Fresh first-join and physical key/menu behavior remain separate checks.
- Automatic SR-260 identity learning from validated model traffic, with bounded
  probes and device-lifecycle activation for new or already-paired unknown
  remotes. Atomic model persistence replaces routine manual cache seeding on
  supported versions; wake/pairing and an initial quirk-load restart are still
  required. The manual method remains a fallback; see the capture-driven
  already-paired acceptance above for the physically verified scope.
- Fixed thermostat range menus: independent Heat/Cool targets, clear measured
  temperature and marked supported modes; safe limits, fractional/negative
  steps and stale-selection handling. Single-target controls remain available.
  Blueprint-only change; quirk files are unchanged.
- Added Hash, Equals, Star and Marker volume styles with ten-position ASCII
  indicators, plus optional one-decimal percentages. Existing styles/defaults
  and volume steps are unchanged; no quirk update is needed.
- Room Off configuration is always visible below Header, line 2 instead of
  inside the collapsed Other keys section. Existing inputs and behavior are unchanged.
- Room blueprint: Watch/Listen menus, Room controls, shortcut keys, TV/streamer
  commands, volume, wake header, clock and optional text color/brightness.
- Fifteen interdependent community quirk modules with raw-frame diagnostics,
  display commands and menu-selection control.
- Manual copy-and-paste installation instructions, downloadable blueprint,
  input reference and deployable-file manifest.
- Apache-2.0 license evidence, upstream attribution, prominent modified-file
  notices, generic examples and public-only documentation.

The full new blueprint behavior has not yet been physically verified. No
private deployment chronology, automation instances, tests or tools are included.
