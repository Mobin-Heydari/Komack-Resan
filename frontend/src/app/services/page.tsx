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
        console.error("Error fetching services:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchServices();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-xl">Loading Services...</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-4xl font-bold mb-8 text-center">Services</h1>
      {services.length === 0 ? (
        <p className="text-center text-gray-600">No services available.</p>
      ) : (
        <div className="grid grid-cols-1 gap-8">
          {services.map((service) => (
            <div
              key={service.id}
              className="bg-white shadow-lg rounded-lg overflow-hidden"
            >
              <div className="p-6">
                {/* Basic Info */}
                <div className="mb-4">
                  <h2 className="text-3xl font-bold">{service.title}</h2>
                  <p className="text-gray-600">{service.descriptions}</p>
                </div>

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
                      {service.payment_status_display} (
                      {service.payment_status})
                    </p>
                  </div>
                  <div>
                    <p>
                      <span className="font-semibold">Time Elapsed:</span>{" "}
                      {service.time_elapsed} sec
                    </p>
                    <p>
                      <span className="font-semibold">Overall Score:</span>{" "}
                      {service.overall_score !== null
                        ? service.overall_score
                        : "N/A"}
                    </p>
                  </div>
                </div>

                {/* Service Basic Info Grid */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                  <div>
                    <p>
                      <span className="font-semibold">Company:</span>{" "}
                      {service.company}
                    </p>
                    <p>
                      <span className="font-semibold">Provider:</span>{" "}
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
                      {service.service_status_display} (
                      {service.service_status})
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

                <div className="mt-6">
                  <Link
                    href={`/services/${service.slug}`}
                    className="inline-block px-6 py-2 bg-green-600 text-white rounded hover:bg-green-500"
                  >
                    View Details
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
