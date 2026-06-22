import type { AssociationRule } from "./types";

export const toPercent = (value: number): string => `${(value * 100).toFixed(2)}%`;
export const toLift = (value: number): string => value.toFixed(2);
export const toSupportLabel = (support: number, supportCount: number): string =>
  `${toPercent(support)} (${supportCount.toLocaleString("id-ID")} transaksi)`;

const LEGACY_FACULTY_PREFIX_CODES = [74, 117, 114, 117, 115, 97, 110, 58];
export const LEGACY_FACULTY_PREFIX = LEGACY_FACULTY_PREFIX_CODES.map((code) =>
  String.fromCharCode(code),
).join("");

export const formatRuleItem = (value: string): string => {
  const trimmed = value.trim();
  const facultyPrefixes = ["Fakultas:", LEGACY_FACULTY_PREFIX];
  for (const prefix of facultyPrefixes) {
    if (trimmed.startsWith(prefix)) return `Fakultas:${trimmed.slice(prefix.length).trim()}`;
  }
  return trimmed;
};

export const cleanRuleItemLabel = (value: string): string => {
  const trimmed = value.trim();
  for (const prefix of ["Fakultas:", "Buku:", LEGACY_FACULTY_PREFIX]) {
    if (trimmed.startsWith(prefix)) return trimmed.slice(prefix.length).trim();
  }
  return trimmed;
};

export const toRuleText = (rule: AssociationRule): string =>
  `Jika [${rule.antecedent.map(formatRuleItem).join(", ")}], maka [${rule.consequent
    .map(formatRuleItem)
    .join(", ")}]`;

export const getRuleStrength = (lift: number): "Sangat Kuat" | "Kuat" | "Cukup" | "Lemah" => {
  if (lift >= 2) return "Sangat Kuat";
  if (lift >= 1.2) return "Kuat";
  if (lift >= 1) return "Cukup";
  return "Lemah";
};
