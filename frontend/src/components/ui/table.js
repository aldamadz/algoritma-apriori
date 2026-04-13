import { jsx as _jsx } from "react/jsx-runtime";
import clsx from "clsx";
export function Table({ className, ...props }) {
    return _jsx("table", { className: clsx("w-full border-collapse text-sm", className), ...props });
}
export function TableHeader({ className, ...props }) {
    return _jsx("thead", { className: clsx("bg-slate-100", className), ...props });
}
export function TableBody({ className, ...props }) {
    return _jsx("tbody", { className: clsx(className), ...props });
}
export function TableRow({ className, ...props }) {
    return _jsx("tr", { className: clsx("border-b", className), ...props });
}
export function TableHead({ className, ...props }) {
    return _jsx("th", { className: clsx("px-3 py-2 text-left font-semibold", className), ...props });
}
export function TableCell({ className, ...props }) {
    return _jsx("td", { className: clsx("px-3 py-2 align-top", className), ...props });
}
