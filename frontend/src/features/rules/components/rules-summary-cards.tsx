import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type Props = {
  totalRules: number;
  topLiftRule?: string;
  dominantDepartment?: string;
};

export function RulesSummaryCards({ totalRules, topLiftRule, dominantDepartment }: Props) {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      <Card>
        <CardHeader>
          <CardTitle>Total Rule Valid</CardTitle>
        </CardHeader>
        <CardContent className="text-2xl font-semibold">{totalRules}</CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Rule Terkuat</CardTitle>
        </CardHeader>
        <CardContent className="text-sm">{topLiftRule ?? "-"}</CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Jurusan Dominan</CardTitle>
        </CardHeader>
        <CardContent className="text-sm">{dominantDepartment ?? "-"}</CardContent>
      </Card>
    </div>
  );
}
