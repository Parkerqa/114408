"use client";

import { PencilLine } from "lucide-react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";

import { useConfig } from "@/lib/context/ConfigContext";
import InputField from "@/components/common/InputField";
import userAPI from "@/services/userAPI";
import styles from "@/styles/components/setting/SelfInfo.module.scss";

export default function SelfInfo() {
  const fields = [
    { label: "您的姓名", name: "username", type: "text" },
    { label: "您的信箱", name: "email", type: "text" },
    { label: "您的密碼", name: "password", type: "password" },
  ] as const;
  const { user, fetchUser } = useConfig();
  const [isEdit, setIsEdit] = useState<boolean>();
  const route = useRouter();

  const { register, reset, handleSubmit } = useForm({
    defaultValues: {
      username: user?.username,
      email: user?.email,
      password: "*********",
    },
  });

  const edit = async (data: any) => {
    const formData = new FormData();
    formData.append("email", data.email);
    formData.append("username", data.username);
    if (!(data.password === "*********")) {
      formData.append("new_password", data.password);
    }

    const finalData = { ...data };
    if (finalData.password === "*********") {
      delete finalData.password;
    } else {
      finalData.new_password = data.password;
      delete finalData.password;
    }

    try {
      await userAPI.editUser(formData);
      fetchUser();
    } catch {
    } finally {
      setIsEdit(false);
    }
  };

  useEffect(() => {
    if (!user) return;

    const { username, email } = user;
    if (username && email) {
      reset({
        username,
        email,
        password: "*********",
      });
    }
  }, [user?.username, user?.email]);

  return (
    <div className={styles.settingWrap}>
      <div className={styles.detail}>
        {fields.map(({ label, name, type }) => (
          <InputField
            key={name}
            type={type}
            label={label}
            style={{ width: "50vw" }}
            register={register(name)}
            icon={<PencilLine />}
            iconRight
            showIcon={isEdit ? true : false}
            readonly={isEdit ? false : true}
          />
        ))}
      </div>
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
  );
}
