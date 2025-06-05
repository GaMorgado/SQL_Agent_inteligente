
## :rocket: Pré-requisitos

Para executar este projeto, você precisará de uma das seguintes configurações de ambiente:

* **Opção 1: Ambiente com Docker**
    * Docker instalado.
    * Docker Compose instalado.
* **Opção 2: Ambiente Local (sem Docker)**
    * Python 3.10 ou superior instalado.
    * Acesso a uma instância de banco de dados PostgreSQL (ou o configurado).

## :wrench: Configuração do Ambiente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/GaMorgado/SQL_Agent_inteligentet](https://github.com/GaMorgado/SQL_Agent_inteligente)
    cd Projeto_Verity
    ```

2.  **Configure as variáveis de ambiente:**
    Crie um arquivo chamado `.env` na raiz do projeto (copiando de um `.env.example` se existir, ou criando um novo). Este arquivo conterá configurações sensíveis e específicas do ambiente.

    Exemplo básico de conteúdo para o `.env`:
    ```env
    # Chaves de API
    OPENAI_API_KEY=sua_chave_openai_aqui

    # Configuração do Banco de Dados (para Docker Compose e execução local)
    # Usado pelo docker-compose.yaml para inicializar o container do banco
    POSTGRES_USER=seu_usuario_db
    POSTGRES_PASSWORD=sua_senha_db
    POSTGRES_DB=nome_do_seu_banco
    
    # String de conexão para a aplicação Python (se rodando localmente ou dentro do Docker)
    # Se estiver usando Docker, o host pode ser o nome do serviço do banco (ex: 'db')
    SQLALCHEMY_DATABASE_URL=postgresql://seu_usuario_db:sua_senha_db@localhost:5432/nome_do_seu_banco
    CHECKPOINTER_DATABASE_URL=postgresql://seu_usuario_db:sua_senha_db@localhost:5432/nome_do_seu_banco 
    # Ajuste 'localhost' para o nome do serviço Docker se a aplicação rodar em um container e o banco em outro.
    ```
    *Adapte as variáveis conforme necessário para o seu projeto (ex: chaves de API de outros serviços, URLs de banco de dados diferentes).*

3.  **(Opcional) Para execução local, configure o banco de dados manualmente:**
    Se você não for usar o Docker para o banco de dados, certifique-se de que sua instância PostgreSQL esteja acessível e execute o script `init-db.sql` para criar as tabelas e carregar os dados iniciais.

## :whale: Execução com Docker

Esta é a forma recomendada para garantir um ambiente consistente.

1.  **Build e subida dos containers:**
    Na raiz do projeto (onde está o `docker-compose.yaml`), execute:
    ```bash
    docker-compose up --build -d
    ```
    O `-d` executa os containers em segundo plano. Remova-o se quiser ver os logs diretamente no terminal.

2.  **Acesso à Aplicação:**
    O serviço principal (provavelmente sua API ou interface) estará rodando localmente na porta configurada no `docker-compose.yaml` e/ou no seu `main.py`. Verifique os logs para confirmar.

## :arrow_forward: Execução Local (sem Docker)

1.  **Crie e ative um ambiente virtual Python:**
    É uma boa prática para isolar as dependências do projeto.
    ```bash
    python -m venv venv 
    ```
    Para ativar:
    * Linux ou macOS:
        ```bash
        source venv/bin/activate
        ```
    * Windows (PowerShell):
        ```ps1
        .\venv\Scripts\Activate.ps1
        ```
    * Windows (CMD):
        ```bash
        venv\Scripts\activate.bat
        ```

2.  **Instale as dependências:**
    Com o ambiente virtual ativo:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure o Banco de Dados:**
    Certifique-se de que você tem uma instância do PostgreSQL rodando e acessível, e que as variáveis de ambiente (como `SQLALCHEMY_DATABASE_URL` no seu `.env`) apontam para ela. Execute o script `init-db.sql` manualmente neste banco, se ainda não o fez.

4.  **Execute o projeto:**
    ```bash
    python main.py
    ```

## :construction_site: Banco de Dados

* O projeto utiliza um banco de dados relacional, configurado para PostgreSQL através da variável de ambiente `SQLALCHEMY_DATABASE_URL` (ou similar, para a aplicação) e `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` (para o container Docker).
* O script `init-db.sql` contém a estrutura inicial do banco de dados e, possivelmente, dados de exemplo.
    * Ao usar Docker, este script é geralmente executado automaticamente na primeira vez que o container do banco de dados é criado (se montado em `/docker-entrypoint-initdb.d/`).
    * Para execução local, você precisa executar este script manualmente no seu servidor de banco de dados.

## :scroll: Comandos Úteis do Docker Compose

(Execute a partir do diretório raiz do projeto)

* **Subir os containers em segundo plano:**
    ```bash
    docker-compose up -d
    ```
* **Subir os containers e recriá-los (útil após mudanças no `docker-compose.yaml`):**
    ```bash
    docker-compose up -d --force-recreate
    ```
* **Subir os containers e fazer build das imagens (útil após mudanças no Dockerfile ou código fonte):**
    ```bash
    docker-compose up --build -d
    ```
* **Ver logs de todos os containers (em tempo real):**
    ```bash
    docker-compose logs -f
    ```
* **Ver logs de um container específico:**
    ```bash
    docker-compose logs -f <nome_do_servico_no_compose_yaml> 
    ``` 
    (ex: `docker-compose logs -f db`)
* **Derrubar (parar e remover) os containers:**
    ```bash
    docker-compose down
    ```
* **Derrubar os containers e remover volumes anônimos:**
    ```bash
    docker-compose down -v
    ```

## :tools: Tecnologias Utilizadas (Exemplos)

* **Python**
* **Docker & Docker Compose**
* **PostgreSQL** 
* **OpenAI API** 
* **LangChain / LangGraph** 