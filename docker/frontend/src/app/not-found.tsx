import Link from "next/link";

export default function NotFound() {
  return (
    <div style={{ textAlign: "center", padding: "100px" }}>
      <h1>404 - 找不到頁面</h1>
      <p style={{ margin: "20px 0" }}>您要找的頁面不存在或已移除</p>
      <Link
        href="/user"
        style={{
          color: "#FEC775",
          fontWeight: "bold",
          letterSpacing: "1px",
        }}
      >
        點我回首頁
      </Link>
    </div>
  );
}
