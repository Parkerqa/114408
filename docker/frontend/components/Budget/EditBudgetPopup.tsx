import { useEffect } from "react";
import { useForm, useFieldArray, Controller } from "react-hook-form";
import { PencilLine, Plus, CircleMinus } from "lucide-react";

import ShadowPopup from "@/components/common/ShadowPopup";
import InputField from "@/components/common/InputField";
import SelectField from "@/components/common/SelectField";
import { FormValues, BudgetRow } from "@/lib/types/BudgetType";
import styles from "@/styles/components/EditBudgetPopup.module.scss";

export default function EditBudgetPopup({
  department,
  setIsPopup,
  budgetData,
}: {
  department: string;
  setIsPopup: (boolean: boolean) => void;
  budgetData: BudgetRow[];
}) {
  const {
    control,
    register,
    handleSubmit,
    reset,
    formState: { isSubmitting },
  } = useForm<FormValues>({
    defaultValues: { budgets: [] },
  });

  const { fields, append, remove, replace } = useFieldArray({
    control,
    name: "budgets",
  });

  useEffect(() => {
    reset({ budgets: budgetData });
    replace(budgetData);
  }, []);

  const onSubmit = async (values: FormValues) => {
    // const payload = values.budgets
    //   .filter((b) => b.department && b.account && b.limit !== "")
    //   .map((b) => ({ ...b, limit: Number(b.limit) }));

    // const res = await fetch("/api/budgets", {
    //   method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify({ budgets: payload }),
    // });

    // if (!res.ok) {
    //   // TODO: 錯誤提示
    //   return;
    // }
    setIsPopup(false);
    console.log(values);
  };

  return (
    <ShadowPopup setIsPopup={setIsPopup} title={`編輯預算 一 ${department}`}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className={styles.wrap}>
          {fields.map((field, index) => (
            <div className={styles.fieldWrap} key={field.id}>
              <Controller
                control={control}
                name={`budgets.${index}.account`}
                rules={{ required: true }}
                render={({ field }) => (
                  <SelectField
                    style={{ width: "200px" }}
                    title="會計科目"
                    value={field.value}
                    onChange={field.onChange}
                    optionData={[
                      { value: "雜支" },
                      { value: "差旅費" },
                      { value: "交通費" },
                      { value: "交際費" },
                      { value: "廣告費" },
                      { value: "郵電費" },
                      { value: "文具用品" },
                    ]}
                  />
                )}
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
              更新
            </button>
          </div>
        </div>
      </form>
    </ShadowPopup>
  );
}
