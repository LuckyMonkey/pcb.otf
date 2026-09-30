export interface HardwareGroup { id: string; label: string; parent: string | null; }
export interface HardwareRecord { id: string; label: string; category: string; system: string; parent: string; aliases: string[]; attributes: Record<string, unknown>; interfaces: string[]; compatible_with: string[]; incompatible_with: string[]; review_required: boolean; codepoint: string; char: string; ligature: string; shortcode: string; glyph_name: string; glyph_base: string; svg: string; color_svg: string; iso_svg: string; external_ids: Record<string, string>; sources: string[]; accessible_label: string; }
export interface HardwareRelation { from: string; relation: string; to: string; }
export const registry: HardwareRecord[];
export const groups: HardwareGroup[];
export const relations: HardwareRelation[];
export function get(id: string): HardwareRecord | null;
export function resolveShortcode(shortcode: string): HardwareRecord | null;
export function unicodeFor(id: string): string | null;
export function search(query: string): HardwareRecord[];
export function parents(id: string): string[];
export function children(id: string): HardwareRecord[];
export function relationsFor(id: string): HardwareRelation[];
export function compatibleWith(id: string): HardwareRecord[];
export function connectionsFor(id: string): HardwareRelation[];
