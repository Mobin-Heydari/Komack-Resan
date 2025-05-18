"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { Invoice } from "@/types/invoices";



export default function InvoiceDetailPage() {
  const { id } = useParams(); // invoice id from URL
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
        console.error("Error fetching invoice details:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchInvoice();
  }, [id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-xl">Loading Invoice Details...</p>
      </div>
    );
  }

  if (!invoice) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-xl text-gray-500">Invoice not found.</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      {/* Invoice Header */}
      <div className="mb-6 border-b pb-4">
        <h1 className="text-4xl font-bold mb-2">{invoice.company} Invoice</h1>
        <div className="text-lg text-gray-700">
          <p>
            <span className="font-semibold">Invoice ID:</span> {invoice.id}
          </p>
          <p>
            <span className="font-semibold">Status:</span>{" "}
            {invoice.is_paid ? "Paid" : "Not Paid"}
          </p>
        </div>
      </div>

      {/* Invoice Financial Summary */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2">Financial Summary</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <p>
            <span className="font-semibold">Total Amount:</span>{" "}
            {invoice.total_amount.toLocaleString()} تومان
          </p>
          <p>
            <span className="font-semibold">Deadline:</span>{" "}
            {new Date(invoice.deadline).toLocaleString()}
          </p>
          <p>
            <span className="font-semibold">Deadline Status:</span>{" "}
            {invoice.deadline_status}
          </p>
        </div>
      </div>

      {/* Timestamps */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2">Timestamps</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <p>
            <span className="font-semibold">Created At:</span>{" "}
            {new Date(invoice.created_at).toLocaleString()}
          </p>
          <p>
            <span className="font-semibold">Updated At:</span>{" "}
            {new Date(invoice.updated_at).toLocaleString()}
          </p>
        </div>
      </div>

      {/* Invoice Items */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-4">Invoice Items</h2>
        {invoice.items.length === 0 ? (
          <p className="text-gray-600">No items available.</p>
        ) : (
          <div className="space-y-4">
            {invoice.items.map((item, index) => (
              <div
                key={index}
                className="p-4 border rounded-md shadow-sm bg-gray-50"
              >
                <p>
                  <span className="font-semibold">Service:</span> {item.service}
                </p>
                <p>
                  <span className="font-semibold">Amount:</span>{" "}
                  {item.amount.toLocaleString()} تومان
                </p>
                <p>
                  <span className="font-semibold">Item Created:</span>{" "}
                  {new Date(item.created_at).toLocaleString()}
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
          Back to Invoices
        </Link>
      </div>
    </div>
  );
}
