import { HtmlDivPropsType } from "@/lib/types/HtmlDivType";
import styles from "@/styles/components/common/ShadowPopup.module.scss";

export default function ShadowPopup({
  children,
  setIsPopup,
  title,
  ...props
}: HtmlDivPropsType & {
  children: React.ReactNode;
  setIsPopup: (boolean: boolean) => void;
  title?: string;
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
        className={styles.childrenWrap}
        onClick={(e) => {
          e.stopPropagation();
        }}
      >
        {title && (
          <div className={styles.title}>
            <span className={styles.decoration}></span>
            {title}
          </div>
        )}
        {children}
      </div>
    </div>
  );
}
