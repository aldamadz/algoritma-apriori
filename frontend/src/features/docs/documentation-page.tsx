import { useEffect, useMemo, useState } from "react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type DocItem = {
  slug: string;
  title: string;
  file: string;
};

const DOCS: DocItem[] = [
  { slug: "penggunaan_sistem", title: "Dokumentasi Penggunaan Sistem", file: "penggunaan_sistem.md" },
  { slug: "kebutuhan_sistem", title: "Kebutuhan Sistem Apriori Engine", file: "kebutuhan_sistem.md" },
  { slug: "panduan_client_sidang", title: "Panduan Client dan Sidang", file: "panduan_client_sidang.md" },
  { slug: "spesifikasi_ui_rules", title: "Spesifikasi UI Rules", file: "spesifikasi_ui_rules.md" },
];

const getSlugFromPath = (pathname: string): string => {
  const chunks = pathname.split("/").filter(Boolean);
  if (chunks.length < 2) return "";
  if (chunks[0] === "dokumentasi" || chunks[0] === "docs") return chunks[1] ?? "";
  return "";
};

export function DocumentationPage() {
  const pathname = window.location.pathname;
  const slug = getSlugFromPath(pathname);
  const selected = useMemo(() => DOCS.find((d) => d.slug === slug), [slug]);
  const [loading, setLoading] = useState(false);
  const [content, setContent] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!selected) return;
    let cancelled = false;
    const load = async () => {
      setLoading(true);
      setError("");
      setContent("");
      try {
        const res = await fetch(`/docs/${selected.file}`);
        if (!res.ok) throw new Error(`Dokumen tidak ditemukan (${res.status})`);
        const text = await res.text();
        if (!cancelled) setContent(text);
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : "Gagal memuat dokumentasi.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    void load();
    return () => {
      cancelled = true;
    };
  }, [selected]);

  return (
    <div className="mx-auto max-w-6xl space-y-4 p-6">
      <Card>
        <CardHeader>
          <CardTitle>Dokumentasi Sistem</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          <div>Daftar dokumen:</div>
          <ul className="list-disc space-y-1 pl-5">
            {DOCS.map((doc) => (
              <li key={doc.slug}>
                <a className="text-blue-700 underline" href={`/dokumentasi/${doc.slug}`}>
                  {doc.title}
                </a>
              </li>
            ))}
          </ul>
          <div className="pt-1 text-slate-600">
            Akses juga via path alternatif: <code>/docs/&#123;slug&#125;</code>
          </div>
          <div>
            <a className="text-blue-700 underline" href="/">
              Kembali ke aplikasi
            </a>
          </div>
        </CardContent>
      </Card>

      {slug ? (
        <Card>
          <CardHeader>
            <CardTitle>{selected?.title ?? "Dokumen tidak ditemukan"}</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? <div className="text-sm">Memuat dokumen...</div> : null}
            {error ? <div className="text-sm text-red-600">{error}</div> : null}
            {!loading && !error && selected ? (
              <pre className="whitespace-pre-wrap rounded-md bg-slate-50 p-4 text-sm">{content}</pre>
            ) : null}
            {!loading && !error && !selected ? (
              <div className="text-sm text-amber-700">Slug dokumen tidak dikenali.</div>
            ) : null}
          </CardContent>
        </Card>
      ) : null}
    </div>
  );
}
