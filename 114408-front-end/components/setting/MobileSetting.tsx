import Image from "next/image";
import { PencilLine } from "lucide-react";
import { useState } from "react";
import { useRouter } from "next/navigation";

import ThemeToggle from "@/components/common/ThemeToggle";
import InputField from "@/components/common/InputField";
import styles from "@/styles/app/SettingPage.module.scss";
import userAPI from "@/services/userAPI";

export const MobileSetting = ({
  register,
  handleSubmit,
}: {
  register: any;
  handleSubmit: any;
}) => {
  const [isEdit, setIsEdit] = useState<boolean>();
  const route = useRouter();

  const edit = async (data: any) => {
    const finalData = { ...data };
    if (finalData.password === "*********") {
      delete finalData.password;
    } else {
      finalData.new_password = data.password;
      delete finalData.password;
    }

    try {
      await userAPI.editUser(finalData);
    } catch {
    } finally {
      setIsEdit(false);
    }
  };

  return (
    <div className={styles.settingWrap}>
      <div className={styles.userTitle}>
        <Image
          alt="頭貼"
          width={110}
          height={110}
          src={"/bottomNavIcon/user.png"}
          style={{ borderRadius: "50%" }}
        />
        <p>使用者</p>
      </div>
      <div className={styles.detail}>
        <p className={styles.detailTitle}>個人資訊</p>
        {[
          { label: "您的姓名", name: "username", type: "text" },
          { label: "您的信箱", name: "email", type: "text" },
          { label: "您的密碼", name: "password", type: "password" },
        ].map(({ label, name, type }) => (
          <InputField
            key={name}
            type={type}
            label={label}
            style={{ width: "80vw" }}
            register={register(name)}
            icon={<PencilLine />}
            iconRight
            showIcon={isEdit ? true : false}
            readonly={isEdit ? false : true}
          />
        ))}
        <div className={styles.button}>
          {isEdit ? (
            <>
              <button
                className={styles.cancel}
                onClick={() => {
                  setIsEdit(false);
                }}
              >
                取消
              </button>
              <button className={styles.editSure} onClick={handleSubmit(edit)}>
                確定修改
              </button>
            </>
          ) : (
            <>
              <button
                className={styles.logout}
                onClick={() => {
                  route.push("/auth");
                  localStorage.clear();
                }}
              >
                登出
              </button>
              <button
                className={styles.edit}
                onClick={() => {
                  setIsEdit(true);
                }}
              >
                修改
              </button>
            </>
          )}
        </div>
        <ThemeToggle />
      </div>
    </div>
  );
};
