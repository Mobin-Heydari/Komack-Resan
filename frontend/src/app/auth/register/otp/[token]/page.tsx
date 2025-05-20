"use client";

import { useState } from "react";
import { useRouter, useParams, useSearchParams } from "next/navigation";

export default function RegistrationOTPVerificationPage() {
  const router = useRouter();
  const { token } = useParams();
  const searchParams = useSearchParams();
  // برای تست: دریافت کد یکبارمصرف از طریق پارامتر query
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
        // در صورت موفقیت‌آمیز بودن تأیید کد، کاربر به داشبورد یا صفحه ورود هدایت می‌شود.
        router.push("/");
      } else {
        setError(data.error || "تأیید کد یکبارمصرف ناموفق بود!");
      }
    } catch (err) {
      setError("خطایی در هنگام تأیید کد یکبارمصرف رخ داد.");
    }
  };

  return (
    <div
      className="max-w-md mx-auto p-6 mt-10 bg-white shadow rounded"
      dir="rtl"
    >
      <h1 className="text-2xl font-bold text-center mb-4">تأیید کد یکبارمصرف</h1>
      <div className="mb-4">
        <p className="text-sm text-gray-600">
          برای تست، کد یکبارمصرف شما:{" "}
          <span className="font-bold">{testOTP}</span>
        </p>
      </div>
      <form onSubmit={handleOTPVerification}>
        <div className="mb-4">
          <label htmlFor="code" className="block mb-1">کد یکبارمصرف را وارد کنید:</label>
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
          تأیید کد
        </button>
      </form>
      {error && <p className="mt-4 text-red-500">{error}</p>}
    </div>
  );
}
