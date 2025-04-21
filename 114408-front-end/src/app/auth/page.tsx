"use client";

import { useState } from "react";
import { Mail } from 'lucide-react';
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
        icon={<Mail size={24} color="#3f3f3f"
        />}
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

  return (
    <>
      {isLogin ? <Login /> : <SignUp />}
    </>
  );
}
