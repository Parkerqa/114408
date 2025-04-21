"use client";

import Image from "next/image";
import { usePathname } from "next/navigation";

import { bottomNavData } from "@/lib/data/bottomNavData";
import styles from "@/styles/components/layout/BottomNav.module.scss";

export default function BottomNav({ title }: { title: string }) {
  const pathname = usePathname();
  const isAuthPage = pathname === "/login" || pathname === "/signup";
  const currentPage = bottomNavData.find((item) => item.title === title);

  if (isAuthPage) return null;

  return (
    <>
      <div className={styles.header}>
        {currentPage && (
          <>
            <Image
              src={currentPage.icon}
              width={27}
              height={27}
              alt={currentPage.title}
            />
            <span className={styles.title}>{currentPage.title}</span>
          </>
        )}
      </div>
      <div className={styles.navWrap}>
        {bottomNavData.map((item, index) => (
          <div className={styles.itemWrap} key={index}>
            <Image
              width={25}
              height={25}
              src={item.icon}
              alt={item.title}
              key={index}
            />
            {
              <div
                className={`${styles.mark} ${
                  title === item.title && styles.focus
                }`}
              />
            }
          </div>
        ))}
        <Image
          width={30}
          height={30}
          src={"/bottomNavIcon/user.png"}
          alt={"user"}
          style={{ borderRadius: "50%" }}
        />
      </div>
    </>
  );
}
