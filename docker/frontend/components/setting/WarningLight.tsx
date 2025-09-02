"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { PencilLine } from "lucide-react";

import { FormValues } from "@/lib/types/WarningType";
import { fields } from "@/lib/data/WarningData";
import InputField from "@/components/common/InputField";
import styles from "@/styles/components/setting/WarningLight.module.scss";

export default function WarningLight() {
  const [isEdit, setIsEdit] = useState<boolean>();

  const { register, handleSubmit } = useForm<FormValues>({
    defaultValues: {
      excess_top: 100,
      excess_bot: 81,
      high_top: 80,
      high_bot: 61,
      good_top: 60,
      good_bot: 41,
      low_top: 40,
      low_bot: 21,
      insufficient_top: 20,
      insufficient_bot: 0,
    },
  });

  const fieldProp = {
    type: "text",
    icon: <PencilLine />,
    style: { width: "100px" },
    showIcon: isEdit,
    readonly: !isEdit,
  };

  const renderInput = (name: keyof FormValues, label: string) => (
    <InputField
      label={label}
      register={register(name, { valueAsNumber: true })}
      iconRight
      {...fieldProp}
    />
  );

  const edit = async (data: any) => {
    const formData = new FormData();
    formData.append("green_top", data.green_top);
    formData.append("green_bot", data.green_bot);
    formData.append("yellow_top", data.yellow_top);
    formData.append("yellow_bot", data.yellow_bot);
    formData.append("red_top", data.red_top);
    formData.append("red_bot", data.red_bot);
  };

  return (
    <div className={styles.settingWrap}>
      <div className={styles.itemWrap}>
        {fields.map((item, index) => (
          <div className={styles.item} key={index}>
            <div className={item.className}></div>
            {renderInput(item.limit_top, item.label_top)}
            {renderInput(item.limit_bot, item.label_bot)}
          </div>
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
