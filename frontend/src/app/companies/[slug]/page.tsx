"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { Company } from "@/types/companies";
import ServiceRequestForm from "@/components/serviceRequestForm";

export default function CompanyDetail() {
  const { slug } = useParams();
  const [company, setCompany] = useState<Company | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      if (!slug) return;
      try {
        const res = await fetch(`http://127.0.0.1:8000/companies/company/${slug}/`);
        const data: Company = await res.json();
        setCompany(data);
      } catch (error) {
        console.error("خطا در دریافت جزییات شرکت:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [slug]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen" dir="rtl">
        <p className="text-xl">در حال بارگذاری...</p>
      </div>
    );
  }

  if (!company) {
    return (
      <div className="flex items-center justify-center h-screen" dir="rtl">
        <p className="text-xl text-gray-500">شرکتی یافت نشد.</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4" dir="rtl">
      {/* Header */}
      <div className="bg-white shadow-lg rounded-lg p-6 mb-6">
        <h1 className="text-4xl font-bold">{company.name}</h1>
        <p className="text-gray-600 mt-2">{company.description}</p>
        <div className="mt-4 flex flex-wrap gap-4">
          {company.website && (
            <a
              href={company.website}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-500"
            >
              مشاهده وبسایت
            </a>
          )}
          {company.linkedin && (
            <a
              href={company.linkedin}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 bg-blue-700 text-white rounded hover:bg-blue-600"
            >
              لینکدین
            </a>
          )}
          {company.twitter && (
            <a
              href={company.twitter}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-400"
            >
              توییتر
            </a>
          )}
          {company.instagram && (
            <a
              href={company.instagram}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 bg-pink-500 text-white rounded hover:bg-pink-400"
            >
              اینستاگرام
            </a>
          )}
        </div>
      </div>

      {/* Banner */}
      {company.banner ? (
        <img
          src={company.banner}
          alt={`بنر ${company.name}`}
          className="w-full h-64 object-cover rounded-md shadow-md mb-6"
        />
      ) : (
        <div className="w-full h-64 bg-gray-300 flex items-center justify-center rounded-md shadow-md mb-6">
          <span className="text-gray-600">بنری موجود نیست</span>
        </div>
      )}

      {/* Basic Info */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">اطلاعات شرکت</h2>
          <p><strong>سال تاسیس:</strong> {company.founded_date}</p>
          <p><strong>نوع خدمات:</strong> {company.service_type}</p>
          <p><strong>ایمیل:</strong> {company.email}</p>
          <p><strong>تلفن:</strong> {company.phone_number}</p>
          <p><strong>کد پستی:</strong> {company.postal_code}</p>
          <p><strong>صنعت:</strong> {company.industry}</p>
        </div>

        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">جزئیات اعتبارسنجی</h2>
          <p><strong>تایید کننده:</strong> {company.validation_status.validated_by}</p>
          <p><strong>وضعیت کلی:</strong> {company.validation_status.overall_status}</p>
          <p><strong>یادداشت‌ها:</strong> {company.validation_status.validation_notes}</p>
          {company.validation_status.business_license && (
            <img
              src={company.validation_status.business_license}
              alt="مجوز کسب و کار"
              className="w-full h-40 object-cover rounded-md shadow-md mt-4"
            />
          )}
        </div>
      </div>

      {/* ویژگی‌های اصلی */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-4">ویژگی‌های اصلی</h2>
        <div className="flex flex-row gap-4 overflow-x-auto">
          {company.companies_first_item.length > 0 ? (
            company.companies_first_item.map((item) => (
              <div key={item.id} className="bg-gray-100 p-4 rounded shadow-sm min-w-max">
                <h3 className="text-lg font-medium">{item.first_item.name}</h3>
                <p className="text-sm text-gray-600">اسلاگ: {item.first_item.slug}</p>
              </div>
            ))
          ) : (
            <p className="text-gray-500">هیچ ویژگی اصلی موجود نیست.</p>
          )}
        </div>
      </div>

      {/* ویژگی‌های ثانویه */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-4">ویژگی‌های ثانویه</h2>
        <div className="flex flex-row gap-4 overflow-x-auto">
          {company.companies_second_item.length > 0 ? (
            company.companies_second_item.map((item) => (
              <div key={item.id} className="bg-gray-100 p-4 rounded shadow-sm min-w-max">
                <h3 className="text-lg font-medium">{item.second_item.name}</h3>
                <p className="text-sm text-gray-600">اسلاگ: {item.second_item.slug}</p>
              </div>
            ))
          ) : (
            <p className="text-gray-500">هیچ ویژگی ثانویه موجود نیست.</p>
          )}
        </div>
      </div>

      {/* روزهای کاری */}
      {company.workdays && company.workdays.length > 0 && (
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-4">روزهای کاری</h2>
          <div className="flex flex-row gap-4 overflow-x-auto">
            {company.workdays.map((day, index) => (
              <div key={index} className="bg-gray-100 p-4 rounded shadow-sm min-w-max">
                <p className="font-bold">{day.day_of_week_display}</p>
                <p>{day.is_closed ? "تعطیل" : `از ${day.open_time} تا ${day.close_time}`}</p>
                <p className="text-xs text-gray-600">
                  {day.is_open_now ? "اکنون باز است" : "اکنون بسته است"}
                </p>
                <p className="text-xs text-gray-600">مدت: {day.time_range}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* فرم درخواست خدمت */}
      <ServiceRequestForm />
    </div>
  );
}
