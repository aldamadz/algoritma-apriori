import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, } from "@/components/ui/dialog";
import { toLift, toPercent } from "../utils";
import { RuleStrengthBadge } from "./rule-strength-badge";
export function RuleDetailDialog({ open, onOpenChange, rule }) {
    if (!rule)
        return null;
    const left = rule.antecedent.join(", ");
    const right = rule.consequent.join(", ");
    return (_jsx(Dialog, { open: open, onOpenChange: onOpenChange, children: _jsxs(DialogContent, { children: [_jsxs(DialogHeader, { children: [_jsx(DialogTitle, { children: "Detail Aturan" }), _jsxs(DialogDescription, { children: ["Mahasiswa yang meminjam [", left, "] cenderung meminjam [", right, "]."] })] }), _jsxs("div", { className: "space-y-2 break-words text-sm", children: [_jsxs("div", { children: ["Support: ", toPercent(rule.support)] }), _jsxs("div", { children: ["Confidence: ", toPercent(rule.confidence)] }), _jsxs("div", { children: ["Lift: ", toLift(rule.lift)] }), _jsxs("div", { className: "pt-1", children: ["Kekuatan: ", _jsx(RuleStrengthBadge, { lift: rule.lift })] })] })] }) }));
}
