#!/bin/bash

set -e

echo "Iniciando FastAPI com Docker Compose..."

if [ "$1" == "--build" ]; then
    echo "Fazendo rebuild das imagens..."
    docker-compose down
    docker-compose build --no-cache
fi

if [ ! -f .env ]; then
    echo "Arquivo .env não encontrado!"
    echo "Criando .env a partir de .env.example..."

    if [ -f .env.example ]; then
        cp .env.example .env
        echo ""
        echo "IMPORTANTE: Edite o arquivo .env e configure:"
        echo "   - SECRET_KEY (gere com: openssl rand -hex 32)"
        echo "   - ENCRYPTION_KEY (gere com: openssl rand -hex 32)"
        echo "   - ENCRYPTION_SALT (gere com: openssl rand -hex 16)"
        echo "   - POSTGRES_PASSWORD"
        echo "   - SMTP_USERNAME e SMTP_PASSWORD (para envio de e-mails)"
        echo ""
        read -p "Pressione ENTER após configurar o .env..."
    else
        echo "❌ Arquivo .env.example não encontrado!"
        exit 1
    fi
fi

echo "Iniciando containers..."
docker-compose up -d

echo ""
echo "⏳ Aguardando serviços ficarem prontos..."
sleep 5

if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "Aplicação iniciada com sucesso!"
    echo ""
    echo "URLs disponíveis:"
    echo "   Backend:       http://localhost:8000"
    echo "   Documentação:  http://localhost:8000/docs"
    echo "   Frontend:      http://localhost:5173"
    echo ""
    echo "Visualizar logs:"
    echo "   docker-compose logs -f backend"
    echo "   docker-compose logs -f frontend"
    echo ""
    echo "Para parar: docker-compose down"
    echo "Para rebuild: ./docker-start.sh --build"
else
    echo "Erro ao iniciar containers!"
    echo "Execute: docker-compose logs"
    exit 1
fi

read -p "Executar migrations do banco? (s/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "Executando migrations..."
    docker-compose exec backend alembic upgrade head
    echo "Migrations executadas!"
fi

echo ""
echo "Tudo pronto! Boa codificação!"
echo ""
echo "Dicas:"
echo "   • Sistema de recuperação de senha está ativo"
echo "   • E-mails são enviados via SMTP configurado no .env"
echo "   • Verifique o SETUP_EMAIL.md para mais informações"
echo ""
