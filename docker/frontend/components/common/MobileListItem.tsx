"use client";

import { useState } from "react";
import { usePathname } from "next/navigation";
import { ChevronDown, ChevronRight, SquarePen, Trash2 } from "lucide-react";

import DetailItem from "@/components/common/DetailItem";
import { useLoading } from "@/lib/context/LoadingContext";
import { ticketListType } from "@/lib/types/TicketType";
import styles from "@/styles/components/common/MobileListItem.module.scss";
import ticketAPI from "@/services/ticketAPI";

export default function MobileListItem({
  data,
  getList,
}: {
  data: ticketListType;
  getList: () => void;
}) {
  const { setLoading } = useLoading();
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [isDetail, setIsDetail] = useState<boolean>(false);
  const [detail, setDetail] = useState<ticketListType>();
  const pathname = usePathname();
  const isPastRecord = pathname === "/past-records";
  const dataArray = [data];

  const getTicket = async (id: number) => {
    setLoading(true);

    try {
      const res = await ticketAPI.getTicket(id);
      if (res.data) {
        setDetail(res.data);
      }
      setIsDetail(true);
    } catch {
    } finally {
      setLoading(false);
    }
  };

  const deleteTicket = async (id: number) => {
    try {
      await ticketAPI.deleteTicket(id);
    } catch {
    } finally {
      getList();
    }
  };

  return (
    <div
      onClick={() => {
        setIsDetail(false);
      }}
    >
      <div className={isOpen ? styles.detailBox : styles.partialBox}>
        {isOpen ? (
          <ChevronDown
            size={20}
            strokeWidth={3}
            className={styles.toggle}
            onClick={() => setIsOpen(false)}
          />
        ) : (
          <ChevronRight
            size={20}
            strokeWidth={3}
            className={styles.toggle}
            onClick={() => setIsOpen(true)}
          />
        )}
        <div className={styles.detail}>
          {isOpen ? (
            dataArray.map((item, index) => (
              <div className={styles.item} key={index}>
                <div className={styles.info}>
                  <span>時間</span>
                  <p>{item.time}</p>
                </div>
                <div className={styles.info}>
                  <span>種類</span>
                  <p>{item.type}</p>
                </div>
                <div className={styles.details}>
                  {item.Details &&
                    item.Details.map((item, index) => (
                      <div key={index}>
                        <div className={styles.info}>
                          <span>細項 {index + 1}</span>
                          <p>{item.title}</p>
                        </div>
                        <div className={styles.info}>
                          <span>金額 {index + 1}</span>
                          <p>{item.money}</p>
                        </div>
                      </div>
                    ))}
                </div>
                <div className={styles.info}>
                  <span>編號</span>
                  <p>{item.invoice_number}</p>
                </div>
                <div className={styles.info}>
                  <span>總額</span>
                  <p>{item.total_money}</p>
                </div>
                <div className={styles.info}>
                  <span>狀態</span>
                  <p>{item.status}</p>
                </div>
                {!isPastRecord && (
                  <div className={styles.info}>
                    <span>操作</span>
                    <div>
                      <SquarePen
                        size={18}
                        className={styles.edit}
                        onClick={() => {
                          getTicket(data.id);
                        }}
                      />
                      <Trash2
                        size={18}
                        className={styles.delete}
                        onClick={() => {
                          deleteTicket(data.id);
                        }}
                      />
                    </div>
                  </div>
                )}
              </div>
            ))
          ) : (
            <div className={styles.item}>
              <p style={{ whiteSpace: "nowrap" }}>{data.time}</p>
              <p className={styles.partial}>
                {dataArray?.[0]?.Details?.[0]?.title ?? "系統辨識中"}{" "}
              </p>
            </div>
          )}
        </div>
      </div>
      {isDetail && detail && (
        <DetailItem data={detail} setIsDetail={setIsDetail} />
      )}
    </div>
  );
}
