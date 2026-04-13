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

  const left = rule.antecedent.join(", ");
  const right = rule.consequent.join(", ");

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Detail Aturan</DialogTitle>
          <DialogDescription>
            Mahasiswa yang meminjam [{left}] cenderung meminjam [{right}].
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-2 break-words text-sm">
          <div>Support: {toPercent(rule.support)}</div>
          <div>Confidence: {toPercent(rule.confidence)}</div>
          <div>Lift: {toLift(rule.lift)}</div>
          <div className="pt-1">
            Kekuatan: <RuleStrengthBadge lift={rule.lift} />
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
