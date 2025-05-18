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

        console.log("Fetched data:", data);

        // If the returned data is an array, use it directly.
        if (Array.isArray(data)) {
          setInvoices(data);
        } else if (data && typeof data === "object") {
          // If the API returns a single invoice object or an object with a property,
          // adjust accordingly. For example, if it's a single invoice:
          // setInvoices([data]);
          // If data is wrapped in a property like 'results':
          // setInvoices(data.results || []);

          // Here we'll assume it's not an array and set an empty array.
          setInvoices([]);
        } else {
          setInvoices([]);
        }
      } catch (error) {
        console.error("Error fetching invoices:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchInvoices();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-xl">Loading Invoices...</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-4xl font-bold mb-8 text-center">Invoices</h1>
      {invoices.length === 0 ? (
        <p className="text-center text-gray-600">No invoices available.</p>
      ) : (
        <div className="grid grid-cols-1 gap-8">
          {invoices.map((invoice) => (
            <div
              key={invoice.id}
              className="bg-white shadow-lg rounded-lg overflow-hidden p-6"
            >
              <div className="mb-4">
                <h2 className="text-2xl font-bold">
                  {invoice.company} —&nbsp;
                  {invoice.total_amount.toLocaleString()} تومان
                </h2>
                <p className="text-gray-600">
                  {invoice.is_paid ? "Paid" : "Not Paid"} &bull; Deadline:{" "}
                  {new Date(invoice.deadline).toLocaleString()} (
                  {invoice.deadline_status})
                </p>
              </div>

              <div className="text-sm text-gray-500 mb-4">
                <p>
                  <span className="font-semibold">Created:</span>{" "}
                  {new Date(invoice.created_at).toLocaleString()}
                </p>
                <p>
                  <span className="font-semibold">Updated:</span>{" "}
                  {new Date(invoice.updated_at).toLocaleString()}
                </p>
              </div>

              <Link
                href={`/invoices/${invoice.id}`}
                className="inline-block px-6 py-2 bg-green-600 text-white rounded hover:bg-green-500"
              >
                View Details
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
