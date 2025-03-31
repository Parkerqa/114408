import { liseData } from "@/lib/data/listData";
import MobileListItem from "@/components/common/MobileListItem";
import styles from "@/styles/app/UserPage.module.scss";

export default function User() {
  return (
    <>
      <input type="text" name="" id="" />
      <div className={styles.list}>
        {liseData.map((item, index) => (
          <MobileListItem data={item} key={index} />
        ))}
      </div>
    </>
  );
}
