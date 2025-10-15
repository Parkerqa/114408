"use client";

import { useEffect, useMemo } from "react";
import { ThemeProvider, createTheme, CssBaseline } from "@mui/material";
import { useConfig } from "@/lib/context/ConfigContext";

export default function MuiThemeProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const { theme } = useConfig();
  const mode = theme === 1 ? "dark" : "light";

  useEffect(() => {
    if (typeof document !== "undefined") {
      document.documentElement.setAttribute("theme", mode);
      document.body.setAttribute("theme", mode);
      localStorage.setItem("theme", mode);
    }
  }, [mode]);

  const muiTheme = useMemo(
    () =>
      createTheme({
        palette: {
          mode,
          ...(mode === "dark"
            ? { background: { default: "#1e1e2f", paper: "#1e1e1e" } }
            : {}),
        },
      }),
    [mode]
  );

  return (
    <ThemeProvider theme={muiTheme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
}
