import { InputHTMLAttributes } from "react";
import clsx from "clsx";

type Props = InputHTMLAttributes<HTMLInputElement>;

export function Input({ className, ...props }: Props) {
  return (
    <input
      className={clsx("h-10 w-full rounded-md border border-slate-300 px-3 text-sm", className)}
      {...props}
    />
  );
}
