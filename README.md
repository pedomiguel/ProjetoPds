Para subir o banco de dados, basta executar:

```bash
docker-compose up -d
```
Para entrar no envirement execute:
```bash
uv venv                     # Cria o ambiente
source .venv/bin/activate   # Ativa o ambiente (Linux)
uv sync                     # Instalar dependências
```

## ✅ Funcionalidades

- _Upload e Manipulação de Áudio via IA_

  - Importar áudio e extrair componentes do audio: instrumental, vocal, bpm, etc.
  - Importar áudio e extrair informações: chave, bpm, etc.
  - Importar áudio e restaurar qualidade da extração
  - Dividir a faixa em multitracks: percursão, melodia, vocal e baixo
  - Dividir vocais em vocais principais e vocais de auxilio
  - Adicionar extrações e/ou restaurações em cascata (pipeline)
  - Ver enviados e os áudios gerados/manipulados

- _Postagens e Interações_

  - Criar postagem com tema
    - Adicionar áudios gerados e/ou manipulados
    - Adiconar uma template de pipeline
  - Ver postagens
  - Filtrar postagens por tema
  - Adicionar comentário com áudio e/ou template de pipeline
  - Ver comentários
  - Apagar postagem
  - Editar postagem
  - Editar comentário
  - Apagar comentário

- _Conta e Comunidade_

  - Login/registro
  - Seguir usuários
  - Perfil público
    - Informações do usuário
    - Posts criados
    - Audios gerados/manipulados com a pipeline

---

## 🏗 Sprint 1

### Geral

- Setup do projeto

### 👤 Pedro

- Login/registro
- Seguir usuários

### 🎵 Miguel & Edson

- Gerenciamento dos áudio (upload/download)
- Integração da LLM no projeto para aplicação das funcionalidades (extração, restauração, etc.)

---

## ✍ Sprint 2

### 👤 Pedro

- Criar postagem com tema
  - Adicionar áudios gerados e/ou manipulados
  - Adiconar uma template de pipeline
- Ver postagens
- Filtrar postagens por tema
- Apagar postagem
- Editar postagem

### 📃 Miguel

- Perfil público
  - Informações do usuário
  - Posts criados
  - Audios gerados/manipulados com a pipeline
- Adicionar comentário com áudio e/ou template de pipeline
- Ver comentários
- Editar comentário
- Apagar comentário

### 🎵 Edson

- Extrair componentes do audio: instrumental, vocal, bpm, etc.
- Extrair informações: chave, bpm, etc.
- Restaurar qualidade da extração
- Dividir a faixa em multitracks: percursão, melodia, vocal e baixo
- Dividir vocais em vocais principais e vocais de auxilio
- Adicionar extrações e/ou restaurações em cascata (pipeline)

---

## 🛠 Sprint 3

### 👤 Miguel

- Página de login
- Página de registro
- Perfil do usuário
  - Postagens
  - Audios gerados/manipulados

### 📃 Edson

- Tela de manipulação do áudio
  - Selecionar os modelos
  - Criar a pipeline
- Histórico de audios manipulados
  - Visualização dos audios enviados e audios gerados

### 🎵 Pedro

- Feed com as postagens
- Página da postagem
- Filtro de postagem
