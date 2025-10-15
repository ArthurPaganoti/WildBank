export const buscarCep = async (cep) => {
  try {
    const cepLimpo = cep.replace(/\D/g, '');
    
    if (cepLimpo.length !== 8) {
      throw new Error('CEP deve conter 8 dígitos');
    }
    
    const response = await fetch(`https://viacep.com.br/ws/${cepLimpo}/json/`);
    const data = await response.json();
    
    if (data.erro) {
      throw new Error('CEP não encontrado');
    }
    
    return {
      cep: data.cep,
      logradouro: data.logradouro,
      complemento: data.complemento,
      bairro: data.bairro,
      cidade: data.localidade,
      estado: data.uf
    };
  } catch (error) {
    throw new Error(error.message || 'Erro ao buscar CEP');
  }
};

export const formatarCep = (cep) => {
  const cepLimpo = cep.replace(/\D/g, '');
  if (cepLimpo.length <= 5) {
    return cepLimpo;
  }
  return `${cepLimpo.slice(0, 5)}-${cepLimpo.slice(5, 8)}`;
};

