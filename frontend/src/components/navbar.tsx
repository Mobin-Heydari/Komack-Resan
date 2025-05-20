"use client";

import { useState } from "react";
import Link from "next/link";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  // Toggle the mobile menu state
  const toggleMenu = () => setIsOpen(!isOpen);

  return (
    <nav className="bg-cyan-800" dir="rtl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Main Navigation */}
        <div className="flex justify-between h-16">
          {/* Logo & main links */}
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <Link href="/" className="text-white font-bold text-xl">
                کمک رسان
              </Link>
            </div>
            <div className="hidden md:mr-6 md:flex md:space-x-reverse md:space-x-8">
              <Link
                href="/services"
                className="text-white inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-cyan-300"
              >
                خدمات
              </Link>
              <Link
                href="/companies"
                className="text-white inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-cyan-300"
              >
                شرکت‌ها
              </Link>
              <Link
                href="/invoices"
                className="text-white inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-cyan-300"
              >
                فاکتورها
              </Link>
            </div>
          </div>
          {/* Right-side links for login/register */}
          <div className="flex items-center">
            <div className="hidden md:flex md:items-center md:space-x-reverse md:space-x-4">
              <Link href="/auth/login" className="text-white hover:text-cyan-300">
                ورود
              </Link>
              <Link href="/auth/register" className="text-white hover:text-cyan-300">
                ثبت نام
              </Link>
            </div>
            {/* Mobile menu button */}
            <div className="-ml-2 flex md:hidden">
              <button
                onClick={toggleMenu}
                type="button"
                className="bg-cyan-700 inline-flex items-center justify-center p-2 rounded-md text-gray-200 hover:text-white hover:bg-cyan-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-cyan-800 focus:ring-white"
              >
                <span className="sr-only">باز کردن منو</span>
                {isOpen ? (
                  <svg
                    className="block h-6 w-6"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M18 6L6 18M6 6l12 12"
                    />
                  </svg>
                ) : (
                  <svg
                    className="block h-6 w-6"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M4 6h16M4 12h16M4 18h16"
                    />
                  </svg>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden">
          <div className="pt-2 pb-3 space-y-1">
            <Link
              href="/services"
              className="block pr-4 pl-3 py-2 border-l-4 border-transparent text-white hover:bg-cyan-700 hover:border-cyan-300"
            >
              خدمات
            </Link>
            <Link
              href="/companies"
              className="block pr-4 pl-3 py-2 border-l-4 border-transparent text-white hover:bg-cyan-700 hover:border-cyan-300"
            >
              شرکت‌ها
            </Link>
            <Link
              href="/invoices"
              className="block pr-4 pl-3 py-2 border-l-4 border-transparent text-white hover:bg-cyan-700 hover:border-cyan-300"
            >
              فاکتورها
            </Link>
          </div>
          <div className="pt-4 pb-3 border-t border-cyan-700">
            <div className="space-y-1">
              <Link
                href="/auth/login"
                className="block pr-4 pl-3 py-2 border-l-4 border-transparent text-white hover:bg-cyan-700 hover:border-cyan-300"
              >
                ورود
              </Link>
              <Link
                href="/auth/register"
                className="block pr-4 pl-3 py-2 border-l-4 border-transparent text-white hover:bg-cyan-700 hover:border-cyan-300"
              >
                ثبت نام
              </Link>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}
