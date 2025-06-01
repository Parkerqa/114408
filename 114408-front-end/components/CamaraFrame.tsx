"use client";

import React, { useRef, useState, useCallback } from "react";
import Webcam from "react-webcam";
import { useRouter } from "next/navigation";

import BasePopup from "@/components/common/BasePopup";
import { base64ToFile } from "@/lib/utils/img-format-convert";
import { HtmlDivPropsType } from "@/lib/types/HtmlDivType";
import styles from "@/styles/components/CamaraFrame.module.scss";
import ticketAPI from "@/services/ticketAPI";

const videoConstraints = {
  facingMode: "environment",
  width: { ideal: 250 },
  height: { ideal: 400 },
};

export default function CameraFrame({
  setIsAdd,
  ...props
}: HtmlDivPropsType & { setIsAdd: (state: boolean) => void }) {
  const webcamRef = useRef<Webcam>(null);
  const route = useRouter();
  const [capturedImage, setCapturedImage] = useState<string | null>(null);

  const handleCapture = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        setCapturedImage(imageSrc);
      }
    }
  }, []);

  const handleSubmit = async () => {
    const base64 = capturedImage;
    const file = base64ToFile(base64!);
    if (!file) return;

    const formData = new FormData();
    formData.append("photo", file);

    try {
      await ticketAPI.addBilling(formData);
    } catch {
    } finally {
      setIsAdd(false);
      window.location.reload();
    }
  };

  return (
    <BasePopup {...props} title="相機掃描">
      <div className={styles.wrap}>
        {capturedImage ? (
          <>
            <img
              src={capturedImage}
              style={{ width: "100%", height: "50vh" }}
              alt="發票照片"
            />
            <p className={styles.hint}>* 請務必上繳紙本證明或保存好紙本證明</p>
            <div className={styles.operateBtn}>
              <button
                className={styles.reset}
                onClick={() => {
                  setCapturedImage(null);
                }}
              >
                重拍
              </button>
              <button className={styles.submit} onClick={handleSubmit}>
                確定送出
              </button>
            </div>
          </>
        ) : (
          <>
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              videoConstraints={videoConstraints}
              style={{ width: "100%", height: "auto" }}
            />
            <p className={styles.hint}>* 請務必上繳紙本證明或保存好紙本證明</p>
            <div className={styles.operateBtn}>
              <button className={styles.shutter} onClick={handleCapture}>
                拍照
              </button>
            </div>
          </>
        )}
      </div>
    </BasePopup>
  );
}
