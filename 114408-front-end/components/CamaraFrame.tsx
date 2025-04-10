"use client";

import React, { useRef, useState, useCallback } from "react";
import Webcam from "react-webcam";

import { HtmlDivPropsType } from "@/lib/types/HtmlDivType";
import TitleBox from "@/components/common/TitleBox";

const videoConstraints = {
  facingMode: "environment", // 後鏡頭
};

const CameraWithPermission = () => {
  const webcamRef = useRef(null);
  const [cameraEnabled, setCameraEnabled] = useState(false);
  const [capturedImage, setCapturedImage] = useState<string | null>(null);

  const handleEnableCamera = useCallback(() => {
    setCameraEnabled(true);
    setCapturedImage(null); // 重設已拍攝圖片
  }, []);

  const handleDisableCamera = useCallback(() => {
    setCameraEnabled(false);
  }, []);

  const handleCapture = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = (webcamRef.current as any).getScreenshot();
      setCapturedImage(imageSrc);
    }
  }, [webcamRef]);

  return (
    <div className="relative w-full max-w-md mx-auto flex flex-col items-center space-y-4">
      {cameraEnabled ? (
        <>
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            videoConstraints={videoConstraints}
            className="rounded-xl"
            style={{ width: "100%", height: "auto" }}
          />
          <div className="flex space-x-4 mt-2">
            <button
              onClick={handleCapture}
              className="bg-blue-500 text-white px-4 py-2 rounded-xl hover:bg-blue-600"
            >
              拍照
            </button>
            <button
              onClick={handleDisableCamera}
              className="bg-red-500 text-white px-4 py-2 rounded-xl hover:bg-red-600"
            >
              關閉相機
            </button>
          </div>
        </>
      ) : (
        <button
          onClick={handleEnableCamera}
          className="bg-green-500 text-white px-4 py-2 rounded-xl hover:bg-green-600"
        >
          點我啟用相機
        </button>
      )}

      {capturedImage && (
        <div className="mt-4">
          <p className="text-center">拍攝結果：</p>
          <img
            src={capturedImage}
            alt="Captured"
            className="rounded-xl border border-gray-300"
          />
        </div>
      )}
    </div>
  );
};

export default function CameraFrame({ ...props }: HtmlDivPropsType) {
  return (
    <TitleBox {...props}>
      <CameraWithPermission />
    </TitleBox>
  );
}
