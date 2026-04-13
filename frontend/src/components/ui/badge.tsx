import { HTMLAttributes } from "react";
import clsx from "clsx";

type Props = HTMLAttributes<HTMLSpanElement> & {
  variant?: "default" | "secondary" | "outline";
};

export function Badge({ className, variant = "default", ...props }: Props) {
  return (
    <span
      className={clsx(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs",
        variant === "default" && "bg-emerald-700 text-white",
        variant === "secondary" && "bg-sky-700 text-white",
        variant === "outline" && "border border-slate-300 bg-white text-slate-700",
        className
      )}
      {...props}
    />
  );
}
