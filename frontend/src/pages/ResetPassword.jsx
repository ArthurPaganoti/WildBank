import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { useNavigate, useSearchParams } from "react-router-dom";
import axios from "../api";
import AuthLayout from "../components/AuthLayout";
import { CheckCircleIcon, ExclamationCircleIcon, EyeIcon, EyeSlashIcon, LockClosedIcon } from '@heroicons/react/24/outline';

export default function ResetPassword() {
  const { register, handleSubmit, watch, formState: { errors } } = useForm();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [token, setToken] = useState("");
  const [apiError, setApiError] = useState("");
  const [success, setSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const password = watch("new_password", "");

  useEffect(() => {
    const tokenParam = searchParams.get("token");
    if (!tokenParam) {
      setApiError("Token não encontrado. Use o link enviado por e-mail.");
    } else {
      setToken(tokenParam);
    }
  }, [searchParams]);

  const passwordRequirements = {
    length: password.length >= 8 && password.length <= 48,
    uppercase: /[A-Z]/.test(password),
    lowercase: /[a-z]/.test(password),
    number: /\d/.test(password),
    special: /[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;`~]/.test(password),
  };

  const allRequirementsMet = Object.values(passwordRequirements).every(Boolean);

  const validatePassword = (value) => {
    if (value.length < 8) return "Senha deve ter no mínimo 8 caracteres";
    if (value.length > 48) return "Senha deve ter no máximo 48 caracteres";
    if (!/[A-Z]/.test(value)) return "Senha deve conter pelo menos uma letra maiúscula";
    if (!/[a-z]/.test(value)) return "Senha deve conter pelo menos uma letra minúscula";
    if (!/\d/.test(value)) return "Senha deve conter pelo menos um número";
    if (!/[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;`~]/.test(value)) {
      return "Senha deve conter pelo menos um caractere especial";
    }
    return true;
  };

  const onSubmit = async (data) => {
    if (!token) {
      setApiError("Token inválido ou ausente.");
      return;
    }

    setApiError("");
    setSuccess(false);
    setIsLoading(true);

    try {
      await axios.post("/users/password-reset/confirm", {
        token: token,
        new_password: data.new_password,
      });
      
      setSuccess(true);

      setTimeout(() => {
        navigate('/login');
      }, 3000);
    } catch (err) {
      const errorMessage = err.response?.data?.message || "Erro ao redefinir senha. O token pode estar expirado.";
      setApiError(errorMessage);

      if (err.response?.status === 400) {
        setTimeout(() => {
          navigate('/login');
        }, 5000);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthLayout title="Redefinir Senha">
      {/* Mensagem de token inválido */}
      {!token && (
        <div className="mb-4 p-3 bg-red-50 border-l-4 border-red-500 rounded-r-lg">
          <div className="flex items-center gap-2">
            <ExclamationCircleIcon className="w-5 h-5 text-red-500 flex-shrink-0" />
            <p className="text-sm text-red-700 font-medium">{apiError}</p>
          </div>
        </div>
      )}

      {/* Ícone de cadeado */}
      {token && (
        <div className="text-center mb-6">
          <div className="mx-auto w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center mb-4">
            <LockClosedIcon className="w-8 h-8 text-white" />
          </div>
          <p className="text-sm text-gray-600">Digite sua nova senha abaixo</p>
        </div>
      )}

      <form className="w-full" onSubmit={handleSubmit(onSubmit)}>
        {/* Mensagem de erro */}
        {apiError && token && (
          <div className="mb-4 p-3 bg-red-50 border-l-4 border-red-500 rounded-r-lg animate-shake">
            <div className="flex items-center gap-2">
              <ExclamationCircleIcon className="w-5 h-5 text-red-500 flex-shrink-0" />
              <p className="text-sm text-red-700 font-medium">{apiError}</p>
            </div>
          </div>
        )}

        {/* Mensagem de sucesso */}
        {success && (
          <div className="mb-4 p-3 bg-green-50 border-l-4 border-green-500 rounded-r-lg">
            <div className="flex items-center gap-2">
              <CheckCircleIcon className="w-5 h-5 text-green-500 flex-shrink-0" />
              <p className="text-sm text-green-700 font-medium">
                Senha redefinida com sucesso! Redirecionando para o login...
              </p>
            </div>
          </div>
        )}

        {token && !success && (
          <>
            {/* Nova Senha */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Nova Senha</label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  {...register("new_password", {
                    required: "Nova senha é obrigatória",
                    validate: validatePassword,
                  })}
                  className="w-full px-3 py-2 pr-10 border rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="Digite sua nova senha"
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
              {errors.new_password && (
                <span className="flex items-center gap-1 text-red-500 text-xs mt-1">
                  <ExclamationCircleIcon className="w-4 h-4" />
                  {errors.new_password.message}
                </span>
              )}
            </div>

            {/* Confirmar Senha */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Confirmar Nova Senha</label>
              <div className="relative">
                <input
                  type={showConfirmPassword ? "text" : "password"}
                  {...register("confirm_password", {
                    required: "Por favor, confirme sua senha",
                    validate: (value) => value === password || "As senhas não coincidem",
                  })}
                  className="w-full px-3 py-2 pr-10 border rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="Digite novamente"
                  disabled={isLoading}
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 focus:outline-none"
                  tabIndex={-1}
                >
                  {showConfirmPassword ? (
                    <EyeSlashIcon className="w-5 h-5" />
                  ) : (
                    <EyeIcon className="w-5 h-5" />
                  )}
                </button>
              </div>
              {errors.confirm_password && (
                <span className="flex items-center gap-1 text-red-500 text-xs mt-1">
                  <ExclamationCircleIcon className="w-4 h-4" />
                  {errors.confirm_password.message}
                </span>
              )}
            </div>

            {/* Requisitos de Senha */}
            {password && (
              <div className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
                <p className="text-sm font-medium text-gray-700 mb-2">Requisitos da senha:</p>
                <ul className="space-y-1 text-xs">
                  <li className={`flex items-center gap-2 ${passwordRequirements.length ? 'text-green-600' : 'text-gray-500'}`}>
                    <span className={`w-4 h-4 rounded-full flex items-center justify-center ${passwordRequirements.length ? 'bg-green-100' : 'bg-gray-200'}`}>
                      {passwordRequirements.length ? '✓' : '○'}
                    </span>
                    8 a 48 caracteres
                  </li>
                  <li className={`flex items-center gap-2 ${passwordRequirements.uppercase ? 'text-green-600' : 'text-gray-500'}`}>
                    <span className={`w-4 h-4 rounded-full flex items-center justify-center ${passwordRequirements.uppercase ? 'bg-green-100' : 'bg-gray-200'}`}>
                      {passwordRequirements.uppercase ? '✓' : '○'}
                    </span>
                    Pelo menos 1 letra maiúscula
                  </li>
                  <li className={`flex items-center gap-2 ${passwordRequirements.lowercase ? 'text-green-600' : 'text-gray-500'}`}>
                    <span className={`w-4 h-4 rounded-full flex items-center justify-center ${passwordRequirements.lowercase ? 'bg-green-100' : 'bg-gray-200'}`}>
                      {passwordRequirements.lowercase ? '✓' : '○'}
                    </span>
                    Pelo menos 1 letra minúscula
                  </li>
                  <li className={`flex items-center gap-2 ${passwordRequirements.number ? 'text-green-600' : 'text-gray-500'}`}>
                    <span className={`w-4 h-4 rounded-full flex items-center justify-center ${passwordRequirements.number ? 'bg-green-100' : 'bg-gray-200'}`}>
                      {passwordRequirements.number ? '✓' : '○'}
                    </span>
                    Pelo menos 1 número
                  </li>
                  <li className={`flex items-center gap-2 ${passwordRequirements.special ? 'text-green-600' : 'text-gray-500'}`}>
                    <span className={`w-4 h-4 rounded-full flex items-center justify-center ${passwordRequirements.special ? 'bg-green-100' : 'bg-gray-200'}`}>
                      {passwordRequirements.special ? '✓' : '○'}
                    </span>
                    Pelo menos 1 caractere especial
                  </li>
                </ul>
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading || !allRequirementsMet}
              className="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white py-2 rounded font-semibold shadow-lg hover:scale-105 transition-transform flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
              {isLoading ? (
                <>
                  <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Redefinindo...
                </>
              ) : (
                <>
                  <LockClosedIcon className="w-5 h-5" /> Redefinir Senha
                </>
              )}
            </button>
          </>
        )}

        {!token && (
          <button
            type="button"
            onClick={() => navigate('/login')}
            className="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white py-2 rounded font-semibold shadow-lg hover:scale-105 transition-transform"
          >
            Voltar para o Login
          </button>
        )}
      </form>
    </AuthLayout>
  );
}

