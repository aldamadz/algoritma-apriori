import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import type { AssociationRule } from "../types";
import { toLift, toPercent } from "../utils";
import { RuleStrengthBadge } from "./rule-strength-badge";

type Props = {
  rules: AssociationRule[];
  page: number;
  limit: number;
  onViewDetail: (rule: AssociationRule) => void;
};

export function RulesTable({ rules, page, limit, onViewDetail }: Props) {
  return (
    <div className="overflow-x-auto rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>No</TableHead>
            <TableHead>Jika</TableHead>
            <TableHead>Maka</TableHead>
            <TableHead>Support</TableHead>
            <TableHead>Confidence</TableHead>
            <TableHead>Lift</TableHead>
            <TableHead>Kekuatan</TableHead>
            <TableHead>Aksi</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {rules.map((rule, index) => (
            <TableRow key={rule.id}>
              <TableCell>{(page - 1) * limit + index + 1}</TableCell>
              <TableCell className="min-w-[220px] break-words">{rule.antecedent.join(", ")}</TableCell>
              <TableCell className="min-w-[220px] break-words">{rule.consequent.join(", ")}</TableCell>
              <TableCell className="whitespace-nowrap">{toPercent(rule.support)}</TableCell>
              <TableCell className="whitespace-nowrap">{toPercent(rule.confidence)}</TableCell>
              <TableCell className="whitespace-nowrap">{toLift(rule.lift)}</TableCell>
              <TableCell>
                <RuleStrengthBadge lift={rule.lift} />
              </TableCell>
              <TableCell>
                <Button variant="outline" size="sm" onClick={() => onViewDetail(rule)}>
                  Detail
                </Button>
              </TableCell>
            </TableRow>
          ))}
          {rules.length === 0 ? (
            <TableRow>
              <TableCell colSpan={8} className="text-center text-muted-foreground">
                Tidak ada data.
              </TableCell>
            </TableRow>
          ) : null}
        </TableBody>
      </Table>
    </div>
  );
}
