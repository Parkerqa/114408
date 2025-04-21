"use client";

import styles from "@/styles/components/common/InputField.module.scss";
import { UseFormRegisterReturn } from "react-hook-form";
import React, { useState } from "react";

export default function InputField({
  type,
  hint,
  label,
  register,
  style,
  icon,
  isCornerRadius,
}: {
  type: string;
  hint?: string;
  label?: string;
  isCornerRadius?: boolean;
  register?: UseFormRegisterReturn;
  style?: React.CSSProperties;
  icon?: React.ReactNode;
}) {
  const [hasValue, setHasValue] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setHasValue(e.target.value !== "");
    register?.onChange?.(e);
  };

  return (
    <div
      className={styles.fieldWrap}
      style={isCornerRadius ? { borderRadius: "50px" } : {}}
    >
      {label && <label className={styles.title}>{label}</label>}
      {!hasValue && icon && (
        <span
          className={styles.icon}
          style={isCornerRadius ? { marginLeft: "20px" } : {}}
        >
          {icon}
        </span>
      )}
      <input
        type={type}
        placeholder={hint}
        className={`${styles.field} ${!hasValue && icon && styles.hasPadding}`}
        style={{
          ...(isCornerRadius ? { borderRadius: "50px" } : {}),
          ...style,
        }}
        {...register}
        onChange={handleChange}
      />
    </div>
  );
}
