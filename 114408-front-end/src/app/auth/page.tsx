"use client";

import { toast } from "sonner";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import { Mail } from "lucide-react";
import { UserRound } from "lucide-react";
import { LockKeyhole } from "lucide-react";

import InputField from "@/components/common/InputField";
import userAPI from "@/services/userAPI";
import styles from "@/styles/app/auth/AuthPage.module.scss";
import { AuthFormData } from "@/lib/types/UserAPIType";

const Login = ({ register }: { register: any }) => {
  return (
    <div className={styles.loginFrame}>
      <InputField
        hint="email"
        type="text"
        isCornerRadius={true}
        style={{ width: "80vw" }}
        icon={<Mail size={24} color="#3f3f3f" />}
        register={register("email", { required: true })}
      />
      <InputField
        hint="password"
        type="password"
        isCornerRadius={true}
        style={{ width: "80vw" }}
        icon={<LockKeyhole size={24} color="#3f3f3f" />}
        register={register("password", { required: true })}
      />
      <span className={styles.forget}>忘記密碼？</span>
    </div>
  );
};

const SignUp = ({ register }: { register: any }) => {
  return (
    <div className={styles.loginFrame}>
      <InputField
        hint="name"
        type="text"
        isCornerRadius={true}
        style={{ width: "80vw" }}
        icon={<UserRound size={24} color="#3f3f3f" />}
        register={register("username", { required: true })}
        showIcon={true}
      />
      <InputField
        hint="email"
        type="text"
        isCornerRadius={true}
        style={{ width: "80vw" }}
        icon={<Mail size={24} color="#3f3f3f" />}
        register={register("email", { required: true })}
        showIcon={true}
      />
      <InputField
        hint="password"
        type="password"
        isCornerRadius={true}
        style={{ width: "80vw" }}
        icon={<LockKeyhole size={24} color="#3f3f3f" />}
        register={register("password", { required: true })}
        showIcon={true}
      />
    </div>
  );
};

export default function Auth() {
  const [isLogin, setIsLogin] = useState<boolean>(false);
  const route = useRouter();
  const { register, handleSubmit } = useForm<AuthFormData>();

  const loginClass = isLogin ? styles.focusItem : styles.item;
  const signupClass = !isLogin ? styles.focusItem : styles.item;

  const onSubmit = async (data: AuthFormData) => {
    let res;
    try {
      if (isLogin) {
        res = await userAPI.login({
          email: data.email,
          password: data.password,
        });
        if (res.state === "success") {
          route.push("/user");
        }
      } else if (data.username) {
        res = await userAPI.register({
          username: data.username,
          email: data.email,
          password: data.password,
        });
        if (res.state === "success") {
          setIsLogin(true);
        }
      }
    } catch {
      toast.error("發生錯誤，請稍後再試");
    }
  };

  const onError = () => {
    toast.error("請完整填寫所有欄位！");
  };

  return (
    <form onSubmit={handleSubmit(onSubmit, onError)}>
      <div className={styles.authWrap}>
        <div className={styles.option}>
          <p className={loginClass} onClick={() => setIsLogin(true)}>
            登入
          </p>
          <p className={signupClass} onClick={() => setIsLogin(false)}>
            註冊
          </p>
        </div>
        {isLogin ? (
          <Login register={register} />
        ) : (
          <SignUp register={register} />
        )}
        <button className={styles.click}>{isLogin ? "登入" : "註冊"}</button>
      </div>
    </form>
  );
}
