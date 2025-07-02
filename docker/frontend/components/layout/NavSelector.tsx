"use client";

import { useConfig } from "@/lib/context/ConfigContext";
import BottomNav from "./BottomNav";
import Sidebar from "./Sidebar";

export default function NavSelector() {
  const { role } = useConfig();

  switch (role) {
    case 0:
    case 1:
      return <BottomNav />;
    case 2:
    case 3:
      return <Sidebar />;

    default:
      return <BottomNav />;
  }
}
