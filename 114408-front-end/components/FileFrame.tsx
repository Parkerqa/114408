import { useDropzone } from "react-dropzone";

export default function FileFrame() {
  const { getRootProps, getInputProps, acceptedFiles } = useDropzone({
    accept: { "image/*": [] },
    multiple: false,
  });

  return (
    <div {...getRootProps()} className="border p-4">
      <input {...getInputProps()} />
      <p>點擊或拖曳圖片到這裡上傳</p>
    </div>
  );
}
