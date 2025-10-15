import React, { useState } from "react";
import { useForm } from "react-hook-form";
import axios from "../api";
import AuthLayout from "../components/AuthLayout";
import { Link, useNavigate } from "react-router-dom";
import { validatePassword, getPasswordStrength } from "../utils/passwordValidator";
import { buscarCep, formatarCep } from "../services/viaCepService";
import { validarCPF, formatarCPF } from "../utils/cpfValidator";
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';

const ESTADOS_BRASILEIROS = [
  { sigla: 'AC', nome: 'Acre' },
  { sigla: 'AL', nome: 'Alagoas' },
  { sigla: 'AP', nome: 'Amapá' },
  { sigla: 'AM', nome: 'Amazonas' },
  { sigla: 'BA', nome: 'Bahia' },
  { sigla: 'CE', nome: 'Ceará' },
  { sigla: 'DF', nome: 'Distrito Federal' },
  { sigla: 'ES', nome: 'Espírito Santo' },
  { sigla: 'GO', nome: 'Goiás' },
  { sigla: 'MA', nome: 'Maranhão' },
  { sigla: 'MT', nome: 'Mato Grosso' },
  { sigla: 'MS', nome: 'Mato Grosso do Sul' },
  { sigla: 'MG', nome: 'Minas Gerais' },
  { sigla: 'PA', nome: 'Pará' },
  { sigla: 'PB', nome: 'Paraíba' },
  { sigla: 'PR', nome: 'Paraná' },
  { sigla: 'PE', nome: 'Pernambuco' },
  { sigla: 'PI', nome: 'Piauí' },
  { sigla: 'RJ', nome: 'Rio de Janeiro' },
  { sigla: 'RN', nome: 'Rio Grande do Norte' },
  { sigla: 'RS', nome: 'Rio Grande do Sul' },
  { sigla: 'RO', nome: 'Rondônia' },
  { sigla: 'RR', nome: 'Roraima' },
  { sigla: 'SC', nome: 'Santa Catarina' },
  { sigla: 'SP', nome: 'São Paulo' },
  { sigla: 'SE', nome: 'Sergipe' },
  { sigla: 'TO', nome: 'Tocantins' }
];

