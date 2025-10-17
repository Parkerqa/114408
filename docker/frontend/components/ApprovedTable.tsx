import { useEffect, useState } from "react";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { Eye } from "lucide-react";

import PriviewImg from "@/components/common/PriviewImg";
import ticketAPI from "@/services/ticketAPI";
import { pendingTicket } from "@/lib/types/TicketType";
import styles from "@/styles/components/LargeTable.module.scss";

export default function ApprovedTable() {
  const [data, setData] = useState<pendingTicket[]>();
  const [imgUrl, setImgUrl] = useState<string>();
  const [preview, setPriview] = useState<boolean>(false);

  const handlePreview = (url: string) => {
    setImgUrl(url);
    setPriview(true);
  };

  useEffect(() => {
    const getData = async () => {
      try {
        const res = await ticketAPI.getApprove();
        if (res.data) {
          setData(res.data);
        }
      } catch {}
    };

    getData();
  }, []);

  const columns: GridColDef[] = [
    { field: "upload_date", headerName: "報帳時間", width: 100 },
    { field: "type", headerName: "報帳種類", width: 100 },
    { field: "title", headerName: "標題", width: 630 },
    { field: "total_money", headerName: "金額", width: 70 },
    {
      field: "creator_name",
      headerName: "申請人",
      width: 120,
      headerAlign: "center",
      align: "center",
    },
    {
      field: "check_man",
      headerName: "核銷人",
      width: 120,
      headerAlign: "center",
      align: "center",
    },
    {
      field: "prove",
      headerName: "證明",
      width: 50,
      headerAlign: "center",
      align: "center",
      renderCell: (params) => (
        <Eye
          style={{ cursor: "pointer" }}
          onClick={() => handlePreview(params.row.img_url)}
        />
      ),
    },
  ];

  return (
    <div style={{ width: "100%", height: "100%" }}>
      <DataGrid
        className={styles.grid}
        rows={data}
        columns={columns}
        pageSizeOptions={[8]}
        getRowId={(row) => `${row.ticket_id}`}
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
      {preview && imgUrl && (
        <PriviewImg imgUrl={imgUrl} setPriview={setPriview} />
      )}
    </div>
  );
}
