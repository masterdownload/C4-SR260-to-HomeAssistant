# Public package changelog

## v0.1

Experimental initial standalone package, not a stable release.

- Fixed registration recovery's two-attempt process-lifetime lockout: keep
  60-second cooldown/two-attempt bursts, but renew on a later announcement
  after 15 quiet minutes, or a changed network address after cooldown.
  Already-active identity/status traffic does not re-register. Preserve the
  existing response/report/MTORR sequence and all blueprint/battery behavior.
  Later physical recovery remains separate from offline regression evidence.
- Dual-target thermostat Heat/Cool rows now open a picker with five reported
  steps below and five above the target, omitting the current value. Filter
  unsafe choices without clamping; Cancel returns one level without a write.
  Entity/layout/snapshot routing rejects stale selections. Single-setpoint
  controls, media mappings and quirks are unchanged. Blueprint-only update;
  physical picker acceptance is not yet claimed.
- Added a UI-first guide for ordered multi-command actions, System Bridge and
  external IR hardware, linked from blueprint help and the README. Clarified
  automation-condition and script-waiting semantics; runtime, selectors and
  defaults are unchanged. Help-only blueprint update, not a new deployment.
- Removed the ten optional digit-action selectors at the owner's request.
  Digits 0-9 still use the unchanged editable command template. The 28 other
  overrides remain; only the blueprint needs updating for this reduction.
- Optional scene/automation overrides for 28 non-digit media keys,
  once per short press; empty selections preserve command text and
  existing command repeats. Added a manual official-source command reference,
  not platform presets or runtime downloads.
- Native ZHA Battery diagnostics from valid passive battery-percent reports,
  unknown before data, with standard half-percent scaling and cache retention.
  Correct only the resolved SR-260's misleading mains-power flag; no polling,
  firmware changes or guesses from unrelated status attributes.
- Experimental controller identity-response form before report/MTORR for
  verified/cached SR-260s, with unchanged existing identity values/endpoints.
  The earlier report/MTORR-only physical attempt did not restore key traffic;
  the response-first form then enabled captured List/Room Off events and menus
  on one cache-preserved replacement, with the wake header owner-confirmed.
  Uncached first-join physical acceptance remains unverified. Radio-return
  failures are validated rather than inferred from a completed API call.
- Added bounded controller identity-report then MTORR registration for verified/
  cached SR-260s, including reset/rejoin. It uses existing helpers/values, logs
  failures, and does not broadcast on unverified models or each key press.
  This earlier report/MTORR-only form did not restore the replacement's key
  traffic; it was superseded by the response-first form above.
- Added strict parsing for the captured manufacturer-`0x1040` cluster-command-1
  identity frame. This adds identity coverage without new outbound commands;
  it is not a fix or acceptance claim for missing physical key/menu traffic.
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
