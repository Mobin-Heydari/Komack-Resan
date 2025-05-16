"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation"; // For the App Router; if using pages directory, use next/router instead
import { Company } from "@/types/companies";

export default function CompanyDetail() {
  // Get the slug from the URL params
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
        console.error("Error fetching company details:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [slug]);

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <p className="text-xl">Loading...</p>
      </div>
    );
  }

  if (!company) {
    return (
      <div className="flex h-screen items-center justify-center">
        <p className="text-xl text-gray-500">Company not found.</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-4xl font-bold mb-6">{company.name}</h1>
      {company.banner ? (
        <img
          src={company.banner}
          alt={`${company.name} banner`}
          className="w-full h-64 object-cover rounded-md shadow-md mb-6"
        />
      ) : (
        <div className="w-full h-64 bg-gray-300 flex items-center justify-center rounded-md shadow-md mb-6">
          <span className="text-gray-600">No Banner Available</span>
        </div>
      )}
      <p className="text-gray-700 text-lg mb-4">{company.description}</p>
      <div className="mb-4">
        <span className="font-semibold">Founded:</span> {company.founded_date}
      </div>
      <div className="mb-4">
        <span className="font-semibold">Service Type:</span> {company.service_type}
      </div>
      <div className="mb-4">
        <span className="font-semibold">Email:</span> {company.email}
      </div>
      <div className="mb-4">
        <span className="font-semibold">Phone Number:</span> {company.phone_number}
      </div>
      {company.website && (
        <a
          href={company.website}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-500"
        >
          Visit Website
        </a>
      )}
    </div>
  );
}