export default function Register() {
  const { register, handleSubmit, formState: { errors }, watch, setValue } = useForm();
  const [apiError, setApiError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loadingCep, setLoadingCep] = useState(false);
  const [cepError, setCepError] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();
  
  const senha = watch("senha", "");
  const cep = watch("cep", "");
  const cpf = watch("cpf", "");
  const passwordChecks = getPasswordStrength(senha);

  const validateEmail = (email) => {
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailRegex.test(email)) {
      return "E-mail inválido. Use o formato: exemplo@dominio.com";
    }
    return true;
  };

  const validateCPF = (cpf) => {
    if (!cpf) return "CPF é obrigatório";
    if (!validarCPF(cpf)) {
      return "CPF inválido. Verifique os dígitos e tente novamente.";
    }
    return true;
  };

  const handleCpfChange = (e) => {
    const valor = e.target.value;
    const cpfFormatado = formatarCPF(valor);
    setValue('cpf', cpfFormatado);
  };

  const handleCepBlur = async () => {
    if (!cep || cep.replace(/\D/g, '').length !== 8) {
      return;
    }

    setLoadingCep(true);
    setCepError("");

    try {
      const endereco = await buscarCep(cep);
      
      setValue('logradouro', endereco.logradouro);
      setValue('bairro', endereco.bairro);
      setValue('cidade', endereco.cidade);
      setValue('estado', endereco.estado);
      if (endereco.complemento) {
        setValue('complemento', endereco.complemento);
      }
      
      setValue('cep', formatarCep(cep));
      
    } catch (error) {
      setCepError(error.message);
    } finally {
      setLoadingCep(false);
    }
  };

  const onSubmit = async (data) => {
    setApiError("");
    setSuccess(false);
    try {
      await axios.post("/users/", data);
      setSuccess(true);

      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err) {
      setApiError(err.response?.data?.detail || "Erro ao cadastrar usuário.");
    }
  };

  return (
    <AuthLayout title="Criar Conta">
      <form className="w-full" onSubmit={handleSubmit(onSubmit)}>
        {/* Dados Pessoais */}
        <div className="mb-6">
          <h3 className="text-sm font-bold text-gray-700 mb-3 flex items-center gap-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            Dados Pessoais
          </h3>
          
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nome</label>
                <input
                  type="text"
                  {...register("nome", { 
                    required: "Nome é obrigatório",
                    minLength: { value: 2, message: "Nome deve ter no mínimo 2 caracteres" },
                    maxLength: { value: 100, message: "Nome deve ter no máximo 100 caracteres" },
                    pattern: { value: /^[A-Za-zÀ-ÿ\s]+$/, message: "Nome não pode conter números" }
                  })}
                  className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="João"
                />
                {errors.nome && <span className="text-red-500 text-xs mt-1">{errors.nome.message}</span>}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Sobrenome</label>
                <input
                  type="text"
                  {...register("sobrenome", { 
                    required: "Sobrenome é obrigatório",
                    minLength: { value: 2, message: "Sobrenome deve ter no mínimo 2 caracteres" },
                    maxLength: { value: 100, message: "Sobrenome deve ter no máximo 100 caracteres" },
                    pattern: { value: /^[A-Za-zÀ-ÿ\s]+$/, message: "Sobrenome não pode conter números" }
                  })}
                  className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="Silva"
                />
                {errors.sobrenome && <span className="text-red-500 text-xs mt-1">{errors.sobrenome.message}</span>}
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">CPF</label>
              <input
                type="text"
                {...register("cpf", { 
                  required: "CPF é obrigatório",
                  validate: validateCPF
                })}
                onChange={handleCpfChange}
                maxLength={14}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                placeholder="000.000.000-00"
              />
              {errors.cpf && <span className="text-red-500 text-xs mt-1">{errors.cpf.message}</span>}
              {cpf && cpf.replace(/\D/g, '').length === 11 && validarCPF(cpf) && (
                <span className="text-green-600 text-xs mt-1 flex items-center gap-1">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  CPF válido
                </span>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">E-mail</label>
              <input
                type="email"
                {...register("email", { 
                  required: "E-mail é obrigatório",
                  validate: validateEmail
                })}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                placeholder="seu@email.com"
              />
              {errors.email && <span className="text-red-500 text-xs mt-1">{errors.email.message}</span>}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Senha</label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  {...register("senha", {
                    required: "Senha é obrigatória",
                    validate: validatePassword
                  })}
                  className="w-full px-3 py-2 pr-10 border rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="Sua senha segura"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 focus:outline-none"
                  tabIndex={-1}
                >
                  {showPassword ? (
                    <EyeSlashIcon className="w-5 h-5" />
                  ) : (
                    <EyeIcon className="w-5 h-5" />
                  )}
                </button>
              </div>
              {errors.senha && <span className="text-red-500 text-xs mt-1">{errors.senha.message}</span>}
              
              {/* Indicadores de força da senha */}
              {senha && passwordChecks && (
                <div className="mt-2 space-y-1">
                  <p className="text-xs font-medium text-gray-600">Requisitos da senha:</p>
                  <div className="grid grid-cols-2 gap-1">
                    <div className={`text-xs flex items-center gap-1 ${passwordChecks.length ? 'text-green-600' : 'text-gray-400'}`}>
                      <span>{passwordChecks.length ? '✓' : '○'}</span> 8-48 caracteres
                    </div>
                    <div className={`text-xs flex items-center gap-1 ${passwordChecks.upper ? 'text-green-600' : 'text-gray-400'}`}>
                      <span>{passwordChecks.upper ? '✓' : '○'}</span> Maiúscula
                    </div>
                    <div className={`text-xs flex items-center gap-1 ${passwordChecks.lower ? 'text-green-600' : 'text-gray-400'}`}>
                      <span>{passwordChecks.lower ? '✓' : '○'}</span> Minúscula
                    </div>
                    <div className={`text-xs flex items-center gap-1 ${passwordChecks.special ? 'text-green-600' : 'text-gray-400'}`}>
                      <span>{passwordChecks.special ? '✓' : '○'}</span> Especial
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Endereço */}
        <div className="mb-6 pt-4 border-t">
          <h3 className="text-sm font-bold text-gray-700 mb-3 flex items-center gap-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Endereço <span className="text-red-500">*</span>
          </h3>
          
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                CEP <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <input
                  type="text"
                  {...register("cep", {
                    required: "CEP é obrigatório",
                    minLength: { value: 8, message: "CEP deve ter 8 dígitos" }
                  })}
                  onBlur={handleCepBlur}
                  maxLength={9}
                  className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="00000-000"
                />
                {loadingCep && (
                  <div className="absolute right-3 top-2.5">
                    <svg className="animate-spin h-5 w-5 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  </div>
                )}
              </div>
              {errors.cep && <span className="text-red-500 text-xs mt-1">{errors.cep.message}</span>}
              {cepError && <span className="text-red-500 text-xs mt-1">{cepError}</span>}
              <p className="text-xs text-gray-500 mt-1">Digite o CEP para preencher automaticamente</p>
            </div>

            <div className="grid grid-cols-3 gap-3">
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Logradouro <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  {...register("logradouro", {
                    required: "Logradouro é obrigatório",
                    minLength: { value: 3, message: "Logradouro deve ter no mínimo 3 caracteres" }
                  })}
                  className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="Rua, Avenida..."
                />
                {errors.logradouro && <span className="text-red-500 text-xs mt-1">{errors.logradouro.message}</span>}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Número <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  {...register("numero", {
                    required: "Número é obrigatório",
                    minLength: { value: 1, message: "Número é obrigatório" }
                  })}
                  className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="123 ou S/N"
                />
                {errors.numero && <span className="text-red-500 text-xs mt-1">{errors.numero.message}</span>}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Complemento <span className="text-gray-400 text-xs">(opcional)</span>
              </label>
              <input
                type="text"
                {...register("complemento")}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                placeholder="Apto, Bloco, etc."
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Bairro <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  {...register("bairro", {
                    required: "Bairro é obrigatório",
                    minLength: { value: 2, message: "Bairro deve ter no mínimo 2 caracteres" }
                  })}
                  className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="Centro"
                />
                {errors.bairro && <span className="text-red-500 text-xs mt-1">{errors.bairro.message}</span>}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Cidade <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  {...register("cidade", {
                    required: "Cidade é obrigatória",
                    minLength: { value: 2, message: "Cidade deve ter no mínimo 2 caracteres" }
                  })}
                  className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="São Paulo"
                />
                {errors.cidade && <span className="text-red-500 text-xs mt-1">{errors.cidade.message}</span>}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Estado (UF) <span className="text-red-500">*</span>
              </label>
              <select
                {...register("estado", {
                  required: "Estado é obrigatório",
                })}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="">Selecione o estado</option>
                {ESTADOS_BRASILEIROS.map(estado => (
                  <option key={estado.sigla} value={estado.sigla}>
                    {estado.nome}
                  </option>
                ))}
              </select>
              {errors.estado && <span className="text-red-500 text-xs mt-1">{errors.estado.message}</span>}
            </div>
          </div>
        </div>
        
        <button
          type="submit"
          className="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white py-3 rounded-lg font-semibold shadow-lg hover:scale-105 transition-transform"
        >
          Criar Conta
        </button>
        
        {apiError && <div className="mt-4 p-3 bg-red-50 border-l-4 border-red-500 rounded text-red-700 text-sm">{apiError}</div>}
        {success && <div className="mt-4 p-3 bg-green-50 border-l-4 border-green-500 rounded text-green-700 text-sm">Cadastro realizado com sucesso! Redirecionando...</div>}
      </form>
      <div className="mt-6 text-sm text-gray-600 text-center">
        Já tem uma conta? <Link to="/login" className="text-green-600 font-semibold hover:underline">Entrar</Link>
      </div>
    </AuthLayout>
  );
}
