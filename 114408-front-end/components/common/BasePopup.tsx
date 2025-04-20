import { HtmlDivPropsType } from "@/lib/types/HtmlDivType";
import styles from "@/styles/components/common/BasePopup.module.scss";

export default function BasePopup({
  children,
  title,
  ...props
}: HtmlDivPropsType & {
  children: React.ReactNode;
  title?: string;
}) {
  return (
    <div className={styles.wrap} {...props}>
      <div className={styles.childrenWrap}>
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
