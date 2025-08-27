import { Clock } from "lucide-react";
import { CalendarDays } from "lucide-react";
import { ChartCandlestick } from "lucide-react";
import { BookOpenText } from "lucide-react";

export const reportItemData = [
  {
    icon: Clock,
    title: "近期核銷圖表",
    link: "/recent",
  },
  {
    icon: CalendarDays,
    title: "年度核銷圖表",
    link: "/year",
  },
  {
    icon: ChartCandlestick,
    title: "自訂期間圖表",
    link: "/custom",
  },
  {
    icon: BookOpenText,
    title: "事件簿",
    link: "/event",
  },
];
