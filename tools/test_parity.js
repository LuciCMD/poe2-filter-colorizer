#!/usr/bin/env node
/*
  Runs the engine inside index.html and filter_themer.py over the same filters, with every theme
  and every option combination, and checks the two outputs are byte-identical and that no item
  moved between Show and Hide.

    node tools/test_parity.js "path/to/a.filter" ["path/to/b.filter" ...]

  Needs Python 3 on PATH as "python" (or set PYTHON).
*/
"use strict";
const fs = require("fs"), os = require("os"), path = require("path");
const { execFileSync } = require("child_process");

const ROOT = path.join(__dirname, "..");
const html = fs.readFileSync(path.join(ROOT, "index.html"), "utf8");
const data = html.match(/<script id="data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const engine = html.match(/\/\* engine:start[\s\S]*?\*\/([\s\S]*?)\/\* engine:end \*\//)[1];
const { convert, verify } = new Function("D", engine + "\nreturn {convert, verify};")(JSON.parse(data));
const D = JSON.parse(data);

const files = process.argv.slice(2);
if (!files.length) { console.error("give one or more .filter files"); process.exit(2); }
const PY = process.env.PYTHON || "python";
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "themer-"));
const OPTS = [{ t0: true, split: true }, { t0: false, split: true }, { t0: true, split: false }, { t0: false, split: false }];
let failed = 0, runs = 0;

for (const file of files) {
  const text = fs.readFileSync(file, "utf8");
  for (const theme of D.themes) {
    const themePath = path.join(tmp, "theme.json");
    fs.writeFileSync(themePath, JSON.stringify(theme));
    for (const o of OPTS) {
      runs++;
      const res = convert(text, theme, o);
      const out = path.join(tmp, "out.filter");
      const args = [path.join(ROOT, "filter_themer.py"), file, out, "--theme=" + themePath];
      if (!o.t0) args.push("--no-t0");
      if (!o.split) args.push("--no-split");
      execFileSync(PY, args, { stdio: "ignore" });
      const py = fs.readFileSync(out, "utf8");
      const label = `${path.basename(file)} | ${theme.name} | t0=${o.t0} split=${o.split}`;
      if (py !== res.text) { failed++; console.log("DIFFERENT  " + label); continue; }
      const moved = verify(res.before, res.after, o).filter(([, d, okAdd, okRem]) => d.add > okAdd || d.rem > okRem);
      if (moved.length) { failed++; console.log("MOVED      " + label + ": " + moved.map(r => r[0]).join(", ")); continue; }
      if (res.unmapped.length) console.log("unmapped   " + label + ": " + res.unmapped.join(" "));
    }
  }
}
fs.rmSync(tmp, { recursive: true, force: true });
console.log(`${runs - failed} of ${runs} runs identical and clean`);
process.exit(failed ? 1 : 0);
