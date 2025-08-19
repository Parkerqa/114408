import Head from "next/head";
import { useState } from "react";
import { LayoutProps } from "@/lib/types/ClientLayout";

export default function ClientLayout({ children, title }: LayoutProps) {
  const [isAdmin, setIsAdmin] = useState<boolean>();
  return (
    <>
      <Head>
        <title>{title}</title>
        <link rel="icon" href="/logo.svg" />
      </Head>
      {children}
    </>
  );
}
