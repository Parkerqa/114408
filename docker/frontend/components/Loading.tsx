import CircularProgress from "@mui/material/CircularProgress";

export default function Loading() {
  return (
    <div
      style={{
        width: "100%",
        height: "100vh",
        position: "absolute",
        top: "0",
        left: "0",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: "10000",
        backgroundColor: "rgba(0, 0, 0, 0.5)",
      }}
    >
      <CircularProgress sx={{ color: "#fff" }} />
    </div>
  );
}
