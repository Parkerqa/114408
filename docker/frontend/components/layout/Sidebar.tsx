"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { PencilLine } from "lucide-react";
import { useDropzone } from "react-dropzone";
import { usePathname } from "next/navigation";

import { useConfig } from "@/lib/context/ConfigContext";
import ThemeToggle from "@/components/common/ThemeToggle";
import { navData } from "@/lib/data/adminNavData";
import userAPI from "@/services/userAPI";
import styles from "@/styles/components/layout/SideBar.module.scss";

const navItem = (
  icon: any,
  title: string,
  url: string,
  key: number,
  currentUrl?: string
) => {
  const current = currentUrl === url;
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
  const [newImg, setNewImg] = useState<string | null>(null);
  const [isEdit, setIsEdit] = useState<boolean>();
  const pathname = usePathname();
  const { user, fetchUser } = useConfig();
  const currentItem = navData.find((item) => pathname.startsWith(item.url));
  const currentUrl = currentItem?.url;

  const { getRootProps, getInputProps, acceptedFiles } = useDropzone({
    accept: { "image/*": [] },
    multiple: false,
  });

  const edit = async () => {
    const file = acceptedFiles[0];
    const formData = new FormData();

    if (user) {
      formData.append("email", user.email);
      formData.append("username", user.username);
    }

    if (file) {
      formData.append("avatar", file);
    }

    try {
      await userAPI.editUser(formData);
      fetchUser();
    } catch {
    } finally {
      setIsEdit(false);
    }
  };

  useEffect(() => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      const objectUrl = URL.createObjectURL(file);
      setNewImg(objectUrl);

      return () => URL.revokeObjectURL(objectUrl);
    }
  }, [acceptedFiles]);

  useEffect(() => {
    if (newImg) {
      edit();
    }
  }, [newImg]);

  return (
    <div className={styles.wrap}>
      <div className={styles.userInfo}>
        <div
          className={styles.userWrap}
          onMouseEnter={() => setIsEdit(true)}
          onMouseLeave={() => setIsEdit(false)}
          {...(isEdit && getRootProps())}
        >
          {isEdit && <input {...getInputProps()} />}
          {(newImg || user?.img) && (
            <Image
              alt="頭貼"
              width={110}
              height={110}
              unoptimized
              src={newImg || user?.img!}
              style={{ borderRadius: "50%" }}
              className={styles.user}
            />
          )}
          {isEdit && (
            <div className={styles.overlay}>
              <PencilLine size={27} color="#fff" />
            </div>
          )}
        </div>
        {user?.username}
      </div>
      {navData.map((item, index) =>
        navItem(<item.icon />, item.title, item.url, index, currentUrl)
      )}
      <ThemeToggle />
    </div>
  );
}
