"use client";

import { ImageUp } from "lucide-react";
import { Camera } from "lucide-react";

import CameraFrame from "@/components/CamaraFrame";
import styles from "@/styles/components/MobileAddPopup.module.scss";
import { useState } from "react";

export default function MobileAddPopup({
  setIsAdd,
}: {
  setIsAdd: (state: boolean) => void;
}) {
  const [openCamera, setOpenCamera] = useState<boolean>(false);

  return (
    <>
      <div
        className={styles.wrap}
        // onClick={() => {
        //   setIsAdd(false);
        // }}
      >
        <div className={styles.iconWrap}>
          <ImageUp size={55} strokeWidth={1.5} className={styles.icon} />
          <p>上傳檔案</p>
        </div>
        <div className={styles.iconWrap} onClick={()=>{
          setOpenCamera(true);
        }}>
          <Camera size={55} strokeWidth={1.5} className={styles.icon} />
          <p>相機掃描</p>
        </div>
      </div>
      {openCamera && <CameraFrame />}
      
    </>
  );
}
