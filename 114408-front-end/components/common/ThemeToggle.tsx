import { Sun } from "lucide-react";
import { Moon } from "lucide-react";

import { useConfig } from "@/lib/context/ConfigContext";
import settingAPI from "@/services/settingAPI";
import styles from "@/styles/components/common/ThemeToggle.module.scss";

export default function ThemeToggle() {
  const { theme, setTheme } = useConfig();
  const isLight = theme === 0 ? true : false;

  const handleToggle = async () => {
    if (isLight) {
      document.body.setAttribute("data-theme", "dark");
      setTheme(1);
      try {
        await settingAPI.editTheme({ theme: 1 });
        localStorage.setItem("theme", "1");
      } catch {}
    } else {
      document.body.setAttribute("data-theme", "light");
      setTheme(0);
      try {
        await settingAPI.editTheme({ theme: 0 });
        localStorage.setItem("theme", "0");
      } catch {}
    }
  };

  return (
    <div className={styles.wrap}>
      <div className={`${isLight && styles.focus} ${styles.iconWrap}`}>
        <Sun size={32} onClick={handleToggle} />
      </div>
      <div className={`${!isLight && styles.focus} ${styles.iconWrap}`}>
        <Moon size={32} strokeWidth={1.6} onClick={handleToggle} />
      </div>
    </div>
  );
}
