import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

import type { AssociationRule } from "../types";
import { toLift, toPercent } from "../utils";
import { RuleStrengthBadge } from "./rule-strength-badge";

type Props = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  rule: AssociationRule | null;
};

export function RuleDetailDialog({ open, onOpenChange, rule }: Props) {
  if (!rule) return null;

  const cleanLabel = (value: string): string => value.replace(/^(Jurusan|Buku):/, "").trim();
  const left = rule.antecedent.map(cleanLabel).join(", ");
  const right = rule.consequent.map(cleanLabel).join(", ");
  const supportText = `${toPercent(rule.support)} dari seluruh transaksi memuat kombinasi jurusan [${left}] dan buku [${right}].`;
  const confidenceText = `Dari transaksi mahasiswa jurusan [${left}], ${toPercent(rule.confidence)} di antaranya meminjam buku [${right}].`;
  const liftText =
    rule.lift > 1
      ? `Nilai lift ${toLift(rule.lift)} menunjukkan hubungan ini ${toLift(rule.lift)} kali lebih kuat dibanding peminjaman acak tanpa melihat jurusan.`
      : `Nilai lift ${toLift(rule.lift)} menunjukkan hubungan ini belum lebih kuat dibanding peminjaman acak tanpa melihat jurusan.`;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Detail Aturan</DialogTitle>
          <DialogDescription>
            Mahasiswa dari jurusan [{left}] memiliki kecenderungan meminjam buku [{right}].
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-3 break-words text-sm">
          <div className="rounded-md border bg-slate-50 p-3">
            <div className="font-medium">Support: {toPercent(rule.support)}</div>
            <div className="mt-1 text-slate-600">{supportText}</div>
          </div>
          <div className="rounded-md border bg-slate-50 p-3">
            <div className="font-medium">Confidence: {toPercent(rule.confidence)}</div>
            <div className="mt-1 text-slate-600">{confidenceText}</div>
          </div>
          <div className="rounded-md border bg-slate-50 p-3">
            <div className="font-medium">Lift: {toLift(rule.lift)}</div>
            <div className="mt-1 text-slate-600">{liftText}</div>
          </div>
          <div className="pt-1">
            Kekuatan: <RuleStrengthBadge lift={rule.lift} />
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
