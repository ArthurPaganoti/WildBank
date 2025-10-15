import httpx
from typing import Optional, Dict, Any
from app.core.logging import get_logger
from app.exceptions import ViaCEPException, InvalidCEPException

logger = get_logger(__name__)

VIACEP_URL = "https://viacep.com.br/ws/{cep}/json/"
TIMEOUT = 5.0


async def consultar_cep(cep: str) -> Optional[Dict[str, Any]]:
    cep_limpo = cep.replace('-', '').replace('.', '').strip()

    if len(cep_limpo) != 8 or not cep_limpo.isdigit():
        raise InvalidCEPException(message="CEP deve conter exatamente 8 dígitos")

    url = VIACEP_URL.format(cep=cep_limpo)

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            logger.info("viacep_request", cep=cep_limpo)
            response = await client.get(url)
            response.raise_for_status()

            data = response.json()

            if data.get('erro'):
                logger.warning("viacep_cep_not_found", cep=cep_limpo)
                raise InvalidCEPException(message=f"CEP {cep_limpo} não encontrado")

            logger.info("viacep_success", cep=cep_limpo, cidade=data.get('localidade'))
            return data

    except httpx.TimeoutException:
        logger.error("viacep_timeout", cep=cep_limpo)
        raise ViaCEPException(
            cep=cep_limpo,
            message="Timeout ao consultar CEP. Tente novamente.",
            original_error="Timeout"
        )
    except httpx.HTTPError as e:
        logger.error("viacep_http_error", cep=cep_limpo, error=str(e))
        raise ViaCEPException(
            cep=cep_limpo,
            message="Erro ao consultar CEP no serviço ViaCEP",
            original_error=str(e)
        )
    except Exception as e:
        logger.error("viacep_unexpected_error", cep=cep_limpo, error=str(e))
        raise ViaCEPException(
            cep=cep_limpo,
            message="Erro inesperado ao consultar CEP",
            original_error=str(e)
        )


def validar_cep_format(cep: str) -> bool:
    cep_limpo = cep.replace('-', '').replace('.', '').strip()
    return len(cep_limpo) == 8 and cep_limpo.isdigit()


def formatar_cep(cep: str) -> str:
    cep_limpo = cep.replace('-', '').replace('.', '').strip()

    if len(cep_limpo) == 8:
        return f"{cep_limpo[:5]}-{cep_limpo[5:]}"

    return cep

