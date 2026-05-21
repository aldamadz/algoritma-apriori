import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, } from "@/components/ui/dialog";
import { toLift, toPercent } from "../utils";
import { RuleStrengthBadge } from "./rule-strength-badge";
export function RuleDetailDialog({ open, onOpenChange, rule }) {
    if (!rule)
        return null;
    const cleanLabel = (value) => value.replace(/^(Jurusan|Buku):/, "").trim();
    const left = rule.antecedent.map(cleanLabel).join(", ");
    const right = rule.consequent.map(cleanLabel).join(", ");
    const supportText = `${toPercent(rule.support)} dari seluruh transaksi memuat kombinasi jurusan [${left}] dan buku [${right}].`;
    const confidenceText = `Dari transaksi mahasiswa jurusan [${left}], ${toPercent(rule.confidence)} di antaranya meminjam buku [${right}].`;
    const liftText = rule.lift > 1
        ? `Nilai lift ${toLift(rule.lift)} menunjukkan hubungan ini ${toLift(rule.lift)} kali lebih kuat dibanding peminjaman acak tanpa melihat jurusan.`
        : `Nilai lift ${toLift(rule.lift)} menunjukkan hubungan ini belum lebih kuat dibanding peminjaman acak tanpa melihat jurusan.`;
    return (_jsx(Dialog, { open: open, onOpenChange: onOpenChange, children: _jsxs(DialogContent, { children: [_jsxs(DialogHeader, { children: [_jsx(DialogTitle, { children: "Detail Aturan" }), _jsxs(DialogDescription, { children: ["Mahasiswa dari jurusan [", left, "] memiliki kecenderungan meminjam buku [", right, "]."] })] }), _jsxs("div", { className: "space-y-3 break-words text-sm", children: [_jsxs("div", { className: "rounded-md border bg-slate-50 p-3", children: [_jsxs("div", { className: "font-medium", children: ["Support: ", toPercent(rule.support)] }), _jsx("div", { className: "mt-1 text-slate-600", children: supportText })] }), _jsxs("div", { className: "rounded-md border bg-slate-50 p-3", children: [_jsxs("div", { className: "font-medium", children: ["Confidence: ", toPercent(rule.confidence)] }), _jsx("div", { className: "mt-1 text-slate-600", children: confidenceText })] }), _jsxs("div", { className: "rounded-md border bg-slate-50 p-3", children: [_jsxs("div", { className: "font-medium", children: ["Lift: ", toLift(rule.lift)] }), _jsx("div", { className: "mt-1 text-slate-600", children: liftText })] }), _jsxs("div", { className: "pt-1", children: ["Kekuatan: ", _jsx(RuleStrengthBadge, { lift: rule.lift })] })] })] }) }));
}
