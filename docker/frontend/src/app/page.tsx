"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { useConfig } from "@/lib/context/ConfigContext";

export default function Home() {
  const { user, role } = useConfig();
  const route = useRouter();

  useEffect(() => {
    switch (role) {
      case 1:
        route.replace("/user");
        break;
      case 0:
      case 2:
      case 3:
        route.replace("/admin");
        break;
      default:
        route.push("/auth");
        break;
    }
  }, [user, role]);

  return <></>;
}
