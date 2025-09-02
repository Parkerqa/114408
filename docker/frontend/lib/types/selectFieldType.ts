import { Control } from "react-hook-form";
import { SxProps } from "@mui/material/styles";

export interface OptionType {
  type: itemType[];
  department: itemType[];
}

export type itemType = {
  [key: string]: string;
};

export type SelectFieldType = {
  label: string;
  name: string;
  control: Control<any>;
  optionData: itemType[];
  required?: boolean;
  inlineStyle?: SxProps;
  className?: any;
};
