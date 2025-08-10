import SelfInfo from "./SelfInfo";
import MoreInfoBar from "@/components/common/MoreInfoBar";
import styles from "@/styles/components/setting/AdminSetting.module.scss";

export default function AdminSetting() {
  return (
    <div className={styles.wrap}>
      <MoreInfoBar title="個人資訊" context={<SelfInfo />} />
    </div>
  );
}
