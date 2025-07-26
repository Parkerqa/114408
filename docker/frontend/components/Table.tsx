type Record = {
  date: string;
  type: string;
  title: string;
  amount: number;
};

const records: Record[] = [
  {
    date: "2025/03/08",
    type: "電子發票",
    title: "PILOT百樂 超級果汁筆-10色*5",
    amount: 2500,
  },
  { date: "2025/03/05", type: "收據", title: "55688 台灣大車隊", amount: 2700 },
  {
    date: "2025/03/05",
    type: "二聯式發票",
    title: "噴墨式印表機",
    amount: 4000,
  },
];

import styles from "@/styles/components/Table.module.scss";

export default function Table() {
  return (
    <div>
      <table className={styles.table}>
        <thead>
          <tr className={styles.tableHead}>
            <th className={styles.item}>報帳時間</th>
            <th className={styles.item}>報帳種類</th>
            <th className={styles.item}>標題</th>
            <th className={styles.item}>金額</th>
          </tr>
        </thead>
        <tbody className={styles.tableBody}>
          {records.map((r, i) => (
            <tr
              className={styles.line}
              key={i}
              onClick={() => alert(`查看：${r.title}`)}
            >
              <td className={styles.item}>{r.date}</td>
              <td className={styles.item}>{r.type}</td>
              <td className={styles.item}>{r.title}</td>
              <td className={styles.item}>{r.amount}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
