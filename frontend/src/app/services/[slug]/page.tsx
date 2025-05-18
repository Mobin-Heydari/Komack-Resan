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
        console.error("Error fetching service details:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchService();
  }, [slug]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-xl">Loading Service Details...</p>
      </div>
    );
  }

  if (!service) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-xl text-gray-500">Service not found.</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-4xl font-bold mb-6">{service.title}</h1>

      {/* Transaction Details (Small Grid) */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
        <div className="flex items-center justify-center">
          {service.transaction_screenshot ? (
            <img
              src={service.transaction_screenshot}
              alt="Transaction"
              className="w-24 h-24 object-cover rounded"
            />
          ) : (
            <div className="w-24 h-24 bg-gray-300 flex items-center justify-center">
              <span className="text-xs text-gray-600">No Image</span>
            </div>
          )}
        </div>
        <div>
          <p>
            <span className="font-semibold">Payment Method:</span>{" "}
            {service.payment_method}
          </p>
          <p>
            <span className="font-semibold">Payment Status:</span>{" "}
            {service.payment_status_display} ({service.payment_status})
          </p>
        </div>
        <div>
          <p>
            <span className="font-semibold">Time Elapsed:</span>{" "}
            {service.time_elapsed} sec
          </p>
          <p>
            <span className="font-semibold">Overall Score:</span>{" "}
            {service.overall_score !== null ? service.overall_score : "N/A"}
          </p>
        </div>
      </div>

      {/* Service Basic Info */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
        <div>
          <p>
            <span className="font-semibold">Company:</span> {service.company}
          </p>
          <p>
            <span className="font-semibold">Service Provider:</span>{" "}
            {service.service_provider}
          </p>
          <p>
            <span className="font-semibold">Recipient Address:</span>{" "}
            {service.recipient_address}
          </p>
          <p>
            <span className="font-semibold">Company Card:</span>{" "}
            {service.company_card ? service.company_card : "N/A"}
          </p>
        </div>
        <div>
          <p>
            <span className="font-semibold">Slug:</span> {service.slug}
          </p>
          <p>
            <span className="font-semibold">Service Status:</span>{" "}
            {service.service_status_display} ({service.service_status})
          </p>
          <p>
            <span className="font-semibold">Invoiced:</span>{" "}
            {service.is_invoiced ? "Yes" : "No"}
          </p>
        </div>
      </div>

      {/* Date and Time Details */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
        <div>
          <p>
            <span className="font-semibold">Started At:</span>{" "}
            {new Date(service.started_at).toLocaleString()}
          </p>
          <p>
            <span className="font-semibold">Finished At:</span>{" "}
            {new Date(service.finished_at).toLocaleString()}
          </p>
        </div>
        <div>
          <p>
            <span className="font-semibold">Created At:</span>{" "}
            {new Date(service.created_at).toLocaleString()}
          </p>
          <p>
            <span className="font-semibold">Updated At:</span>{" "}
            {new Date(service.updated_at).toLocaleString()}
          </p>
        </div>
      </div>

      <p className="mb-4">
        <span className="font-semibold">Descriptions:</span> {service.descriptions}
      </p>

      <div>
        <Link
          href="/services"
          className="inline-block px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Back to Services
        </Link>
      </div>
    </div>
  );
}
