"use client";

import { IS_LAB } from "@/lib/api";
import { useI18n } from "@/lib/i18n";

export function LabBanner() {
  const { t } = useI18n();
  if (!IS_LAB) return null;
  return (
    <div className="border-b border-forest/25 bg-forest/10 text-ink">
      <div className="mx-auto max-w-6xl px-4 py-2.5 text-sm leading-snug">
        <span className="text-slate">
          {t("lab.banner")}{" "}
          <code className="rounded bg-white/70 px-1 text-xs">NEXT_PUBLIC_USE_API=true</code>.
        </span>
      </div>
    </div>
  );
}
