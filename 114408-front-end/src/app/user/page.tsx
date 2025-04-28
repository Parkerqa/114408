"use client";

import { useEffect, useState } from "react";
import { Plus } from "lucide-react";
import { Pencil } from "lucide-react";
import { Search } from "lucide-react";
import { useForm } from "react-hook-form";

import MobileAddPopup from "@/components/MobileAddPopup";
import InputField from "@/components/common/InputField";
import { listData } from "@/lib/data/listData";
import MobileListItem from "@/components/common/MobileListItem";
import styles from "@/styles/app/UserPage.module.scss";
import ticketAPI from "@/services/ticketAPI";

export default function User() {
  const [isAdd, setIsAdd] = useState<boolean>(false);
  const [data, setData] = useState();
  const { register, watch } = useForm();

  const keyword = watch("keyword");
  const onSearch = !!keyword;

  const getList = async () => {
    try {
      const res = await ticketAPI.getList();
      console.log(res);
    } catch {}
  };

  getList();
  // useEffect(() => {
  //   getList();
  // }, []);

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
          />
        </div>
        <div className={styles.list}>
          {listData?.map((item, index) => (
            <MobileListItem data={item} key={index} />
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
      {isAdd && <MobileAddPopup setIsAdd={setIsAdd} />}
    </>
  );
}
