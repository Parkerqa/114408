import { useForm } from "react-hook-form";
import { ScanFace } from "lucide-react";
import { Mail } from "lucide-react";

import { useConfig } from "@/lib/context/ConfigContext";
import ShadowPopup from "@/components/common/ShadowBg";
import InputField from "@/components/common/InputField";
import styles from "@/styles/components/ForgetPassword.module.scss";
import userAPI from "@/services/userAPI";

export default function ForgetPassword({
  setIsPopup,
}: {
  setIsPopup: (boolean: boolean) => void;
}) {
  const { getValues, register } = useForm();
  const { theme } = useConfig();
  const iconColor = theme === 0 ? "#3f4360" : "#f0f0f5";

  const sendEmail = async () => {
    const data = {
      email: getValues("email"),
    };
    try {
      await userAPI.forgetPassword(data);
      setIsPopup(false);
    } catch {}
  };

  return (
    <ShadowPopup title="忘記密碼" setIsPopup={setIsPopup}>
      <div className={styles.wrap}>
        <p className={styles.title}>
          <ScanFace size={65} />
          讓我們協助您重設密碼
        </p>
        <InputField
          type="text"
          register={register("email")}
          isCornerRadius={true}
          style={{ width: "20vw" }}
          icon={<Mail size={24} color={iconColor} />}
          showIcon={true}
        />
        <span className={styles.hint}>請輸入您的信箱</span>
        <button onClick={sendEmail} className={styles.reset}>
          重設
        </button>
      </div>
    </ShadowPopup>
  );
}
