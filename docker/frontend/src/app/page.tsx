"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { useLoading } from "@/lib/context/LoadingContext";
import { useConfig } from "@/lib/context/ConfigContext";

export default function Home() {
  const { setLoading } = useLoading();
  const { role } = useConfig();
  const route = useRouter();

  useEffect(() => {
    switch (role) {
      case 1:
        setLoading(false);
        route.push("/user");
        break;
      case 0:
      case 2:
      case 3:
        setLoading(false);
        route.push("/admin");
        break;
    }
  }, [role, route, setLoading]);

  return <></>;
}
