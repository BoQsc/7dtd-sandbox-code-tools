# SandboxCode Format Notes

The observed/publicly documented format is compact and not encrypted.

```text
A AAG ABG ACG ...
^ ^^^ ^^^ ^^^
| |   |   |
| repeated 3-character blocks
format/version header
```

Each block is:

```text
AAJ
^^^
|||
|||_ value index, A = 0, B = 1, C = 2, ...
||__ option id, base-26 letters, AA = 0, AB = 1, BA = 26, ...
```

Examples:

```text
AAJ = option AA / id 0 / value index J / index 9
CD A = option CD / id 55 / value index A / index 0
```

Defaults are normally omitted. A minimal default code can be represented as:

```text
A
```

Unknown blocks should be preserved rather than discarded, because the table can be incomplete or game builds can change.

## Mapping note: `EH` / `EHK`

The older public technical report does not list `EH` / option id `111`. Newer/current public generators list 151 settings and include **Book Abundance** / `BookLootCount` after **Magazine Abundance** / `CraftingMagazinesLootCount`.

This package maps `EH` to `BookLootCount`. Therefore `EHK` decodes as value index `K` = `2` = 200% in the loot-abundance value list. Treat this as an interoperability inference unless you verify it against your exact game build.
