import { useState } from "react";

export default function MoreInfoBar({
  title,
  context,
}: {
  title: string;
  context: any;
}) {
  const [isOpen, setIsOpen] = useState<boolean>(false);

  return (
    <div
      onClick={() => {
        setIsOpen(isOpen ? false : true);
      }}
    >
      <p>{title}</p>
      {isOpen && <div>{context}</div>}
    </div>
  );
}
