"use client";

import { createContext, useContext, useState } from "react";

import Loading from "@/components/Loading";

const LoadingContext = createContext<{
  isLoading: boolean;
  setLoading: (loading: boolean) => void;
}>({
  isLoading: false,
  setLoading: () => {},
});

export const LoadingProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [isLoading, setIsLoading] = useState(false);

  return (
    <LoadingContext.Provider value={{ isLoading, setLoading: setIsLoading }}>
      {isLoading ? <Loading /> : children}
    </LoadingContext.Provider>
  );
};

export const useLoading = () => useContext(LoadingContext);
