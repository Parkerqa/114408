"use client";

import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { ChartDataType } from "@/lib/types/ChartDataType";
import { useEffect, useState } from "react";

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
  width,
  height,
}: {
  data: ChartDataType;
  title: string;
  width?: number;
  height?: number;
}) {
  const [size, setSize] = useState(150);

  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      if (width < 1440) setSize(150);
      else if (width < 1680) setSize(170);
      else setSize(210);
    };
    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const options = {
    cutout: "65%",
    maintainAspectRatio: false,
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
        width: `${size}px`,
        height: `${size}px`,
        margin: "0 auto",
        textAlign: "center",
      }}
    >
      <Doughnut data={data} options={options} />
    </div>
  );
}
