"use client";

import { Pencil } from "lucide-react";
import { Search } from "lucide-react";
import { useForm } from "react-hook-form";

import MobileAddPopup from "@/components/MobileAddPopup";
import InputField from "@/components/common/InputField";
import { liseData } from "@/lib/data/listData";
import MobileListItem from "@/components/common/MobileListItem";
import styles from "@/styles/app/UserPage.module.scss";

export default function User() {
  const { register, watch } = useForm();

  const keyword = watch("keyword");
  const onSearch = !!keyword;

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
          {liseData.map((item, index) => (
            <MobileListItem data={item} key={index} />
          ))}
        </div>
      </div>
      <MobileAddPopup />
    </>
  );
}
