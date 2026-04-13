export const toPercent = (value) => `${(value * 100).toFixed(2)}%`;
export const toLift = (value) => value.toFixed(2);
export const toRuleText = (rule) => `Jika [${rule.antecedent.join(", ")}], maka [${rule.consequent.join(", ")}]`;
export const getRuleStrength = (lift) => {
    if (lift >= 2)
        return "Sangat Kuat";
    if (lift >= 1.2)
        return "Kuat";
    if (lift >= 1)
        return "Cukup";
    return "Lemah";
};
