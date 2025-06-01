"use client";

import styles from "@/styles/components/common/InputField.module.scss";
import React from "react";

export default function InputField({
  type,
  hint,
  label,
  register,
  style,
  icon,
  showIcon = false,
  isCornerRadius,
  iconRight,
  readonly = false,
}: {
  type: string;
  hint?: string;
  label?: string;
  isCornerRadius?: boolean;
  register?: any;
  style?: React.CSSProperties;
  showIcon?: boolean;
  icon?: React.ReactNode;
  iconRight?: boolean;
  readonly?: boolean;
}) {
  const showLeftIcon = icon && showIcon && !iconRight;
  const showRightIcon = icon && showIcon && iconRight;

  return (
    <div
      className={styles.fieldWrap}
      style={isCornerRadius ? { borderRadius: "50px" } : {}}
    >
      {label && <label className={styles.title}>{label}</label>}
      {showLeftIcon && (
        <span
          className={styles.iconLeft}
          style={isCornerRadius ? { marginLeft: "20px" } : {}}
        >
          {icon}
        </span>
      )}
      {showRightIcon && (
        <span
          className={styles.iconRight}
          style={isCornerRadius ? { marginRight: "20px" } : {}}
        >
          {icon}
        </span>
      )}
      <input
        type={type}
        placeholder={hint}
        className={`${styles.field}
        ${showLeftIcon && styles.hasPadding}
        `}
        style={{
          ...(isCornerRadius ? { borderRadius: "50px" } : {}),
          ...style,
        }}
        {...register}
        readOnly={readonly}
      />
    </div>
  );
}
