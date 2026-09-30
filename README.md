# PoE 2 Filter Themer

Recolour a [NeverSink](https://github.com/NeverSinkDev/NeverSink-Filter-for-PoE2) loot filter for
Path of Exile 2 with a theme, without touching which items it shows or hides.

**Use it here: https://lucicmd.github.io/poe2-filter-colorizer/**

Everything runs in your browser. Your filter is never uploaded, and the page also works offline if
you download `index.html` and open it from disk.

## How to Use It

1. Set up your filter on [FilterBlade](https://www.filterblade.xyz/?game=Poe2) as usual and download it.
2. Open the themer and drop the `.filter` file onto it.
3. Pick a theme. The Live Preview shows every tier as it will look on the ground.
4. Press **Apply Theme & Download**, then put the new file in
   `Documents/My Games/Path of Exile 2/` and pick it in the game's options.

Read the **What Changed** panel before you use the file. It compares the items shown and hidden
before and after, and turns red if anything moved, which should never happen.

## Themes

| Theme | Look |
|---|---|
| Cotton Candy | Pastel plates for loud drops, pastel text on dark for the rest. |
| Twilight | Deep jewel grounds with luminous accents; richer and colder than Cotton Candy. |
| Moonlight | Cool colours only: lavender, periwinkle, ice and seafoam. The calmest. |
| Ember | Warm and high contrast: orange and gold currency, deep crimson uniques, ash for the rest. |
| Vivid | Bold, saturated colours closest to classic filters. |
| Verdant | Forest tones: leaf and jade currency, honey fragments, deep berry uniques. |
| Graphite | Monochrome greys ranked by brightness, with one ember accent for uniques. |
| Clarity | Colourblind-friendly, after the Okabe-Ito palette; rank shows by brightness and fill. |

Want your own? See [THEMES.md](THEMES.md) for the file format and the design rules, then load it
with **Load Theme File**.

## Options

- **Give Top-Tier Uniques Their Own Colour**: NeverSink styles chase uniques exactly like Divine
  Orbs. This retags that one rule so a theme can colour them apart.
- **Split Transmutation from Alchemy**: they share one rule, so no theme can colour them apart.
  This splits it so plain Transmutation and Whetstones are quieter. Every part still shows.

Turn both off for a pure recolour.

## What It Changes, and What It Doesn't

Every rule in a NeverSink filter ends its comment with a style class, such as `!currency_a`. The
themer looks that class up in the theme and rewrites only the colour lines the rule already has:
`SetTextColor`, `SetBorderColor`, `SetBackgroundColor`, `PlayEffect` and `MinimapIcon`. Minimap icon
shape and size and temporary beams are kept from your file, and the `# STYLE:` comment at the top
names the theme. It never adds, removes or reorders a condition.

A style class a theme doesn't know, for example from a new league, is left at its original colour
and listed in the report.

## Usage Count

The page shows how many filters have been themed and by how many players. When you download a
filter from the published site, it adds one to a public counter at
[Abacus](https://jasoncameron.dev/abacus/), plus one more the first time a browser downloads. Nothing
about you or your filter is sent. Copies opened from disk make no network requests at all.

## Command Line

`filter_themer.py` does the same job from a terminal and gives byte-identical output:

```bash
python3 filter_themer.py "My Filter.filter" --theme=twilight
```

`--theme` takes a bundled theme's name or a path to a theme file (Cotton Candy if left out), and
`--no-t0` and `--no-split` turn the two options off.

## For Contributors

- `index.html` is the whole tool. The themes are embedded in it so it works from disk.
- `themes/` and `roles.json` are the sources. After changing them, run
  `python3 tools/embed_themes.py` to copy them into `index.html` and `filter_themer.py`.
- `node tools/test_parity.js some.filter` checks that the page and the command-line tool agree and
  that no item moves between Show and Hide, for every theme and option.

## Credits

Made by LuciCMD. Built for NeverSink's filters, which do all the hard work of deciding what matters;
this project isn't affiliated with NeverSink, FilterBlade or Grinding Gear Games.

Released under the [MIT Licence](LICENSE).
