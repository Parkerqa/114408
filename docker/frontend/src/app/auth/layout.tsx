import Image from "next/image";

import styles from "@/styles/app/auth/Layout.module.scss";

export default function LoginLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <section className={styles.wrap}>
      <Image
        src={"/logo.svg"}
        height={80}
        width={80}
        alt="logo"
        className={styles.logo}
        priority
      />
      {children}
    </section>
  );
}
