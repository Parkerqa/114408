"use client";

import React, { useRef, useState, useCallback } from "react";
import Webcam from "react-webcam";

import { HtmlDivPropsType } from "@/lib/types/HtmlDivType";
import BasePopup from "@/components/common/BasePopup";

const videoConstraints = {
  facingMode: "environment",
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
      <div>
        {cameraEnabled ? (
          <>
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              videoConstraints={videoConstraints}
              style={{ width: "100%", height: "auto" }}
            />
            <div>
              <button onClick={handleCapture}>拍照</button>
              <button onClick={handleDisableCamera}>關閉相機</button>
            </div>
          </>
        ) : (
          <div>
            <button onClick={handleEnableCamera}>點我啟用相機</button>
          </div>
        )}
      </div>
    </BasePopup>
  );
}
