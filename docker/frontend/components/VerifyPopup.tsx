import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { Paperclip } from "lucide-react";

import ShadowBg from "@/components/common/ShadowBg";
import InputField from "@/components/common/InputField";
import { ApplyType } from "@/lib/types/ApplyType";
import styles from "@/styles/components/VerifyPopup.module.scss";

type FormValues = {
  items: ApplyType[];
};

export default function VerifyPopup({
  setIsPopup,
  data,
}: {
  setIsPopup: (boolean: boolean) => void;
  data: ApplyType[];
}) {
  const { register, reset } = useForm<FormValues>({
    defaultValues: { items: data },
  });

  useEffect(() => {
    reset({ items: data });
  }, [data, reset]);

  return (
    <ShadowBg setIsPopup={setIsPopup}>
      <div className={styles.wrap}>
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
                  value={0}
                  {...register(`items.${index}.status` as const)}
                />
                可核銷
              </label>
              <label>
                <input
                  className={styles.disagree}
                  type="radio"
                  value={1}
                  {...register(`items.${index}.status` as const)}
                />
                不可核銷
              </label>
            </div>
          </div>
        ))}
      </div>
    </ShadowBg>
  );
}
