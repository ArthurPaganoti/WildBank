export const validarCPF = (cpf) => {
  const cpfLimpo = cpf.replace(/\D/g, '');
  
  if (cpfLimpo.length !== 11) {
    return false;
  }
  
  if (/^(\d)\1{10}$/.test(cpfLimpo)) {
    return false;
  }
  
  let soma = 0;
  for (let i = 0; i < 9; i++) {
    soma += parseInt(cpfLimpo.charAt(i)) * (10 - i);
  }
  let resto = soma % 11;
  const digito1 = resto < 2 ? 0 : 11 - resto;
  
  if (parseInt(cpfLimpo.charAt(9)) !== digito1) {
    return false;
  }
  
  soma = 0;
  for (let i = 0; i < 10; i++) {
    soma += parseInt(cpfLimpo.charAt(i)) * (11 - i);
  }
  resto = soma % 11;
  const digito2 = resto < 2 ? 0 : 11 - resto;
  
  if (parseInt(cpfLimpo.charAt(10)) !== digito2) {
    return false;
  }
  
  return true;
};

export const formatarCPF = (cpf) => {
  const cpfLimpo = cpf.replace(/\D/g, '');
  
  if (cpfLimpo.length <= 3) {
    return cpfLimpo;
  } else if (cpfLimpo.length <= 6) {
    return `${cpfLimpo.slice(0, 3)}.${cpfLimpo.slice(3)}`;
  } else if (cpfLimpo.length <= 9) {
    return `${cpfLimpo.slice(0, 3)}.${cpfLimpo.slice(3, 6)}.${cpfLimpo.slice(6)}`;
  } else {
    return `${cpfLimpo.slice(0, 3)}.${cpfLimpo.slice(3, 6)}.${cpfLimpo.slice(6, 9)}-${cpfLimpo.slice(9, 11)}`;
  }
};

