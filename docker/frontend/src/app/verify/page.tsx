"use client";

import { useState } from "react";
import { Search, ListChecks } from "lucide-react";

import VerifyPopup from "@/components/VerifyPopup";
import InputField from "@/components/common/InputField";
import PendingTable from "@/components/PendingTable";
import ApprovedTable from "@/components/ApprovedTable";
import { ApplyType } from "@/lib/types/ApplyType";
import styles from "@/styles/app/VerifyPage.module.scss";

export default function Verify() {
  const [isPast, setIsPast] = useState<boolean>(false);
  const [isVerify, setIsVerify] = useState<boolean>(false);
  const [tableData, setTableData] = useState();

  const verifyData: ApplyType[] = [
    {
      Details: [
        { title: "測資1標題1", money: 150 },
        { title: "測資1標題2", money: 300 },
      ],
      time: "2025/8/20",
      type: "電子發票",
      applicant: "員工A",
      status: 0,
    },
    {
      Details: [
        { title: "測資2標題1", money: 150 },
        { title: "測資2標題2", money: 300 },
      ],
      time: "2025/8/20",
      type: "電子發票",
      applicant: "員工B",
      status: 0,
    },
    {
      Details: [
        { title: "測資3標題1", money: 150 },
        { title: "測資3標題2", money: 300 },
      ],
      time: "2025/8/20",
      type: "電子發票",
      applicant: "員工C",
      status: 0,
    },
    {
      Details: [
        { title: "測資4標題1", money: 150 },
        { title: "測資4標題2", money: 300 },
      ],
      time: "2025/8/20",
      type: "電子發票",
      applicant: "員工D",
      status: 0,
    },
  ];

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
            {!isPast && (
              <button className={styles.verifyBtn}>
                <ListChecks />
                <p>批量核銷</p>
              </button>
            )}
          </div>
        </div>
        {isPast ? <ApprovedTable /> : <PendingTable />}
      </div>
      {isVerify && <VerifyPopup setIsPopup={setIsVerify} data={verifyData} />}
    </>
  );
}
