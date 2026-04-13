import { jsx as _jsx } from "react/jsx-runtime";
export function Dialog({ open, onOpenChange, children }) {
    if (!open)
        return null;
    return (_jsx("div", { className: "fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4", onClick: () => onOpenChange(false), children: _jsx("div", { onClick: (e) => e.stopPropagation(), children: children }) }));
}
export function DialogContent({ className = "", ...props }) {
    return _jsx("div", { className: `w-[min(640px,95vw)] rounded-lg bg-white p-4 ${className}`, ...props });
}
export function DialogHeader({ className = "", ...props }) {
    return _jsx("div", { className: `mb-3 ${className}`, ...props });
}
export function DialogTitle({ className = "", ...props }) {
    return _jsx("h3", { className: `text-lg font-semibold ${className}`, ...props });
}
export function DialogDescription({ className = "", ...props }) {
    return _jsx("p", { className: `text-sm text-slate-600 ${className}`, ...props });
}
