"use client";

import { usePathname } from "next/navigation";
import { useConfig } from "@/lib/context/ConfigContext";
import BottomNav from "./BottomNav";
import Sidebar from "./Sidebar";

export default function NavSelector() {
  const { role } = useConfig();
  const pathname = usePathname();

  if (pathname.startsWith("/auth")) {
    return null;
  }

  switch (role) {
    case 1:
      return <BottomNav />;
    case 0:
    case 2:
    case 3:
      return <Sidebar />;

    default:
      return <BottomNav />;
  }
}
