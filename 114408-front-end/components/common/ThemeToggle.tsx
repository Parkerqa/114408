import { Sun } from "lucide-react";
import { Moon } from "lucide-react";

import { useConfig } from "@/lib/context/ConfigContext";
import styles from "@/styles/components/common/ThemeToggle.module.scss";

export default function ThemeToggle() {
  const { theme, setTheme } = useConfig();
  const isLight = theme === 0 ? true : false;

  const handleToggle = () => {
    if (isLight) {
      document.body.setAttribute("data-theme", "dark");
      setTheme(1);
    } else {
      document.body.setAttribute("data-theme", "light");
      setTheme(0);
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
