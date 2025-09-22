"use client";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { Pencil } from "lucide-react";
import { Search } from "lucide-react";

import InputField from "@/components/common/InputField";
import MobileListItem from "@/components/common/MobileListItem";
import { ticketListType } from "@/lib/types/TicketType";
import ticketAPI from "@/services/ticketAPI";
import styles from "@/styles/app/PastPage.module.scss";

export default function PastRecords() {
  const [data, setData] = useState<ticketListType[]>([]);
  const { register, watch } = useForm();

  const keyword = watch("keyword");
  const onSearch = !!keyword;

  const getList = async () => {
    try {
      const res = await ticketAPI.getList(1);
      if (res.data) {
        setData(res.data);
      }
    } catch {}
  };

  useEffect(() => {
    getList();
  }, []);

  return (
    <div className={styles.wrap}>
      <div className={styles.searchBar}>
        <InputField
          style={{ width: 250 }}
          type="text"
          icon={<Pencil size={20} />}
          register={register("keyword")}
        />
        <Search
          className={`${styles.searchBtn} ${onSearch ? styles.onSearch : ""}`}
        />
      </div>
      <div className={styles.list}>
        {data?.map((item, index) => (
          <MobileListItem data={item} key={index} getList={getList} />
        ))}
      </div>
    </div>
  );
}
