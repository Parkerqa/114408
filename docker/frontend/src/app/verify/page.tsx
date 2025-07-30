"use client";

import { useState } from "react";
import { Search } from "lucide-react";
import { ListChecks } from "lucide-react";

import InputField from "@/components/common/InputField";

import styles from "@/styles/app/VerifyPage.module.scss";

export default function Verify() {
  const [isPast, setIsPast] = useState<boolean>(false);
  return (
    <>
      <div>
        <p>待核銷報帳</p>
        <span>|</span>
        <p>過去核銷紀錄</p>
      </div>
      <div className={styles.wrap}>
        <div className={styles.operateBar}>
          <div className={styles.searchBar}>
            <InputField type="date" />
            <InputField type="text" />
            <InputField type="text" />
            <button className={styles.searchBtn}>
              <Search strokeWidth={3} />
            </button>
          </div>
          <button className={styles.verifyBtn}>
            <ListChecks />
            批量核銷
          </button>
        </div>
      </div>
    </>
  );
}
