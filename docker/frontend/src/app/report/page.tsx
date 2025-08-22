import Link from "next/link";
import { ChartLine } from "lucide-react";

import { reportItemData } from "@/lib/data/reportItemData";
import styles from "@/styles/app/report/ReportPage.module.scss";

const Item = ({
  Icon,
  title,
  link,
}: {
  Icon: any;
  title: string;
  link: string;
}) => {
  return (
    <Link href={link}>
      <div className={styles.item}>
        <Icon size={50} className={styles.icon} />
        <p>{title}</p>
      </div>
    </Link>
  );
};

export default function Report() {
  return (
    <div className={styles.wrap}>
      <p className={styles.title}>
        <ChartLine size={35} />
        報表專區
      </p>
      <div className={styles.itemWrap}>
        {reportItemData.map((item, index) => (
          <Item
            Icon={item.icon}
            title={item.title}
            link={item.link}
            key={index}
          />
        ))}
      </div>
    </div>
  );
}
