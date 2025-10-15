import React, { useState } from "react";
import { SunIcon, MoonIcon } from "@heroicons/react/24/outline";

export default function AuthLayout({ children, title }) {
  const [isDarkMode, setIsDarkMode] = useState(false);

  return (
    <div className={`min-h-screen flex ${isDarkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
      {/* Left Side - Branding/Info */}
      <div className={`hidden lg:flex lg:w-1/2 relative overflow-hidden ${
        isDarkMode 
          ? 'bg-gradient-to-br from-gray-900 via-gray-800 to-black' 
          : 'bg-gradient-to-br from-green-900 via-green-800 to-emerald-900'
        }`}>
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-96 h-96 bg-white rounded-full -translate-x-1/2 -translate-y-1/2"></div>
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-white rounded-full translate-x-1/2 translate-y-1/2"></div>
          <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-yellow-400 rounded-full -translate-x-1/2 -translate-y-1/2 blur-3xl"></div>
        </div>

        {/* Content */}
        <div className="relative z-10 flex flex-col justify-center px-16 text-white">
          <div className="mb-8">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-16 h-16 bg-gradient-to-br from-yellow-400 to-amber-500 rounded-xl flex items-center justify-center shadow-2xl">
                <svg className="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z"/>
                  <path fillRule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clipRule="evenodd"/>
                </svg>
              </div>
              <div>
                <h1 className="text-3xl font-bold">Wild Bank</h1>
                <p className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-green-200'}`}>
                  Liberte suas finanças
                </p>
              </div>
            </div>

            <h2 className="text-4xl font-bold mb-4 leading-tight">
              A Nova Era da<br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-amber-500">
                Liberdade Financeira
              </span>
            </h2>
            <p className={`text-lg mb-8 ${isDarkMode ? 'text-gray-300' : 'text-green-100'}`}>
              Revolucione a forma como você gerencia seu dinheiro. Simples, rápido e totalmente seguro.
            </p>
          </div>

          {/* Features */}
          <div className="space-y-4">
            <div className="flex items-center gap-3 group hover:translate-x-2 transition-transform duration-300">
              <div className={`w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0 ${
                isDarkMode 
                  ? 'bg-gradient-to-br from-green-400 to-emerald-600' 
                  : 'bg-white bg-opacity-10'
                } group-hover:scale-110 transition-transform`}>
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <div>
                <h3 className="font-bold text-lg">Segurança Militar</h3>
                <p className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-green-200'}`}>
                  Proteção de nível bancário com criptografia de ponta a ponta
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3 group hover:translate-x-2 transition-transform duration-300">
              <div className={`w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0 ${
                isDarkMode 
                  ? 'bg-gradient-to-br from-yellow-400 to-amber-600' 
                  : 'bg-white bg-opacity-10'
                } group-hover:scale-110 transition-transform`}>
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div>
                <h3 className="font-bold text-lg">Velocidade Extrema</h3>
                <p className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-green-200'}`}>
                  Transações instantâneas sem burocracia, 24h por dia
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3 group hover:translate-x-2 transition-transform duration-300">
              <div className={`w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0 ${
                isDarkMode 
                  ? 'bg-gradient-to-br from-green-400 to-teal-600' 
                  : 'bg-white bg-opacity-10'
                } group-hover:scale-110 transition-transform`}>
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <div>
                <h3 className="font-bold text-lg">Inteligência Total</h3>
                <p className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-green-200'}`}>
                  Dashboard inteligente com insights poderosos sobre seu dinheiro
                </p>
              </div>
            </div>
          </div>

          {/* Testimonial/Stats */}
          <div className="mt-12 pt-8 border-t border-white border-opacity-20">
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <p className="text-3xl font-bold text-yellow-400">99.9%</p>
                <p className={`text-xs mt-1 ${isDarkMode ? 'text-gray-400' : 'text-green-200'}`}>Uptime</p>
              </div>
              <div>
                <p className="text-3xl font-bold text-yellow-400">50k+</p>
                <p className={`text-xs mt-1 ${isDarkMode ? 'text-gray-400' : 'text-green-200'}`}>Usuários</p>
              </div>
              <div>
                <p className="text-3xl font-bold text-yellow-400">4.9★</p>
                <p className={`text-xs mt-1 ${isDarkMode ? 'text-gray-400' : 'text-green-200'}`}>Avaliação</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side - Form */}
      <div className={`flex-1 flex items-center justify-center p-8 lg:p-16 relative ${
        isDarkMode ? 'bg-gray-900' : 'bg-gray-50'
      }`}>
        {/* Theme Toggle */}
        <button
          onClick={() => setIsDarkMode(!isDarkMode)}
          className={`absolute top-6 right-6 p-3 rounded-full shadow-lg transition-all hover:scale-110 ${
            isDarkMode 
              ? 'bg-gray-800 text-yellow-400 hover:bg-gray-700' 
              : 'bg-white text-gray-700 hover:bg-gray-100'
          }`}
          title={isDarkMode ? "Modo Claro" : "Modo Escuro"}
        >
          {isDarkMode ? (
            <SunIcon className="w-6 h-6" />
          ) : (
            <MoonIcon className="w-6 h-6" />
          )}
        </button>

        <div className="w-full max-w-md">
          {/* Logo for mobile */}
          <div className="lg:hidden mb-8 text-center">
            <div className="inline-flex items-center gap-2 mb-2">
              <div className="w-10 h-10 bg-gradient-to-br from-yellow-400 to-amber-500 rounded-lg flex items-center justify-center shadow-lg">
                <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z"/>
                  <path fillRule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clipRule="evenodd"/>
                </svg>
              </div>
              <span className={`text-2xl font-bold ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>
                Wild Bank
              </span>
            </div>
          </div>

          {/* Form Card */}
          <div className={`rounded-2xl shadow-2xl border p-8 ${
            isDarkMode 
              ? 'bg-gray-800 border-gray-700' 
              : 'bg-white border-gray-200'
          }`}>
            <div className="mb-8">
              <h1 className={`text-3xl font-bold mb-2 ${
                isDarkMode ? 'text-white' : 'text-gray-800'
              }`}>
                {title}
              </h1>
              <p className={isDarkMode ? 'text-gray-400' : 'text-gray-600'}>
                {title === "Entrar"
                  ? "Entre na sua conta e comece a liberar seu potencial financeiro"
                  : "Junte-se a milhares de pessoas que já escolheram a liberdade"}
              </p>
            </div>
            {children}
          </div>

          {/* Footer */}
          <div className={`mt-6 text-center text-sm ${
            isDarkMode ? 'text-gray-500' : 'text-gray-500'
          }`}>
            <p>© 2025 Wild Bank. Seu dinheiro, suas regras.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
