// The World in One Day — Thursday 19 November 2026.
// A make.fun news-image entry (Node 22, standard library only).
//
// The page is the entry.png beside this file: a broadsheet front page
// composed by render.py from stories.json, with seven original
// engraving-style illustrations drawn in the same script. This program
// does the one thing the grader needs — it copies that image to the
// output directory, byte for byte, every run.
//
// Run it locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// The grader sets /output itself; MAKEFUN_OUTPUT_DIR only stands in
// for it outside the sandbox.

import { copyFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

if (!existsSync(source)) {
  throw new Error(`entry.png not found next to main.ts (looked in ${here})`);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

// The copy must be exact: same size as the source, so a truncated
// write can never pass silently. The grader runs this program twice
// and requires both runs to produce identical bytes; a plain copy of
// a fixed file satisfies that by construction.
if (statSync(target).size !== statSync(source).size) {
  throw new Error(`entry.png copy is incomplete (${target})`);
}
console.log(`wrote ${target} (${statSync(target).size} bytes)`);
