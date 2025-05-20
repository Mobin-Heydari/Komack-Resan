import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/navbar";
import { dir } from "console";


export const metadata: Metadata = {
  title: "کمک رسان",
  description: "پلتفرم سرویس دهی",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fa" dir="rtl">
      <body>
        <Navbar />
        {children}
      </body>
    </html>
  );
}
