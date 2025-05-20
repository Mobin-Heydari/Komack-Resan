"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function RegisterPage() {
  const router = useRouter();

  // وضعیت‌های فرم ثبت نام
  const [phone, setPhone] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [username, setUsername] = useState<string>("");
  const [userType, setUserType] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [passwordConf, setPasswordConf] = useState<string>("");
  const [fullName, setFullName] = useState<string>("");
  const [error, setError] = useState<string>("");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");

    // چک اولیه برای همسان بودن رمز عبور و تأیید آن
    if (password !== passwordConf) {
      setError("رمز عبور و تأیید آن مطابقت ندارند.");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/auth/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          phone,
          email,
          username,
          user_type: userType,
          password,
          full_name: fullName,
          password_conf: passwordConf,
        }),
      });
      const data = await res.json();
      if (res.ok && data.Detail.token && data.Detail.code) {
        // ریدایرکت به صفحه تأیید OTP:
        // کد یکبارمصرف را در querystring ارسال می‌کنیم (برای تست)
        router.push(
          `/auth/register/otp/${data.Detail.token}?code=${data.Detail.code}`
        );
      } else {
        setError(data.error || "ثبت نام ناموفق بود!");
      }
    } catch (err) {
      setError("خطایی در هنگام ثبت نام رخ داد.");
    }
  };

  return (
    <div
      className="max-w-md mx-auto p-6 mt-10 bg-white shadow rounded"
      dir="rtl"
    >
      <h1 className="text-2xl font-bold text-center mb-4">ثبت نام</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="phone" className="block mb-1">شماره تلفن:</label>
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
          <label htmlFor="email" className="block mb-1">ایمیل:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="username" className="block mb-1">نام کاربری:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="userType" className="block mb-1">نوع کاربر:</label>
          <select
            id="userType"
            value={userType}
            onChange={(e) => setUserType(e.target.value)}
            className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="SC">سرویس گیرنده</option>
            <option value="SP">سرویس دهنده</option>
            <option value="OW">مالک</option>
          </select>
        </div>
        <div className="mb-4">
          <label htmlFor="password" className="block mb-1">رمز عبور:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="passwordConf" className="block mb-1">تأیید رمز عبور:</label>
          <input
            type="password"
            id="passwordConf"
            value={passwordConf}
            onChange={(e) => setPasswordConf(e.target.value)}
            required
            className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="fullName" className="block mb-1">نام کامل:</label>
          <input
            type="text"
            id="fullName"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            required
            className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button
          type="submit"
          className="w-full py-2 px-4 bg-blue-600 text-white font-semibold rounded hover:bg-blue-700 transition-colors"
        >
          ثبت نام
        </button>
      </form>
      {error && <p className="mt-4 text-red-500">{error}</p>}
      <p className="text-center mt-4">
        قبلاً ثبت‌نام کرده‌اید؟{" "}
        <a href="/auth/login" className="text-blue-600 hover:underline">
          ورود به سیستم
        </a>
      </p>
    </div>
  );
}
