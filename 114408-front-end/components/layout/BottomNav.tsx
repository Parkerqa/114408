import { bottomNavData } from "@/lib/data/bottomNavData";
import styles from "@/styles/components/layout/BottomNav.module.scss";
import Image from "next/image";

export default function BottomNav() {
  return (
    <div className={styles.navWrap}>
      {bottomNavData.map((item, index) => (
        <Image
          width={25}
          height={25}
          src={item.icon}
          alt={item.title}
          key={index}
        />
      ))}
      <Image
        width={30}
        height={30}
        src={"/bottomNavIcon/user.png"}
        alt={"user"}
        style={{ borderRadius: "50%" }}
      />
    </div>
  );
}
