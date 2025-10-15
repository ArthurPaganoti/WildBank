import { useState } from "react";
import { useForm } from "react-hook-form";
import axios from "../api";
import AuthLayout from "../components/AuthLayout";
import { Link, useNavigate } from "react-router-dom";
import { ArrowRightCircleIcon, ExclamationCircleIcon, CheckCircleIcon, EyeIcon, EyeSlashIcon, XMarkIcon, EnvelopeIcon } from '@heroicons/react/24/outline';
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const { register: registerReset, handleSubmit: handleSubmitReset, formState: { errors: errorsReset }, reset: resetForm } = useForm();
  const [apiError, setApiError] = useState("");
  const [success, setSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showForgotPasswordModal, setShowForgotPasswordModal] = useState(false);
  const [resetPasswordLoading, setResetPasswordLoading] = useState(false);
  const [resetPasswordSuccess, setResetPasswordSuccess] = useState(false);
  const [resetPasswordError, setResetPasswordError] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const validateEmail = (email) => {
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailRegex.test(email)) {
      return "E-mail inválido. Use o formato: exemplo@dominio.com";
    }
    return true;
  };

  const onSubmit = async (data) => {
    setApiError("");
    setSuccess(false);
    setIsLoading(true);

    try {
      const response = await axios.post("/users/login", data);
      setSuccess(true);

      login(response.data.user, response.data.access_token);

      setTimeout(() => {
        navigate('/dashboard');
      }, 1000);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || "E-mail ou senha incorretos. Verifique suas credenciais e tente novamente.";
      setApiError(errorMessage);

      setTimeout(() => {
        setApiError("");
      }, 5000);
    } finally {
      setIsLoading(false);
    }
  };

  const onForgotPasswordSubmit = async (data) => {
    setResetPasswordError("");
    setResetPasswordSuccess(false);
    setResetPasswordLoading(true);

    try {
      const response = await axios.post("/users/password-reset/request", data);
      setResetPasswordSuccess(true);
      resetForm();

      setTimeout(() => {
        setShowForgotPasswordModal(false);
        setResetPasswordSuccess(false);
      }, 3000);
    } catch (err) {
      const errorMessage = err.response?.data?.message || "Erro ao processar solicitação. Tente novamente.";
      setResetPasswordError(errorMessage);

      setTimeout(() => {
        setResetPasswordError("");
      }, 5000);
    } finally {
      setResetPasswordLoading(false);
    }
  };

  const openForgotPasswordModal = () => {
    setShowForgotPasswordModal(true);
    setResetPasswordError("");
    setResetPasswordSuccess(false);
    resetForm();
  };

  const closeForgotPasswordModal = () => {
    setShowForgotPasswordModal(false);
    setResetPasswordError("");
    setResetPasswordSuccess(false);
    resetForm();
  };

  return (
    <AuthLayout title="Entrar">
      <form className="w-full" onSubmit={handleSubmit(onSubmit)}>
        {/* Mensagem de erro no topo do formulário */}
        {apiError && (
          <div className="mb-4 p-3 bg-red-50 border-l-4 border-red-500 rounded-r-lg animate-shake">
            <div className="flex items-center gap-2">
              <ExclamationCircleIcon className="w-5 h-5 text-red-500 flex-shrink-0" />
              <p className="text-sm text-red-700 font-medium">{apiError}</p>
            </div>
          </div>
        )}

        {/* Mensagem de sucesso no topo do formulário */}
        {success && (
          <div className="mb-4 p-3 bg-green-50 border-l-4 border-green-500 rounded-r-lg">
            <div className="flex items-center gap-2">
              <CheckCircleIcon className="w-5 h-5 text-green-500 flex-shrink-0" />
              <p className="text-sm text-green-700 font-medium">Login realizado com sucesso! Redirecionando...</p>
            </div>
          </div>
        )}

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">E-mail</label>
          <input
            type="email"
            {...register("email", {
              required: "E-mail é obrigatório",
              validate: validateEmail
            })}
            className={`w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-500 ${apiError ? 'border-red-300' : ''}`}
            placeholder="seu@email.com"
            disabled={isLoading}
          />
          {errors.email && <span className="flex items-center gap-1 text-red-500 text-xs mt-1"><ExclamationCircleIcon className="w-4 h-4" />{errors.email.message}</span>}
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">Senha</label>
          <div className="relative">
            <input
              type={showPassword ? "text" : "password"}
              {...register("senha", { required: "Senha é obrigatória" })}
              className={`w-full px-3 py-2 pr-10 border rounded focus:outline-none focus:ring-2 focus:ring-green-500 ${apiError ? 'border-red-300' : ''}`}
              placeholder="Sua senha"
              disabled={isLoading}
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
          {errors.senha && <span className="flex items-center gap-1 text-red-500 text-xs mt-1"><ExclamationCircleIcon className="w-4 h-4" />{errors.senha.message}</span>}
        </div>

        {/* Link Esqueci minha senha */}
        <div className="mb-6 text-right">
          <button
            type="button"
            onClick={openForgotPasswordModal}
            className="text-sm text-green-600 hover:text-green-700 font-medium hover:underline"
          >
            Esqueci minha senha
          </button>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white py-2 rounded font-semibold shadow-lg hover:scale-105 transition-transform flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
        >
          {isLoading ? (
            <>
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Entrando...
            </>
          ) : (
            <>
              <ArrowRightCircleIcon className="w-5 h-5" /> Entrar
            </>
          )}
        </button>
      </form>
      <div className="mt-6 text-sm text-gray-600">
        Não tem uma conta? <Link to="/register" className="text-green-600 font-semibold hover:underline">Criar conta</Link>
      </div>

      {/* Modal de Esqueci Minha Senha */}
      {showForgotPasswordModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 animate-fadeIn">
          <div className="bg-white rounded-lg shadow-2xl max-w-md w-full p-6 relative animate-slideUp">
            {/* Botão Fechar */}
            <button
              onClick={closeForgotPasswordModal}
              className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
            >
              <XMarkIcon className="w-6 h-6" />
            </button>

            {/* Cabeçalho */}
            <div className="text-center mb-6">
              <div className="mx-auto w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center mb-4">
                <EnvelopeIcon className="w-8 h-8 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">Recuperar Senha</h2>
              <p className="text-sm text-gray-600">Digite seu e-mail para receber as instruções</p>
            </div>

            {/* Mensagens */}
            {resetPasswordError && (
              <div className="mb-4 p-3 bg-red-50 border-l-4 border-red-500 rounded-r-lg">
                <div className="flex items-center gap-2">
                  <ExclamationCircleIcon className="w-5 h-5 text-red-500 flex-shrink-0" />
                  <p className="text-sm text-red-700 font-medium">{resetPasswordError}</p>
                </div>
              </div>
            )}

            {resetPasswordSuccess && (
              <div className="mb-4 p-3 bg-green-50 border-l-4 border-green-500 rounded-r-lg">
                <div className="flex items-center gap-2">
                  <CheckCircleIcon className="w-5 h-5 text-green-500 flex-shrink-0" />
                  <p className="text-sm text-green-700 font-medium">
                    E-mail enviado! Verifique sua caixa de entrada e spam.
                  </p>
                </div>
              </div>
            )}

            {/* Formulário */}
            <form onSubmit={handleSubmitReset(onForgotPasswordSubmit)}>
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">E-mail</label>
                <input
                  type="email"
                  {...registerReset("email", {
                    required: "E-mail é obrigatório",
                    validate: validateEmail
                  })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                  placeholder="seu@email.com"
                  disabled={resetPasswordLoading || resetPasswordSuccess}
                />
                {errorsReset.email && (
                  <span className="flex items-center gap-1 text-red-500 text-xs mt-1">
                    <ExclamationCircleIcon className="w-4 h-4" />
                    {errorsReset.email.message}
                  </span>
                )}
              </div>

              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={closeForgotPasswordModal}
                  className="flex-1 px-4 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
                  disabled={resetPasswordLoading}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={resetPasswordLoading || resetPasswordSuccess}
                  className="flex-1 px-4 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {resetPasswordLoading ? (
                    <>
                      <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Enviando...
                    </>
                  ) : (
                    <>
                      <EnvelopeIcon className="w-5 h-5" />
                      Enviar E-mail
                    </>
                  )}
                </button>
              </div>
            </form>

            {/* Informação adicional */}
            <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <p className="text-xs text-blue-800">
                <strong>📧 Dica:</strong> O link de recuperação expira em 1 hora. Não esqueça de verificar a pasta de spam!
              </p>
            </div>
          </div>
        </div>
      )}
    </AuthLayout>
  );
}
