import { HtmlDivPropsType } from "@/lib/types/HtmlDivType";
import styles from "@/styles/components/common/TitleBox.module.scss";

export default function TitleBox({
  children,
  ...props
}: HtmlDivPropsType & {
  children: React.ReactNode;
}) {
  return (
    <div className={styles.wrap} {...props}>
      <div className={styles.operation}>{children}</div>
    </div>
  );
}
