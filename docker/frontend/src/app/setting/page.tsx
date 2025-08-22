"use client";

import AdminSetting from "@/components/setting/AdminSetting";
import { MobileSetting } from "@/components/setting/MobileSetting";
import { useConfig } from "@/lib/context/ConfigContext";

export default function Setting() {
  const { role } = useConfig();
  return (
    <>
      {role === 0 && <MobileSetting />}
      {role === 1 && <AdminSetting />}
    </>
  );
}
