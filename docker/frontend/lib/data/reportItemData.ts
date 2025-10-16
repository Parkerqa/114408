import { Clock } from "lucide-react";
import { CalendarDays } from "lucide-react";
import { ChartCandlestick } from "lucide-react";
import { BookOpenText } from "lucide-react";

export const reportItemData = [
  {
    icon: Clock,
    title: "近期核銷圖表",
    link: "/report/recent",
  },
  {
    icon: CalendarDays,
    title: "年度核銷圖表",
    link: "/report/year",
  },
  {
    icon: BookOpenText,
    title: "事件簿",
    link: "/report/event",
  },
];
