"use client";

import { useState } from "react";
import { useRouter, useParams, useSearchParams } from "next/navigation";



export default function RegistrationOTPVerificationPage() {
  const router = useRouter();
  const { token } = useParams();
  const searchParams = useSearchParams();
  // For testing: retrieve the OTP code from the query parameter
  const testOTP = searchParams.get("code") ?? "";
  const [code, setcode] = useState<string>("");
  const [error, setError] = useState<string>("");

  const handleOTPVerification = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/auth/register/validate-otp/${token}/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code }),
        }
      );
      const data = await res.json();
      if (res.ok) {
        // On successful OTP verification, redirect the user to the dashboard or login page.
        router.push("/");
      } else {
        setError(data.error || "OTP verification failed!");
      }
    } catch (err) {
      setError("An error occurred during OTP verification.");
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 mt-10 bg-white shadow rounded">
      <h1 className="text-2xl font-bold text-center mb-4">OTP Verification</h1>
      <div className="mb-4">
        <p className="text-sm text-gray-600">
          For testing, your OTP code is:{" "}
          <span className="font-bold">{testOTP}</span>
        </p>
      </div>
      <form onSubmit={handleOTPVerification}>
        <div className="mb-4">
          <label htmlFor="code" className="block mb-1">Enter OTP:</label>
          <input
            type="text"
            id="code"
            value={code}
            onChange={(e) => setcode(e.target.value)}
            required
            className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button
          type="submit"
          className="w-full py-2 px-4 bg-blue-600 text-white font-semibold rounded hover:bg-blue-700 transition-colors"
        >
          Verify OTP
        </button>
      </form>
      {error && <p className="mt-4 text-red-500">{error}</p>}
    </div>
  );
}
