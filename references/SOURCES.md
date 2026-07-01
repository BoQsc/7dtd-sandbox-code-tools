# Sources and References

Retrieved / packaged: 2026-07-01.

## Official game context

- 7 Days to Die official V3.0 Dead Hot Summer release notes:
  https://7daystodie.com/v3-0-dead-hot-summer-release-notes/

  Used as the official context that V3.0 introduced sandbox customization options and SandboxCode/server configuration changes.

- Steam News mirror for V3.0 Dead Hot Summer release notes:
  https://store.steampowered.com/news/app/251570/view/515245684596671416

## Technical format and setting table reference

- Labyricorn / 7D2D-Sandbox-Settings-Reports repository:
  https://github.com/Labyricorn/7D2D-Sandbox-Settings-Reports

- Sandbox settings report:
  https://github.com/Labyricorn/7D2D-Sandbox-Settings-Reports/blob/main/sandbox_settings_report.md

  Used for the public technical description of the format:

  - first character is the format version header;
  - remaining body is 3-character option blocks;
  - first two characters are the option id in A-Z base-26;
  - third character is the value index in A-Z;
  - default values may be omitted.

  Also used as the primary public reference for option names, properties, ids, defaults, and allowed values in `data/sandbox_options.json`; `BookLootCount` / `EH` is cross-checked separately because it is missing from this older 150-option report.

- Sandbox presets report:
  https://github.com/Labyricorn/7D2D-Sandbox-Settings-Reports/blob/main/sandbox-presets-report.md

  Useful for checking built-in preset codes.


- Host Havoc 7 Days to Die SandboxCode Generator:
  https://hosthavoc.com/tools/7-days-to-die/sandbox-code-generator

  Used as a cross-check for the newer/current 151-option set. This source lists **Book Abundance** / `BookLootCount` in the Resources section after **Magazine Abundance** / `CraftingMagazinesLootCount`, with the same loot-abundance value range from None through 500%.

  `BookLootCount` is included in this package as `EH` / option id `111` by inference from the current generator list plus the observed `EHK` block. The older Labyricorn report used as the main format source documents 150 options and does not list `EH`.

## Notes about copied content

The package does not include a full copy of the third-party report pages. It includes source URLs and a derived setting table for interoperability. If you want a stricter legal posture, verify the third-party reference license or regenerate the mapping directly from your own game installation.
