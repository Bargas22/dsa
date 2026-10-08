# VISAGIO — entrega de funcionalidades completas

Aplicação de visagismo com **30 funcionalidades disponíveis na interface web**, API Flask e persistência SQLAlchemy. Interface → Controller em classe → Service de um caso de uso → Model (ou Repository para consulta especial) → banco.

## Executar no Windows

Requer Python 3.11 ou superior. Extraia o ZIP antes de executar. No terminal, dentro de `backend`:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"
```

Cole a chave gerada no campo `JWT_SECRET=` de `backend/.env`. Em seguida:

```powershell
python -m flask --app app:create_app init-db
python -m flask --app app:create_app seed-demo
python app.py
```

Abra **http://localhost:5000**. Clique em **Ainda não tenho conta** e cadastre seu usuário (senha com pelo menos 8 caracteres). O banco SQLite é criado em `backend/instance/visagio.db`; as alterações permanecem após fechar o navegador e reiniciar o servidor. Não há conta/senha de usuário pronta no pacote.

Linux/macOS: use `source .venv/bin/activate` e `cp .env.example .env`; os demais comandos são os mesmos.

### MySQL

A aplicação aceita MySQL 8 via SQLAlchemy/PyMySQL. Crie um banco **novo** `visagio_v2` com `utf8mb4`, configure `DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/visagio_v2?charset=utf8mb4` no `.env` e execute os comandos `init-db` e `seed-demo`. Credenciais com caracteres reservados devem ser codificadas para URL.

O esquema antigo foi substituído pelas Models ORM. Não aponte esta versão diretamente para um banco antigo: `create_all` não migra tabelas. Consulte [backend/database/README.md](backend/database/README.md). O teste executado nesta entrega usa SQLite; MySQL exige validação no ambiente do grupo.

## Funcionalidades Implementadas

Cada item abaixo possui acesso na interface web e consulta ou gravação real no banco. Detalhes de rotas, Controllers e Services estão na [matriz de rastreabilidade](docs/funcionalidades.md).

1. Cadastrar usuário
2. Entrar na conta
3. Consultar perfil
4. Atualizar perfil
5. Consultar preferências
6. Salvar preferências
7. Consultar profissionais
8. Consultar e filtrar sugestões por análise/categoria
9. Consultar detalhes de uma sugestão
10. Gerar e salvar sugestões do catálogo
11. Listar análise autodeclarada
12. Cadastrar análise autodeclarada
13. Consultar detalhes de análise autodeclarada
14. Editar análise autodeclarada
15. Excluir análise autodeclarada
16. Listar procedimento do histórico
17. Cadastrar procedimento do histórico
18. Consultar detalhes de procedimento do histórico
19. Editar procedimento do histórico
20. Excluir procedimento do histórico
21. Listar agendamento
22. Cadastrar agendamento
23. Consultar detalhes de agendamento
24. Editar agendamento
25. Excluir agendamento
26. Listar comparação de visual
27. Cadastrar comparação de visual
28. Consultar detalhes de comparação de visual
29. Editar comparação de visual
30. Excluir comparação de visual

## Arquitetura e diagrama

```text
backend/
  controllers/    classes por recurso, leitura HTTP e resposta JSON
  services/       uma classe por caso de uso, validações e transações
  models/         nove entidades db.Model + mixin de CRUD
  repositories/   filtros de recomendações e conflitos de agenda
  middleware/     autenticação JWT
  tests/          testes reais de API com banco SQLite
frontend/
  web/            interface completa validada nesta entrega
  visagio/        aplicativo Flutter original preservado como legado
```

As Models herdam de `db.Model` e `PersistenceMixin`. `salvar`, `atualizar`, `deletar`, `listar_todos` e `buscar_por_id` estão em `models/base.py` e são herdados por todas as entidades. Models fazem `flush`; Services concluem a transação com `commit`. Em caso de erro, a API faz rollback. CRUD simples não passa por Repository. As consultas especiais são `RecommendationRepository.search` e `AppointmentRepository.overlaps`. Não há Stored Procedure.

O [diagrama de classes do domínio](docs/diagrama-classes.md) documenta atributos, cardinalidades, herança e composição. O código Mermaid também está em [docs/diagrama-classes.mmd](docs/diagrama-classes.mmd).

## Escopo e limitações explícitas

- **Interface de entrega:** `frontend/web`, servida pelo próprio Flask. Não precisa de Node, Flutter ou internet para abrir.
- **Flutter:** foi preservado para continuidade do projeto; não foi compilado/testado nesta entrega e não contém todas as novas operações. O antigo modo demonstrativo e suas pontuações fixas não servem como evidência. Use a interface web para a avaliação.
- **Análise:** registro de características informadas pelo usuário, sem detecção facial automática. As sugestões são regras de catálogo local em `SuggestStylesService`, sem LLM ou chave externa. Não se conta análise por IA como funcionalidade.
- **Comparação:** registra referências antes/depois por URL. Não transforma imagens. A abertura das imagens depende de URLs públicas acessíveis.
- **Agenda:** profissionais fictícios; nenhuma reserva é enviada a um estabelecimento real. Horários entram no fuso local do navegador e são armazenados em UTC. Registros futuros não podem ser concluídos; horários sobrepostos são recusados.
- **Autenticação:** hash de senha Werkzeug, JWT de 8 horas e autorização por proprietário; token apenas na sessão do navegador. Rotas não confiam em `client_id` enviado pelo cliente.
- **Produção:** esta é uma entrega acadêmica. Não inclui migração automática, recuperação de senha, infraestrutura de produção ou garantia de concorrência em SQLite. MySQL usa bloqueio de linha do profissional nas reservas.
- **Segredos:** `.env`, banco de dados local, caches e builds estão no `.gitignore`; `.env.example` contém apenas campos vazios/exemplos.

## Testes

Na raiz:

```bash
python -m pytest backend/tests -q
```

Resultado desta entrega: **15 testes Python aprovados**, além de teste de navegador com **67 requisições reais cobrindo as 30 operações**, sem erros.

Os testes cobrem CRUD com verificação do banco, autenticação, dados inválidos, isolamento entre contas, rollback, vínculos entre análises e recomendações, exclusão em cascata e conflito de horários. Consulte [docs/validacao.md](docs/validacao.md) para resultados e limites.

## Entrega ao professor

1. Extraia e execute o projeto; confira os fluxos com os dados do grupo.
2. Confira o [vídeo demonstrativo incluído (1min22s)](docs/demonstracao.mp4) e o [roteiro de até 5 minutos](docs/roteiro-video.md). O vídeo é obrigatório para a avaliação; o grupo ainda precisa enviá-lo.
3. Copie os arquivos para o clone do repositório oficial, em uma branch de entrega. Revise `git diff` e `git status` antes do commit.
4. Execute os testes, faça commit e push. O endereço/acesso do repositório oficial não veio no ZIP; nenhum push oficial foi realizado nesta entrega.
5. Envie o link do repositório e o vídeo no ambiente da disciplina.

```bash
git switch -c entrega-funcionalidades
# Copie os arquivos atualizados para o clone antes dos comandos abaixo.
git add README.md .gitignore backend frontend docs
git commit -m "Implementa funcionalidades completas e arquitetura em camadas"
git push -u origin entrega-funcionalidades
```

Há também um [bundle do commit local](docs/git.md) no pacote. Ele não substitui o push oficial.
