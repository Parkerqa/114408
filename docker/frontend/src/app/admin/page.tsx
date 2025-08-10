"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Bot } from "lucide-react";

import Table from "@/components/Table";
import Chart from "@/components/chart/Chart";
import ticketAPI from "@/services/ticketAPI";
import styles from "@/styles/app/AdminPage.module.scss";

const chartData = {
  labels: ["使用金額", "尚未使用金額"],
  datasets: [
    {
      label: "金額",
      data: [1200, 500],
      backgroundColor: ["#5caed6", "#f8f8f8"],
    },
  ],
};

export default function Admin() {
  const [count, setCount] = useState();

  useEffect(() => {
    const getCount = async () => {
      try {
        const res = await ticketAPI.getUnVerifyCount();
        if (res.data) {
          setCount(res.data.status_1_count);
        }
      } catch {}
    };

    getCount();
  }, []);

  return (
    <div className={styles.wrap}>
      <div className={styles.rightArea}>
        <div className={styles.chartArea}>
          <p className={styles.title}>支出占比</p>
          <div className={styles.total}>
            <Chart data={chartData} title="總預算" />
          </div>
          <div className={styles.topThree}>
            <p>前三支出種類</p>
            <div className={styles.charts}>
              <Chart data={chartData} title="交通類" />
              <Chart data={chartData} title="交通類" />
              <Chart data={chartData} title="交通類" />
            </div>
          </div>
        </div>
        <div className={styles.aiSuggest}>
          <p style={{ display: "flex", alignItems: "center" }}>
            <Bot />
            &nbsp;&nbsp;幫你分析：
          </p>
          <p className={styles.aiMessage}>
            　　本月支出最高總額為資產類，第二為文具類，第三為交通類，還請主人再多加留意資產類的支出。
            資產類雖為最高支出總額，支出狀況卻為”健康”，建議主人可以調整該預算上限，讓其他資金能充分運用喔！
          </p>
        </div>
        <div className={styles.pending}>
          <div className={styles.guide}>
            <p>
              您尚有<span>&nbsp;{count}&nbsp;</span>筆報帳待審核
            </p>
            <Link href={"/verify"}>
              <button>去審核</button>
            </Link>
          </div>
          <p
            style={{ fontWeight: "bold", fontSize: "28px", margin: "10px 0px" }}
          >
            近期審核紀錄
          </p>
          <p style={{ fontSize: "12px", marginBottom: "10px" }}>
            更多請至核銷報帳查詢
          </p>
          <Table />
        </div>
      </div>
      <div className={styles.budgetArea}>
        <div className={styles.budget}></div>
      </div>
    </div>
  );
}
