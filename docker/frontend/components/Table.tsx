import { useEffect, useState } from "react";

import { latestTicket } from "@/lib/types/TicketType";
import ticketAPI from "@/services/ticketAPI";
import styles from "@/styles/components/Table.module.scss";

export default function Table() {
  const [data, setData] = useState<latestTicket[]>();

  useEffect(() => {
    const getLatest = async () => {
      try {
        const res = await ticketAPI.getLatest();
        if (res.data) {
          setData(res.data);
        }
      } catch {}
    };

    getLatest();
  }, []);

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
          {data &&
            data.map((item, index) => (
              <tr
                className={styles.line}
                key={index}
                onClick={() => alert(`查看：${item.title}`)}
              >
                <td className={styles.item}>{item.upload_date}</td>
                <td className={styles.item}>{item.type}</td>
                <td className={styles.item}>{item.title}</td>
                <td className={styles.item}>{item.total_money}</td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
}
