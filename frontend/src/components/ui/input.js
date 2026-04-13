import { jsx as _jsx } from "react/jsx-runtime";
import clsx from "clsx";
export function Input({ className, ...props }) {
    return (_jsx("input", { className: clsx("h-10 w-full rounded-md border border-slate-300 px-3 text-sm", className), ...props }));
}
