import "@/styles/main.scss";
import type { Metadata } from "next";
import BottomNav from "@/components/layout/BottomNav";

export const metadata: Metadata = {
  title: "Ｅ筆勾銷",
  description: "協助您報帳核銷，輕鬆自在",
  keywords: ["AI", "發票辨識", "報帳核銷", "自動分類", "智慧財務"],
  icons: {
    icon: "/logo.svg",
    shortcut: "/logo-32x32.png",
    apple: "on-apple-logo.png",
  },
  manifest: "/manifest.webmanifest",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh">
      <body>
        <BottomNav title="待核銷報帳"/>
        {children}
      </body>
    </html>
  );
}
