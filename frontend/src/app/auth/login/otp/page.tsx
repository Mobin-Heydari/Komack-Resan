"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function OTPRequestPage() {
  const router = useRouter();
  const [phone, setPhone] = useState<string>("");
  const [error, setError] = useState<string>("");

  const handleOTPRequest = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/auth/login/otp/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone }),
      });
      const data = await res.json();
      if (res.ok && data.Details.token && data.Details.code) {
        // Redirect with the token as a path parameter and the OTP code as a query param for testing.
        router.push(`/auth/login/otp/${data.Details.token}?code=${data.Details.code}`);
      } else {
        setError(data.error || "OTP request failed!");
    }
    } catch (err) {
        setError("An error occurred while requesting OTP.");
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 mt-10 bg-white shadow rounded">
      <h1 className="text-2xl font-bold text-center mb-4">OTP Login Request</h1>
      <form onSubmit={handleOTPRequest}>
        <div className="mb-4">
          <label htmlFor="phone" className="block mb-1">
            Phone:
          </label>
          <input
            type="text"
            id="phone"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            required
            className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button
          type="submit"
          className="w-full py-2 px-4 bg-blue-600 text-white font-semibold rounded hover:bg-blue-700 transition-colors"
        >
          Request OTP
        </button>
      </form>
      {error && <p className="mt-4 text-red-500">{error}</p>}
    </div>
  );
}
