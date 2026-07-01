# 7D2D SandboxCode Tools

Unofficial encoder/decoder for the **7 Days to Die V3.0 SandboxCode** format.

This repo gives you two simple tools:

- `index.html` - browser-only encoder/decoder for GitHub Pages.
- `sandbox_code.py` - standard-library Python CLI encoder/decoder.

No build step. No third-party Python packages. No game files or game assets are included.

## Use on GitHub Pages

Put this repository on GitHub, then enable Pages for the repository root or the branch root. The `index.html` file is already at the root, so GitHub Pages can serve it directly.

## Browser use

Open `index.html` in a browser, paste a SandboxCode, click **Decode input**, edit values, then copy the generated code.

Unknown blocks are shown separately and preserved when the **keep unknown blocks** checkbox is enabled.

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
- unknown block `EHK` is preserved;
- decode -> JSON -> encode can roundtrip the sample code.

## Known limitation

The bundled mapping is based on public references and is not guaranteed to match every future game build. Unknown blocks are still preserved, but their setting names and values cannot be displayed until the mapping is updated.

Known missing public mapping at package time:

- `EH` / option id `111`
- `EI` / option id `112`

That is why a block like `EHK` is preserved but shown as unknown.

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
