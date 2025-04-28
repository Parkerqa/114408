"use client";

import { useState } from "react";
import { ImageUp } from "lucide-react";
import { Camera } from "lucide-react";

import FileFrame from "@/components/FileFrame";
import CameraFrame from "@/components/CamaraFrame";
import styles from "@/styles/components/MobileAddPopup.module.scss";

export default function MobileAddPopup({
  setIsAdd,
}: {
  setIsAdd: (state: boolean) => void;
}) {
  const [isFileUpload, setIsFileUpload] = useState<boolean>(false);
  const [isCameraScan, setIsCameraScan] = useState<boolean>(false);

  return (
    <>
      <div
        className={styles.wrap}
        onClick={() => {
          setIsAdd(false);
        }}
      >
        <div
          className={styles.iconWrap}
          onClick={(e) => {
            setIsFileUpload(true);
            e.stopPropagation();
          }}
        >
          <ImageUp size={55} strokeWidth={1.5} className={styles.icon} />
          <p>上傳檔案</p>
        </div>
        <div
          className={styles.iconWrap}
          onClick={(e) => {
            setIsCameraScan(true);
            e.stopPropagation();
          }}
        >
          <Camera size={55} strokeWidth={1.5} className={styles.icon} />
          <p>相機掃描</p>
        </div>
        {isCameraScan && (
          <CameraFrame
            onClick={(e) => {
              e.stopPropagation();
            }}
          />
        )}
        {isFileUpload && (
          <FileFrame
            onClick={(e) => {
              e.stopPropagation();
            }}
          />
        )}
      </div>
    </>
  );
}
