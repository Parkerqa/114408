"use client";

import { useForm } from "react-hook-form";
import { useEffect, useState } from "react";

import { MobileSetting } from "@/components/setting/MobileSetting";
import userAPI from "@/services/userAPI";

export default function Setting() {
  const [user, setUser] = useState();
  const { register, reset, handleSubmit } = useForm({
    defaultValues: {
      username: "",
      email: "",
      password: "",
    },
  });

  const getUser = async () => {
    try {
      const res = await userAPI.getUser();
      if (res.data) {
        reset({
          username: res.data.username,
          email: res.data.email,
          password: "*********",
        });
        setUser(res.data);
      }
    } catch {}
  };

  useEffect(() => {
    getUser();
  }, []);

  return <MobileSetting register={register} handleSubmit={handleSubmit} />;
}
