import styles from "@/styles/components/setting/WarningLight.module.scss";

export const fields = [
  {
    className: styles.green,
    label_top: "資金使用率",
    label_bot: "資金剩餘率",
    limit_top: "green_top" as const,
    limit_bot: "green_bot" as const,
  },
  {
    className: styles.yellow,
    label_top: "資金使用率",
    label_bot: "資金剩餘率",
    limit_top: "yellow_top" as const,
    limit_bot: "yellow_bot" as const,
  },
  {
    className: styles.red,
    label_top: "資金使用率",
    label_bot: "資金剩餘率",
    limit_top: "red_top" as const,
    limit_bot: "red_bot" as const,
  },
];
