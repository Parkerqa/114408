"use client";

import { toast } from "sonner";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import { Mail } from "lucide-react";
import { UserRound } from "lucide-react";
import { LockKeyhole } from "lucide-react";

import { useLoading } from "@/lib/context/LoadingContext";
import { useConfig } from "@/lib/context/ConfigContext";
import { AuthFormData } from "@/lib/types/UserAPIType";
import InputField from "@/components/common/InputField";
import ForgetPassword from "@/components/ForgetPassword";
import userAPI from "@/services/userAPI";
import styles from "@/styles/app/auth/AuthPage.module.scss";

const Login = ({
  register,
  setIsPopup,
}: {
  register: any;
  setIsPopup: (boolean: boolean) => void;
}) => {
  const { theme } = useConfig();
  const iconColor = theme === 0 ? "#3f4360" : "#f0f0f5";

  return (
    <div className={styles.loginFrame}>
      <InputField
        hint="email"
        type="text"
        isCornerRadius={true}
        style={{ width: "80vw" }}
        icon={<Mail size={24} color={iconColor} />}
        register={register("email", { required: true })}
        showIcon={true}
      />
      <InputField
        hint="password"
        type="password"
        isCornerRadius={true}
        style={{ width: "80vw" }}
        icon={<LockKeyhole size={24} color={iconColor} />}
        register={register("password", { required: true })}
        showIcon={true}
      />
      <span
        className={styles.forget}
        onClick={() => {
          setIsPopup(true);
        }}
      >
        忘記密碼？
      </span>
    </div>
  );
};

const SignUp = ({ register }: { register: any }) => {
  const { theme } = useConfig();
  const iconColor = theme === 0 ? "#3f4360" : "#f0f0f5";

  return (
    <div className={styles.loginFrame}>
      <InputField
        hint="name"
        type="text"
        isCornerRadius={true}
        style={{ width: "80vw" }}
        icon={<UserRound size={24} color={iconColor} />}
        register={register("username", { required: true })}
        showIcon={true}
      />
      <InputField
        hint="email"
        type="text"
        isCornerRadius={true}
        style={{ width: "80vw" }}
        icon={<Mail size={24} color={iconColor} />}
        register={register("email", { required: true })}
        showIcon={true}
      />
      <InputField
        hint="password"
        type="password"
        isCornerRadius={true}
        style={{ width: "80vw" }}
        icon={<LockKeyhole size={24} color={iconColor} />}
        register={register("password", { required: true })}
        showIcon={true}
      />
    </div>
  );
};

export default function Auth() {
  const route = useRouter();
  const [isLogin, setIsLogin] = useState<boolean>(true);
  const [isForget, setIsForget] = useState<boolean>();
  const { register, handleSubmit } = useForm<AuthFormData>();
  const { setLoading } = useLoading();

  const loginClass = isLogin ? styles.focusItem : styles.item;
  const signupClass = !isLogin ? styles.focusItem : styles.item;

  const onSubmit = async (data: AuthFormData) => {
    setLoading(true);
    try {
      if (isLogin) {
        const res = await userAPI.login({
          email: data.email,
          password: data.password,
        });
        if (res.state === "success") {
          route.push("./");
        }
      } else if (data.username) {
        const res = await userAPI.register({
          username: data.username,
          email: data.email,
          password: data.password,
        });
        if (res.state === "success") {
          setIsLogin(true);
        }
      }
    } catch {
    } finally {
      setLoading(false);
    }
  };

  const onError = () => {
    toast.error("請完整填寫所有欄位！");
  };

  return (
    <>
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
            <Login register={register} setIsPopup={setIsForget} />
          ) : (
            <SignUp register={register} />
          )}
          <button className={styles.click}>{isLogin ? "登入" : "註冊"}</button>
        </div>
      </form>
      {isForget && <ForgetPassword setIsPopup={setIsForget} />}
    </>
  );
}
