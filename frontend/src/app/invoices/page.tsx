"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Invoice } from "@/types/invoices";

export default function InvoicesList() {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchInvoices() {
      try {
        const res = await fetch("http://127.0.0.1:8000/invoices/");
        const data = await res.json();

        console.log("داده‌های واکشی شده:", data);

        // اگر داده برگشتی آرایه است، مستقیم استفاده می‌کنیم.
        if (Array.isArray(data)) {
          setInvoices(data);
        } else if (data && typeof data === "object") {
          // اگر API یک شی واحد یا ابجکتی با یک ویژگی برمی‌گرداند،
          // لازم است بر اساس وضعیت خودتان آن را تنظیم کنید.
          setInvoices([]);
        } else {
          setInvoices([]);
        }
      } catch (error) {
        console.error("خطا در دریافت فاکتورها:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchInvoices();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen" dir="rtl">
        <p className="text-xl">در حال بارگذاری فاکتورها...</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4" dir="rtl">
      <h1 className="text-4xl font-bold mb-8 text-center">فاکتورها</h1>
      {invoices.length === 0 ? (
        <p className="text-center text-gray-600">هیچ فاکتوری موجود نیست.</p>
      ) : (
        <div className="grid grid-cols-1 gap-8">
          {invoices.map((invoice) => (
            <div
              key={invoice.id}
              className="bg-white shadow-lg rounded-lg overflow-hidden p-6"
            >
              <div className="mb-4">
                <h2 className="text-2xl font-bold">
                  {invoice.company} — {invoice.total_amount.toLocaleString()} تومان
                </h2>
                <p className="text-gray-600">
                  {invoice.is_paid ? "پرداخت شده" : "پرداخت نشده"} &bull; مهلت:{" "}
                  {new Date(invoice.deadline).toLocaleString("fa-IR")} (
                  {invoice.deadline_status})
                </p>
              </div>

              <div className="text-sm text-gray-500 mb-4">
                <p>
                  <span className="font-semibold">ایجاد شده:</span>{" "}
                  {new Date(invoice.created_at).toLocaleString("fa-IR")}
                </p>
                <p>
                  <span className="font-semibold">به‌روزرسانی شده:</span>{" "}
                  {new Date(invoice.updated_at).toLocaleString("fa-IR")}
                </p>
              </div>

              <Link
                href={`/invoices/${invoice.id}`}
                className="inline-block px-6 py-2 bg-green-600 text-white rounded hover:bg-green-500"
              >
                مشاهده جزئیات
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
