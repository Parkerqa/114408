import settingAPI from "@/services/settingAPI";

export type ExpenditureItem = {
  account_name: string;
  total_budget: number;
  total_amount: number;
};

export type DoughnutData = {
  labels: ["使用金額", "尚未使用金額"];
  datasets: Array<{
    label: "金額";
    data: [number, number];
    backgroundColor: [string, string];
  }>;
};

type ColorThresholds = {
  red_usage_rate: number;
  red_remaining_rate: number;
  yellow_usage_rate: number;
  yellow_remaining_rate: number;
  green_usage_rate: number;
  green_remaining_rate: number;
};

let cachedThresholds: ColorThresholds | null = null;

async function getColorThresholds(): Promise<ColorThresholds> {
  if (cachedThresholds) return cachedThresholds;
  try {
    const res = await settingAPI.getColor();
    const data = res?.data as ColorThresholds | undefined;
    if (data) {
      cachedThresholds = data;
      return data;
    }
  } catch {}
  // 後備預設：可依你後端預設調整
  cachedThresholds = {
    red_usage_rate: 20,
    red_remaining_rate: 80,
    yellow_usage_rate: 50,
    yellow_remaining_rate: 50,
    green_usage_rate: 80,
    green_remaining_rate: 20,
  };
  return cachedThresholds;
}

function pickUsageColor(remainingRate: number, t: ColorThresholds): string {
  if (remainingRate >= t.red_remaining_rate) return "var(--point-red)";
  if (remainingRate >= t.yellow_remaining_rate) return "var(--point-yellow)";
  return "var(--point-green)";
}

export async function formatChartData(
  items: ExpenditureItem[]
): Promise<Array<{ title: string; chartData: DoughnutData }>> {
  const thresholds = await getColorThresholds();
  const top3 = (items ?? []).slice(0, 3);

  const getColorRange = async () => {
    try {
      const res = await settingAPI.getColor();
      console.log(res.data);
    } catch {}
  };

  getColorRange();

  const FALLBACK_COLORS: Record<string, string> = {
    "--point-red": "#e74c3c",
    "--point-yellow": "#f1c40f",
    "--point-green": "#2ecc71",
  };

  function getCSSVarValue(varName: string): string {
    // SSR 環境（Next.js 伺服端）先回退
    if (typeof window === "undefined")
      return FALLBACK_COLORS[varName] ?? "#000";
    // 從 <html> 讀取（若你把變數掛在 body，可改成 document.body）
    const value = getComputedStyle(document.documentElement)
      .getPropertyValue(varName)
      .trim();
    return value || FALLBACK_COLORS[varName] || "#000";
  }

  function getThemeColors() {
    // 讀一次，之後重用
    return {
      red: getCSSVarValue("--point-red"),
      yellow: getCSSVarValue("--point-yellow"),
      green: getCSSVarValue("--point-green"),
    };
  }

  // ========= 挑選「使用金額」的顏色（依剩餘比例） =========
  // 規則：remainingRate >= red_remaining → 紅；>= yellow_remaining → 黃；否則綠
  function pickUsageColor(
    remainingRate: number,
    t: ColorThresholds,
    colors: { red: string; yellow: string; green: string }
  ) {
    if (remainingRate >= t.red_remaining_rate) return colors.red;
    if (remainingRate >= t.yellow_remaining_rate) return colors.yellow;
    return colors.green;
  }
  const colors = getThemeColors();

  return top3.map((it) => {
    const used = Number(it.total_amount) || 0;
    const budget = Number(it.total_budget) || 0;
    const unused = Math.max(budget - used, 0);

    const remainingRate = budget > 0 ? (unused / budget) * 100 : 0;

    const usageColor = pickUsageColor(remainingRate, thresholds, colors);

    const chartData: DoughnutData = {
      labels: ["使用金額", "尚未使用金額"],
      datasets: [
        {
          label: "金額",
          data: [used, unused],
          backgroundColor: [usageColor, "#f8f8f8"],
        },
      ],
    };

    return {
      title: it.account_name,
      chartData,
    };
  });
}
