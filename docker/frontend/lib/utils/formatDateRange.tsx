import { DateRange } from "react-day-picker";

export function formatDateRange(range: DateRange | undefined): {
  from?: string;
  to?: string;
} {
  if (!range) return {};

  const format = (date: Date) => date.toISOString().split("T")[0]; // 直接取 yyyy-mm-dd

  return {
    from: range.from ? format(range.from) : undefined,
    to: range.to ? format(range.to) : undefined,
  };
}
