import { useState } from "react";
import { ChevronLeft } from "lucide-react";
import { ChevronDown } from "lucide-react";

import styles from "@/styles/components/common/MoreInfoBar.module.scss";

export default function MoreInfoBar({
  title,
  context,
}: {
  title: string;
  context: React.ReactNode;
}) {
  const [isOpen, setIsOpen] = useState<boolean>(false);

  return (
    <>
      <div
        onClick={() => {
          setIsOpen(isOpen ? false : true);
        }}
        className={styles.wrap}
      >
        <p>{title}</p>
        {isOpen ? <ChevronDown /> : <ChevronLeft />}
      </div>
      {isOpen && <div className={styles.contextWrap}>{context}</div>}
    </>
  );
}
