"use client";

import AdminSetting from "@/components/setting/AdminSetting";
import { MobileSetting } from "@/components/setting/MobileSetting";
import { useConfig } from "@/lib/context/ConfigContext";

export default function Setting() {
  const { role } = useConfig();
  
  return (
    <>
      {role === 1 && <MobileSetting />}
      {(role === 0 || role === 2 || role === 3) && <AdminSetting />}
    </>
  );
}
