import { useEffect } from "react";
import { useForm } from "react-hook-form";

import BasePopup from "@/components/common/BasePopup";
import InputField from "@/components/common/InputField";
import { ticketListType } from "@/lib/types/TicketType";
import styles from "@/styles/components/common/DtailItem.module.scss";

export default function DetailItem({
  data,
  setIsDetail,
  ...props
}: {
  data: ticketListType;
  setIsDetail: (state: boolean) => void;
}) {
  const { register, handleSubmit, reset } = useForm<ticketListType>();

  useEffect(() => {
    if (data) {
      reset({
        time: data.time,
        type: data.type,
        title: data.title,
        number: data.number,
        money: data.money,
        state: data.state,
      });
    }
  }, [data]);

  const onSubmit = async () => {};

  return (
    <BasePopup title="修改報帳細項" {...props}>
      <div>
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className={styles.inputWrap}>
            <InputField
              style={{ width: 250 }}
              label="時間"
              type="text"
              register={register("time")}
            />
            <InputField
              style={{ width: 250 }}
              label="種類"
              type="text"
              register={register("type")}
            />
            <InputField
              style={{ width: 250 }}
              label="標題"
              type="text"
              register={register("title")}
            />
            <InputField
              style={{ width: 250 }}
              label="編號"
              type="text"
              register={register("number")}
            />
            <InputField
              style={{ width: 250 }}
              label="金額"
              type="number"
              register={register("money")}
            />
            <InputField
              style={{ width: 250 }}
              label="狀態"
              type="text"
              register={register("state")}
            />
          </div>
          <div className={styles.operateBtn}>
            <button
              type="submit"
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
