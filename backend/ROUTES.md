# API

Veja a [matriz completa](../docs/funcionalidades.md).

Todas as rotas fora de `/api/auth` exigem `Authorization: Bearer <token>`. Corpo JSON; erros retornam `{ "message": "descrição" }`. Códigos: 200 leitura/edição, 201 criação, 204 exclusão, 400 validação, 401 autenticação, 404 registro inexistente/outra conta, 409 conflito.

Datas de procedimentos: `AAAA-MM-DD`. Horários: ISO 8601 com fuso; armazenados em UTC. IDs numéricos positivos. PUT aceita alterações parciais, exceto preferências, que recebe os dois campos. Categorias: haircut, beard, coloring, care.
