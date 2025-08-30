import { HtmlDivPropsType } from "@/lib/types/HtmlDivType";
import styles from "@/styles/components/common/ShadowBg.module.scss";

export default function ShadowPopup({
  children,
  setIsPopup,
  ...props
}: HtmlDivPropsType & {
  children: React.ReactNode;
  setIsPopup: (boolean: boolean) => void;
}) {
  return (
    <div
      className={styles.wrap}
      {...props}
      onClick={() => {
        setIsPopup(false);
      }}
    >
      <div
        onClick={(e) => {
          e.stopPropagation();
        }}
      >
        {children}
      </div>
    </div>
  );
}
