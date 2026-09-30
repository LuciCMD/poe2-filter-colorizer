#!/usr/bin/env python3
"""
Command-line counterpart to index.html. Same engine, same result.
Use the web page unless you want to script this.

USAGE
  python3 filter_themer.py <input.filter> [output.filter] [--theme=NAME_OR_FILE]
         [--no-t0] [--no-split]

  --theme=twilight      a bundled theme, from themes/theme-twilight.json next to this script
  --theme=my-theme.json any theme file; with no --theme, Cotton Candy is used

WHAT IT GUARANTEES
  Only SetTextColor / SetBorderColor / SetBackgroundColor / PlayEffect / MinimapIcon
  lines that already exist are rewritten. The set of items under Show and under Hide
  is compared before and after and printed; if it ever differs, do not use the file.
"""
import re, sys, json, os

ROLES = json.loads(r'''{"rolemap":{"apex_stier":"apex","currency_a":"currency_a","currency_b":"currency_b","currency_c":"currency_c","currency_d":"currency_d","currency_dlow":"supply_mid","currency_e":"currency_e","currency_supply2":"supply_mid","currency_supply4":"supply_low","fragments_a":"fragment_a","fragments_b":"fragment_b","fragments_c":"fragment_c","fragments_d":"fragment_d","fragments_e":"fragment_e","fragments_fragdmuted":"fragment_d","fragments_splinter1":"fragment_a","fragments_splinter2":"fragment_b","fragments_splinter3":"fragment_c","fragments_splinter4":"fragment_d","fragments_splinter5":"fragment_e","uniques_t0":"unique_t0","uniques_a":"unique_a","uniques_b":"unique_b","uniques_c":"unique_c","uniques_exceptional":"unique_exceptional","uniques_x":"unique_special","uniques_xbossdrop":"unique_boss","exotics_btier":"exotic_high","exotics_ctier":"exotic_high","exotics_dtier":"exotic_low","exotics_identifiedmod":"exotic_mod","exotics_artifacthigh":"artifact_high","exotics_artifact":"artifact","exotics_corrupt":"corrupt","exotics_corrupthigh":"corrupt_high","typebased_gems1":"gem_high","typebased_gems2":"gem_high","typebased_gems3":"gem_low","typebased_quest":"quest","maps_regularhighest":"map_top","maps_regularhigh":"map_high","maps_regularmid":"map_mid","maps_regularlow":"map_low","maps_specialb":"map_special_high","maps_specialc":"map_special_low","maps_deco1":"deco_bright","maps_deco2":"deco_bright","maps_deco3":"deco_dim","maps_deco4":"deco_dim","maps_decooverlevel":"deco_dim","maps_decotierupgrade":"deco_upgrade","gear_tieredjewellery":"jewel_tiered","gear_jewelrare":"jewel_tiered","gear_jewellery1":"jewel_ground_high","gear_jewellery2":"jewel_ground_low","gear_decojewellery":"jewel_deco","gear_jewelmagic":"jewel_magic","gear_jewelmagiclow":"jewel_magic_low","gear_highlightdrop2":"ground_high","gear_highlightdrop3":"ground_high","gear_highlightedsize":"ground_mid","gear_weakrare1":"ground_weak","gear_weakrareleveling1":"ground_weak","gear_weakrare2":"ground_weak2","gear_vendor":"ground_vendor","utility_unremarkabledrop":"ground_unremarkable","itemproperty_achancing":"craft_chance","itemproperty_bchancing":"craft_chance_low","itemproperty_aecocraft":"craft_eco_a","itemproperty_becocraft":"craft_eco_b","itemproperty_level82":"craft_level82","itemproperty_toplevelbased1":"craft_toplevel","itemproperty_salvage1":"salvage_bright","itemproperty_salvagelvl1":"salvage_bright","itemproperty_salvage2":"salvage_dim","typebased_flaskcharms":"flask_charm","typebased_flaskcharms1high":"flask_charm_high","gold_pilehuge":"gold_huge","gold_pilelarge":"gold_large","gold_pilemedium":"gold_medium","gold_pilesmall":"gold_small","xeno_a":"currency_a","xeno_b":"currency_b","xeno_c":"currency_c","xeno_d":"xeno_d","xeno_e":"supply_low","utility_unknownitem":"unknown_item","utility_decoremovernormal":"deco_remove_normal","utility_decoremovermagic":"deco_remove_magic","utility_basicraredecorator":"rare_deco","currency_dvariant":"supply_variant"},"noColour":["gear_unstyled","utility_highlight3","utility_highlight4","utility_minimize"],"noClass":[["\\$type->endgame->flasks","flask_endgame"],["\\$type->leveling->flasks->life","flask_life"],["\\$type->leveling->flasks->mana","flask_mana"],["\\$type->currency->leveling \\$tier->rare","leveling_currency_rare"],["\\$type->currency->leveling \\$tier->magic","leveling_currency_magic"],["\\$type->currency->leveling \\$tier->wisdomstart","leveling_currency_start"]],"roleInfo":{"apex":["Apex","Divine Orb","Currency"],"currency_a":["Currency A","Orb of Chance","Currency"],"currency_b":["Currency B","Chaos Orb","Currency"],"currency_c":["Currency C","Exalted Orb","Currency"],"currency_d":["Currency D","Orb of Alchemy","Currency"],"currency_e":["Currency E","Lesser Jeweller's Orb","Currency"],"supply_mid":["Vendor Supplies","Orb of Transmutation","Currency"],"supply_low":["Supplies, Low","Scroll of Wisdom","Currency"],"fragment_a":["Fragment A","Breachstone","Fragments"],"fragment_b":["Fragment B","Simulacrum Splinter","Fragments"],"fragment_c":["Fragment C","Breach Splinter","Fragments"],"fragment_d":["Fragment D","Timeless Splinter","Fragments"],"fragment_e":["Fragment E","Splinter","Fragments"],"unique_t0":["Unique T0 / Chase","Unique Item","Uniques"],"unique_a":["Unique T2","Unique Item","Uniques"],"unique_b":["Unique T3","Unique Item","Uniques"],"unique_c":["Unique, Low","Unique Item","Uniques"],"unique_exceptional":["Unique, Exceptional","Corrupted Unique","Uniques"],"unique_special":["Unique, Special Base","Unique Item","Uniques"],"unique_boss":["Unique, Boss Drop","Unique Item","Uniques"],"exotic_high":["Exotic Base","Breach Ring","Exotics"],"exotic_low":["Exotic Base, Low","Breach Ring","Exotics"],"exotic_mod":["Exotic Mod","Recombinator Base","Exotics"],"artifact_high":["Artifact, High","Expert Dualstring Bow","Exotics"],"artifact":["Artifact","Fishing Rod","Exotics"],"corrupt":["Corrupted Marker","Corrupted Base","Exotics"],"corrupt_high":["Corrupted, High","Corrupted Base","Exotics"],"gem_high":["Gem","Uncut Skill Gem","Gems"],"gem_low":["Gem, Low","Uncut Support Gem","Gems"],"quest":["Quest Item","Quest Item","Gems"],"map_top":["Waystone T16","Waystone (Tier 16)","Waystones"],"map_high":["Waystone, High","Waystone (Tier 14)","Waystones"],"map_mid":["Waystone, Mid","Waystone (Tier 9)","Waystones"],"map_low":["Waystone, Low","Waystone (Tier 3)","Waystones"],"map_special_high":["Map-Like, High","Expedition Logbook","Waystones"],"map_special_low":["Map-Like","Trial Coins","Waystones"],"deco_bright":["Waystone Deco","Waystone (Tier 15)","Waystones"],"deco_dim":["Waystone Deco, Dim","Waystone (Tier 10)","Waystones"],"deco_upgrade":["Waystone Upgrade","Waystone (Tier 16)","Waystones"],"jewel_tiered":["Jewellery, Tiered","Stellar Amulet","Gear"],"jewel_ground_high":["Jewellery Ground","Sapphire Ring","Gear"],"jewel_ground_low":["Jewellery Ground, Low","Gold Amulet","Gear"],"jewel_deco":["Jewellery Deco","Amber Amulet","Gear"],"jewel_magic":["Jewel, Magic","Breach Ring","Gear"],"jewel_magic_low":["Jewel, Magic Low","Breach Ring","Gear"],"ground_high":["Gear Ground, High","Sapphire Ring","Gear"],"ground_mid":["Gear Ground","Stellar Amulet","Gear"],"ground_weak":["Weak Rare","Rusted Sallet","Gear"],"ground_weak2":["Weak Rare, Alt","Hardwood Buckler","Gear"],"ground_vendor":["Vendor Trash","Iron Greaves","Gear"],"ground_unremarkable":["Unremarkable","Leather Belt","Gear"],"craft_chance":["Chancing Base","Sapphire Ring","Crafting"],"craft_chance_low":["Chancing Base, Low","Silver Charm","Crafting"],"craft_eco_a":["Economy Craft A","Expert Dualstring Bow","Crafting"],"craft_eco_b":["Economy Craft B","Expert Laced Boots","Crafting"],"craft_level82":["Item Level 82+","Furtive Wraps","Crafting"],"craft_toplevel":["Top Base Level","Omen Sceptre","Crafting"],"salvage_bright":["Salvageable","Advanced Vaal Cuirass","Crafting"],"salvage_dim":["Salvageable, Dim","Studded Vest","Crafting"],"flask_charm":["Charm","Ruby Charm","Flasks"],"flask_charm_high":["Charm, High","Golden Charm","Flasks"],"flask_endgame":["Flask, Endgame","Ultimate Life Flask","Flasks"],"flask_life":["Life Flask","Greater Life Flask","Flasks"],"flask_mana":["Mana Flask","Greater Mana Flask","Flasks"],"gold_huge":["Gold, Huge Pile","Gold","Gold"],"gold_large":["Gold, Large","Gold","Gold"],"gold_medium":["Gold, Medium","Gold","Gold"],"gold_small":["Gold, Small","Gold","Gold"],"xeno_d":["New League D","Unknown Item","New League"],"unknown_item":["Unrecognised Item","Unrecognised Item","New League"],"deco_remove_normal":["Deco Remover","Iron Ring","Utility"],"deco_remove_magic":["Deco Remover, Magic","Lazuli Ring","Utility"],"rare_deco":["Rare Outline","Rare Item","Utility"],"leveling_currency_rare":["Levelling Currency","Orb of Alchemy","Levelling"],"leveling_currency_magic":["Levelling Currency, Magic","Orb of Transmutation","Levelling"],"leveling_currency_start":["Levelling Currency, Start","Scroll of Wisdom","Levelling"],"supply_variant":["Utility Variant","Greater Orb of Transmutation","Currency"]}}''')
THEME = json.loads(r'''{"name":"Cotton Candy","author":"LuciferTFFT#1636","notes":"Pastel. Fill = importance: filled plate with dark text means stop for this; pastel text on a dark ground means keep moving. Uniques stay orange-red so they never read as rare-yellow.","roles":{"apex":{"t":"44 16 62","b":"255 176 208","g":"255 232 168","e":"Pink","m":"Pink"},"currency_a":{"t":"58 18 36","b":"255 226 234","g":"255 168 190","e":"Pink","m":"Pink"},"currency_b":{"t":"40 18 58","b":"242 224 255","g":"212 176 250","e":"Purple","m":"Purple"},"currency_c":{"t":"22 26 62","b":"226 232 255","g":"178 188 248","e":"Blue","m":"Blue"},"currency_d":{"t":"12 44 32","b":"216 250 234","g":"172 238 206","e":"Cyan","m":"Cyan"},"supply_mid":{"t":"186 196 208","b":"116 128 146","g":"56 62 74"},"currency_e":{"t":"176 208 250","b":"176 208 250","g":"28 32 70","e":"White","m":"White"},"supply_low":{"t":"146 148 158"},"fragment_a":{"t":"52 42 8","b":"255 248 216","g":"250 226 148","e":"Pink","m":"Pink"},"fragment_b":{"t":"50 40 16","b":"250 240 208","g":"230 212 158","e":"Orange","m":"Orange"},"fragment_c":{"t":"250 232 176","b":"250 232 176","g":"63 36 22","e":"Yellow","m":"Yellow"},"fragment_d":{"t":"250 232 176","b":"170 150 96","g":"63 36 22"},"fragment_e":{"t":"232 210 172","b":"140 126 96","g":"40 37 48"},"unique_t0":{"t":"56 12 10","b":"255 240 232","g":"255 150 128","e":"Orange","m":"Orange"},"unique_a":{"t":"56 26 4","b":"255 246 230","g":"255 196 150","e":"Orange","m":"Orange"},"unique_b":{"t":"238 168 140","b":"238 168 140","g":"60 32 24","e":"Brown","m":"Brown"},"unique_c":{"t":"198 150 130","b":"130 92 78","g":"54 37 30","e":"Brown","m":"Brown"},"unique_exceptional":{"t":"255 244 206","b":"170 240 208","g":"74 30 100","e":"Purple","m":"Purple"},"unique_special":{"t":"40 18 58","b":"238 226 255","g":"206 186 246","e":"Blue","m":"Blue"},"unique_boss":{"t":"40 18 58","b":"252 226 250","g":"240 178 232","e":"Purple","m":"Purple"},"exotic_high":{"t":"170 240 208","b":"170 240 208","g":"21 63 63","e":"Green","m":"Green"},"exotic_low":{"t":"150 206 170","b":"150 206 170","e":"Green"},"exotic_mod":{"t":"170 240 208","b":"170 240 208","g":"44 26 68","e":"Green","m":"Green"},"artifact_high":{"t":"255 182 168","b":"255 182 168","g":"62 23 39","e":"Orange","m":"Orange"},"artifact":{"t":"255 182 168","b":"255 182 168","g":"51 33 38","e":"Orange","m":"Orange"},"corrupt":{"b":"170 96 96 240"},"corrupt_high":{"b":"255 156 150"},"gem_high":{"t":"168 234 240","b":"168 234 240","g":"16 40 68","e":"Cyan","m":"Cyan"},"gem_low":{"t":"140 200 212","b":"140 200 212","e":"Cyan"},"quest":{"t":"176 244 168","e":"Green","m":"Green"},"map_top":{"t":"58 18 36","b":"255 226 234","g":"255 168 190","e":"Pink","m":"Pink"},"map_high":{"t":"250 232 176","b":"250 232 176","g":"62 57 22","e":"Yellow","m":"Yellow"},"map_mid":{"t":"250 244 238","e":"White","m":"White"},"map_low":{"t":"196 194 204","e":"White","m":"White"},"map_special_high":{"t":"40 18 58","b":"252 226 250","g":"240 178 232","e":"Purple","m":"Purple"},"map_special_low":{"t":"240 184 234","b":"240 184 234","e":"Purple","m":"Purple"},"deco_bright":{"b":"250 244 238"},"deco_dim":{"b":"196 194 204"},"deco_upgrade":{"b":"255 170 150"},"jewel_tiered":{"t":"250 232 176","b":"250 232 176","g":"62 57 22","e":"Yellow","m":"Yellow"},"jewel_ground_high":{"g":"46 42 16","e":"Yellow","m":"Yellow"},"jewel_ground_low":{"g":"28 26 16","e":"Yellow","m":"White"},"jewel_deco":{"b":"228 212 140"},"jewel_magic":{"t":"176 208 250","b":"176 208 250","g":"28 32 70","e":"Blue","m":"Blue"},"jewel_magic_low":{"t":"156 188 240","b":"156 188 240","e":"Blue","m":"Blue"},"ground_high":{"g":"44 26 68"},"ground_mid":{"g":"30 28 34"},"ground_weak":{"g":"36 33 42 240"},"ground_weak2":{"g":"58 56 66 190"},"ground_vendor":{"g":"28 26 32 180"},"ground_unremarkable":{"g":"28 26 32 140"},"craft_chance":{"t":"255 168 190","b":"255 168 190","g":"62 23 39","e":"Pink","m":"Pink"},"craft_chance_low":{"b":"170 240 208","e":"Green","m":"Green"},"craft_eco_a":{"t":"250 244 238","b":"255 182 168","g":"62 23 39","e":"Pink","m":"Pink"},"craft_eco_b":{"b":"255 182 168","g":"24 22 28","e":"Yellow","m":"Yellow"},"craft_level82":{"t":"250 214 150"},"craft_toplevel":{"b":"176 152 104"},"salvage_bright":{"b":"186 184 194"},"salvage_dim":{"b":"128 126 138"},"flask_charm":{"b":"150 206 170"},"flask_charm_high":{"b":"250 214 150","g":"18 46 32"},"gold_huge":{"t":"250 244 238","b":"250 232 176","g":"62 57 22","e":"Yellow","m":"Yellow"},"gold_large":{"t":"250 232 176","b":"250 232 176","e":"Yellow","m":"Yellow"},"gold_medium":{"t":"244 230 186","b":"216 200 150","e":"Yellow"},"gold_small":{"t":"180 176 172","b":"40 38 44","g":"48 44 37 180"},"xeno_d":{"t":"180 190 250","b":"180 190 250","e":"Cyan","m":"Cyan"},"unknown_item":{"t":"40 18 58","b":"168 234 240","g":"240 178 232","e":"Pink","m":"Pink"},"deco_remove_normal":{"t":"196 194 204","b":"32 30 36","g":"40 38 46 240"},"deco_remove_magic":{"t":"172 176 252","b":"32 30 36","g":"40 38 46 240"},"rare_deco":{"b":"32 30 36"},"flask_endgame":{"b":"250 214 150"},"flask_life":{"b":"244 168 178"},"flask_mana":{"b":"168 190 244"},"leveling_currency_rare":{"t":"250 244 238","b":"250 244 238","g":"28 32 70","e":"White","m":"White"},"leveling_currency_magic":{"t":"228 234 244","b":"228 234 244","g":"35 39 49"},"leveling_currency_start":{"t":"150 176 200","b":"150 176 200"},"supply_variant":{"t":"150 214 186","b":"150 214 186","g":"34 58 52","e":"Cyan","m":"Cyan"}}}''')

