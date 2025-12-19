"use client";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { Paperclip } from "lucide-react";
import { PencilLine } from "lucide-react";

import PriviewImg from "@/components/common/PriviewImg";
import ShadowBg from "@/components/common/ShadowBg";
import InputField from "@/components/common/InputField";
import {
  auditTicket,
  multiTicketDetail,
  pendingTicket,
} from "@/lib/types/TicketType";
import ticketAPI from "@/services/ticketAPI";
import styles from "@/styles/components/VerifyPopup.module.scss";

type FormValues = {
  items: multiTicketDetail[];
};

export default function VerifyPopup({
  setIsPopup,
  data,
  setPendingTable,
}: {
  setIsPopup: (boolean: boolean) => void;
  setPendingTable: (data: pendingTicket[]) => void;
  data: multiTicketDetail[];
}) {
  const [priview, setPriview] = useState<boolean>(false);
  const { register, reset, handleSubmit, watch } = useForm<FormValues>({
    defaultValues: { items: data },
  });

  const watchedItems = watch("items");

  useEffect(() => {
    reset({ items: data });
  }, [data, reset]);

  useEffect(() => {}, []);

  const getData = async () => {
    try {
      const res = await ticketAPI.getPending();
      if (res.data) {
        setPendingTable(res.data);
      }
    } catch {}
  };

  const onSubmit = async (data: FormValues) => {
    const payload: auditTicket = {
      items: data.items.map(({ ticket_id, state, reason }) => ({
        ticket_id: ticket_id,
        status: state!,
        reject_reason: reason,
      })),
    };

    try {
      await ticketAPI.auditTicket(payload);
    } catch {
    } finally {
      setIsPopup(false);
      getData();
    }
  };

  return (
    <ShadowBg setIsPopup={setIsPopup}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div
          className={styles.wrap}
          style={{ marginLeft: `${(data.length - 1) * 20}vw` }}
        >
          {data.map((item, index) => {
            const currentState = watchedItems?.[index]?.state;
            const isRejected = currentState == 4;

            return (
              <div key={index} className={styles.itemWrap}>
                <div className={styles.title}>
                  <span className={styles.decoration}></span>
                  詳細資訊
                </div>
                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "10px",
                  }}
                >
                  <InputField
                    type="text"
                    readonly={true}
                    label="時間"
                    style={{ width: "350px" }}
                    register={register(`items.${index}.time` as const)}
                  />
                  <InputField
                    type="text"
                    readonly={true}
                    label="種類"
                    style={{ width: "350px" }}
                    register={register(`items.${index}.type` as const)}
                  />
                  <InputField
                    type="text"
                    readonly={true}
                    label="申請人"
                    style={{ width: "350px" }}
                    register={register(`items.${index}.applicant` as const)}
                  />
                  <div className={styles.file}>
                    <button
                      type="button"
                      onClick={() => {
                        setPriview(true);
                      }}
                    >
                      <Paperclip />
                      報帳附件
                    </button>
                    <span className={styles.hint}>*點擊檢視</span>
                  </div>
                  <div className={styles.status}>
                    <label>
                      <input
                        className={styles.agree}
                        type="radio"
                        value={3}
                        {...register(`items.${index}.state` as const)}
                      />
                      可核銷
                    </label>
                    <label>
                      <input
                        className={styles.disagree}
                        type="radio"
                        value={4}
                        {...register(`items.${index}.state` as const)}
                      />
                      不可核銷
                    </label>
                  </div>
                  {isRejected && (
                    <InputField
                      type="text"
                      label="不可核銷原因"
                      style={{ width: "350px" }}
                      register={register(`items.${index}.reason` as const)}
                      showIcon
                      icon={<PencilLine size={20} />}
                      iconRight
                    />
                  )}
                  {priview && (
                    <PriviewImg imgUrl={item.img_url} setPriview={setPriview} />
                  )}
                </div>
                <hr className={styles.hr} />
                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "10px",
                  }}
                >
                  {item.Details.map((d, j) => (
                    <div
                      key={j}
                      style={{
                        display: "flex",
                        flexDirection: "column",
                        gap: "10px",
                      }}
                    >
                      <InputField
                        type="text"
                        readonly={true}
                        label={`細項${j + 1}`}
                        style={{ width: "350px" }}
                        register={register(
                          `items.${index}.Details.${j}.title` as const
                        )}
                      />
                      <InputField
                        type="number"
                        readonly={true}
                        label={`細項金額${j + 1}`}
                        style={{ width: "350px" }}
                        register={register(
                          `items.${index}.Details.${j}.money` as const,
                          {
                            valueAsNumber: true,
                          }
                        )}
                      />
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
        <button type="submit" className={styles.verify}>
          送出核銷
        </button>
      </form>
    </ShadowBg>
  );
}
