import { useEffect, useState } from "react";
import { DataGrid, GridColDef, GridRowSelectionModel } from "@mui/x-data-grid";
import { Eye } from "lucide-react";

import { pendingTicket } from "@/lib/types/TicketType";
import ticketAPI from "@/services/ticketAPI";
import styles from "@/styles/components/LargeTable.module.scss";

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

export default function PendingTable({
  pendingData,
  setVerifyData,
}: {
  pendingData: pendingTicket[];
  setVerifyData: (any: any) => void;
}) {
  const handleSelectionChange = async (selection: GridRowSelectionModel) => {
    const ids = {
      ticket_id: Array.from(selection.ids).map((id) => Number(id)),
    };

    try {
      const res = await ticketAPI.getMultiList(ids);
      setVerifyData(res.data);
    } catch {}
  };

  return (
    <div style={{ width: "100%", height: "100%  " }}>
      <DataGrid
        className={styles.grid}
        rows={pendingData}
        columns={columns}
        getRowId={(row) => `${row.ticket_id}`}
        pageSizeOptions={[8]}
        onRowSelectionModelChange={handleSelectionChange}
        checkboxSelection
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
