# Sebo — Backend de Encomendas de Livros

Django puro (MVT, templates, sem DRF) para vendedores de sebo receberem encomendas via link/formulário com QR Code.

## Fluxo
- Vendedor cria conta em `/accounts/signup/` e entra em `/accounts/login/`.
- Página `Links` (`/dashboard/links/`) tem **1 link único por vendedor** + QR Code + botão Copiar.
- Cliente abre `/pedido/<token>/`, preenche nome, telefone, livro e autor (opcional).
- Sistema faz `get_or_create` de `Cliente` por telefone, vincula ao vendedor, cria `LivroInteresse` + `Encomenda(aberta)`.
- Vendedor gerencia em Dashboard, Clientes, Encomendas, export CSV e WhatsApp (`wa.me`).

## Stack
Django 6.1, Postgres 16 (via `psycopg`), auth custom `vendedores.Vendedor`, CBVs, `qrcode[pillow]`, PWA (manifest + SW em `/sw.js` + botão Instalar), CSS minimalista responsivo.

## Modelos
- `Vendedor(AbstractUser)`: username, email/telefone/cpf únicos
- `Cliente`: nome, telefone único, favorito, vendedores M2M
- `LivroInteresse`: cliente FK, titulo, autor
- `Encomenda`: cliente FK, vendedor FK, livro_titulo, status (aberta/fechada/cancelada)
- `LinkFormulario`: token UUID, vendedor FK, ativo

## Rodar com Docker (Recomendado)
```powershell
Copy-Item .env.example .env   # só na primeira vez; ajuste o SECRET_KEY em produção
docker compose up --build
# http://127.0.0.1:8000/
```
- O container roda `migrate` + `collectstatic` + `gunicorn` automaticamente.
- O banco Postgres persiste no volume `pgdata` (serviço `db`, `postgres:16-alpine`).
- Para criar um superusuário: `docker compose run --rm web python manage.py createsuperuser`
- Para parar: `docker compose down` (o banco é mantido no volume; `down -v` apaga).

## Rodar local (sem Docker)
```powershell
pip install django qrcode pillow
python manage.py migrate
python manage.py runserver 8000
# http://127.0.0.1:8000/ (raiz redireciona: logado->/dashboard/, anônimo->/accounts/login/)
```

## Rotas principais
- `/` raiz condicional, `/admin/`, `/accounts/login|signup|logout`
- `/pedido/<uuid>/` + `/sucesso/` (público)
- `/dashboard/` + `/dashboard/links/` (QR único, sem gerar/deletar)
- `/clientes/` (busca, favoritos ★/☆, telefone mascarado `(85) 9 8***-**72`, botão Encomenda se aberta)
- `/encomendas/` (`?status=&cliente=`), `/<pk>/editar/` (status), `/export/csv/`

## Privacidade/UX
Login obrigatório (302 `?next=`), raiz protege igual, PWA instalável, responsivo mobile.