RM=ROLES["rolemap"]; NOCOL=set(ROLES["noColour"])
NOCLASS=[(re.compile(p), r) for p, r in ROLES["noClass"]]
PROPKEY={"SetTextColor":"t","SetBorderColor":"b","SetBackgroundColor":"g",
         "PlayEffect":"e","MinimapIcon":"m"}
HEAD=re.compile(r"^(#?)\s*(Show|Hide)\b"); CLS=re.compile(r"!([A-Za-z0-9_]+)\s*$")
PROP=re.compile(r"^(#?)(\s*)(SetTextColor|SetBorderColor|SetBackgroundColor|PlayEffect|MinimapIcon)\s+(.*?)\s*$")

def colour(val, orig):
    t, o = val.split(), orig.split()
    if len(t)==3 and len(o)==4: t.append(o[3])   # keep the original alpha
    return " ".join(t)
def beam(val, orig): return val + (" Temp" if "Temp" in orig else "")
def icon(val, orig):
    o=orig.split()
    return orig if len(o)<3 else " ".join([o[0], val] + o[2:])

def structural(lines, opt, log):
    if opt["t0"] and not any("!uniques_t0" in l for l in lines):
        for n,l in enumerate(lines):
            if l.startswith("Show # $type->uniques $tier->t1 !apex_stier"):
                lines[n]=l.replace("!apex_stier","!uniques_t0"); log("+","top-tier uniques given their own colour"); break
        else: log("!","top-tier unique rule not found - left as apex")
    if opt["split"] and not any("!currency_dlow" in l for l in lines):
        try:
            i=next(n for n,l in enumerate(lines) if l.startswith("Show # %H5 $type->currency $tier->d !currency_d"))
            end=next(n for n in range(i,len(lines)) if lines[n].startswith("CustomAlertSound"))
        except StopIteration:
            log("!","currency tier D rule not found - left exactly as it was"); return lines
        blk=lines[i:end+1]
        bi=next((n for n,l in enumerate(blk) if l.strip().startswith("BaseType")), -1)
        items=re.findall(r'"[^"]*"', blk[bi]) if bi>=0 else []
        # A Greater or Perfect orb outranks its base version and is never demoted to
        # the vendor bucket. Anything not named here stays loud, so a future change
        # to NeverSink's tier D fails safe.
        VENDOR =re.compile(r'^"(Orb of Transmutation|Blacksmith\'s Whetstone)"$')
        VARIANT=re.compile(r'^"(Greater|Perfect) Orb of (Transmutation|Augmentation)"$')
        vendor =[x for x in items if VENDOR.match(x)]
        variant=[x for x in items if VARIANT.match(x)]
        loud   =[x for x in items if not VENDOR.match(x) and not VARIANT.match(x)]
        if not items: log("!","tier D has no BaseType list - left as it was"); return lines
        def mk(head, names, size, eff, ico):
            out=[]
            for l in blk:
                s=l.strip()
                if   s.startswith("BaseType"):    out.append("\tBaseType == "+" ".join(names))
                elif s.startswith("SetFontSize"): out.append("\tSetFontSize %d"%size)
                elif s.startswith("PlayEffect"):  out.append("\tPlayEffect "+eff)
                elif s.startswith("MinimapIcon"): out.append("\tMinimapIcon "+ico)
                elif l.startswith("Show"):        out.append(head)
                else: out.append(l)
            return out
        new=[]
        if loud:    new += mk("Show # %H5 $type->currency $tier->d !currency_d", loud,45,"Cyan","1 Cyan Circle")+[""]
        if variant: new += mk("Show # %H4 $type->currency $tier->dvariant !currency_dvariant", variant,40,"Cyan Temp","2 Cyan Circle")+[""]
        if vendor:  new += mk("Show # %H3 $type->currency $tier->dsupply !currency_dlow", vendor,38,"White Temp","2 Grey Circle")+[""]
        new.pop()
        lines[i:end+1]=new
        log("+","tier D split: %d loud, %d variants stepped down, %d vendor orbs quieted"
              % (len(loud),len(variant),len(vendor)))
    return lines

