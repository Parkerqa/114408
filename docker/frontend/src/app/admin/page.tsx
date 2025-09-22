"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Bot, Settings, Trash2, Plus } from "lucide-react";
import { useRouter } from "next/navigation";

import { useConfig } from "@/lib/context/ConfigContext";
import Table from "@/components/Table";
import Chart from "@/components/chart/Chart";
import AddBudgetPopup from "@/components/Budget/AddBudgetPopup";
import EditBudgetPopup from "@/components/Budget/EditBudgetPopup";
import { SummaryRow } from "@/lib/types/BudgetType";
import n8nAPI from "@/services/n8nAPI";
import departmentAPI from "@/services/departmentAPI";
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
  const route = useRouter();
  const { role } = useConfig();
  const [count, setCount] = useState();
  const [editTitle, setEditTitle] = useState<string>();
  const [editId, setEditId] = useState<number>();
  const [isAdd, setIsAdd] = useState<boolean>(false);
  const [isEdit, setIsEdit] = useState<boolean>(false);
  const [summaryData, setSummaryData] = useState<SummaryRow[]>();

  if (role) {
    if ([0, 2, 3].includes(role)) {
      route.push("/user");
    }
  }

  useEffect(() => {
    const getCount = async () => {
      try {
        const res = await ticketAPI.getUnVerifyCount();
        if (res.data) {
          setCount(res.data.total);
        }
      } catch {}
    };

    // const getChart = async () => {
    //   try {
    //     const res = await n8nAPI.getHomeChart();
    //   } catch {}
    // };

    const getSummary = async () => {
      try {
        const res = await departmentAPI.getDeptSummary();
        if (res.data) {
          setSummaryData(res.data);
        }
      } catch {}
    };

    // getChart();
    getCount();
    getSummary();
  }, []);

  return (
    <>
      <div className={styles.wrap}>
        <div className={styles.rightArea}>
          <div className={styles.chartArea}>
            <p className={styles.title}>支出占比</p>
            <div className={styles.total}>
              <Chart data={chartData} title="總預算" />
            </div>
            <div className={styles.topThree}>
              <p>前三支出會計科目</p>
              <div className={styles.charts}>
                <Chart data={chartData} title="旅費" />
                <Chart data={chartData} title="雜支" />
                <Chart data={chartData} title="交際費 " />
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
              style={{
                fontWeight: "bold",
                fontSize: "28px",
                margin: "10px 0px",
              }}
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
          <div className={styles.budget}>
            <table className={styles.budgetTable}>
              <thead className={styles.tableThead}>
                <tr>
                  <th>部門</th>
                  <th>上限</th>
                  <th>修改</th>
                </tr>
              </thead>
              <tbody className={styles.tableTbody}>
                {summaryData &&
                  summaryData.map((item, index) => (
                    <tr key={index}>
                      <td>{item.dept_name}</td>
                      <td>{item.total_budget}</td>
                      <td>
                        <Settings
                          className={styles.edit}
                          size={20}
                          onClick={() => {
                            setIsEdit(true);
                            setEditTitle(item.dept_name);
                            setEditId(item.department_id);
                          }}
                        />
                        <Trash2 className={styles.delete} size={20} />
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
            <Plus
              className={styles.addBudget}
              strokeWidth={3}
              onClick={() => {
                setIsAdd(true);
              }}
            />
          </div>
        </div>
      </div>
      {isAdd && <AddBudgetPopup setIsPopup={setIsAdd} />}
      {isEdit && editTitle && editId && (
        <EditBudgetPopup
          setIsPopup={setIsEdit}
          deptTitle={editTitle}
          deptId={editId}
        />
      )}
    </>
  );
}
