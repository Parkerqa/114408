import { DateRange } from "react-day-picker";

export const formatLocalDate = (d?: Date) => {
  if (!d) return undefined;
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
};

export function formatDateRange(range?: DateRange): {
  from?: string;
  to?: string;
} {
  return {
    from: formatLocalDate(range?.from),
    to: formatLocalDate(range?.to),
  };
}
