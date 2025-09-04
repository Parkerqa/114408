"use client";

import { useState } from "react";
import { FaCaretDown, FaCaretUp } from "react-icons/fa";

import { itemType } from "@/lib/types/selectFieldType";
import styles from "@/styles/components/common/SelectField.module.scss";

export default function SelectField({
  title,
  optionData,
  value,
  onChange,
  style,
  placeholder = "請選擇",
}: {
  title: string;
  optionData: itemType[];
  value?: string;
  onChange?: (v: string) => void;
  style?: React.CSSProperties;
  placeholder?: string;
}) {
  const [isOpen, setIsOpen] = useState(false);

  const handleSelect = (v: string) => {
    onChange?.(v);
    setIsOpen(false)
  };

  return (
    <div className={styles.wrap}>
      <div
        style={style}
        className={styles.field}
        onClick={() => setIsOpen((o) => !o)}
        role="button"
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        tabIndex={0}
      >
        <span className={styles.label}>{title}</span>
        <p>{value || placeholder}</p>
        {isOpen ? <FaCaretUp size={20} /> : <FaCaretDown size={20} />}
      </div>

      {isOpen && (
        <ul className={styles.optionWrap} role="listbox">
          {optionData.map((item) => (
            <li
              className={styles.option}
              key={item.value}
              role="option"
              aria-selected={item.value === value}
              onClick={() => handleSelect(item.value)}
            >
              {item.value}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
