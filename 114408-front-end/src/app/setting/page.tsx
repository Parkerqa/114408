"use client";

import Image from "next/image";
import { toast } from "sonner";
import { PencilLine } from "lucide-react";
import { useForm } from "react-hook-form";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import InputField from "@/components/common/InputField";
import styles from "@/styles/app/SettingPage.module.scss";
import userAPI from "@/services/userAPI";

const MobileSetting = ({ register, watch }: { register: any; watch: any }) => {
  const [isEdit, setIsEdit] = useState<boolean>();
  const route = useRouter();

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
        <InputField
          type="text"
          label="您的姓名"
          style={{ width: "80vw" }}
          register={register("username")}
          icon={<PencilLine />}
          iconRight={true}
          showIcon={isEdit ? true : false}
          value={watch("username")}
        />
        <InputField
          type="text"
          label="您的信箱"
          style={{ width: "80vw" }}
          register={register("email")}
          icon={<PencilLine />}
          iconRight={true}
          showIcon={isEdit ? true : false}
          value={watch("email")}
        />
        <InputField
          type="password"
          label="您的密碼"
          style={{ width: "80vw" }}
          register={register("password")}
          icon={<PencilLine />}
          iconRight={true}
          showIcon={isEdit ? true : false}
          value={watch("password")}
        />
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
              <button
                className={styles.editSure}
                onClick={() => {
                  setIsEdit(false);
                }}
              >
                確定修改
              </button>
            </>
          ) : (
            <>
              <button
                className={styles.logout}
                onClick={() => {
                  route.push("/auth");
                  localStorage.clear;
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
      </div>
    </div>
  );
};

export default function Setting() {
  const [user, setUser] = useState();
  const { register, watch, reset } = useForm();

  const getUser = async () => {
    try {
      const res = await userAPI.getUser();
      if (res.data) {
        reset({
          username: res.data.username,
          email: res.data.email,
          password:"*********"
        });
        setUser(res.data);
      }
    } catch {
      toast.error("未知錯誤，請重新刷新或登入");
    }
  };

  useEffect(() => {
    getUser();
  }, []);

  return <MobileSetting register={register} watch={watch} />;
}
