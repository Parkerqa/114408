"use client";

import { useEffect, useState } from "react";
import { Plus, Pencil, Search } from "lucide-react";
import { useForm } from "react-hook-form";

import { useLoading } from "@/lib/context/LoadingContext";
import MobileAddPopup from "@/components/MobileAddPopup";
import MobileListItem from "@/components/common/MobileListItem";
import InputField from "@/components/common/InputField";
import { ticketListType } from "@/lib/types/TicketType";
import ticketAPI from "@/services/ticketAPI";
import styles from "@/styles/app/UserPage.module.scss";

export default function User() {
  const { setLoading } = useLoading();
  const [isAdd, setIsAdd] = useState<boolean>(false);
  const [data, setData] = useState<ticketListType[]>([]);
  const { register, watch } = useForm();

  const keyword = watch("keyword");
  const onSearch = !!keyword;

  const getList = async () => {
    setLoading(true);

    try {
      const res = await ticketAPI.getList(0);
      if (res.data) {
        setData(res.data);
      }
    } catch {}
    setLoading(false);
  };

  const search = async () => {
    try {
      const res = await ticketAPI.searchTicket({ status: 2, q: keyword });
      if (res.data) {
        setData(res.data);
      }
    } catch {}
  };

  useEffect(() => {
    getList();
  }, []);

  return (
    <>
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
            onClick={search}
          />
        </div>
        <div className={styles.list}>
          {data?.map((item, index) => (
            <MobileListItem data={item} key={index} getList={getList} />
          ))}
        </div>
      </div>
      <Plus
        onClick={() => {
          setIsAdd(true);
        }}
        className={styles.addBtn}
        strokeWidth={4}
      />
      {isAdd && <MobileAddPopup setIsAdd={setIsAdd} getList={getList} />}
    </>
  );
}
