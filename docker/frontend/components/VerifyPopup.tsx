import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { Paperclip } from "lucide-react";

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
  const route = useRouter();
  const { register, reset, handleSubmit } = useForm<FormValues>({
    defaultValues: { items: data },
  });

  useEffect(() => {
    reset({ items: data });
  }, [data, reset]);

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
      items: data.items.map(({ ticket_id, state }) => ({
        ticket_id: ticket_id,
        status: state!,
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
          {data.map((item, index) => (
            <div key={index} className={styles.itemWrap}>
              <div className={styles.title}>
                <span className={styles.decoration}></span>
                詳細資訊
              </div>
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
              <hr className={styles.hr} />
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
              <p className={styles.file}>
                <Paperclip />
                報帳附件
                <span className={styles.hint}>*點擊檢視</span>
              </p>
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
            </div>
          ))}
        </div>
        <button type="submit" className={styles.verify}>
          送出核銷
        </button>
      </form>
    </ShadowBg>
  );
}
