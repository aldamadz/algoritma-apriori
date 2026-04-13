import { ButtonHTMLAttributes } from "react";
import clsx from "clsx";

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "default" | "outline" | "secondary";
  size?: "default" | "sm";
};

export function Button({ className, variant = "default", size = "default", ...props }: Props) {
  return (
    <button
      className={clsx(
        "rounded-md border px-3 py-2 text-sm",
        variant === "default" && "border-slate-900 bg-slate-900 text-white",
        variant === "outline" && "border-slate-300 bg-white text-slate-900",
        variant === "secondary" && "border-slate-200 bg-slate-100 text-slate-900",
        size === "sm" && "px-2 py-1 text-xs",
        "disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      {...props}
    />
  );
}
