import MoreInfoBar from "@/components/common/MoreInfoBar";
import styles from "@/styles/components/setting/AdminSetting.module.scss";

export default function AdminSetting() {
  const context = <div>123</div>;

  return (
    <div className={styles.wrap}>
      <MoreInfoBar title="其他設定" context={context} />;
    </div>
  );
}
