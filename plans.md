# Adapter Architecture Plan (Detailed)

## Objectives
- Support multiple browser backends with a unified adapter interface.
- Split configuration into:
  - BaseConfig: required, shared across all adapters.
  - ExtraConfig: adapter-defined optional fields, rendered dynamically in UI.
- Provide a single launch entry point that accepts BaseConfig + ExtraConfig.
- Keep backward compatibility with existing profiles where possible.

## Constraints and Assumptions
- Two adapters required: Chromium and Camoufox.
- UI controls allowed for ExtraConfig fields:
  - LineEdit, DatePicker/TimePicker, SpinBox, CheckBox, ComboBox, SwitchButton, Slider.
- Large refactor allowed.
- Camoufox uses Playwright-based launch (not Chromium/DrissionPage).

## Current System Audit (Summary)
- Launch flow: `app/features/launch.py` -> `app/workers.py` -> `app/profile_utils.py` -> DrissionPage `ChromiumPage`.
- Profile storage: `spoofers/profile.py` saves a JSON per profile.
- Profile UI is static in `app/ui_builders.py`; change handling in `app/features/profiles.py`.

---

## Phase 1: Design the Adapter Layer

### 1.1 Adapter Interface
Define an abstract adapter interface and registry.

Proposed interface:
- `id`: unique adapter id (e.g., "chromium", "camoufox")
- `label`: display name
- `get_base_config_schema() -> BaseConfigSchema`
- `get_extra_config_schema() -> list[FieldSchema]`
- `validate(base_config, extra_config) -> list[ValidationError]`
- `launch(base_config, extra_config) -> LaunchResult`

Notes:
- `BaseConfigSchema` is fixed across adapters.
- `FieldSchema` includes field type, label, default, options, validation rules.

### 1.2 BaseConfig Definition
BaseConfig should include fields required for any adapter. Proposed minimum:
- `profile_id` (string)
- `browser_adapter` (string)  // adapter id
- `browser_path` (optional string)
- `target_url` (string)
- `user_data_dir` or profile storage path (string)
- `proxy` (optional string or dict)

Validation rules:
- `profile_id` non-empty
- `browser_adapter` exists in registry
- `target_url` valid URL (or allow empty -> default)
- `browser_path` exists if provided

### 1.3 ExtraConfig Schema
FieldSchema example:
- `key`: string
- `label`: string
- `type`: enum: text/date/time/spin/checkbox/combo/switch/slider
- `default`: any
- `options`: list of (label, value) for combo
- `min`, `max`, `step`: for spin/slider
- `placeholder`, `help_text`
- `required`: bool

ExtraConfig stored as key/value map per adapter.

### 1.4 Storage Format
Extend profile JSON to include:
- `base_config`: object
- `extra_config`: object
- `adapter_id`: string

Backward compatibility strategy:
- On load: if old format, map legacy fields to BaseConfig + Chromium ExtraConfig.
- On save: always write new format, optionally keep legacy fields until migration complete.

---

## Phase 2: UI and Data Flow

### 2.1 UI Structure
- Profile list remains left.
- Right panel contains:
  - BaseConfig section (fixed fields)
  - ExtraConfig section (dynamic fields from adapter)

### 2.2 Dynamic Form Renderer
Implement a renderer that takes FieldSchema list and builds widgets:
- text -> LineEdit
- date/time -> DatePicker/TimePicker
- spin -> SpinBox
- checkbox -> CheckBox
- combo -> ComboBox
- switch -> SwitchButton
- slider -> Slider

Binding:
- On value change, update ExtraConfig dict in memory.
- Apply validation on edit commit; show error if invalid; revert to last valid.

### 2.3 Validation + Save
- When any field changes:
  - Validate BaseConfig + ExtraConfig via adapter.
  - If valid, persist to JSON.
  - If invalid, show dialog with example and keep previous value.

---

## Phase 3: Adapter Implementations

### 3.1 Chromium Adapter
- Uses current DrissionPage + spoofers logic.
- Map existing fields to BaseConfig / ExtraConfig:
  - BaseConfig: profile_id, adapter_id=chromium, browser_path, target_url
  - ExtraConfig: existing fingerprint fields (user_agent, timezone, locale, screen, etc.)
- Launch:
  - Use current `build_chromium_options` and `apply_pre_navigation_spoofing`.

### 3.2 Camoufox Adapter
- Use Playwright-based launcher.
- Provide ExtraConfig fields relevant to Camoufox (os, locale, geo, timezone, humanize, headless, proxy, etc.).
- Launch strategy:
  - Create a dedicated worker to run Playwright.
  - Provide mapping from ExtraConfig to Camoufox config JSON.
- Use a separate browser process lifecycle from DrissionPage.

---

## Phase 4: Plumbing Changes

### 4.1 Adapter Registry
- New module: `app/adapters/__init__.py`
- Register ChromiumAdapter and CamoufoxAdapter.
- Provide `get_adapter(adapter_id)` and `list_adapters()`.

### 4.2 Update Launch Flow
- Replace direct Chromium launch with adapter dispatch:
  - `BrowserLaunchWorker` should select adapter by `base_config.adapter_id`.
  - Invoke adapter.launch with unified config.

### 4.3 Update Profile Load/Save
- Replace direct `SpoofProfile` dependency with BaseConfig + ExtraConfig storage.
- Provide migration for existing JSON files.

---

## Phase 5: Compatibility and Migration

### 5.1 Migration Strategy
- On load:
  - If legacy profile found, build new structure in memory.
  - Allow user to save to upgrade format.
- On save:
  - Always save new structure.

### 5.2 Versioning
- Add `profile_schema_version` to JSON.
- Use version to determine migration path.

---

## Phase 6: Testing and Verification

### 6.1 Manual Verification
- Create profile with Chromium adapter and launch successfully.
- Switch adapter to Camoufox, set ExtraConfig, launch successfully.
- Save and reload; verify Base/Extra persisted.

### 6.2 Regression Areas
- Existing profile list and display name
- Browser library integration
- Onboarding flow

---

## Implementation Order (Suggested)
1) Define adapter interface + registry.
2) Define BaseConfig + ExtraConfig schema and storage changes.
3) Build dynamic UI for ExtraConfig.
4) Port Chromium adapter.
5) Implement Camoufox adapter.
6) Add migration and validation.
7) Manual verification.
