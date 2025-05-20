"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function PasswordLoginPage() {
  const router = useRouter();
  const [phone, setPhone] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string>("");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/auth/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone, password }),
      });
      const data = await res.json();
      if (res.ok) {
        // هدایت کاربر به داشبورد در صورت موفقیت‌آمیز بودن ورود
        router.push("/");
      } else {
        setError(data.error || "ورود ناموفق بود!");
      }
    } catch (err) {
      setError("خطایی در هنگام ورود رخ داد.");
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 mt-10 bg-white shadow rounded" dir="rtl">
      <h1 className="text-2xl font-bold text-center mb-4">ورود به سیستم</h1>
      <form onSubmit={handleSubmit}>
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
        <div className="mb-4">
          <label htmlFor="password" className="block mb-1">
            رمز عبور:
          </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button
          type="submit"
          className="w-full py-2 px-4 bg-blue-600 text-white font-semibold rounded hover:bg-blue-700 transition-colors"
        >
          ورود
        </button>
      </form>
      {error && <p className="mt-4 text-red-500">{error}</p>}
      <p className="text-center mt-4">
        ثبت نام نکرده‌اید؟{" "}
        <a href="/register" className="text-blue-600 hover:underline">
          ثبت نام
        </a>
      </p>
    </div>
  );
}
