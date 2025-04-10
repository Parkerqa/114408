import { useDropzone } from "react-dropzone";

import { HtmlDivPropsType } from "@/lib/types/HtmlDivType";
import TitleBox from "@/components/common/TitleBox";

export default function FileFrame({ ...props }: HtmlDivPropsType) {
  const { getRootProps, getInputProps, acceptedFiles } = useDropzone({
    accept: { "image/*": [] },
    multiple: false,
  });

  return (
    <TitleBox {...props}>
      <div {...getRootProps()} className="border p-4">
        <input {...getInputProps()} />
        <p>點擊或拖曳圖片到這裡上傳</p>
      </div>
    </TitleBox>
  );
}
