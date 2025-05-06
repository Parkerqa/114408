type NavItem = {
  icon: string;
  title: string;
  url: string;
};

export const bottomNavData: NavItem[] = [
  { icon: "/bottomNavIcon/home.svg", title: "待核銷報帳", url: "/user" },
  { icon: "/bottomNavIcon/list.svg", title: "過去核銷紀錄", url: "/past" },
  { icon: "/bottomNavIcon/robot.svg", title: "FQA智慧回覆", url: "/line" },
  { icon: "/bottomNavIcon/setting.svg", title: "其他設定", url: "/setting" },
];
