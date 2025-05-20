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
      if (res.ok && data.Detail.token && data.Detail.code) {
        router.push(`/auth/login/otp/${data.Detail.token}?code=${data.Detail.code}`);
      } else {
        setError(data.error || "درخواست کد یکبارمصرف ناموفق بود!");
      }

    } catch (err) {
      setError("خطایی در درخواست کد یکبارمصرف رخ داد.");
    }
  };

  return (
    <div
      className="max-w-md mx-auto p-6 mt-10 bg-white shadow rounded"
      dir="rtl"
    >
      <h1 className="text-2xl font-bold text-center mb-4">
        درخواست ورود با کد یکبارمصرف
      </h1>
      <form onSubmit={handleOTPRequest}>
        <div className="mb-4">
          <label htmlFor="phone" className="block mb-1">
            شماره تلفن:
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
          درخواست کد یکبارمصرف
        </button>
      </form>
      {error && <p className="mt-4 text-red-500">{error}</p>}
    </div>
  );
}
