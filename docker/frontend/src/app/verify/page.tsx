"use client";

import { useEffect, useState } from "react";
import { Search, ListChecks } from "lucide-react";
import { useForm, Controller } from "react-hook-form";

import VerifyPopup from "@/components/VerifyPopup";
import InputField from "@/components/common/InputField";
import SelectField from "@/components/common/SelectField";
import PendingTable from "@/components/PendingTable";
import ApprovedTable from "@/components/ApprovedTable";
import { pendingTicket } from "@/lib/types/TicketType";
import ticketAPI from "@/services/ticketAPI";
import styles from "@/styles/app/VerifyPage.module.scss";

const optionData = [
  { value: "無" },
  { value: "傳統發票" },
  { value: "電子發票" },
  { value: "二聯發票" },
  { value: "三聯發票" },
  { value: "收據" },
];

type FormValues = {
  date: string;
  type: string;
  keywords: string;
};

export default function Verify() {
  const [isPast, setIsPast] = useState<boolean>(false);
  const [isVerify, setIsVerify] = useState<boolean>(false);
  const [pendingTable, setPendingTable] = useState<pendingTicket[]>([]);
  const [verifyData, setVerifyData] = useState();

  const { register, control, handleSubmit } = useForm<FormValues>({
    defaultValues: {
      date: "",
      type: "",
      keywords: "",
    },
  });

  const search = async (value: FormValues) => {
    const q = value.keywords || undefined;
    const class_info_id = value.type || undefined;
    const date = value.date || undefined;

    try {
      const res = await ticketAPI.searchTicket({ q, class_info_id, date });
      if (res.data) {
        setPendingTable(res.data);
      }
    } catch {}
  };

  useEffect(() => {
    const getData = async () => {
      try {
        const res = await ticketAPI.getPending();
        if (res.data) {
          setPendingTable(res.data);
        }
      } catch {}
    };

    getData();
  }, []);

  return (
    <>
      <div className={styles.wrap}>
        <div className={styles.title}>
          <p
            className={`${!isPast ? styles.focus : styles.normal}`}
            onClick={() => {
              setIsPast(false);
            }}
          >
            待核銷報帳
          </p>
          <span>|</span>
          <p
            className={`${isPast ? styles.focus : styles.normal}`}
            onClick={() => {
              setIsPast(true);
            }}
          >
            過去核銷紀錄
          </p>
        </div>
        <div className={styles.searchBar}>
          <p>報帳申請查詢</p>
          <div className={styles.operateBar}>
            <form onSubmit={handleSubmit(search)}>
              <div className={styles.searchItem}>
                <InputField register={register("date")} type="date" />
                <Controller
                  control={control}
                  name={"type"}
                  render={({ field }) => (
                    <SelectField
                      style={{ width: "200px" }}
                      title="報帳種類"
                      value={field.value}
                      onChange={field.onChange}
                      optionData={optionData}
                    />
                  )}
                />
                <InputField
                  register={register("keywords")}
                  type="text"
                  hint="關鍵字查詢"
                />
                <button type="submit" className={styles.searchBtn}>
                  <Search strokeWidth={3} />
                </button>
              </div>
            </form>
            {!isPast && (
              <button
                className={styles.verifyBtn}
                onClick={() => {
                  setIsVerify(true);
                }}
              >
                <ListChecks />
                <p>批量核銷</p>
              </button>
            )}
          </div>
        </div>
        {isPast ? (
          <ApprovedTable />
        ) : (
          <PendingTable
            setVerifyData={setVerifyData}
            pendingData={pendingTable}
          />
        )}
      </div>
      {isVerify && verifyData && (
        <VerifyPopup
          setIsPopup={setIsVerify}
          data={verifyData}
          setPendingTable={setPendingTable}
        />
      )}
    </>
  );
}
