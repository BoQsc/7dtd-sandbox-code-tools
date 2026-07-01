# 7D2D SandboxCode Tools

Unofficial encoder/decoder for the **7 Days to Die V3.0 SandboxCode** format.

This repo gives you two simple tools:

- `index.html` - browser-only encoder/decoder for GitHub Pages.
- `sandbox_code.py` - standard-library Python CLI encoder/decoder.

No build step. No third-party Python packages. No game files or game assets are included.

## Use on GitHub Pages

Put this repository on GitHub, then enable Pages for the repository root or the branch root. The `index.html` file is already at the root, so GitHub Pages can serve it directly.

The HTML page includes a **Source Code** button that opens `https://github.com/BoQsc/7dtd-sandbox-code-tools`.

## Browser use

Open `index.html` in a browser, paste a SandboxCode, click **Decode input**, edit values by category, then copy the generated code.

The browser page also supports shareable links. The current generated code is written into the URL as `?code=...`, so browser links can pass settings around directly. Opening a link like `index.html?code=AAAGCDA` loads that code automatically. The **Copy share link** button copies the current page URL with the latest generated SandboxCode.

Accepted URL forms:

```text
?code=AAAJABJACJADJARFBNC
?sandbox=AAAJABJACJADJARFBNC
?sandboxcode=AAAJABJACJADJARFBNC
#AAAJABJACJADJARFBNC
#code=AAAJABJACJADJARFBNC
```

The browser page uses category tabs/cards instead of one long settings table. Unknown blocks are shown separately and preserved when the **keep unknown blocks** checkbox is enabled.

## Python CLI use

Decode a code:

```bash
python sandbox_code.py decode AAAJABJACJADJARFBNC
```

Decode as JSON:

```bash
python sandbox_code.py decode AAAGABGACGADGARJAMJBUEBHIBOACDACVDCFBCHCCOHDAGDKKEHKFFAETA --json > decoded.json
```

Encode from individual settings:

```bash
python sandbox_code.py encode --set RangedDamage=0.85 --set BiomeProgression=False
```

The command above prints:

```text
AAAGCDA
```

Encode back from a decoded JSON file:

```bash
python sandbox_code.py encode --json decoded.json --keep-defaults
```

## Run tests

```bash
python tests.py
```

Expected output:

```text
OK: all tests passed
```

The tests check:

- default encoding returns `A`;
- simple `--set` encoding works;
- the sample code decodes known blocks;
- `EHK` decodes as `BookLootCount=2` / 200%;
- decode -> JSON -> encode can roundtrip the sample code.

## Known limitation

The bundled mapping is based on public references and is not guaranteed to match every future game build. Unknown blocks are still preserved, but their setting names and values cannot be displayed until the mapping is updated.

`EH` / option id `111` is included as **Book Abundance / `BookLootCount`**. This is not from the older 150-option report; it is inferred from newer/current public generators that list 151 settings and include Book Abundance after Magazine Abundance, together with a real observed `EHK` block whose `K` value index matches 200% in the shared loot-abundance value list. Verify against the exact game build if you need absolute certainty.

Known missing public mapping at package time:

- `EI` / option id `112`

## Project files

```text
index.html                         Browser encoder/decoder
sandbox_code.py                    Python CLI encoder/decoder
tests.py                           Basic tests
data/sandbox_options.json          Known setting table
examples/                          JSON generated during tests
references/SOURCES.md              Source links and derivation notes
references/FORMAT_NOTES.md         Short format summary
LICENSE                            MIT license for this package
NOTICE.md                          Unofficial/trademark/legal notes
```

## License

The scripts, HTML, README, and packaging files in this repository are released under the MIT License. See `LICENSE`.

The game title, setting names, and trademarks belong to their owners. This project is unofficial and is not affiliated with The Fun Pimps.


## HTML design note

The `index.html` page uses a compact dark grey / black in-game style layout inspired by the 7 Days to Die sandbox options screen. Settings are grouped by category instead of shown as one long list. The whole page is scaled to 110% with a single `--site-zoom` CSS variable near the top of the file. The page also supports URL sharing through the `code` query parameter.

## URL sharing

Supported URL forms:

```text
?code=AAAGCDA
?sandboxcode=AAAGCDA
?sandbox=AAAGCDA
#code=AAAGCDA
#AAAGCDA
```

The page writes the latest generated code back to `?code=...` with `history.replaceState`, so editing a setting does not create a long browser-back history chain.

