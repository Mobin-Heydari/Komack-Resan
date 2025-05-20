"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { Invoice } from "@/types/invoices";

export default function InvoiceDetailPage() {
  const { id } = useParams(); // شناسه فاکتور از URL
  const [invoice, setInvoice] = useState<Invoice | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchInvoice() {
      if (!id) return;
      try {
        const res = await fetch(`http://127.0.0.1:8000/invoices/${id}/`);
        const data: Invoice = await res.json();
        setInvoice(data);
      } catch (error) {
        console.error("خطا در دریافت جزئیات فاکتور:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchInvoice();
  }, [id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen" dir="rtl">
        <p className="text-xl">در حال بارگذاری جزئیات فاکتور...</p>
      </div>
    );
  }

  if (!invoice) {
    return (
      <div className="flex items-center justify-center h-screen" dir="rtl">
        <p className="text-xl text-gray-500">فاکتوری یافت نشد.</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4" dir="rtl">
      {/* سرصفحه فاکتور */}
      <div className="mb-6 border-b pb-4">
        <h1 className="text-4xl font-bold mb-2">فاکتور شرکت {invoice.company}</h1>
        <div className="text-lg text-gray-700">
          <p>
            <span className="font-semibold">شناسه فاکتور:</span> {invoice.id}
          </p>
          <p>
            <span className="font-semibold">وضعیت:</span>{" "}
            {invoice.is_paid ? "پرداخت شده" : "پرداخت نشده"}
          </p>
        </div>
      </div>

      {/* خلاصه مالی فاکتور */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2">خلاصه مالی</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <p>
            <span className="font-semibold">مبلغ کل:</span>{" "}
            {invoice.total_amount.toLocaleString()} تومان
          </p>
          <p>
            <span className="font-semibold">مهلت:</span>{" "}
            {new Date(invoice.deadline).toLocaleString("fa-IR")}
          </p>
          <p>
            <span className="font-semibold">وضعیت مهلت:</span> {invoice.deadline_status}
          </p>
        </div>
      </div>

      {/* زمان‌بندی‌ها */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2">زمان‌بندی‌ها</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <p>
            <span className="font-semibold">ایجاد شده:</span>{" "}
            {new Date(invoice.created_at).toLocaleString("fa-IR")}
          </p>
          <p>
            <span className="font-semibold">به‌روزرسانی شده:</span>{" "}
            {new Date(invoice.updated_at).toLocaleString("fa-IR")}
          </p>
        </div>
      </div>

      {/* اقلام فاکتور */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-4">موارد فاکتور</h2>
        {invoice.items.length === 0 ? (
          <p className="text-gray-600">هیچ موردی موجود نیست.</p>
        ) : (
          <div className="space-y-4">
            {invoice.items.map((item, index) => (
              <div
                key={index}
                className="p-4 border rounded-md shadow-sm bg-gray-50"
              >
                <p>
                  <span className="font-semibold">خدمت:</span> {item.service}
                </p>
                <p>
                  <span className="font-semibold">مبلغ:</span>{" "}
                  {item.amount.toLocaleString()} تومان
                </p>
                <p>
                  <span className="font-semibold">تاریخ ایجاد مورد:</span>{" "}
                  {new Date(item.created_at).toLocaleString("fa-IR")}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      <div>
        <Link
          href="/invoices"
          className="inline-block mt-4 px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          بازگشت به فاکتورها
        </Link>
      </div>
    </div>
  );
}
