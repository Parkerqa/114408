import "@/styles/main.scss";
import type { Metadata } from "next";
import { Toaster } from "sonner";

import MuiThemeProvider from "@/lib/context/MuiThemeProvider";
import { ConfigProvider } from "@/lib/context/ConfigContext";
import { LoadingProvider } from "@/lib/context/LoadingContext";
import NavSelector from "@/components/layout/NavSelector";

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
        <Toaster richColors position="top-center" />
        <LoadingProvider>
          <ConfigProvider>
            <MuiThemeProvider>
              <NavSelector />
              {children}
            </MuiThemeProvider>
          </ConfigProvider>
        </LoadingProvider>
      </body>
    </html>
  );
}
