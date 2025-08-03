import { House } from "lucide-react";
import { Bot } from "lucide-react";
import { Settings2 } from "lucide-react";
import { SquareCheckBig } from "lucide-react";
import { ChartLine } from "lucide-react";

type NavItem = {
  icon: any;
  title: string;
  url: string;
};

export const navData: NavItem[] = [
  { icon: House, title: "主頁", url: "/admin" },
  { icon: SquareCheckBig, title: "核銷報帳", url: "/verify" },
  {
    icon: ChartLine,
    title: "報表專區",
    url: "/chart",
  },
  {
    icon: Bot,
    title: "FQA智慧回覆",
    url: "https://line.me/R/ti/p/%40643foras",
  },
  { icon: Settings2, title: "其他設定", url: "/setting" },
];
