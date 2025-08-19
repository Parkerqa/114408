"use client";

import Image from "next/image";

import { useConfig } from "@/lib/context/ConfigContext";
import { navData } from "@/lib/data/navData";

export default function Sidebar() {
  const { user } = useConfig();
  return (
    <div>
      {user?.img && <Image alt="user" width={50} height={50} src={user?.img} />}
      
    </div>
  );
}
