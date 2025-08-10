import Image from "next/image";
import { PencilLine } from "lucide-react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useDropzone } from "react-dropzone";
import { useForm } from "react-hook-form";

import { useConfig } from "@/lib/context/ConfigContext";
import ThemeToggle from "@/components/common/ThemeToggle";
import InputField from "@/components/common/InputField";
import userAPI from "@/services/userAPI";
import styles from "@/styles/components/setting/MobileSetting.module.scss";

export const MobileSetting = () => {
  const { user, fetchUser } = useConfig();
  const [isEdit, setIsEdit] = useState<boolean>();
  const [newImg, setNewImg] = useState<string | null>(null);
  const route = useRouter();
  const { getRootProps, getInputProps, acceptedFiles } = useDropzone({
    accept: { "image/*": [] },
    multiple: false,
  });
  const { register, reset, handleSubmit } = useForm({
    defaultValues: {
      username: user?.username,
      email: user?.email,
      password: "*********",
    },
  });

  const edit = async (data: any) => {
    const file = acceptedFiles[0];

    const formData = new FormData();
    formData.append("email", data.email);
    formData.append("username", data.username);
    if (!(data.password === "*********")) {
      formData.append("new_password", data.password);
    }
    if (file) {
      formData.append("avatar", file);
    }

    const finalData = { img: file, ...data };
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

  const fields = [
    { label: "您的姓名", name: "username", type: "text" },
    { label: "您的信箱", name: "email", type: "text" },
    { label: "您的密碼", name: "password", type: "password" },
  ] as const;

  useEffect(() => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      const objectUrl = URL.createObjectURL(file);
      setNewImg(objectUrl);

      return () => URL.revokeObjectURL(objectUrl);
    }
  }, [acceptedFiles]);

  return (
    <div className={styles.settingWrap}>
      <div className={styles.user} {...(isEdit && getRootProps())}>
        {isEdit && <input {...getInputProps()} />}
        {(newImg || user?.img) && (
          <Image
            alt="頭貼"
            width={110}
            height={110}
            unoptimized
            src={newImg || user?.img!}
            style={{ borderRadius: "50%" }}
            className={styles.userImg}
          />
        )}
        {isEdit && (
          <div className={styles.overlay}>
            <PencilLine size={27} color="#fff" />
          </div>
        )}
      </div>
      <div className={styles.detail}>
        <p className={styles.detailTitle}>個人資訊</p>
        {fields.map(({ label, name, type }) => (
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
                  document.body.setAttribute("data-theme", "light");
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
