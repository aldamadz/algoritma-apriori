import { jsx as _jsx } from "react/jsx-runtime";
import clsx from "clsx";
export function Card({ className, ...props }) {
    return _jsx("div", { className: clsx("rounded-lg border bg-white", className), ...props });
}
export function CardHeader({ className, ...props }) {
    return _jsx("div", { className: clsx("border-b p-4", className), ...props });
}
export function CardTitle({ className, ...props }) {
    return _jsx("h3", { className: clsx("text-sm font-semibold", className), ...props });
}
export function CardContent({ className, ...props }) {
    return _jsx("div", { className: clsx("p-4", className), ...props });
}
