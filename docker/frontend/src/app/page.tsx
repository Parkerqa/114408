"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { useConfig } from "@/lib/context/ConfigContext";

export default function Home() {
  const { user, role } = useConfig();
  const route = useRouter();

  useEffect(() => {
    if (user === null) {
      route.push("/auth");
      return;
    }

    switch (role) {
      case 1:
        route.replace("/user");
        break;
      case 0:
      case 2:
      case 3:
        route.replace("/admin");
        break;
    }
  }, [user, role]);

  return <></>;
}
