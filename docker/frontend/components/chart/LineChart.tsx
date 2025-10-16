"use client";

import { memo, useMemo } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler,
  ChartOptions,
  ChartData,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler
);

export type MoneyPoint = { id: number; money: number };

type Props = {
  data: MoneyPoint[];
  title?: string;
  /** 預設 false：用線性座標顯示 id；若想把 id 當分類(1,2,3…間距一致)就設 true */
  xAsCategory?: boolean;
  /** 預設：千分位；可自行覆寫 */
  formatMoney?: (v: number) => string;
  /** 外層容器控制高度時，請把這裡維持 undefined；若想直接指定高度，可傳入像素值 */
  fixedHeightPx?: number;
};

const defaultFormat = (v: number) =>
  v.toLocaleString(undefined, { maximumFractionDigits: 2 });

function toChartDataset(points: MoneyPoint[]) {
  // 使用 parsing:false + {x,y} 可避免多餘解析開銷且支援線性 x
  return points.map((p) => ({ x: p.id, y: p.money }));
}

function LineMoneyChart({
  data,
  title,
  xAsCategory = false,
  formatMoney = defaultFormat,
  fixedHeightPx,
}: Props) {
  const hasData = data && data.length > 0;

  const chartData = useMemo<ChartData<"line">>(() => {
    if (!hasData) {
      return { datasets: [] };
    }

    const dataset = toChartDataset(data);

    return {
      // 若使用分類軸，labels 要是字串；否則忽略 labels，使用 {x,y}
      labels: xAsCategory ? data.map((d) => String(d.id)) : undefined,
      datasets: [
        {
          label: title ?? "金額",
          data: dataset as any,
          borderWidth: 2,
          tension: 0.25,
          pointRadius: 2,
          pointHoverRadius: 4,
          fill: true,
          borderColor: "#5caed6",
          backgroundColor: "#cfe7f0",
        },
      ],
    };
  }, [data, hasData, xAsCategory, title]);

  const options = useMemo<ChartOptions<"line">>(
    () => ({
      responsive: true,
      maintainAspectRatio: fixedHeightPx ? true : false, // 若外層控制高度，關掉比例維持
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { display: !!title },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              const v = ctx.parsed.y;
              return `${ctx.dataset.label ?? "金額"}：${formatMoney(v)}`;
            },
          },
        },
      },
      parsing: false, // 我們已提供 {x,y}
      scales: {
        x: xAsCategory
          ? {
              type: "category",
              title: { display: false },
              grid: { display: false },
            }
          : {
              type: "linear",
              title: { display: false },
              ticks: { display: false },
              grid: { display: false },
            },
        y: {
          type: "linear",
          title: { display: false, text: "money" },
          ticks: {
            callback: (value) => formatMoney(Number(value)),
          },
        },
      },
      elements: {
        line: { borderWidth: 2 },
        point: { radius: 2 },
      },
    }),
    [fixedHeightPx, formatMoney, title, xAsCategory]
  );

  if (!hasData) {
    return (
      <div
        style={{
          width: "100%",
          height: fixedHeightPx ?? 100,
          padding: 100,
          boxSizing: "border-box",
          display: "grid",
          placeItems: "center",
          border: "1px dashed var(--border-color, #ccc)",
          borderRadius: 8,
        }}
      >
        載入中...
      </div>
    );
  }

  return (
    <div
      style={{
        width: "340px",
        height: fixedHeightPx ?? "230px",
      }}
    >
      <Line data={chartData} options={options} />
    </div>
  );
}

export default memo(LineMoneyChart);
