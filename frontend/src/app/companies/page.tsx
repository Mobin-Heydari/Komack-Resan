"use client";

import { useState, useEffect } from "react";
import { Company } from "@/types/companies";
import { useRouter } from "next/router";


export default function Companies() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch("http://127.0.0.1:8000/companies/company/");
        const data: Company[] = await res.json();
        setCompanies(data);
      } catch (error) {
        console.error("Error fetching companies:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <p className="text-xl">Loading...</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6 text-center">Companies</h1>
      {companies.length === 0 ? (
        <p className="text-center text-gray-600">No companies found.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {companies.map((company) => (
            <div
              key={company.id}
              className="bg-white shadow-md rounded-lg overflow-hidden"
            >
              {company.banner ? (
                <img
                  src={company.banner}
                  alt={`${company.name} Banner`}
                  className="w-full h-40 object-cover"
                />
              ) : (
                <div className="w-full h-40 bg-gray-200 flex items-center justify-center">
                  <span className="text-gray-500">No Banner</span>
                </div>
              )}
              <div className="p-4">
                <a className="text-xl font-semibold mb-2" href={`companies/${company.slug}`}>{company.name}</a>
                <p className="text-gray-600 text-sm">{company.description}</p>
                {company.website && (
                  <a
                    href={company.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-500 hover:underline mt-2 inline-block"
                  >
                    Visit Website
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
