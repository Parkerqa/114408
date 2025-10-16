"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useLoading } from "@/lib/context/LoadingContext";
import { useConfig } from "@/lib/context/ConfigContext";

export default function Home() {
  const { setLoading } = useLoading();
  const { role, fetch, fetchUser } = useConfig();
  const route = useRouter();

  useEffect(() => {
    if (role === undefined || role === null) {
      fetch();
      fetchUser();
    }

    setLoading(true);

    const redirect = async () => {
      switch (role) {
        case 1:
          route.push("/user");
          break;
        case 0:
        case 2:
        case 3:
          route.push("/admin");
          break;
      }
    };

    redirect();
    setLoading(false);
  }, [role, route, setLoading]);

  return null;
}
