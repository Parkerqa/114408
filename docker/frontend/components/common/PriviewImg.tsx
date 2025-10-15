import { SquareX } from "lucide-react";

import styles from "@/styles/components/common/ProviewImg.module.scss";

export default function PriviewImg({
  imgUrl,
  setPriview,
}: {
  imgUrl: string;
  setPriview: (boolean: boolean) => void;
}) {
  return (
    <div className={styles.preview} onClick={() => setPriview(false)}>
      <SquareX size={35} className={styles.close} />
      <img src={imgUrl} alt="預覽圖片" className={styles.previewImage} />
    </div>
  );
}
