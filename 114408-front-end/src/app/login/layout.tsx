import Image from "next/image";

import styles from "@/styles/app/login/Layout.module.scss";

export default function LoginLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh">
      <body>
        <Image src={"/logo.svg"} height={70} width={70} alt="logo" />
        {children}
        <div className={styles.circles}>
          <div className={styles.bigCircle}></div>
          <div className={styles.meduimCircle}></div>
          <div className={styles.smallCircle}></div>
        </div>
      </body>
    </html>
  );
}
