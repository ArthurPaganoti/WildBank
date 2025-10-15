import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import {
  HomeIcon,
  UserIcon,
  CreditCardIcon,
  ChartBarIcon,
  CogIcon,
  ArrowRightOnRectangleIcon,
  BellIcon,
  MagnifyingGlassIcon,
  BanknotesIcon,
  ArrowTrendingUpIcon,
  ShieldCheckIcon,
  ClockIcon,
  SunIcon,
  MoonIcon
} from '@heroicons/react/24/outline';

export default function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [activeMenu, setActiveMenu] = useState('dashboard');
  const [isDarkMode, setIsDarkMode] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: HomeIcon },
    { id: 'profile', label: 'Meu Perfil', icon: UserIcon },
    { id: 'transactions', label: 'Transações', icon: CreditCardIcon },
    { id: 'analytics', label: 'Relatórios', icon: ChartBarIcon },
    { id: 'settings', label: 'Configurações', icon: CogIcon },
  ];

  const stats = [
    { label: 'Saldo Total', value: 'R$ 12.450,00', icon: BanknotesIcon, color: 'bg-green-500', trend: '+12.5%' },
    { label: 'Transações Hoje', value: '24', icon: ArrowTrendingUpIcon, color: 'bg-yellow-500', trend: '+8.2%' },
    { label: 'Segurança', value: 'Ativa', icon: ShieldCheckIcon, color: 'bg-emerald-500', trend: '100%' },
    { label: 'Último Acesso', value: 'Agora', icon: ClockIcon, color: 'bg-amber-500', trend: 'Online' },
  ];

  const recentActivities = [
    { id: 1, type: 'Login', description: 'Login realizado com sucesso', time: 'Agora', status: 'success' },
    { id: 2, type: 'Perfil', description: 'Perfil visualizado', time: 'Há 5 min', status: 'info' },
    { id: 3, type: 'Segurança', description: 'Token JWT renovado', time: 'Há 15 min', status: 'info' },
  ];

  return (
    <div className={`flex h-screen overflow-hidden ${isDarkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
      {/* Sidebar */}
      <aside className={`w-64 text-white flex flex-col shadow-2xl ${
        isDarkMode 
          ? 'bg-gradient-to-b from-gray-900 via-gray-800 to-black border-r border-gray-700' 
          : 'bg-gradient-to-b from-green-900 via-green-800 to-green-900'
      }`}>
        {/* Logo */}
        <div className={`p-6 ${isDarkMode ? 'border-b border-gray-700' : 'border-b border-green-700'}`}>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-yellow-400 to-amber-500 rounded-lg flex items-center justify-center shadow-lg">
              <BanknotesIcon className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold">Wild Bank</h1>
              <p className={`text-xs ${isDarkMode ? 'text-gray-400' : 'text-green-300'}`}>
                Liberte suas finanças
              </p>
            </div>
          </div>
        </div>

        {/* Menu Navigation */}
        <nav className="flex-1 px-4 py-6 space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeMenu === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveMenu(item.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                  isActive
                    ? isDarkMode
                      ? 'bg-yellow-500 text-gray-900 shadow-lg'
                      : 'bg-white text-green-900 shadow-lg'
                    : isDarkMode
                      ? 'text-gray-300 hover:bg-gray-800 hover:text-white'
                      : 'text-green-100 hover:bg-green-800 hover:text-white'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* User Info & Logout */}
        <div className={`p-4 ${isDarkMode ? 'border-t border-gray-700' : 'border-t border-green-700'}`}>
          <div className={`flex items-center gap-3 px-3 py-2 mb-3 rounded-lg ${
            isDarkMode ? 'bg-gray-800' : 'bg-green-800'
          }`}>
            <div className="w-10 h-10 bg-gradient-to-br from-yellow-400 to-amber-500 rounded-full flex items-center justify-center font-bold text-white shadow-lg">
              {user?.nome?.charAt(0).toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-semibold text-sm truncate">{user?.nome}</p>
              <p className={`text-xs truncate ${isDarkMode ? 'text-gray-400' : 'text-green-300'}`}>
                {user?.email}
              </p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition-colors font-medium"
          >
            <ArrowRightOnRectangleIcon className="w-5 h-5" />
            Sair
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        {/* Header */}
        <header className={`shadow-sm border-b sticky top-0 z-10 ${
          isDarkMode 
            ? 'bg-gray-800 border-gray-700' 
            : 'bg-white border-gray-200'
        }`}>
          <div className="px-8 py-4 flex items-center justify-between">
            <div>
              <h2 className={`text-2xl font-bold ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>
                Bem-vindo de volta, {user?.nome}!
              </h2>
              <p className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                Aqui está um resumo da sua conta
              </p>
            </div>
            <div className="flex items-center gap-4">
              {/* Theme Toggle */}
              <button
                onClick={() => setIsDarkMode(!isDarkMode)}
                className={`p-2 rounded-lg shadow-md transition-all hover:scale-110 ${
                  isDarkMode 
                    ? 'bg-gray-700 text-yellow-400 hover:bg-gray-600' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
                title={isDarkMode ? "Modo Claro" : "Modo Escuro"}
              >
                {isDarkMode ? (
                  <SunIcon className="w-6 h-6" />
                ) : (
                  <MoonIcon className="w-6 h-6" />
                )}
              </button>

              {/* Search */}
              <div className="relative">
                <input
                  type="text"
                  placeholder="Pesquisar..."
                  className={`pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 w-64 ${
                    isDarkMode
                      ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400 focus:ring-yellow-500'
                      : 'bg-white border-gray-300 text-gray-900 focus:ring-green-500'
                  }`}
                />
                <MagnifyingGlassIcon className={`w-5 h-5 absolute left-3 top-2.5 ${
                  isDarkMode ? 'text-gray-400' : 'text-gray-400'
                }`} />
              </div>

              {/* Notifications */}
              <button className={`relative p-2 rounded-lg transition-colors ${
                isDarkMode 
                  ? 'text-gray-300 hover:bg-gray-700' 
                  : 'text-gray-600 hover:bg-gray-100'
              }`}>
                <BellIcon className="w-6 h-6" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
              </button>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <div className="p-8">
          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {stats.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <div key={index} className={`rounded-xl shadow-sm border p-6 hover:shadow-lg transition-shadow ${
                  isDarkMode 
                    ? 'bg-gray-800 border-gray-700' 
                    : 'bg-white border-gray-200'
                }`}>
                  <div className="flex items-center justify-between mb-4">
                    <div className={`${stat.color} w-12 h-12 rounded-lg flex items-center justify-center`}>
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <span className="text-xs font-semibold text-green-600 bg-green-50 px-2 py-1 rounded">
                      {stat.trend}
                    </span>
                  </div>
                  <p className={`text-sm mb-1 ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                    {stat.label}
                  </p>
                  <p className={`text-2xl font-bold ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>
                    {stat.value}
                  </p>
                </div>
              );
            })}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* User Details Card */}
            <div className={`lg:col-span-2 rounded-xl shadow-sm border p-6 ${
              isDarkMode 
                ? 'bg-gray-800 border-gray-700' 
                : 'bg-white border-gray-200'
            }`}>
              <h3 className={`text-lg font-bold mb-6 flex items-center gap-2 ${
                isDarkMode ? 'text-white' : 'text-gray-800'
              }`}>
                <UserIcon className="w-5 h-5 text-green-600" />
                Informações da Conta
              </h3>
              <div className="grid grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div>
                    <label className={`text-xs font-medium uppercase ${
                      isDarkMode ? 'text-gray-400' : 'text-gray-500'
                    }`}>Nome Completo</label>
                    <p className={`text-base font-semibold mt-1 ${
                      isDarkMode ? 'text-white' : 'text-gray-800'
                    }`}>{user?.nome} {user?.sobrenome}</p>
                  </div>
                  <div>
                    <label className={`text-xs font-medium uppercase ${
                      isDarkMode ? 'text-gray-400' : 'text-gray-500'
                    }`}>CPF</label>
                    <p className={`text-base font-semibold mt-1 ${
                      isDarkMode ? 'text-white' : 'text-gray-800'
                    }`}>{user?.cpf}</p>
                  </div>
                  <div>
                    <label className={`text-xs font-medium uppercase ${
                      isDarkMode ? 'text-gray-400' : 'text-gray-500'
                    }`}>E-mail</label>
                    <p className={`text-base font-semibold mt-1 ${
                      isDarkMode ? 'text-white' : 'text-gray-800'
                    }`}>{user?.email}</p>
                  </div>
                  <div>
                    <label className={`text-xs font-medium uppercase ${
                      isDarkMode ? 'text-gray-400' : 'text-gray-500'
                    }`}>ID do Usuário</label>
                    <p className={`text-base font-semibold mt-1 ${
                      isDarkMode ? 'text-white' : 'text-gray-800'
                    }`}>#{user?.id}</p>
                  </div>
                </div>
                <div className="space-y-4">
                  <div>
                    <label className={`text-xs font-medium uppercase ${
                      isDarkMode ? 'text-gray-400' : 'text-gray-500'
                    }`}>Status</label>
                    <p className="text-base font-semibold text-green-600 mt-1 flex items-center gap-2">
                      <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                      Ativo
                    </p>
                  </div>
                  {user?.cep && (
                    <>
                      <div>
                        <label className={`text-xs font-medium uppercase ${
                          isDarkMode ? 'text-gray-400' : 'text-gray-500'
                        }`}>CEP</label>
                        <p className={`text-base font-semibold mt-1 ${
                          isDarkMode ? 'text-white' : 'text-gray-800'
                        }`}>{user?.cep}</p>
                      </div>
                      <div>
                        <label className={`text-xs font-medium uppercase ${
                          isDarkMode ? 'text-gray-400' : 'text-gray-500'
                        }`}>Endereço</label>
                        <p className={`text-sm mt-1 ${
                          isDarkMode ? 'text-gray-300' : 'text-gray-700'
                        }`}>
                          {user?.logradouro}{user?.numero ? `, ${user.numero}` : ''}
                          {user?.complemento && <br />}
                          {user?.complemento}
                          {(user?.bairro || user?.cidade || user?.estado) && <br />}
                          {user?.bairro && `${user.bairro} - `}
                          {user?.cidade}{user?.estado ? `/${user.estado}` : ''}
                        </p>
                      </div>
                    </>
                  )}
                </div>
              </div>
              <div className={`mt-6 pt-6 border-t flex gap-3 ${
                isDarkMode ? 'border-gray-700' : 'border-gray-200'
              }`}>
                <button className="flex-1 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors">
                  Editar Perfil
                </button>
                <button className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors ${
                  isDarkMode
                    ? 'bg-gray-700 hover:bg-gray-600 text-white'
                    : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
                }`}>
                  Configurações
                </button>
              </div>
            </div>

            {/* Recent Activity */}
            <div className={`rounded-xl shadow-sm border p-6 ${
              isDarkMode 
                ? 'bg-gray-800 border-gray-700' 
                : 'bg-white border-gray-200'
            }`}>
              <h3 className={`text-lg font-bold mb-6 flex items-center gap-2 ${
                isDarkMode ? 'text-white' : 'text-gray-800'
              }`}>
                <ClockIcon className="w-5 h-5 text-green-600" />
                Atividades Recentes
              </h3>
              <div className="space-y-4">
                {recentActivities.map((activity) => (
                  <div key={activity.id} className={`flex items-start gap-3 pb-4 border-b last:border-0 last:pb-0 ${
                    isDarkMode ? 'border-gray-700' : 'border-gray-100'
                  }`}>
                    <div className={`w-2 h-2 rounded-full mt-2 ${
                      activity.status === 'success' ? 'bg-green-500' : 'bg-yellow-500'
                    }`}></div>
                    <div className="flex-1 min-w-0">
                      <p className={`text-sm font-semibold ${
                        isDarkMode ? 'text-white' : 'text-gray-800'
                      }`}>{activity.type}</p>
                      <p className={`text-xs mt-1 ${
                        isDarkMode ? 'text-gray-400' : 'text-gray-600'
                      }`}>{activity.description}</p>
                      <p className={`text-xs mt-1 ${
                        isDarkMode ? 'text-gray-500' : 'text-gray-400'
                      }`}>{activity.time}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className={`mt-8 rounded-xl shadow-lg p-6 text-white ${
            isDarkMode
              ? 'bg-gradient-to-r from-gray-800 via-gray-700 to-gray-800'
              : 'bg-gradient-to-r from-green-600 via-emerald-600 to-green-700'
          }`}>
            <h3 className="text-lg font-bold mb-4">Ações Rápidas</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <button className="bg-white bg-opacity-20 hover:bg-opacity-30 backdrop-blur-sm rounded-lg p-4 transition-all text-center group">
                <CreditCardIcon className="w-8 h-8 mx-auto mb-2 group-hover:scale-110 transition-transform" />
                <span className="text-sm font-medium">Nova Transação</span>
              </button>
              <button className="bg-white bg-opacity-20 hover:bg-opacity-30 backdrop-blur-sm rounded-lg p-4 transition-all text-center group">
                <ChartBarIcon className="w-8 h-8 mx-auto mb-2 group-hover:scale-110 transition-transform" />
                <span className="text-sm font-medium">Relatórios</span>
              </button>
              <button className="bg-white bg-opacity-20 hover:bg-opacity-30 backdrop-blur-sm rounded-lg p-4 transition-all text-center group">
                <ShieldCheckIcon className="w-8 h-8 mx-auto mb-2 group-hover:scale-110 transition-transform" />
                <span className="text-sm font-medium">Segurança</span>
              </button>
              <button className="bg-white bg-opacity-20 hover:bg-opacity-30 backdrop-blur-sm rounded-lg p-4 transition-all text-center group">
                <CogIcon className="w-8 h-8 mx-auto mb-2 group-hover:scale-110 transition-transform" />
                <span className="text-sm font-medium">Configurar</span>
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
