# Making a Theme

A theme is a small JSON file that says what colour each kind of drop gets. You can load one into
the page with **Load Theme File**, or add it to `themes/` so it ships with the tool.

## Theme File Format

```json
{
  "name": "Cotton Candy",
  "author": "LuciferTFFT#1636",
  "notes": "One or two sentences shown under the theme picker.",
  "roles": {
    "currency_a": { "t": "58 18 36", "b": "255 226 234", "g": "255 168 190",
                    "e": "Pink", "m": "Pink" }
  }
}
```

| Key | Meaning |
|---|---|
| `t` | text colour, `"r g b"` |
| `b` | border colour |
| `g` | background colour |
| `e` | light beam colour, one word |
| `m` | minimap icon colour, one word |

**Colours are `"r g b"`: three numbers, no alpha.** The themer copies the alpha from the original
line, which is how translucent backgrounds survive. Add a fourth number only to override it on purpose.

**`e` and `m` take a colour name only**, from the set the game allows:
`Red Green Blue Brown White Yellow Cyan Grey Orange Pink Purple`.
Minimap icon shape and size, and the `Temp` flag on beams, come from the player's own filter and
aren't part of a theme; that keeps shapes right when the filter changes.

Any key can be left out, and that property is then left alone. A role with no entry at all keeps
its original colours and is listed in the report.

The easiest start is to copy one of the files in `themes/` and change the colours.

## Design Rules

The bundled themes follow these, and a theme that breaks them tends to look wrong in play:

1. **Fill means importance.** A filled plate says *stop for this*; coloured text on a dark ground
   says *keep moving*. Rank within a category moves down that ramp rather than tinting everything
   the same way.
2. **Higher tier, more vibrant.** Saturation and contrast fall as the tier falls.
3. **Uniques are never yellow.** Rare gear is yellow in PoE, and the two are easy to confuse at a
   glance. Keep uniques in one hue family well away from it, and give rare gear no filled background,
   so a filled warm plate can only mean a unique.
4. **Apex is unmistakable and unique in the file.** No other role shares its look.
5. **Contrast of at least 4.5:1** between `t` and `g` on every role that sets both. Labels are small
   and read in motion.
6. **No ground darker than about 15% lightness on a role that also sets text.** Below that it reads
   as a black box, which looks broken rather than quiet. Quiet tiers get a muted colour, not an
   absence of one.
7. **Categories get hue families, ranks get brightness.** Currency, fragments, uniques, exotics and
   gems should be recognisable by hue before you read the word. A demoted rank keeps its family's hue
   so the relationship stays visible.

Graphite breaks rule 7 on purpose, ranking everything by brightness, and says so in its notes.

## Currency Variants

PoE 2 currencies come in ranks: **Lesser, base, Greater, Perfect**. They do the same thing but force
a higher minimum modifier tier, and their values differ wildly. NeverSink already tiers them by
economy value, and a theme shouldn't fight that:

| Example | NeverSink Tier |
|---|---|
| Perfect Chaos, Exalted and Jeweller's Orb | S (apex) |
| Greater Chaos, Perfect Augmentation, Perfect Regal | A |
| Greater Exalted, Perfect Transmutation | B |
| Greater Jeweller's, Greater Regal | C |
| Greater Augmentation, Greater Transmutation | D |
| Orb of Transmutation, Blacksmith's Whetstone | D (vendor filler in practice) |

**A Greater or Perfect orb is never styled as junk.** With **Split Transmutation from Alchemy** on,
the themer moves only plain `Orb of Transmutation` and `Blacksmith's Whetstone` to the quiet
`supply_mid` step, moves the Greater and Perfect Transmutation and Augmentation orbs one notch down
into `supply_variant`, and leaves everything else in tier D loud. Anything it doesn't recognise stays
loud, so a future change to tier D fails safe.

## Adding a Theme to the Tool

1. Put the file in `themes/` as `theme-yourname.json`.
2. Run `python3 tools/embed_themes.py`. It copies every theme into `index.html` and the command-line
   tool, so the page keeps working as a single file opened from disk.
3. Open `index.html` and check the Live Preview.
4. If you have a NeverSink filter handy, `node tools/test_parity.js your.filter` checks that the page
   and the command-line tool give the same result, and that no item moved between Show and Hide.

## Role Reference

77 roles, covering 91 style classes. A theme should define all of them.

**Currency**

| Role | What It Is | Style Classes It Covers |
|---|---|---|
| `apex` | Apex | `apex_stier` |
| `currency_a` | Currency A | `currency_a`, `xeno_a` |
| `currency_b` | Currency B | `currency_b`, `xeno_b` |
| `currency_c` | Currency C | `currency_c`, `xeno_c` |
| `currency_d` | Currency D | `currency_d` |
| `currency_e` | Currency E | `currency_e` |
| `supply_mid` | Vendor Supplies | `currency_dlow`, `currency_supply2` |
| `supply_low` | Supplies, Low | `currency_supply4`, `xeno_e` |
| `supply_variant` | Utility Variant | `currency_dvariant` |

**Fragments**

| Role | What It Is | Style Classes It Covers |
|---|---|---|
| `fragment_a` | Fragment A | `fragments_a`, `fragments_splinter1` |
| `fragment_b` | Fragment B | `fragments_b`, `fragments_splinter2` |
| `fragment_c` | Fragment C | `fragments_c`, `fragments_splinter3` |
| `fragment_d` | Fragment D | `fragments_d`, `fragments_fragdmuted`, `fragments_splinter4` |
| `fragment_e` | Fragment E | `fragments_e`, `fragments_splinter5` |

**Uniques**

