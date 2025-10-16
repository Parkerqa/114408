import { useForm, useFieldArray, Controller } from "react-hook-form";
import { PencilLine, Plus, CircleMinus } from "lucide-react";

import ShadowPopup from "@/components/common/ShadowPopup";
import InputField from "@/components/common/InputField";
import SelectField from "@/components/common/SelectField";
import { useLoading } from "@/lib/context/LoadingContext";

import styles from "@/styles/components/AddBudgetPopup.module.scss";
import departmentAPI from "@/services/departmentAPI";

export type BudgetRow = {
  department: string;
  account: string;
  limit: number;
  dept_id?: number;
  accounting_id?: number;
};

type FormValues = {
  budgets: BudgetRow[];
};

const DEPT_OPTIONS = [
  { id: 5, name: "人力資源部" },
  { id: 6, name: "財務部" },
  { id: 7, name: "市場部" },
  { id: 8, name: "資訊部" },
];

const ACCOUNT_OPTIONS = [
  { id: 1, name: "雜支" },
  { id: 2, name: "差旅費" },
  { id: 3, name: "交通費" },
  { id: 4, name: "廣告費" },
  { id: 5, name: "文具用品" },
];

export default function AddBudgetPopup({
  setIsPopup,
  getSummary,
}: {
  setIsPopup: (boolean: boolean) => void;
  getSummary: () => void;
}) {
  const { setLoading } = useLoading();

  const {
    control,
    register,
    handleSubmit,
    setValue,
    formState: { isSubmitting },
  } = useForm<FormValues>({
    defaultValues: { budgets: [] },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: "budgets",
  });

  const mapDeptNameToId = (name: string) =>
    DEPT_OPTIONS.find((o) => o.name === name)?.id ?? 0;

  const mapAccNameToId = (name: string) =>
    ACCOUNT_OPTIONS.find((o) => o.name === name)?.id ?? 0;

  const mergeItems = (
    baseline: { accounting_id: number; budget_limit: number }[],
    edits: { accounting_id: number; budget_limit: number }[]
  ) => {
    const map = new Map<number, number>();
    baseline.forEach((i) => map.set(i.accounting_id, i.budget_limit));
    edits.forEach((i) =>
      map.set(Number(i.accounting_id), Number(i.budget_limit))
    );
    return Array.from(map, ([accounting_id, budget_limit]) => ({
      accounting_id,
      budget_limit,
    }));
  };

  const onSubmit = async (values: FormValues) => {
    setLoading(true);

    const groups = new Map<
      number,
      { accounting_id: number; budget_limit: number }[]
    >();
    for (const row of values.budgets) {
      const deptId = Number(row.dept_id ?? mapDeptNameToId(row.department));
      const accId = Number(row.accounting_id ?? mapAccNameToId(row.account));
      if (!deptId || !accId) continue;
      const list = groups.get(deptId) ?? [];
      list.push({ accounting_id: accId, budget_limit: Number(row.limit || 0) });
      groups.set(deptId, list);
    }

    for (const [deptId, incomingItems] of groups.entries()) {
      try {
        const res = await departmentAPI.getDeptAccount(deptId);
        const baseline = (res?.data ?? []).map((r: any) => ({
          accounting_id: Number(r.accounting_id),
          budget_limit: Number(r.budget_limit ?? 0),
        })) as { accounting_id: number; budget_limit: number }[];

        const accounting_items = mergeItems(baseline, incomingItems);
        await departmentAPI.editBudget(deptId, { accounting_items });
      } catch (e) {
        console.error("新增預算失敗:", deptId, e);
      }
    }

    getSummary();
    setIsPopup(false);
    setLoading(false);
  };

  return (
    <ShadowPopup setIsPopup={setIsPopup} title="新增預算">
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className={styles.wrap}>
          {fields.map((field, index) => (
            <div className={styles.fieldWrap} key={field.id}>
              <Controller
                control={control}
                name={`budgets.${index}.department`}
                rules={{ required: true }}
                render={({ field }) => (
                  <SelectField
                    style={{ width: "200px" }}
                    title="部門"
                    value={field.value}
                    onChange={(name: string) => {
                      field.onChange(name);
                      const id = mapDeptNameToId(name);
                      setValue(`budgets.${index}.dept_id`, id, {
                        shouldDirty: true,
                        shouldValidate: true,
                      });
                    }}
                    optionData={DEPT_OPTIONS.map((o) => ({ value: o.name }))}
                  />
                )}
              />
              <Controller
                control={control}
                name={`budgets.${index}.account`}
                rules={{ required: true }}
                render={({ field }) => (
                  <SelectField
                    style={{ width: "200px" }}
                    title="會計科目"
                    value={field.value}
                    onChange={(name: string) => {
                      field.onChange(name);
                      const id = mapAccNameToId(name);
                      setValue(`budgets.${index}.accounting_id`, id, {
                        shouldDirty: true,
                        shouldValidate: true,
                      });
                    }}
                    optionData={ACCOUNT_OPTIONS.map((o) => ({ value: o.name }))}
                  />
                )}
              />
              <input
                type="hidden"
                {...register(`budgets.${index}.dept_id`, {
                  valueAsNumber: true,
                  required: true,
                  min: 1,
                })}
              />
              <input
                type="hidden"
                {...register(`budgets.${index}.accounting_id`, {
                  valueAsNumber: true,
                  required: true,
                  min: 1,
                })}
              />
              <InputField
                type="text"
                label="預算上限"
                showIcon
                icon={<PencilLine size={20} />}
                iconRight
                register={register(`budgets.${index}.limit`, {
                  valueAsNumber: true,
                })}
              />
              <CircleMinus
                size={20}
                className={styles.minus}
                onClick={() => (fields.length > 1 ? remove(index) : null)}
              />
            </div>
          ))}
          <hr className={styles.hr} />
          <Plus
            className={styles.addBudget}
            onClick={() => append({ department: "", account: "", limit: 0 })}
          />
          <div className={styles.buttonWrap}>
            <button
              type="button"
              className={styles.cancel}
              onClick={() => setIsPopup(false)}
            >
              取消
            </button>
            <button
              type="submit"
              className={styles.add}
              disabled={isSubmitting}
            >
              新增
            </button>
          </div>
        </div>
      </form>
    </ShadowPopup>
  );
}
