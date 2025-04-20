import { useDropzone } from "react-dropzone";

import { HtmlDivPropsType } from "@/lib/types/HtmlDivType";
import BasePopup from "@/components/common/BasePopup";

export default function FileFrame({ ...props }: HtmlDivPropsType) {
  const { getRootProps, getInputProps, acceptedFiles } = useDropzone({
    accept: { "image/*": [] },
    multiple: false,
  });

  return (
    <BasePopup {...props}>
      <div {...getRootProps()} className="border p-4">
        <input {...getInputProps()} />
        <p>點擊或拖曳圖片到這裡上傳</p>
      </div>
    </BasePopup>
  );
}
