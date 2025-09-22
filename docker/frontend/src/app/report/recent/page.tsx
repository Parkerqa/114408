"use client";

import { useState, useMemo } from "react";
import { DayPicker, DateRange } from "react-day-picker";
import "react-day-picker/style.css";

import ReportNav from "@/components/ReportNav";
import styles from "@/styles/app/report/RecentPage.module.scss";

export default function Recent() {
  return (
    <div className={styles.wrap}>
      <ReportNav />
      <div className={styles.infoArea}>
        <div>
          <div>前三支出部門</div>
          <div>核銷金額變動圖</div>
          <div>
            <div className={styles.dayWrap}>
              <DayPicker animate mode="range" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
