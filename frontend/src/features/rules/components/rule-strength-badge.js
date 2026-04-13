import { jsx as _jsx } from "react/jsx-runtime";
import { Badge } from "@/components/ui/badge";
import { getRuleStrength } from "../utils";
export function RuleStrengthBadge({ lift }) {
    const strength = getRuleStrength(lift);
    const variant = strength === "Sangat Kuat" ? "default" : strength === "Kuat" ? "secondary" : "outline";
    return _jsx(Badge, { variant: variant, children: strength });
}
