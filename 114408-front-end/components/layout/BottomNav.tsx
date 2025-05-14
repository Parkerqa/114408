"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";

import { bottomNavData } from "@/lib/data/bottomNavData";
import styles from "@/styles/components/layout/BottomNav.module.scss";

export default function BottomNav() {
  const pathname = usePathname();
  const isAuthPage = pathname === "/auth";
  const currentItem = bottomNavData.find((item) =>
    pathname.startsWith(item.url)
  );
  const title = currentItem?.title || "";

  if (isAuthPage) return null;

  return (
    <>
      <div className={styles.header}>
        {currentItem && (
          <>
            <Image
              src={currentItem.icon}
              width={27}
              height={27}
              alt={currentItem.title}
              className={styles.focusIcon}
            />
            <span className={styles.title}>{currentItem.title}</span>
          </>
        )}
      </div>
      <div className={styles.navWrap}>
        {bottomNavData.map((item, index) => (
          <div className={styles.itemWrap} key={index}>
            <Link href={item.url}>
              <Image
                width={25}
                height={25}
                src={item.icon}
                alt={item.title}
                key={index}
                className={`
                  ${item.title === title && styles.focusIcon}`}
              />
            </Link>
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
          width={32}
          height={32}
          src={"/bottomNavIcon/user.png"}
          alt={"user"}
          style={{ borderRadius: "50%", marginBottom: "2%" }}
        />
      </div>
    </>
  );
}
