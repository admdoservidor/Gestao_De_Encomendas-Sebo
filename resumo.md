# resumo.md — Contexto do projeto Sebo

## O que é
Backend Django templates puro para encomenda de livros de sebo. Vendedor divulga 1 link/QR; cliente pede sem login; vendedor acompanha.

## Arquitetura (MVT padrão)
- `config/`: settings (`AUTH_USER_MODEL=vendedores.Vendedor`, `LOGIN_URL`, `STATICFILES_DIRS`, `ALLOWED_HOSTS=*`), urls (root condicional, `sw.js`, auth, apps)
- Apps: `vendedores` (auth+signup), `clientes` (Cliente/LivroInteresse + `phone_mask`), `encomendas` (Encomenda+CSV), `formularios` (LinkFormulario+Pedido público), `dashboard` (home+link único/QR)
- `templates/`: base (nav h1 Sebo, PWA, install btn) + registration + dashboard + clientes + encomendas + formularios
- `static/`: css minimalista responsivo, manifest, icons 192/512, sw.js

## Regras-chave
- Cliente identificado por telefone único; `get_or_create` não duplica.
- `Cliente.vendedores` M2M; `Encomenda(vendedor, status)` com índice.
- 1 `LinkFormulario` ativo por vendedor (`get_or_create` + desativa extras).
- Todas privadas com `LoginRequiredMixin`/`@login_required`; raiz `/` redireciona.
- Telefone exibido mascarado via `mask_phone`: móvel `(85) 9 8***-**72`, fixo `(85) 3***-**72`.
- Contatos sem lista de livros; botão Encomenda (ghost, ml 20px) só se `tem_aberta` (Exists); favorito é ★/☆.
- Recentes e stats clicáveis (pedidos do cliente / áreas).
- PWA: manifest standalone, `/sw.js` raiz, botão Instalar (`beforeinstallprompt`).

## Estado atual
Migrations OK, `check` OK, fluxos verificados via test Client (signup, pedido, mascaramento, redirects, QR único, PWA). Servidor dev `runserver 8000`.
