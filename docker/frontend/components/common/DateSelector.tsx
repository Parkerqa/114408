"use client";

import { useEffect, useState } from "react";
import { DayPicker, DateRange } from "react-day-picker";
import "react-day-picker/style.css";

import styles from "@/styles/components/common/DateSelector.module.scss";

type props = {
  recentBtn?: boolean;
  initRange?: DateRange;
  onChange?: (range: DateRange | undefined) => void;
};

export default function DateSelector({
  recentBtn = false,
  initRange,
  onChange,
}: props) {
  const toNoonLocal = (d?: Date) =>
    d ? new Date(d.getFullYear(), d.getMonth(), d.getDate(), 12) : undefined;

  const today = new Date();

  const getRange = (number: number): DateRange => {
    const from = new Date();
    from.setDate(today.getDate() - (number - 1));
    return { from, to: today };
  };

  const [rangeNum, setRangeNum] = useState<number>(7);
  const [range, setRange] = useState<DateRange | undefined>(
    initRange ?? getRange(7)
  );

  const handleSelect = (newRange: DateRange | undefined) => {
    const fixed: DateRange | undefined = newRange
      ? {
          from: toNoonLocal(newRange.from),
          to: toNoonLocal(newRange.to),
        }
      : undefined;

    setRange(fixed);
    if (onChange) onChange(fixed);
  };

  useEffect(() => {
    if (range && onChange) {
      onChange(range);
    }
  }, [range, onChange]);

  return (
    <div className={styles.dayWrap}>
      {recentBtn && (
        <div
          style={{
            marginTop: "10px",
            display: "flex",
            gap: "10px",
          }}
        >
          <button
            className={`${rangeNum === 7 && styles.isFocus} `}
            onClick={() => {
              setRangeNum(7);
              setRange(getRange(7));
            }}
          >
            近一週
          </button>
          <button
            className={`${rangeNum === 30 && styles.isFocus} `}
            onClick={() => {
              setRangeNum(30);
              setRange(getRange(30));
            }}
          >
            近一個月
          </button>
        </div>
      )}
      <DayPicker
        mode="range"
        selected={range}
        onSelect={handleSelect}
        defaultMonth={today}
      />
    </div>
  );
}
