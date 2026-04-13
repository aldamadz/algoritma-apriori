import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
export function RulesSummaryCards({ totalRules, topLiftRule, dominantDepartment }) {
    return (_jsxs("div", { className: "grid gap-4 md:grid-cols-3", children: [_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Total Rule Valid" }) }), _jsx(CardContent, { className: "text-2xl font-semibold", children: totalRules })] }), _jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Rule Terkuat" }) }), _jsx(CardContent, { className: "text-sm", children: topLiftRule ?? "-" })] }), _jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Jurusan Dominan" }) }), _jsx(CardContent, { className: "text-sm", children: dominantDepartment ?? "-" })] })] }));
}
