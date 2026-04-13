import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
const DOCS = [
    { slug: "penggunaan_sistem", title: "Dokumentasi Penggunaan Sistem", file: "penggunaan_sistem.md" },
    { slug: "kebutuhan_sistem", title: "Kebutuhan Sistem Apriori Engine", file: "kebutuhan_sistem.md" },
    { slug: "panduan_client_sidang", title: "Panduan Client dan Sidang", file: "panduan_client_sidang.md" },
    { slug: "spesifikasi_ui_rules", title: "Spesifikasi UI Rules", file: "spesifikasi_ui_rules.md" },
];
const getSlugFromPath = (pathname) => {
    const chunks = pathname.split("/").filter(Boolean);
    if (chunks.length < 2)
        return "";
    if (chunks[0] === "dokumentasi" || chunks[0] === "docs")
        return chunks[1] ?? "";
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
        if (!selected)
            return;
        let cancelled = false;
        const load = async () => {
            setLoading(true);
            setError("");
            setContent("");
            try {
                const res = await fetch(`/docs/${selected.file}`);
                if (!res.ok)
                    throw new Error(`Dokumen tidak ditemukan (${res.status})`);
                const text = await res.text();
                if (!cancelled)
                    setContent(text);
            }
            catch (e) {
                if (!cancelled)
                    setError(e instanceof Error ? e.message : "Gagal memuat dokumentasi.");
            }
            finally {
                if (!cancelled)
                    setLoading(false);
            }
        };
        void load();
        return () => {
            cancelled = true;
        };
    }, [selected]);
    return (_jsxs("div", { className: "mx-auto max-w-6xl space-y-4 p-6", children: [_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Dokumentasi Sistem" }) }), _jsxs(CardContent, { className: "space-y-2 text-sm", children: [_jsx("div", { children: "Daftar dokumen:" }), _jsx("ul", { className: "list-disc space-y-1 pl-5", children: DOCS.map((doc) => (_jsx("li", { children: _jsx("a", { className: "text-blue-700 underline", href: `/dokumentasi/${doc.slug}`, children: doc.title }) }, doc.slug))) }), _jsxs("div", { className: "pt-1 text-slate-600", children: ["Akses juga via path alternatif: ", _jsx("code", { children: "/docs/{slug}" })] }), _jsx("div", { children: _jsx("a", { className: "text-blue-700 underline", href: "/", children: "Kembali ke aplikasi" }) })] })] }), slug ? (_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: selected?.title ?? "Dokumen tidak ditemukan" }) }), _jsxs(CardContent, { children: [loading ? _jsx("div", { className: "text-sm", children: "Memuat dokumen..." }) : null, error ? _jsx("div", { className: "text-sm text-red-600", children: error }) : null, !loading && !error && selected ? (_jsx("pre", { className: "whitespace-pre-wrap rounded-md bg-slate-50 p-4 text-sm", children: content })) : null, !loading && !error && !selected ? (_jsx("div", { className: "text-sm text-amber-700", children: "Slug dokumen tidak dikenali." })) : null] })] })) : null] }));
}
