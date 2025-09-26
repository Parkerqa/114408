"use client";

import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

type BudgetData = {
  account_class: string;
  total_budget: number;
  total_amount: number;
};

export default function BarChart({ data }: { data: BudgetData[] }) {
  const labels = data.map((item) => item.account_class);

  const chartData = {
    labels,
    datasets: [
      {
        label: "預算金額",
        data: data.map((item) => item.total_budget),
        backgroundColor: "#5caed6",
      },
      {
        label: "已使用金額",
        data: data.map((item) => item.total_amount),
        backgroundColor: "#cfe7f0",
      },
    ],
  };

  const options = {
    indexAxis: "y" as const, // 橫條圖
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top" as const,
      },
    },
  };

  return (
    <div
      style={{
        width: "320px",
        height: "230px",
        borderRadius: 10,
      }}
    >
      <Bar data={chartData} options={options} />
    </div>
  );
}
