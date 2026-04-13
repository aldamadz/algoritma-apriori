import type { AssociationRule } from "./types";

export const toPercent = (value: number): string => `${(value * 100).toFixed(2)}%`;
export const toLift = (value: number): string => value.toFixed(2);

export const toRuleText = (rule: AssociationRule): string =>
  `Jika [${rule.antecedent.join(", ")}], maka [${rule.consequent.join(", ")}]`;

export const getRuleStrength = (lift: number): "Sangat Kuat" | "Kuat" | "Cukup" | "Lemah" => {
  if (lift >= 2) return "Sangat Kuat";
  if (lift >= 1.2) return "Kuat";
  if (lift >= 1) return "Cukup";
  return "Lemah";
};
