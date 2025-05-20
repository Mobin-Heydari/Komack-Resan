"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { Service } from "@/types/services";

export default function ServiceDetailPage() {
  const { slug } = useParams();
  const [service, setService] = useState<Service | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchService() {
      if (!slug) return;
      try {
        const res = await fetch(`http://127.0.0.1:8000/services/service/${slug}/`);
        const data: Service = await res.json();
        setService(data);
      } catch (error) {
        console.error("خطا در دریافت جزئیات خدمت:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchService();
  }, [slug]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen" dir="rtl">
        <p className="text-xl">در حال بارگذاری جزئیات خدمت...</p>
      </div>
    );
  }

  if (!service) {
    return (
      <div className="flex items-center justify-center h-screen" dir="rtl">
        <p className="text-xl text-gray-500">خدمتی یافت نشد.</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4" dir="rtl">
      <h1 className="text-4xl font-bold mb-6">{service.title}</h1>

      {/* جزئیات تراکنش */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
        <div className="flex items-center justify-center">
          {service.transaction_screenshot ? (
            <img
              src={service.transaction_screenshot}
              alt="تصویر تراکنش"
              className="w-24 h-24 object-cover rounded"
            />
          ) : (
            <div className="w-24 h-24 bg-gray-300 flex items-center justify-center">
              <span className="text-xs text-gray-600">تصویری موجود نیست</span>
            </div>
          )}
        </div>
        <div>
          <p>
            <span className="font-semibold">روش پرداخت:</span> {service.payment_method}
          </p>
          <p>
            <span className="font-semibold">وضعیت پرداخت:</span> {service.payment_status_display} ({service.payment_status})
          </p>
        </div>
        <div>
          <p>
            <span className="font-semibold">زمان سپری شده:</span> {service.time_elapsed} ثانیه
          </p>
          <p>
            <span className="font-semibold">امتیاز کلی:</span> {service.overall_score !== null ? service.overall_score : "بدون امتیاز"}
          </p>
        </div>
      </div>

      {/* اطلاعات پایه خدمت */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
        <div>
          <p>
            <span className="font-semibold">شرکت:</span> {service.company}
          </p>
          <p>
            <span className="font-semibold">ارائه‌دهنده:</span> {service.service_provider}
          </p>
          <p>
            <span className="font-semibold">آدرس گیرنده:</span> {service.recipient_address}
          </p>
          <p>
            <span className="font-semibold">کارت شرکت:</span> {service.company_card ? service.company_card : "ناموجود"}
          </p>
        </div>
        <div>
          <p>
            <span className="font-semibold">اسلاگ:</span> {service.slug}
          </p>
          <p>
            <span className="font-semibold">وضعیت خدمت:</span> {service.service_status_display} ({service.service_status})
          </p>
          <p>
            <span className="font-semibold">فاکتور شده:</span> {service.is_invoiced ? "بله" : "خیر"}
          </p>
        </div>
      </div>

      {/* تاریخ و زمان */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
        <div>
          <p>
            <span className="font-semibold">زمان شروع:</span> {new Date(service.started_at).toLocaleString("fa-IR")}
          </p>
          <p>
            <span className="font-semibold">زمان پایان:</span> {new Date(service.finished_at).toLocaleString("fa-IR")}
          </p>
        </div>
        <div>
          <p>
            <span className="font-semibold">ایجاد شده:</span> {new Date(service.created_at).toLocaleString("fa-IR")}
          </p>
          <p>
            <span className="font-semibold">به‌روزرسانی شده:</span> {new Date(service.updated_at).toLocaleString("fa-IR")}
          </p>
        </div>
      </div>

      {/* توضیحات */}
      <p className="mb-4">
        <span className="font-semibold">توضیحات:</span> {service.descriptions}
      </p>

      <div>
        <Link
          href="/services"
          className="inline-block px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          بازگشت به خدمات
        </Link>
      </div>
    </div>
  );
}
