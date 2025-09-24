import { useEffect, useState } from "react";
import { useForm, useFieldArray, Controller } from "react-hook-form";
import { PencilLine, Plus, CircleMinus } from "lucide-react";

import ShadowPopup from "@/components/common/ShadowPopup";
import InputField from "@/components/common/InputField";
import SelectField from "@/components/common/SelectField";
import { BudgetRow } from "@/lib/types/BudgetType";
import styles from "@/styles/components/EditBudgetPopup.module.scss";
import departmentAPI from "@/services/departmentAPI";

type FormValues = {
  budgets: BudgetRow[];
};

export default function EditBudgetPopup({
  deptTitle,
  deptId,
  setIsPopup,
}: {
  deptTitle: string;
  deptId: number;
  setIsPopup: (boolean: boolean) => void;
}) {
  // const [budgetData, setBudgetData] = useState<BudgetRow[]>();
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
    const getBudget = async () => {
      try {
        const res = await departmentAPI.getDeptAccount(deptId);
        if (res.data) {
          // setBudgetData(res.data);
          reset({ budgets: res.data });
        }
      } catch {}
    };

    getBudget();
  }, []);

  const onSubmit = async (values: FormValues) => {
    setIsPopup(false);
  };

  return (
    <ShadowPopup setIsPopup={setIsPopup} title={`編輯預算 一 ${deptTitle}`}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className={styles.wrap}>
          {fields.map((item, index) => (
            <div className={styles.fieldWrap} key={item.id}>
              <Controller
                control={control}
                name={`budgets.${index}.account_name`}
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
                register={register(`budgets.${index}.budget_limit`, {
                  valueAsNumber: true,
                  required: true,
                  min: 0,
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
          <Plus className={styles.addBudget} />
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
