#!/usr/bin/env python3
"""
Copies roles.json and every themes/theme-*.json into index.html and filter_themer.py, so the page
still works as a single file opened straight from disk. Run it after adding or editing a theme:

  python3 tools/embed_themes.py
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDER = ["cotton-candy", "twilight", "moonlight", "ember", "vivid", "verdant", "graphite", "clarity"]

def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f: return f.read()

def write(path, text):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8", newline="\n") as f: f.write(text)

def compact(obj): return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

def load_themes():
    names = [f[6:-5] for f in os.listdir(os.path.join(ROOT, "themes"))
             if f.startswith("theme-") and f.endswith(".json")]
    names.sort(key=lambda n: (ORDER.index(n) if n in ORDER else len(ORDER), n))
    themes = [json.loads(read(os.path.join("themes", "theme-%s.json" % n))) for n in names]
    for n, t in zip(names, themes):
        if not isinstance(t.get("roles"), dict) or not t.get("name"):
            sys.exit("themes/theme-%s.json needs a name and a roles object" % n)
    return themes

def main():
    roles = json.loads(read("roles.json"))
    themes = load_themes()

    html = read("index.html")
    data = compact({"roles": roles, "themes": themes}).replace("</", "<\\/")
    html, n = re.subn(r'(<script id="data" type="application/json">).*?(</script>)',
                      lambda m: m.group(1) + data + m.group(2), html, flags=re.S)
    if n != 1: sys.exit("index.html: data block not found")
    write("index.html", html)

    py = read("filter_themer.py")
    py, a = re.subn(r"^ROLES = json\.loads\(r'''.*?'''\)$",
                    lambda m: "ROLES = json.loads(r'''" + compact(roles) + "''')", py, flags=re.M)
    py, b = re.subn(r"^THEME = json\.loads\(r'''.*?'''\)$",
                    lambda m: "THEME = json.loads(r'''" + compact(themes[0]) + "''')", py, flags=re.M)
    if a != 1 or b != 1: sys.exit("filter_themer.py: ROLES or THEME line not found")
    write("filter_themer.py", py)

    print("embedded %d themes: %s" % (len(themes), ", ".join(t["name"] for t in themes)))

if __name__ == "__main__":
    main()
