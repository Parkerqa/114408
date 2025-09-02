import styles from "@/styles/components/setting/WarningLight.module.scss";

export const fields = [
  {
    className: styles.red,
    label_top: "過剩上限",
    label_bot: "過剩下限",
    limit_top: "excess_top" as const,
    limit_bot: "excess_bot" as const,
  },
  {
    className: styles.yellow,
    label_top: "偏高上限",
    label_bot: "偏高下限",
    limit_top: "high_top" as const,
    limit_bot: "high_bot" as const,
  },
  {
    className: styles.green,
    label_top: "良好上限",
    label_bot: "良好下限",
    limit_top: "good_top" as const,
    limit_bot: "good_bot" as const,
  },
  {
    className: styles.yellow,
    label_top: "偏低上限",
    label_bot: "偏低下限",
    limit_top: "low_top" as const,
    limit_bot: "low_bot" as const,
  },
  {
    className: styles.red,
    label_top: "不足上限",
    label_bot: "不足下限",
    limit_top: "insufficient_top" as const,
    limit_bot: "insufficient_bot" as const,
  },
];
