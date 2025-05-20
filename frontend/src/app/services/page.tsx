"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Service } from "@/types/services";

export default function ServicesList() {
  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchServices() {
      try {
        const res = await fetch("http://127.0.0.1:8000/services/service/");
        const data: Service[] = await res.json();
        setServices(data);
      } catch (error) {
        console.error("خطا در دریافت خدمات:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchServices();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen" dir="rtl">
        <p className="text-xl">در حال بارگذاری خدمات...</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4" dir="rtl">
      <h1 className="text-4xl font-bold mb-8 text-center">خدمات</h1>
      {services.length === 0 ? (
        <p className="text-center text-gray-600">هیچ خدماتی موجود نیست.</p>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {services.map((service) => (
            <div
              key={service.id}
              className="bg-white shadow rounded p-4 flex justify-between items-center"
            >
              <span className="text-xl">{service.title}</span>
              <Link
                href={`/services/${service.slug}`}
                className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-500"
              >
                مشاهده
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
