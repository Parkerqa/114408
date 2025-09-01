"use client";

import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { ChartDataType } from "@/lib/types/ChartDataType";

const centerTextPlugin = {
  id: "centerText",
  beforeDraw(chart: any) {
    const { width, height, ctx } = chart;
    const title = chart.config.options.plugins.centerText?.text || "";
    ctx.save();
    ctx.font = "15px sans-serif";
    ctx.fillStyle = "#8a8c9d";
    ctx.textBaseline = "middle";
    const textX = Math.round((width - ctx.measureText(title).width) / 2);
    const textY = height / 2;
    ctx.fillText(title, textX, textY);
    ctx.restore();
  },
};

ChartJS.register(ArcElement, Tooltip, Legend, centerTextPlugin);

export default function Chart({
  data,
  title,
}: {
  data: ChartDataType;
  title: string;
}) {
  const options = {
    cutout: "65%",
    plugins: {
      legend: {
        display: false,
      },
      centerText: {
        text: title,
      },
    },
  };

  return (
    <div
      style={{
        position: "relative",
        width: `${title === "總預算" ? "160px" : "150px"}`,
        margin: "0 auto",
        textAlign: "center",
      }}
    >
      <Doughnut data={data} options={options} />
    </div>
  );
}
