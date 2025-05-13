export const base64ToBlob = (base64Img: string) => {
  const base64 = base64Img;
  if (!base64) return null;

  const arr = base64.split(",");
  const mime = arr[0].match(/:(.*?);/)?.[1] || "image/jpeg";
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n--) u8arr[n] = bstr.charCodeAt(n);
  return new Blob([u8arr], { type: mime });
};

export const base64ToFile = (base64: string) => {
  const blob = base64ToBlob(base64);
  if (!blob) return null;
  return new File([blob], "photo.jpg", { type: blob.type });
};
