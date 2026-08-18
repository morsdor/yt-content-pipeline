/**
 * Load Bearing — font loading (brand_guide_software.md §4).
 *
 * Google Fonts via @remotion/google-fonts: no files to vendor, no FOUT at render time.
 * Import this module once from Root.tsx; the loads are module-level side effects.
 *
 * The rule that defines the channel typographically: EVERY number, identifier,
 * timestamp and filename is set in `IBM Plex Mono`. A metric in a proportional face
 * instantly reads as a generic explainer.
 */

import { loadFont as loadArchivoBlack } from '@remotion/google-fonts/ArchivoBlack';
import { loadFont as loadIBMPlexSans } from '@remotion/google-fonts/IBMPlexSans';
import { loadFont as loadIBMPlexMono } from '@remotion/google-fonts/IBMPlexMono';

/** Display — wordmark, titles, thumbnail hero. Archivo Black ships weight 400 only. */
export const { fontFamily: displayFamily } = loadArchivoBlack('normal', {
  weights: ['400'],
  subsets: ['latin'],
});

/** Body/labels — 400 and 600 only. More weights is how a brand starts to blur. */
export const { fontFamily: sansFamily } = loadIBMPlexSans('normal', {
  weights: ['400', '600'],
  subsets: ['latin'],
});

/** Numbers, code, data. */
export const { fontFamily: monoFamily } = loadIBMPlexMono('normal', {
  weights: ['400', '600'],
  subsets: ['latin'],
});
