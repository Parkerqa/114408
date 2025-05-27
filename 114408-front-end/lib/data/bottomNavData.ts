import { House } from "lucide-react";
import { AlignLeft } from "lucide-react";
import { Bot } from "lucide-react";
import { Settings2 } from "lucide-react";

type NavItem = {
  icon: any;
  title: string;
  url: string;
};

export const bottomNavData: NavItem[] = [
  { icon: House, title: "待核銷報帳", url: "/user" },
  {
    icon: AlignLeft,
    title: "過去核銷紀錄",
    url: "/past-records",
  },
  {
    icon: Bot,
    title: "FQA智慧回覆",
    url: "https://line.me/R/ti/p/%40643foras",
  },
  { icon: Settings2, title: "其他設定", url: "/setting" },
];
