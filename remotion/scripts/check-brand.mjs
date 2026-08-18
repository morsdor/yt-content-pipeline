#!/usr/bin/env node
/**
 * brand:check — enforce brand_guide_software.md §3/§4/§5 across scene and family files.
 *
 * Why a linter instead of imported constants: Remotion Studio only makes a style
 * canvas-interactive when every value is an inline literal, so scenes MUST hardcode
 * colours and easing curves (see src/brand/tokens.ts). This script is what stops those
 * literals from drifting — it reads the allowed values straight out of tokens.ts, so
 * there is still exactly one source of truth.
 *
 * Run: npm run brand:check
 */

import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(fileURLToPath(new URL('.', import.meta.url)), '..');
const SRC = join(ROOT, 'src');
const TOKENS = join(SRC, 'brand', 'tokens.ts');

// ── read the single source of truth ─────────────────────────────────────────
const tokenSrc = readFileSync(TOKENS, 'utf8');

const allowedColors = new Set(
  [...tokenSrc.matchAll(/'(#[0-9A-Fa-f]{6})'/g)].map((m) => m[1].toUpperCase()),
);

// Scope to the EASE block only — CAMERA.pullBack is also a 4-number `as const` tuple,
// and hoovering it up here would silently whitelist Easing.bezier(6, 7, 8, 9).
const easeBlock = /export const EASE = \{([\s\S]*?)\n\} as const;/.exec(tokenSrc)?.[1] ?? '';
const allowedEasings = new Set(
  [...easeBlock.matchAll(/\[\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)\s*\]/g)].map((m) =>
    [m[1], m[2], m[3], m[4]].map(Number).join(','),
  ),
);
if (allowedEasings.size === 0) {
  console.error('brand:check ✗  could not parse EASE from src/brand/tokens.ts');
  process.exit(1);
}

const MIN_FONT_SIZE = Number(/min:\s*(\d+)/.exec(tokenSrc)?.[1] ?? 36);
const MIN_DAMPING = Number(/MIN_SPRING_DAMPING\s*=\s*(\d+)/.exec(tokenSrc)?.[1] ?? 200);

// ── walk the files we police ────────────────────────────────────────────────
const walk = (dir) => {
  let out = [];
  for (const entry of readdirSync(dir)) {
    const p = join(dir, entry);
    if (statSync(p).isDirectory()) out = out.concat(walk(p));
    else if (/\.tsx?$/.test(p) && !p.includes(`${'brand'}/`)) out.push(p);
  }
  return out;
};

const violations = [];
const add = (file, line, rule, detail) =>
  violations.push({ file: relative(ROOT, file), line, rule, detail });

for (const file of walk(SRC)) {
  const lines = readFileSync(file, 'utf8').split('\n');

  lines.forEach((text, i) => {
    const n = i + 1;

    // §3 — colours must be brand tokens
    for (const m of text.matchAll(/#[0-9A-Fa-f]{6}\b/g)) {
      if (!allowedColors.has(m[0].toUpperCase())) {
        add(file, n, '§3 colour', `${m[0]} is not a brand token`);
      }
    }

    // §5 — only the two sanctioned easing curves
    for (const m of text.matchAll(/Easing\.bezier\(\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)\s*\)/g)) {
      const key = [m[1], m[2], m[3], m[4]].map(Number).join(',');
      if (!allowedEasings.has(key)) {
        add(file, n, '§5 easing', `Easing.bezier(${key}) is not EASE.standard or EASE.exit`);
      }
    }

    // §5 — springs banned except a diagram node locking, damping >= 200
    for (const m of text.matchAll(/Easing\.spring\(\{[^}]*damping:\s*(\d+)/g)) {
      if (Number(m[1]) < MIN_DAMPING) {
        add(file, n, '§5 spring', `damping ${m[1]} < ${MIN_DAMPING} — visible overshoot; nothing wobbles`);
      }
    }
    if (/Easing\.spring\(\s*\)/.test(text) || /Easing\.spring\(\{\s*\}\)/.test(text)) {
      add(file, n, '§5 spring', `spring without damping >= ${MIN_DAMPING}`);
    }

    // §4 — nothing legible below the minimum is information
    for (const m of text.matchAll(/fontSize:\s*(\d+)/g)) {
      if (Number(m[1]) < MIN_FONT_SIZE) {
        add(file, n, '§4 type', `fontSize ${m[1]} < ${MIN_FONT_SIZE}px at 4K — decoration, cut it`);
      }
    }

    // §5 — CSS transitions/animations never render
    if (/\b(transition|animation):/.test(text)) {
      add(file, n, 'remotion', 'CSS transition/animation does not render — drive it with interpolate()');
    }
  });
}

// ── report ──────────────────────────────────────────────────────────────────
if (violations.length === 0) {
  console.log(
    `brand:check ✓  ${walk(SRC).length} files · ${allowedColors.size} colours · ` +
      `${allowedEasings.size} easing curves · min ${MIN_FONT_SIZE}px · damping >= ${MIN_DAMPING}`,
  );
  process.exit(0);
}

console.error(`brand:check ✗  ${violations.length} violation(s)\n`);
for (const v of violations) {
  console.error(`  ${v.file}:${v.line}  [${v.rule}]  ${v.detail}`);
}
console.error('\nSee brand_guide_software.md — these are hard limits, not preferences.');
process.exit(1);
