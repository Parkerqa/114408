"use client";

import { useState } from "react";
import { ChevronRight } from "lucide-react";
import styles from "@/styles/components/common/MobileListItem.module.scss";
import { listType } from "@/lib/types/listType";

export default function MobileListItem({ data }: { data: listType }) {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  return (
    <>
      <div className={styles.wrap}>
        <ChevronRight size={20} strokeWidth={3} className={styles.circle} />
        <div className={styles.detail}>
          <div className={styles.item}>
            <p>時間</p>
            <p className={styles.info}>{data.time}</p>
          </div>
          <div className={styles.item}>
            <p>種類</p>
            <p className={styles.info}>{data.type}</p>
          </div>
          <div className={styles.item}>
            <p>標題</p>
            <p className={styles.info}>{data.title}</p>
          </div>
          <div className={styles.item}>
            <p>編號</p>
            <p className={styles.info}>{data.number}</p>
          </div>
          <div className={styles.item}>
            <p>金額</p>
            <p className={styles.info}>{data.money}</p>
          </div>
          <div className={styles.item}>
            <p>狀態</p>
            <p className={styles.info}>{data.state}</p>
          </div>
        </div>
      </div>
    </>
  );
}
