"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";
import { ChevronRight } from "lucide-react";
import styles from "@/styles/components/common/MobileListItem.module.scss";
import { listType } from "@/lib/types/listType";

export default function MobileListItem({ data }: { data: listType }) {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const title = ["時間", "種類", "標題", "編號", "金額", "狀態"];
  const values = [
    data.time,
    data.type,
    data.title,
    data.number,
    data.money,
    data.state,
  ];

  return (
    <div className={isOpen ? styles.detailBox : styles.partialBox}>
      {isOpen ? (
        <ChevronDown
          size={20}
          strokeWidth={3}
          className={styles.toggle}
          onClick={() => setIsOpen(false)}
        />
      ) : (
        <ChevronRight
          size={20}
          strokeWidth={3}
          className={styles.toggle}
          onClick={() => setIsOpen(true)}
        />
      )}
      <div className={styles.detail}>
        {isOpen ? (
          title.map((item, index) => (
            <div className={styles.item} key={index}>
              <p>{item}</p>
              <p className={styles.info}>{values[index]}</p>
            </div>
          ))
        ) : (
          <div className={styles.item}>
            <p>{data.time}</p>
            <p className={styles.partial}>{data.title}</p>
          </div>
        )}
      </div>
    </div>
  );
}
