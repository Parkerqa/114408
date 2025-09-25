"use client";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { PencilLine } from "lucide-react";

import { useLoading } from "@/lib/context/LoadingContext";
import { FormValues } from "@/lib/types/WarningType";
import InputField from "@/components/common/InputField";
import settingAPI from "@/services/settingAPI";
import styles from "@/styles/components/setting/WarningLight.module.scss";

export default function WarningLight() {
  const { setLoading } = useLoading();
  const [isEdit, setIsEdit] = useState<boolean>();
  const [data, setData] = useState<FormValues>();

  const { register, handleSubmit, reset } = useForm<FormValues>({
    defaultValues: {
      green_usage_rate: data?.green_usage_rate,
      green_remaining_rate: data?.green_remaining_rate,
      yellow_usage_rate: data?.yellow_usage_rate,
      yellow_remaining_rate: data?.yellow_remaining_rate,
      red_usage_rate: data?.red_usage_rate,
      red_remaining_rate: data?.red_remaining_rate,
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
    setLoading(true);
    const editData = {
      red_remaining_rate: data.red_remaining_rate,
      red_usage_rate: data.red_usage_rate,
      yellow_remaining_rate: data.yellow_remaining_rate,
      yellow_usage_rate: data.yellow_usage_rate,
      green_remaining_rate: data.green_remaining_rate,
      green_usage_rate: data.green_usage_rate,
    };

    try {
      await settingAPI.editColor(editData);
    } catch {}
    setIsEdit(false);
    setLoading(false);
  };

  const getColor = async () => {
    setLoading(true);

    try {
      const res = await settingAPI.getColor();
      if (res.data) {
        setData(res.data);
        reset(res.data);
      }
    } catch {}

    setLoading(false);
  };

  useEffect(() => {
    getColor();
  }, []);

  return (
    <div className={styles.settingWrap}>
      <div className={styles.itemWrap}>
        {data && (
          <>
            <div className={styles.item}>
              <div className={styles.green}></div>
              {renderInput("green_usage_rate", "資金使用率")}
              {renderInput("green_remaining_rate", "資金剩餘率")}
            </div>
            <div className={styles.item}>
              <div className={styles.yellow}></div>
              {renderInput("yellow_usage_rate", "資金使用率")}
              {renderInput("yellow_remaining_rate", "資金剩餘率")}
            </div>
            <div className={styles.item}>
              <div className={styles.red}></div>
              {renderInput("red_usage_rate", "資金使用率")}
              {renderInput("red_remaining_rate", "資金剩餘率")}
            </div>
          </>
        )}
      </div>
      <div className={styles.button}>
        {isEdit ? (
          <>
            <button
              className={styles.cancel}
              onClick={() => {
                setIsEdit(false);
                getColor();
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
