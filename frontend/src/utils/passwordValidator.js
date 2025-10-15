export const validatePassword = (value) => {
  if (!value) return "Senha é obrigatória";
  if (value.length < 8) return "Senha deve ter no mínimo 8 caracteres";
  if (value.length > 48) return "Senha deve ter no máximo 48 caracteres";
  if (!/[A-Z]/.test(value)) return "Senha deve conter pelo menos uma letra maiúscula";
  if (!/[a-z]/.test(value)) return "Senha deve conter pelo menos uma letra minúscula";
  if (!/[!@#$%^&*(),.?":{}|<>_\-+=[\]\\;`~]/.test(value)) return "Senha deve conter pelo menos um caractere especial";
  return true;
};

export const getPasswordStrength = (senha) => {
  if (!senha) return null;
  return {
    length: senha.length >= 8 && senha.length <= 48,
    upper: /[A-Z]/.test(senha),
    lower: /[a-z]/.test(senha),
    special: /[!@#$%^&*(),.?":{}|<>_\-+=[\]\\;`~]/.test(senha)
  };
};
