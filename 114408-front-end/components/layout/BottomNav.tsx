"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";

import { useConfig } from "@/lib/context/ConfigContext";
import { bottomNavData } from "@/lib/data/bottomNavData";
import styles from "@/styles/components/layout/BottomNav.module.scss";

export default function BottomNav() {
  const { user } = useConfig();
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
            <currentItem.icon size={32} className={styles.focusIcon} />
            <span className={styles.title}>{currentItem.title}</span>
          </>
        )}
      </div>
      <div className={styles.navWrap}>
        {bottomNavData.map((item, index) => {
          const Icon = item.icon;
          return (
            <div className={styles.itemWrap} key={index}>
              <Link href={item.url}>
                <Icon
                  key={index}
                  size={25}
                  className={`
                  ${
                    item.title === title
                      ? styles.focusIcon
                      : styles.notFocusIcon
                  }`}
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
          );
        })}
        {user?.img && (
          <Image
            width={32}
            height={32}
            src={user?.img}
            alt={"user"}
            style={{ borderRadius: "50%", marginBottom: "2%" }}
          />
        )}
      </div>
    </>
  );
}
