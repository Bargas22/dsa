# Banco de dados
As Models SQLAlchemy são a fonte do esquema. Execute `flask --app app:create_app init-db` e `flask --app app:create_app seed-demo` no diretório backend.

Para MySQL 8, crie um banco vazio `visagio_v2` com charset utf8mb4 e configure DATABASE_URL. Não execute sobre o banco do ZIP antigo: esta entrega altera tipos e colunas. Faça backup antes de planejar qualquer migração. `create_all` cria tabelas, não migra tabelas existentes.

SQLite é o padrão para demonstração local e testes. Datas de agendamento são armazenadas em UTC; a interface web converte do horário local do navegador. MySQL precisa de transações InnoDB; a reserva bloqueia a linha do profissional para evitar conflitos concorrentes. SQLite destina-se a uso local, não a reservas concorrentes em produção.
