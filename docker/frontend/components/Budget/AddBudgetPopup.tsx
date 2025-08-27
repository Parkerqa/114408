import { useForm, useFieldArray, Controller } from "react-hook-form";
import { PencilLine, Plus, CircleMinus } from "lucide-react";

import ShadowPopup from "@/components/common/ShadowPopup";
import InputField from "@/components/common/InputField";
import SelectField from "@/components/common/SelectField";
import styles from "@/styles/components/AddBudgetPopup.module.scss";

type BudgetRow = {
  department: string;
  account: string;
  limit: number | string;
};
type FormValues = { budgets: BudgetRow[] };

export default function AddBudgetPopup({
  setIsPopup,
}: {
  setIsPopup: (boolean: boolean) => void;
}) {
  const {
    control,
    register,
    handleSubmit,
    formState: { isSubmitting },
  } = useForm<FormValues>({
    defaultValues: { budgets: [{ department: "", account: "", limit: "" }] },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: "budgets",
  });

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
                    onChange={field.onChange}
                    optionData={[
                      { value: "銷售部門" },
                      { value: "技術部門" },
                      { value: "研發部門" },
                    ]}
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
                type="number"
                label="預算上限"
                showIcon
                icon={<PencilLine size={20} />}
                iconRight
                register={register(`budgets.${index}.limit`)}
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
            onClick={() => append({ department: "", account: "", limit: "" })}
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
