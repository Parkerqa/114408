"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useDropzone } from "react-dropzone";
import { FileText, Image, Eye, SquareX } from "lucide-react";

import BasePopup from "@/components/common/BasePopup";
import { HtmlDivPropsType } from "@/lib/types/HtmlDivType";
import styles from "@/styles/components/FileFrame.module.scss";
import ticketAPI from "@/services/ticketAPI";

export default function FileFrame({
  setIsAdd,
  ...props
}: HtmlDivPropsType & { setIsAdd: (state: boolean) => void }) {
  const route = useRouter();
  const [preview, setPreview] = useState<string | null>(null);
  const { getRootProps, getInputProps, acceptedFiles } = useDropzone({
    accept: { "image/*": [] },
    multiple: false,
  });

  const handlePreview = (file: File) => {
    const url = URL.createObjectURL(file);
    setPreview(url);
  };

  const handleSubmit = async () => {
    const file = acceptedFiles[0];
    const formdata = new FormData();
    formdata.append("photo", file);

    try {
      await ticketAPI.addBilling(formdata);
    } catch {
    } finally {
      setIsAdd(false);
      route.replace("/user");
    }
  };

  return (
    <BasePopup {...props} title="檔案上傳">
      <div {...getRootProps()} className={styles.uploadWrap}>
        <FileText size={55} strokeWidth={1.25} />
        <input {...getInputProps()} className={styles.upload} />
        {acceptedFiles.length > 0 ? (
          <p>點擊此處即可重新上傳圖片</p>
        ) : (
          <p>點擊或拖曳圖片到這裡上傳</p>
        )}
      </div>
      {acceptedFiles.length > 0 && (
        <div className={styles.detail}>
          {acceptedFiles.map((item, index) => (
            <div className={styles.item} key={index}>
              <p style={{ fontWeight: "bold", fontSize: "20px" }}>
                {index + 1}.
              </p>
              <Image />
              <p>{item.name}</p>
              <Eye
                style={{ marginLeft: "auto" }}
                onClick={() => handlePreview(item)}
              />
            </div>
          ))}
        </div>
      )}
      {preview && (
        <div className={styles.preview} onClick={() => setPreview(null)}>
          <SquareX size={35} className={styles.close} />
          <img src={preview} alt="預覽圖片" className={styles.previewImage} />
        </div>
      )}
      <p className={styles.hint}>* 請務必上繳紙本證明或保存好紙本證明</p>
      <button className={styles.submit} onClick={handleSubmit}>
        送出
      </button>
    </BasePopup>
  );
}
