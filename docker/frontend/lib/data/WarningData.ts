import styles from "@/styles/components/setting/WarningLight.module.scss";

export const fields = [
  {
    className: styles.green,
    label_top: "健康上限",
    label_bot: "健康下限",
    limit_top: "green_top" as const,
    limit_bot: "green_bot" as const,
  },
  {
    className: styles.yellow,
    label_top: "良好上限",
    label_bot: "良好下限",
    limit_top: "yellow_top" as const,
    limit_bot: "yellow_bot" as const,
  },
  {
    className: styles.red,
    label_top: "危險上限",
    label_bot: "危險下限",
    limit_top: "red_top" as const,
    limit_bot: "red_bot" as const,
  },
];
