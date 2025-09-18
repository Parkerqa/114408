"use client";

import { useRouter } from "next/navigation";
import { usePathname } from "next/navigation";
import { ChevronRight } from "lucide-react";
import { ChartLine } from "lucide-react";

import { reportItemData } from "@/lib/data/reportItemData";
import styles from "@/styles/components/ReportNav.module.scss";

export default function ReportNav() {
  const router = useRouter();
  const pathname = usePathname();
  const current = reportItemData.find((item) => item.link === pathname);

  return (
    <div className={styles.wrap}>
      <ChartLine size={40} />
      <div className={styles.back} onClick={() => router.back()}>
        <p>報表專區</p>
      </div>
      <ChevronRight size={20} />
      <p style={{ fontWeight: "bold" }}>
        {current ? current.title : "載入失敗"}
      </p>
    </div>
  );
}
