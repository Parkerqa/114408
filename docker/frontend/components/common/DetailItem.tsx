import { useEffect, useState } from "react";
import { useFieldArray, useForm, Controller, useWatch } from "react-hook-form";

import BasePopup from "@/components/common/BasePopup";
import InputField from "@/components/common/InputField";
import SelectField from "@/components/common/SelectField";
import { useLoading } from "@/lib/context/LoadingContext";
import { ticketListType } from "@/lib/types/TicketType";
import ticketAPI from "@/services/ticketAPI";
import styles from "@/styles/components/common/DetailItem.module.scss";

const typeMap: Record<string, number> = {
  系統辨識失敗: 0,
  等待系統辨識: 1,
  傳統發票: 2,
  電子發票: 3,
  二聯發票: 4,
  三聯發票: 5,
  收據: 6,
};

type editType = {
  id: number;
  Details: {
    td_id: number;
    title: string;
    money: number;
  }[];
  type: string;
  invoice_number: string;
  total_money: number;
};

export default function DetailItem({
  data,
  setIsDetail,
  ...props
}: {
  data: ticketListType;
  setIsDetail: (state: boolean) => void;
}) {
  const { setLoading } = useLoading();
  const { register, handleSubmit, reset, control, setValue } =
    useForm<editType>({
      defaultValues: {
        id: 0,
        Details: [{ td_id: 1, title: "", money: 0 }],
        type: "",
        invoice_number: "",
        total_money: 0,
      },
    });
  const { fields, append, remove } = useFieldArray({
    control,
    name: "Details",
  });
  const details = useWatch({ control, name: "Details" });

  useEffect(() => {
    if (data) {
      reset({
        id: data.id,
        Details: data.Details?.length
          ? data.Details
          : [{ td_id: 1, title: "", money: 0 }],
        type: data.type,
        invoice_number: data.invoice_number ?? "",
        total_money: data.total_money,
      });
    }
  }, [data]);

  useEffect(() => {
    const total =
      (details ?? []).reduce((sum, d) => sum + (Number(d?.money) || 0), 0) || 0;
    setValue("total_money", total, { shouldValidate: true, shouldDirty: true });
  }, [details, setValue]);

  const onSubmit = async (data: editType) => {
    setLoading(true);
    const payload = {
      type: typeMap[data.type],
      invoice_number: (data.invoice_number ?? "").trim(),
      total_money: data.total_money || 0,
      Details: (data.Details ?? []).map((d) => ({
        td_id: d.td_id || 0,
        title: (d.title ?? "").trim(),
        money: Number(d.money) || 0,
      })),
    };

    try {
      await ticketAPI.editTicket(data.id, payload);
    } catch {
    } finally {
      setIsDetail(false);
      setLoading(false);
    }
  };

  return (
    <BasePopup title="修改報帳細項" {...props}>
      <div>
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className={styles.inputWrap}>
            <div className={styles.state}>
              <p>
                <span>時間：</span>
                {data.time}
              </p>
              <p>|</p>
              <p>
                <span>狀態：</span>
                {data.status}
              </p>
            </div>
            <Controller
              control={control}
              name={"type"}
              rules={{ required: true }}
              render={({ field }) => (
                <SelectField
                  style={{ width: 250 }}
                  title="種類"
                  value={field.value}
                  onChange={field.onChange}
                  optionData={[
                    { value: "系統辨識失敗" },
                    { value: "等待系統辨識" },
                    { value: "傳統發票" },
                    { value: "電子發票" },
                    { value: "二聯發票" },
                    { value: "三聯發票" },
                    { value: "收據" },
                  ]}
                />
              )}
            />
            <InputField
              style={{ width: 250 }}
              label="編號"
              type="text"
              register={register("invoice_number")}
            />
            <div className={styles.detailList}>
              {fields.map((field, index) => (
                <div key={field.id} className={styles.detailRow}>
                  <input
                    type="hidden"
                    {...register(`Details.${index}.td_id` as const, {
                      valueAsNumber: true,
                    })}
                  />
                  <InputField
                    style={{ width: 130 }}
                    label={`細項#${index + 1}`}
                    type="text"
                    register={register(`Details.${index}.title` as const)}
                  />
                  <InputField
                    style={{ width: 100 }}
                    label={`金額#${index + 1}`}
                    type="number"
                    register={register(`Details.${index}.money` as const, {
                      valueAsNumber: true,
                      validate: (v) => (v ?? 0) >= 0 || "金額需為非負數",
                    })}
                  />
                </div>
              ))}
            </div>
            <InputField
              style={{ width: 250 }}
              label="總金額"
              type="number"
              register={register("total_money")}
              readonly={true}
            />
          </div>
          <div className={styles.operateBtn}>
            <button
              type="button"
              className={styles.close}
              onClick={() => {
                setIsDetail(false);
              }}
            >
              取消
            </button>
            <button type="submit" className={styles.submit}>
              確定修改
            </button>
          </div>
        </form>
      </div>
    </BasePopup>
  );
}
