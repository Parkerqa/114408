"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";

import { useConfig } from "@/lib/context/ConfigContext";
import ThemeToggle from "@/components/common/ThemeToggle";
import { navData } from "@/lib/data/adminNavData";
import styles from "@/styles/components/layout/SideBar.module.scss";

const navItem = (
  icon: any,
  title: string,
  url: string,
  key: number,
  currentItem: any
) => {
  const current = currentItem.url === url ? true : false;
  return (
    <Link key={key} href={url} className={styles.navItem}>
      {current && <div className={styles.point} />}
      <div className={`${styles.item} ${current && styles.focus}`}>
        {icon}
        <p>{title}</p>
      </div>
    </Link>
  );
};

export default function Sidebar() {
  const pathname = usePathname();
  const { user } = useConfig();
  const currentItem = navData.find((item) => pathname.startsWith(item.url));

  return (
    <div className={styles.wrap}>
      <div className={styles.userInfo}>
        {user?.img && (
          <Image
            alt="user"
            width={110}
            height={110}
            src={user?.img}
            className={styles.user}
          />
        )}
        {user?.username}
      </div>

      {navData.map((item, index) =>
        navItem(<item.icon />, item.title, item.url, index, currentItem)
      )}
      <ThemeToggle />
    </div>
  );
}
