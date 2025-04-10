"use client";

import React, { useRef } from "react";
import Webcam from "react-webcam";
import CameraWithScanner from "./CameraWithScanner";
import FileFrame from "./FileFrame"

import styles from "@/styles/components/CamaraFrame.module.scss";

export default function CameraFrame() {
  const videoConstraints = {
    facingMode: "environment",
  };

  const webcamRef = useRef(null);

  return (
    <>
      <div className={styles.wrap}>
        <div className={styles.operation}>
          <FileFrame />
        </div>
      </div>
    </>
  );
}
