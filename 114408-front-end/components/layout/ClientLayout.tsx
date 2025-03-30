import Head from "next/head";

type LayoutProps = {
  children: React.ReactNode;
  title: string;
};

export default function ClientLayout({ children, title }: LayoutProps) {
  return (
    <>
      <Head>
        <title>{title}</title>
        <link rel="icon" href="/logo.svg" />
      </Head>
      {children}
    </>
  );
}