def visibility(ls):
    shown,hidden=set(),set(); cur=None
    for l in ls:
        h=HEAD.match(l)
        if h: cur=None if h.group(1)=="#" else h.group(2); continue
        if not cur or not re.match(r"^\s*(BaseType|Class)\b", l): continue
        for q in re.findall(r'"[^"]*"', l): (shown if cur=="Show" else hidden).add(q)
    return shown,hidden

def apply(src, dst, theme, opt):
    raw=open(src,encoding="utf-8",newline="").read()
    nl="\r\n" if "\r\n" in raw else "\n"
    before=raw.split(nl); notes=[]
    lines=structural(before[:], opt, lambda k,m: notes.append((k,m)))
    out=lines[:]; spec=None; styled=touched=0; unmapped=set()
    for i,line in enumerate(lines):
        if HEAD.match(line):
            m=CLS.search(line.strip()); spec=None
            if m:
                role=RM.get(m.group(1))
                if role and role in theme["roles"]: spec=theme["roles"][role]; styled+=1
                elif m.group(1) not in NOCOL: spec={"__unknown":m.group(1)}
            else:
                spec=next((theme["roles"].get(r) for p,r in NOCLASS if p.search(line)), None)
            continue
        if not spec: continue
        p=PROP.match(line)
        if not p: continue
        if "__unknown" in spec: unmapped.add(spec["__unknown"]); continue
        v=spec.get(PROPKEY[p.group(3)])
        if v is None: continue
        nv = beam(v,p.group(4)) if p.group(3)=="PlayEffect" else \
             icon(v,p.group(4)) if p.group(3)=="MinimapIcon" else colour(v,p.group(4))
        if nv!=p.group(4): out[i]=p.group(1)+p.group(2)+p.group(3)+" "+nv; touched+=1
    for n,l in enumerate(out[:20]):   # name the theme in the header comment; the game ignores it
        if l.startswith("# STYLE:"):
            out[n]=("# STYLE:    "+theme["name"].upper()+
                    (" ("+theme["author"].split("#")[0]+")" if theme.get("author") else ""))
    open(dst,"w",encoding="utf-8",newline="").write(nl.join(out))

    sb,hb=visibility(before); sa,ha=visibility(out)
    print("  items shown  %5d  %s" % (len(sb), "unchanged" if sb==sa else "*** CHANGED - DO NOT USE ***"))
    print("  items hidden %5d  %s" % (len(hb), "unchanged" if hb==ha else "*** CHANGED - DO NOT USE ***"))
    print("  %d rules styled, %d colour lines rewritten" % (styled,touched))
    for k,m in notes: print("  %s %s" % (k,m))
    if unmapped:
        print("  UNMAPPED (left at original colours, add them to the theme):")
        for c in sorted(unmapped): print("    !"+c)
    print("  ->", dst)

def load_theme(arg):
    here=os.path.dirname(os.path.abspath(__file__))
    for p in (arg, os.path.join(here,"themes","theme-%s.json" % arg.lower().replace(" ","-"))):
        if os.path.isfile(p):
            with open(p,encoding="utf-8") as f: return json.load(f)
    sys.exit("theme not found: %s" % arg)

if __name__=="__main__":
    a=[x for x in sys.argv[1:] if not x.startswith("--")]
    f=[x for x in sys.argv[1:] if x.startswith("--")]
    if not a: sys.exit(__doc__)
    tp=[x.split("=",1)[1] for x in f if x.startswith("--theme=")]
    theme=load_theme(tp[0]) if tp else THEME
    src=a[0]
    dst=a[1] if len(a)>1 else re.sub(r"\.filter$","",src)+" - "+theme["name"]+".filter"
    apply(src,dst,theme,{"t0":"--no-t0" not in f,"split":"--no-split" not in f})
