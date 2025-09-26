"use client";

import { useState, useEffect, useCallback, useRef, useMemo } from "react";
import { useForm } from "react-hook-form";
import { DateRange } from "react-day-picker";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { Eye } from "lucide-react";
import "react-day-picker/style.css";

import BarChart from "@/components/chart/BarChart";
import LineChart from "@/components/chart/LineChart";
import { formatDateRange } from "@/lib/utils/formatDateRange";
import ReportNav from "@/components/ReportNav";
import InputField from "@/components/common/InputField";
import DateSelector from "@/components/common/DateSelector";
import {
  bar_chart,
  daily_amounts,
  report_ticket,
} from "@/lib/types/TicketType";
import ticketAPI from "@/services/ticketAPI";
import styles from "@/styles/app/report/YearPage.module.scss";

const columns: GridColDef[] = [
  { field: "upload_date", headerName: "報帳時間", width: 100 },
  { field: "type", headerName: "報帳種類", width: 100 },
  { field: "title", headerName: "標題", width: 350 },
  {
    field: "total_money",
    headerName: "金額",
    width: 80,
    headerAlign: "center",
    align: "center",
  },
  {
    field: "creator_name",
    headerName: "申請人",
    width: 100,
    headerAlign: "center",
    align: "center",
  },
  {
    field: "check_date",
    headerName: "核銷日期",
    width: 100,
    headerAlign: "center",
    align: "center",
  },
  {
    field: "check_man",
    headerName: "核銷人",
    width: 100,
    headerAlign: "center",
    align: "center",
  },
  {
    field: "prove",
    headerName: "證明",
    width: 50,
    renderCell: (params) => (
      <Eye
        style={{ cursor: "pointer" }}
        onClick={() => window.open(params.row.img_url, "_blank")}
      />
    ),
  },
];

const toNoonLocal = (d: Date) =>
  new Date(d.getFullYear(), d.getMonth(), d.getDate(), 12);

const fmt = (d: Date) =>
  `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(
    d.getDate()
  ).padStart(2, "0")}`;

export default function Custom() {
  const [customRange, setCustomRange] = useState<DateRange | undefined>();
  const [barData, setBarData] = useState<bar_chart[]>([]);
  const [lineData, setLineData] = useState<daily_amounts[]>([]);
  const [ticketData, setTicketData] = useState<report_ticket[]>([]);
  const [dateRange, setDateRange] = useState<DateRange | undefined>();

  const { register, watch, setValue } = useForm<{ start: string; end: string }>(
    {
      defaultValues: { start: "", end: "" },
    }
  );

  const start = watch("start");
  const end = watch("end");

  useEffect(() => {
    if (!start && !end) {
      setDateRange(undefined);
      return;
    }
    const s = start ? toNoonLocal(new Date(start)) : undefined;
    const e = end ? toNoonLocal(new Date(end)) : undefined;

    if (s && e) {
      if (s > e) {
        setValue("start", fmt(e));
        setValue("end", fmt(s));
        setDateRange({ from: e, to: s });
      } else {
        setDateRange({ from: s, to: e });
      }
    } else {
      setDateRange({ from: s, to: e });
    }
  }, [start, end, setValue]);

  const { from, to } = useMemo(() => {
    const r = formatDateRange(dateRange);
    return { from: r?.from ?? "", to: r?.to ?? "" };
  }, [dateRange]);

  const getReport = useCallback(async (from: string, to: string) => {
    try {
      const res = await ticketAPI.report(from, to);
      if (res.data?.daily_amounts) {
        setLineData(res.data.daily_amounts);
      }
      if (res.data?.top_accounts) {
        setBarData(res.data.top_accounts);
      }
      if (res.data?.tickets) {
        setTicketData(res.data.tickets);
      }
    } catch {}
  }, []);

  const lastKeyRef = useRef("");
  useEffect(() => {
    if (!from || !to) return;
    const key = `${from}-${to}`;
    if (key === lastKeyRef.current) return;
    lastKeyRef.current = key;
    getReport(from, to);
  }, [from, to, getReport]);

  return (
    <div className={styles.wrap}>
      <div style={{ display: "flex", gap: "30px" }}>
        <ReportNav />
        <InputField type="date" label="開始" register={register("start")} />
        <InputField type="date" label="結束" register={register("end")} />
      </div>

      <div className={styles.infoArea}>
        <div style={{ marginRight: "30px" }} className={styles.infoItem}>
          <p className={styles.title}>前三支出會計項目</p>
          {barData && <BarChart data={barData} />}
        </div>
        <div className={styles.infoItem}>
          <p className={styles.title}>核銷金額變動圖</p>
          {lineData && <LineChart data={lineData} />}
        </div>
        {dateRange?.from && dateRange?.to && (
          <DateSelector
            recentBtn={false}
            initRange={customRange}
            onChange={setDateRange}
          />
        )}
      </div>
      <div>
        <DataGrid
          columns={columns}
          rows={ticketData}
          pageSizeOptions={[4]}
          initialState={{
            pagination: { paginationModel: { pageSize: 4 } },
          }}
          disableRowSelectionOnClick
          getRowId={(row) => `${row.ticket_id}`}
        />
      </div>
    </div>
  );
}
