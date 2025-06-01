"use client";

import { useState } from "react";
import { usePathname } from "next/navigation";
import { ChevronDown } from "lucide-react";
import { ChevronRight } from "lucide-react";
import { SquarePen } from "lucide-react";
import { Trash2 } from "lucide-react";

import DetailItem from "@/components/common/DetailItem";
import { ticketListType } from "@/lib/types/TicketType";
import styles from "@/styles/components/common/MobileListItem.module.scss";
import ticketAPI from "@/services/ticketAPI";

export default function MobileListItem({ data }: { data: ticketListType }) {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [isDetail, setIsDetail] = useState<boolean>(false);
  const [detail, setDetail] = useState<ticketListType>({
    id: 1,
    time: "123",
    type: "string",
    title: "string",
    number: "string",
    money: 123,
    state: "string",
  });
  const pathname = usePathname();
  const isPastRecord = pathname === "/past-records";
  const title = [
    "時間",
    "種類",
    "標題",
    "編號",
    "金額",
    "狀態",
    ...(isPastRecord ? [] : ["操作"]),
  ];
  const values = [
    data.time,
    data.type,
    data.title,
    data.number,
    data.money,
    data.state,
  ];

  const getBilling = async (id: number) => {
    try {
      const res = await ticketAPI.getBilling(id);
      if (res.data) {
        setDetail(res.data);
      }
      setIsDetail(true);
    } catch {}
  };

  const deleteBilling = async (id: number) => {
    try {
      await ticketAPI.deleteBilling(id);
    } catch {
    } finally {
      window.location.reload();
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
            title.map((item, index) => (
              <div className={styles.item} key={index}>
                <p>{item}</p>
                {item === "操作" ? (
                  <div>
                    <SquarePen
                      size={18}
                      className={styles.edit}
                      onClick={() => {
                        getBilling(data.id);
                      }}
                    />
                    <Trash2
                      size={18}
                      className={styles.delete}
                      onClick={() => {
                        deleteBilling(data.id);
                      }}
                    />
                  </div>
                ) : (
                  <p className={styles.info}>{values[index]}</p>
                )}
              </div>
            ))
          ) : (
            <div className={styles.item}>
              <p>{data.time}</p>
              <p className={styles.partial}>{data.title}</p>
            </div>
          )}
        </div>
      </div>
      {isDetail && <DetailItem data={detail} setIsDetail={setIsDetail} />}
    </div>
  );
}
