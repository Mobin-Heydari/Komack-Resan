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
        console.error("Error fetching company details:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [slug]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-xl">Loading...</p>
      </div>
    );
  }

  if (!company) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-xl text-gray-500">Company not found.</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      {/* Company Header */}
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
              Visit Website
            </a>
          )}
          {company.linkedin && (
            <a
              href={company.linkedin}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 bg-blue-700 text-white rounded hover:bg-blue-600"
            >
              LinkedIn
            </a>
          )}
          {company.twitter && (
            <a
              href={company.twitter}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-400"
            >
              Twitter
            </a>
          )}
          {company.instagram && (
            <a
              href={company.instagram}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 bg-pink-500 text-white rounded hover:bg-pink-400"
            >
              Instagram
            </a>
          )}
        </div>
      </div>

      {/* Company Banner */}
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

      {/* Company Basic Info */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Company Information</h2>
          <p><strong>Founded:</strong> {company.founded_date}</p>
          <p><strong>Service Type:</strong> {company.service_type}</p>
          <p><strong>Email:</strong> {company.email}</p>
          <p><strong>Phone:</strong> {company.phone_number}</p>
          <p><strong>Postal Code:</strong> {company.postal_code}</p>
          <p><strong>Industry:</strong> {company.industry}</p>
        </div>

        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Validation Details</h2>
          <p><strong>Validated By:</strong> {company.validation_status.validated_by}</p>
          <p><strong>Overall Status:</strong> {company.validation_status.overall_status}</p>
          <p><strong>Notes:</strong> {company.validation_status.validation_notes}</p>
          {company.validation_status.business_license && (
            <img
              src={company.validation_status.business_license}
              alt="Business License"
              className="w-full h-40 object-cover rounded-md shadow-md mt-4"
            />
          )}
        </div>
      </div>

      {/* Primary Features: Rendered in a row if available */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-4">Primary Features</h2>
        <div className="flex flex-row gap-4 overflow-x-auto">
          {company.companies_first_item.length > 0 ? (
            company.companies_first_item.map((item) => (
              <div key={item.id} className="bg-gray-100 p-4 rounded shadow-sm min-w-max">
                <h3 className="text-lg font-medium">{item.first_item.name}</h3>
                <p className="text-sm text-gray-600">Slug: {item.first_item.slug}</p>
              </div>
            ))
          ) : (
            <p className="text-gray-500">No primary features available.</p>
          )}
        </div>
      </div>

      {/* Secondary Features: Rendered in a row if available */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-4">Secondary Features</h2>
        <div className="flex flex-row gap-4 overflow-x-auto">
          {company.companies_second_item.length > 0 ? (
            company.companies_second_item.map((item) => (
              <div key={item.id} className="bg-gray-100 p-4 rounded shadow-sm min-w-max">
                <h3 className="text-lg font-medium">{item.second_item.name}</h3>
                <p className="text-sm text-gray-600">Slug: {item.second_item.slug}</p>
              </div>
            ))
          ) : (
            <p className="text-gray-500">No secondary features available.</p>
          )}
        </div>
      </div>

      {/* Workdays: Rendered in a row if any exist */}
      {company.workdays && company.workdays.length > 0 && (
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-4">Workdays</h2>
          <div className="flex flex-row gap-4 overflow-x-auto">
            {company.workdays.map((day: any, index: number) => (
              <div key={index} className="bg-gray-100 p-4 rounded shadow-sm min-w-max">
                <p>{day}</p>
              </div>
            ))}
          </div>
        </div>
      )}
      <ServiceRequestForm />
    </div>
  );
}
