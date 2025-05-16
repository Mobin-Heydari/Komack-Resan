"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";

interface ServiceRequest {
  company_slug: string;
  recipient_address_id: string;
  title: string;
  slug: string;
  descriptions: string;
}

export default function ServiceRequestForm() {
  // Extract the slug from the URL and ensure it's a string.
  const { slug } = useParams();
  const extractedSlug = Array.isArray(slug) ? slug[0] : slug ?? "";

  // Initialize the form state with company_slug prefilled.
  const [formData, setFormData] = useState<ServiceRequest>({
    company_slug: extractedSlug,
    recipient_address_id: "",
    title: "",
    slug: "",
    descriptions: "",
  });

  // If the slug updates, update the formData accordingly.
  useEffect(() => {
    setFormData((prev) => ({ ...prev, company_slug: extractedSlug }));
  }, [extractedSlug]);

  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSubmitting(true);
    setSubmitted(false);

    try {
      // Adjust the URL below to your actual service request API endpoint.
      const res = await fetch("http://127.0.0.1:8000/services/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        throw new Error("Failed to submit service request.");
      }

      setSubmitted(true);

      // Reset the form fields; the company_slug stays pre-filled.
      setFormData({
        company_slug: extractedSlug,
        recipient_address_id: "",
        title: "",
        slug: "",
        descriptions: "",
      });
    } catch (error) {
      console.error("Error submitting service request:", error);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto my-8 p-6 bg-white rounded shadow-lg">
      <h2 className="text-2xl font-bold mb-4">Request Service</h2>

      {submitted && (
        <div className="mb-4 p-4 bg-green-100 text-green-700 rounded">
          Your service request has been submitted successfully!
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* company_slug is automatically set from the URL and is hidden */}
        <input type="hidden" name="company_slug" value={formData.company_slug} />

        <div>
          <label
            htmlFor="recipient_address_id"
            className="block text-sm font-medium text-gray-700"
          >
            Recipient Address ID
          </label>
          <input
            type="text"
            name="recipient_address_id"
            id="recipient_address_id"
            value={formData.recipient_address_id}
            onChange={handleChange}
            required
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label
            htmlFor="title"
            className="block text-sm font-medium text-gray-700"
          >
            Title
          </label>
          <input
            type="text"
            name="title"
            id="title"
            value={formData.title}
            onChange={handleChange}
            required
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label
            htmlFor="slug"
            className="block text-sm font-medium text-gray-700"
          >
            Slug
          </label>
          <input
            type="text"
            name="slug"
            id="slug"
            value={formData.slug}
            onChange={handleChange}
            required
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label
            htmlFor="descriptions"
            className="block text-sm font-medium text-gray-700"
          >
            Descriptions
          </label>
          <textarea
            name="descriptions"
            id="descriptions"
            value={formData.descriptions}
            onChange={handleChange}
            required
            rows={4}
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          ></textarea>
        </div>

        <div>
          <button
            type="submit"
            disabled={submitting}
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
          >
            {submitting ? "Submitting..." : "Submit Request"}
          </button>
        </div>
      </form>
    </div>
  );
}