| Role | What It Is | Style Classes It Covers |
|---|---|---|
| `unique_t0` | Unique T0 / Chase | `uniques_t0` |
| `unique_a` | Unique T2 | `uniques_a` |
| `unique_b` | Unique T3 | `uniques_b` |
| `unique_c` | Unique, Low | `uniques_c` |
| `unique_exceptional` | Unique, Exceptional | `uniques_exceptional` |
| `unique_special` | Unique, Special Base | `uniques_x` |
| `unique_boss` | Unique, Boss Drop | `uniques_xbossdrop` |

**Exotics**

| Role | What It Is | Style Classes It Covers |
|---|---|---|
| `exotic_high` | Exotic Base | `exotics_btier`, `exotics_ctier` |
| `exotic_low` | Exotic Base, Low | `exotics_dtier` |
| `exotic_mod` | Exotic Mod | `exotics_identifiedmod` |
| `artifact_high` | Artifact, High | `exotics_artifacthigh` |
| `artifact` | Artifact | `exotics_artifact` |
| `corrupt` | Corrupted Marker | `exotics_corrupt` |
| `corrupt_high` | Corrupted, High | `exotics_corrupthigh` |

**Gems**

| Role | What It Is | Style Classes It Covers |
|---|---|---|
| `gem_high` | Gem | `typebased_gems1`, `typebased_gems2` |
| `gem_low` | Gem, Low | `typebased_gems3` |
| `quest` | Quest Item | `typebased_quest` |

**Waystones**

| Role | What It Is | Style Classes It Covers |
|---|---|---|
| `map_top` | Waystone T16 | `maps_regularhighest` |
| `map_high` | Waystone, High | `maps_regularhigh` |
| `map_mid` | Waystone, Mid | `maps_regularmid` |
| `map_low` | Waystone, Low | `maps_regularlow` |
| `map_special_high` | Map-Like, High | `maps_specialb` |
| `map_special_low` | Map-Like | `maps_specialc` |
| `deco_bright` | Waystone Deco | `maps_deco1`, `maps_deco2` |
| `deco_dim` | Waystone Deco, Dim | `maps_deco3`, `maps_deco4`, `maps_decooverlevel` |
| `deco_upgrade` | Waystone Upgrade | `maps_decotierupgrade` |

**Gear**

| Role | What It Is | Style Classes It Covers |
|---|---|---|
| `jewel_tiered` | Jewellery, Tiered | `gear_jewelrare`, `gear_tieredjewellery` |
| `jewel_ground_high` | Jewellery Ground | `gear_jewellery1` |
| `jewel_ground_low` | Jewellery Ground, Low | `gear_jewellery2` |
| `jewel_deco` | Jewellery Deco | `gear_decojewellery` |
| `jewel_magic` | Jewel, Magic | `gear_jewelmagic` |
| `jewel_magic_low` | Jewel, Magic Low | `gear_jewelmagiclow` |
| `ground_high` | Gear Ground, High | `gear_highlightdrop2`, `gear_highlightdrop3` |
| `ground_mid` | Gear Ground | `gear_highlightedsize` |
| `ground_weak` | Weak Rare | `gear_weakrare1`, `gear_weakrareleveling1` |
| `ground_weak2` | Weak Rare, Alt | `gear_weakrare2` |
| `ground_vendor` | Vendor Trash | `gear_vendor` |
| `ground_unremarkable` | Unremarkable | `utility_unremarkabledrop` |

**Crafting**

| Role | What It Is | Style Classes It Covers |
|---|---|---|
| `craft_chance` | Chancing Base | `itemproperty_achancing` |
| `craft_chance_low` | Chancing Base, Low | `itemproperty_bchancing` |
| `craft_eco_a` | Economy Craft A | `itemproperty_aecocraft` |
| `craft_eco_b` | Economy Craft B | `itemproperty_becocraft` |
| `craft_level82` | Item Level 82+ | `itemproperty_level82` |
| `craft_toplevel` | Top Base Level | `itemproperty_toplevelbased1` |
| `salvage_bright` | Salvageable | `itemproperty_salvage1`, `itemproperty_salvagelvl1` |
| `salvage_dim` | Salvageable, Dim | `itemproperty_salvage2` |

**Flasks**

| Role | What It Is | Style Classes It Covers |
|---|---|---|
| `flask_charm` | Charm | `typebased_flaskcharms` |
| `flask_charm_high` | Charm, High | `typebased_flaskcharms1high` |
| `flask_endgame` | Flask, Endgame | none (matched by rule path) |
| `flask_life` | Life Flask | none (matched by rule path) |
| `flask_mana` | Mana Flask | none (matched by rule path) |

**Gold**

| Role | What It Is | Style Classes It Covers |
|---|---|---|
| `gold_huge` | Gold, Huge Pile | `gold_pilehuge` |
| `gold_large` | Gold, Large | `gold_pilelarge` |
| `gold_medium` | Gold, Medium | `gold_pilemedium` |
| `gold_small` | Gold, Small | `gold_pilesmall` |

**New League**

| Role | What It Is | Style Classes It Covers |
|---|---|---|
| `xeno_d` | New League D | `xeno_d` |
| `unknown_item` | Unrecognised Item | `utility_unknownitem` |

**Utility**

| Role | What It Is | Style Classes It Covers |
|---|---|---|
| `deco_remove_normal` | Deco Remover | `utility_decoremovernormal` |
| `deco_remove_magic` | Deco Remover, Magic | `utility_decoremovermagic` |
| `rare_deco` | Rare Outline | `utility_basicraredecorator` |

**Levelling**

| Role | What It Is | Style Classes It Covers |
|---|---|---|
| `leveling_currency_rare` | Levelling Currency | none (matched by rule path) |
| `leveling_currency_magic` | Levelling Currency, Magic | none (matched by rule path) |
| `leveling_currency_start` | Levelling Currency, Start | none (matched by rule path) |

