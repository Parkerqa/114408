"use client";

import { useRouter } from "next/navigation";
import { useConfig } from "@/lib/context/ConfigContext";

import SelfInfo from "./SelfInfo";
import AddDepartment from "./AddDepartment";
import AddAccount from "./AddAccount";
import WarningLight from "./WarningLight";
import MoreInfoBar from "@/components/common/MoreInfoBar";
import styles from "@/styles/components/setting/AdminSetting.module.scss";

export default function AdminSetting() {
  const route = useRouter();
  const { setRole, setUser } = useConfig();

  return (
    <div className={styles.wrap}>
      <div className={styles.items}>
        <MoreInfoBar title="個人資訊" context={<SelfInfo />} />
        <MoreInfoBar title="編輯儀錶板警示燈" context={<WarningLight />} />
        <MoreInfoBar title="編輯部門" context={<AddDepartment />} />
        <MoreInfoBar title="編輯會計科目" context={<AddAccount />} />
      </div>
      <button
        className={styles.logout}
        onClick={() => {
          localStorage.clear();
          setRole(undefined);
          setUser(undefined);
          route.push("/auth");
          document.body.setAttribute("data-theme", "light");
        }}
      >
        登出
      </button>
    </div>
  );
}
