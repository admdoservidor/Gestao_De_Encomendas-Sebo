# Plano - Sebo Backend Django Templates Puro

Origem: `C:\Users\L\Documents\Coding\Python\Sebo\sobre.md`

## 1. Objetivo
Backend para encomenda de livros: vendedor envia link de formulário, cliente preenche nome/telefone/livro(s), sistema preenche clientes/encomendas/livros_interesse. Dashboard vendedor com contatos, encomendas, export e WhatsApp.

## 2. Diagnóstico sobre.md
- `clientes.livros_interesse` + tabela `livros_interesse` redundante -> remover campo, usar FK reverso.
- `clientes.id_vendedor` único conflita com "vários vendedores" -> usar M2M `Cliente.vendedores` + FK `Encomenda.vendedor`.
- `livros_interesse <-> clientes` N:N -> MVP: `LivroInteresse FK -> Cliente` com `titulo, genero`.
- Identidade cliente = `telefone unique`.

## 3. Stack padrão Django MVT
- Django 5.x, SQLite dev / Postgres prod, `django.contrib.auth`, CBV, Forms, Templates, Messages, Admin.
- Sem DRF/SPA. WhatsApp v1 via `wa.me` deep-link.
- `AUTH_USER_MODEL = vendedores.Vendedor`
- `templates/base.html` + `registration/login.html`

## 4. Estrutura
```
sebo_project/
  config/settings.py, urls.py, wsgi.py, asgi.py
  apps/
    vendedores/ models.py, admin.py, apps.py
    clientes/ models.py (Cliente, LivroInteresse), forms.py, views.py, urls.py
    encomendas/ models.py, views.py, urls.py
    formularios/ models.py (LinkFormulario), forms.py (PedidoPublicoForm), views.py (PedidoCreateView)
    dashboard/ views.py, urls.py
  templates/
    base.html
    registration/login.html
    formularios/pedido_form.html, pedido_sucesso.html
    dashboard/home.html
    clientes/cliente_list.html, cliente_form.html, cliente_confirm_delete.html
    encomendas/encomenda_list.html, encomenda_form.html
  static/css/, static/js/
```

## 5. Modelos
```python
# vendedores/models.py
class Vendedor(AbstractUser):
    telefone = CharField(unique=True)
    cpf = CharField(unique=True)
    email = EmailField(unique=True)

# clientes/models.py
class Cliente(models.Model):
    nome = CharField(max_length=150)
    telefone = CharField(max_length=20, unique=True)
    favorito = BooleanField(default=False)
    vendedores = ManyToManyField(Vendedor, related_name='clientes')
    criado_em = DateTimeField(auto_now_add=True)

class LivroInteresse(models.Model):
    cliente = ForeignKey(Cliente, on_delete=CASCADE, related_name='interesses')
    titulo = CharField(max_length=255)
    genero = CharField(max_length=100, blank=True)
    criado_em = DateTimeField(auto_now_add=True)

# encomendas/models.py
class Encomenda(models.Model):
    class Status(TextChoices):
        ABERTA='aberta'; FECHADA='fechada'; CANCELADA='cancelada'
    cliente = ForeignKey(Cliente, on_delete=CASCADE)
    vendedor = ForeignKey(Vendedor, on_delete=CASCADE)
    livro_titulo = CharField(max_length=255)
    status = CharField(choices=Status, default=Status.ABERTA)
    criado_em = DateTimeField(auto_now_add=True)
    class Meta: indexes = [Index(fields=['vendedor','status'])]

# formularios/models.py
class LinkFormulario(models.Model):
    token = UUIDField(default=uuid4, unique=True)
    vendedor = ForeignKey(Vendedor, on_delete=CASCADE)
    ativo = BooleanField(default=True)
```

## 6. URLs
- `config/urls.py`: `admin/`, `accounts/` (auth.urls), `pedido/<uuid:token>/` (formularios), `dashboard/`, `clientes/`, `encomendas/`, `export/`
- Público sem login: `GET/POST pedido/<token>/`
- Privado `LoginRequiredMixin`: dashboard, CRUD cliente, lista/update encomenda, criar link, export csv

## 7. Views + Forms
- `PedidoPublicoForm`: nome, telefone, formset (titulo+genero, min 1). `clean_telefone` normaliza dígitos.
- `PedidoCreateView(FormView)`: valida token ativo -> `Cliente.get_or_create(telefone)` -> update nome se vazio -> `vendedores.add(vendedor)` -> `bulk_create LivroInteresse + Encomenda(aberta)`.
- `DashboardView`: counts abertas, total clientes, últimas 10 abertas.
- `ClienteListView`: filtro `q` (nome/telefone), `favorito=1`, só `vendedores=request.user`.
- `ClienteCreate/Update/DeleteView`, `toggle_favorito` POST.
- `EncomendaListView` filtro `status`, `EncomendaUpdateView` só status.
- `LinkCreateView`: cria token, exibe URL copiável + botão wa.me.
- `ExportCSVView`: `GET ?status=aberta` -> `values(livro_titulo).annotate(qtd=Count).order_by(-qtd)` -> `text/csv`.

## 8. Permissões
Sobrescrever `get_queryset` em todas views privadas para `vendedor=request.user`. Nunca `all()`. WhatsApp: `https://wa.me/55<telefone>?text=...`.

## 9. Ordem build
1. startproject + 4 apps + Custom User dia 1 + base.html + login
2. Cliente/LivroInteresse + Admin + migrations
3. Encomenda + indexes
4. LinkFormulario + form público + sucesso
5. Dashboard + CRUD + favoritos + busca
6. Links + export CSV + wa.me
7. Testes: get_or_create telefone, isolamento vendedor, agregação export
8. Recomendação futura: query `genero em comum`

## 10. Testes mínimos
- Cliente novo cria 1 Cliente + N Interesses + N Encomendas.
- Telefone existente não duplica Cliente, só adiciona.
- Vendedor A não vê clientes/encomendas de B.
- Export agrupa corretamente.
