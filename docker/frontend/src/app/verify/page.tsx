"use client";

import { useState } from "react";
import { Search } from "lucide-react";
import { ListChecks } from "lucide-react";

import InputField from "@/components/common/InputField";
import LargeTable from "@/components/LargeTable";
import styles from "@/styles/app/VerifyPage.module.scss";

export default function Verify() {
  const [isPast, setIsPast] = useState<boolean>(false);
  return (
    <>
      <div className={styles.wrap}>
        <div className={styles.title}>
          <p
            className={`${!isPast ? styles.focus : styles.normal}`}
            onClick={() => {
              setIsPast(false);
            }}
          >
            待核銷報帳
          </p>
          <span>|</span>
          <p
            className={`${isPast ? styles.focus : styles.normal}`}
            onClick={() => {
              setIsPast(true);
            }}
          >
            過去核銷紀錄
          </p>
        </div>
        <div className={styles.searchBar}>
          <p>報帳申請查詢</p>
          <div className={styles.operateBar}>
            <div className={styles.searchItem}>
              <InputField type="date" />
              <InputField type="text" />
              <InputField type="text" />
              <button className={styles.searchBtn}>
                <Search strokeWidth={3} />
              </button>
            </div>
            <button className={styles.verifyBtn}>
              <ListChecks />
              <p>批量核銷</p>
            </button>
          </div>
        </div>
        <LargeTable />
      </div>
    </>
  );
}
