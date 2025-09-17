import { DataGrid, GridRowsProp, GridColDef } from "@mui/x-data-grid";
import { Eye } from "lucide-react";

import styles from "@/styles/components/LargeTable.module.scss";
import { useEffect, useState } from "react";
import ticketAPI from "@/services/ticketAPI";
import { pendingTicket } from "@/lib/types/TicketType";

const columns: GridColDef[] = [
  { field: "upload_date", headerName: "報帳時間", width: 100 },
  { field: "type", headerName: "報帳種類", width: 100 },
  { field: "title", headerName: "標題", width: 580 },
  { field: "total_money", headerName: "金額", width: 50 },
  {
    field: "creator_name",
    headerName: "申請人",
    width: 70,
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

export default function PendingTable() {
  const [data, setData] = useState<pendingTicket[]>();

  useEffect(() => {
    const getData = async () => {
      try {
        const res = await ticketAPI.getPending();
        if (res.data) {
          setData(res.data);
        }
      } catch {}
    };

    getData();
  }, []);

  return (
    <div style={{ width: "100%", height: "100%  " }}>
      <DataGrid
        className={styles.grid}
        rows={data}
        columns={columns}
        pageSizeOptions={[8]}
        checkboxSelection
        getRowId={(row) => `${row.upload_date}-${row.img_url}`}
        disableRowSelectionOnClick
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
