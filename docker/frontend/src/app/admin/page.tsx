"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Bot, Settings, Trash2, Plus } from "lucide-react";
import { notFound } from "next/navigation";

import { useConfig } from "@/lib/context/ConfigContext";
import { useLoading } from "@/lib/context/LoadingContext";
import Table from "@/components/Table";
import Chart from "@/components/chart/Chart";
import AddBudgetPopup from "@/components/Budget/AddBudgetPopup";
import EditBudgetPopup from "@/components/Budget/EditBudgetPopup";
import { SummaryRow, EditBudget } from "@/lib/types/BudgetType";
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
  const { role } = useConfig();
  const { setLoading } = useLoading();
  const [count, setCount] = useState();
  const [size, setSize] = useState<number>(20);
  const [editTitle, setEditTitle] = useState<string>();
  const [editId, setEditId] = useState<number>();
  const [isAdd, setIsAdd] = useState<boolean>(false);
  const [isEdit, setIsEdit] = useState<boolean>(false);
  const [chartSummary, setChartSummary] = useState<string>();
  const [summaryData, setSummaryData] = useState<SummaryRow[]>();

  if (role) {
    if (![0, 2, 3].includes(role)) {
      notFound();
    }
  }

  const getSummary = async () => {
    try {
      const res = await departmentAPI.getDeptSummary();
      if (res.data) {
        setSummaryData(res.data);
      }
    } catch {}
  };

  const getCount = async () => {
    try {
      const res = await ticketAPI.getUnVerifyCount();
      if (res.data) {
        setCount(res.data.total);
      }
    } catch {}
  };

  const getDropdown = async () => {
    try {
      const res = await departmentAPI.getDropdown();
    } catch {}
  };

  const getChartSummary = async () => {
    try {
      const res = await n8nAPI.getSummary({
        question: "請幫我綜整目前支出的狀況，並提醒我個部分需要注意",
      });
      if (res.data) {
        setChartSummary(res.data);
      }
    } catch {}
  };

  useEffect(() => {
    // const getChart = async () => {
    //   try {
    //     const res = await n8nAPI.getHomeChart();
    //   } catch {}
    // };

    // getChart();
    setLoading(false);

    const handleResize = () => {
      const width = window.innerWidth;
      if (width < 1440) setSize(20);
      else setSize(30);
    };

    handleResize();
    getChartSummary();
    getCount();
    getSummary();
    getDropdown();
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
              <div className={styles.charts} style={{ gap: `${size}px` }}>
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
              　　{/*chartSummary*/}
              近期支出狀況良好，無異常支出紀錄。但請注意交際費使用頻率較高，建議檢視相關報銷單據以確保符合公司政策。
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
                        <Trash2
                          className={styles.delete}
                          size={20}
                          onClick={async () => {
                            const id = item.department_id;
                            const data: EditBudget = {
                              accounting_items: [],
                            };
                            try {
                              await departmentAPI.editBudget(id, data);
                            } catch {}
                          }}
                        />
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
            <Plus
              size={20}
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
          getSummary={getSummary}
        />
      )}
    </>
  );
}
