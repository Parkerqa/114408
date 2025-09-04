import { DataGrid, GridRowsProp, GridColDef } from "@mui/x-data-grid";
import { Eye } from "lucide-react";

import styles from "@/styles/components/LargeTable.module.scss";

const rows: GridRowsProp = [
  {
    id: 1,
    time: "2025/08/01",
    type: "電子發票",
    title: "飲冰室極品紅奶茶",
    money: "25",
    applicant: "周品君",
  },
  {
    id: 2,
    time: "2025/08/01",
    type: "電子發票",
    title: "飲冰室極品紅奶茶",
    money: "25",
    applicant: "周品君",
  },
  {
    id: 3,
    time: "2025/08/01",
    type: "電子發票",
    title: "飲冰室極品紅奶茶",
    money: "25",
    applicant: "周品君",
  },
  {
    id: 4,
    time: "2025/08/01",
    type: "電子發票",
    title: "飲冰室極品紅奶茶",
    money: "25",
    applicant: "周品君",
  },
  {
    id: 5,
    time: "2025/08/01",
    type: "電子發票",
    title: "飲冰室極品紅奶茶",
    money: "25",
    applicant: "周品君",
  },
  {
    id: 6,
    time: "2025/08/01",
    type: "電子發票",
    title: "飲冰室極品紅奶茶",
    money: "25",
    applicant: "周品君",
  },
  {
    id: 7,
    time: "2025/08/01",
    type: "電子發票",
    title: "飲冰室極品紅奶茶",
    money: "25",
    applicant: "周品君",
  },
  {
    id: 8,
    time: "2025/08/01",
    type: "電子發票",
    title: "飲冰室極品紅奶茶",
    money: "25",
    applicant: "周品君",
  },
  {
    id: 9,
    time: "2025/08/01",
    type: "電子發票",
    title: "飲冰室極品紅奶茶",
    money: "25",
    applicant: "周品君",
  },
  {
    id: 10,
    time: "2025/08/01",
    type: "電子發票",
    title: "飲冰室極品紅奶茶",
    money: "25",
    applicant: "周品君",
  },
];

const columns: GridColDef[] = [
  { field: "time", headerName: "報帳時間", width: 100 },
  { field: "type", headerName: "報帳種類", width: 100 },
  { field: "title", headerName: "標題", width: 580 },
  { field: "money", headerName: "金額", width: 50 },
  {
    field: "applicant",
    headerName: "申請人",
    width: 70,
    headerAlign: "center",
    align: "center",
  },
  {
    field: "prove",
    headerName: "證明",
    width: 50,
    renderCell: (params) => <Eye style={{ cursor: "pointer" }} />,
  },
];

export default function LargeTable() {
  return (
    <div style={{ width: "100%" }}>
      <DataGrid
        className={styles.grid}
        rows={rows}
        columns={columns}
        pageSizeOptions={[8]}
        checkboxSelection
        initialState={{
          pagination: {
            paginationModel: { pageSize: 8, page: 0 },
          },
        }}
        sx={{
          backgroundColor: "var(--list-bg)",
          color: "var(--text-color)",
          "& .MuiDataGrid-columnHeader": {
            backgroundColor: "var(--list-bg)",
            color: "var(--text-color)",
          },
          "& .MuiSvgIcon-root": {
            color: "var(--text-color)",
          },
        }}
      />
    </div>
  );
}
