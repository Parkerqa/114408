"use client";

import React, { useRef, useState, useCallback } from "react";
import Webcam from "react-webcam";

import BasePopup from "@/components/common/BasePopup";
import { HtmlDivPropsType } from "@/lib/types/HtmlDivType";
import styles from "@/styles/components/CamaraFrame.module.scss";

const videoConstraints = {
  facingMode: "environment",
  width: { ideal: 250 },
  height: { ideal: 400 },
};

export default function CameraFrame({ ...props }: HtmlDivPropsType) {
  const webcamRef = useRef<Webcam>(null);
  const [cameraEnabled, setCameraEnabled] = useState(false);
  const [capturedImage, setCapturedImage] = useState<string | null>(null);

  const handleEnableCamera = useCallback(() => {
    setCameraEnabled(true);
    setCapturedImage(null);
  }, []);

  const handleDisableCamera = useCallback(() => {
    setCameraEnabled(false);
  }, []);

  const handleCapture = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        setCapturedImage(imageSrc);
      }
    }
  }, []);

  return (
    <BasePopup {...props} title="相機掃描">
      <>
        {cameraEnabled ? (
          <div className={styles.webWrap}>
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              videoConstraints={videoConstraints}
              style={{ width: "100%", height: "auto" }}
            />
            <div className={styles.operateBtn}>
              <button className={styles.close} onClick={handleDisableCamera}>
                關閉相機
              </button>
              <button className={styles.shutter} onClick={handleCapture}>
                拍照
              </button>
            </div>
          </div>
        ) : (
          <div>
            <button onClick={handleEnableCamera} className={styles.enable}>
              點我啟用相機
            </button>
          </div>
        )}
      </>
    </BasePopup>
  );
}
