import { Badge } from "@/components/ui/badge";

import { getRuleStrength } from "../utils";

type Props = {
  lift: number;
};

export function RuleStrengthBadge({ lift }: Props) {
  const strength = getRuleStrength(lift);
  const variant =
    strength === "Sangat Kuat" ? "default" : strength === "Kuat" ? "secondary" : "outline";

  return <Badge variant={variant}>{strength}</Badge>;
}
