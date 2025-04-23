"use client";

import { useState } from "react";
import { Mail } from "lucide-react";
import { UserRound } from "lucide-react";
import { LockKeyhole } from "lucide-react";

import InputField from "@/components/common/InputField";
import styles from "@/styles/app/auth/AuthPage.module.scss";

const Login = () => {
  return (
    <div className={styles.loginFrame}>
      <InputField
        hint="email"
        type="text"
        isCornerRadius={true}
        style={{ width: "80vw" }}
        icon={<Mail size={24} color="#3f3f3f" />}
      />
      <InputField
        hint="password"
        type="text"
        isCornerRadius={true}
        style={{ width: "80vw" }}
        icon={<LockKeyhole size={24} color="#3f3f3f" />}
      />
      <span className={styles.forget}>忘記密碼？</span>
    </div>
  );
};

const SignUp = () => {
  return (
    <div className={styles.loginFrame}>
      <InputField
        hint="name"
        type="text"
        isCornerRadius={true}
        style={{ width: "80vw" }}
        icon={<UserRound size={24} color="#3f3f3f" />}
      />
      <InputField
        hint="email"
        type="text"
        isCornerRadius={true}
        style={{ width: "80vw" }}
        icon={<Mail size={24} color="#3f3f3f" />}
      />
      <InputField
        hint="password"
        type="text"
        isCornerRadius={true}
        style={{ width: "80vw" }}
        icon={<LockKeyhole size={24} color="#3f3f3f" />}
      />
    </div>
  );
};

export default function Auth() {
  const [isLogin, setIsLogin] = useState<boolean>(false);

  const loginClass = isLogin ? styles.focusItem : styles.item;
  const signupClass = !isLogin ? styles.focusItem : styles.item;

  return (
    <div className={styles.authWrap}>
      <div className={styles.option}>
        <p className={loginClass} onClick={() => setIsLogin(true)}>
          登入
        </p>
        <p className={signupClass} onClick={() => setIsLogin(false)}>
          註冊
        </p>
      </div>
      {isLogin ? <Login /> : <SignUp />}
      <button className={styles.click}>{isLogin ? "登入" : "註冊"}</button> 
    </div>
  );
}
