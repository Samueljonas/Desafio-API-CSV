
# Desafio de Integração de Dados Web com Django

Este projeto consiste em uma aplicação web desenvolvida com o framework Django. O objetivo principal é demonstrar a capacidade de integrar dados de fontes externas — especificamente, uma API pública do IBGE e um arquivo CSV da Receita Federal — e persistir essas informações em um banco de dados relacional. Posteriormente, os dados são apresentados em uma interface web com funcionalidades de navegação, filtragem e paginação para uma visualização organizada.

### Tabela de Conteúdo

1.  [Instalação e Execução Local](https://www.google.com/search?q=%231-instala%C3%A7%C3%A3o-e-execu%C3%A7%C3%A3o-local)
2.  [Configuração do Ambiente](https://www.google.com/search?q=%232-configura%C3%A7%C3%A3o-do-ambiente)
3.  [Importação dos Dados](https://www.google.com/search?q=%233-importa%C3%A7%C3%A3o-dos-dados)
4.  [Acessando a Aplicação Web](https://www.google.com/search?q=%234-acessando-a-aplica%C3%A7%C3%A3o-web)
5.  [Funcionalidades](https://www.google.com/search?q=%235-funcionalidades)

### 1\. Instalação e Execução Local

As instruções a seguir detalham o processo para clonar e executar o projeto em um ambiente de desenvolvimento local.

#### Pré-requisitos

  * Python 3.9+
  * PostgreSQL

#### Passos

1.  Clone o repositório do projeto:

    ```
    git clone https://github.com/Samueljonas/Desafio-API-CSV.git
    cd Desafio-API-CSV
    ```

2.  Crie e ative um ambiente virtual para isolar as dependências do projeto:

    ```
    python -m venv venv
    source venv/bin/activate
    ```

3.  Instale as dependências necessárias, conforme especificado no arquivo `requirements.txt`:

    ```
    pip install -r requirements.txt
    ```

### 2\. Configuração do Ambiente

#### Banco de Dados (PostgreSQL)

O projeto utiliza o PostgreSQL como sistema de gerenciamento de banco de dados. É necessário criar um usuário e um banco de dados dedicados para a aplicação.

1.  Acesse o shell do PostgreSQL como o usuário padrão `postgres`:

    ```
    sudo -i -u postgres psql
    ```

2.  Crie um usuário e um banco de dados, atribuindo permissões totais ao usuário. Substitua `seu_usuario` e `sua_senha` pelas suas credenciais:

    ```sql
    CREATE USER seu_usuario WITH PASSWORD 'sua_senha';
    CREATE DATABASE ibge_data OWNER seu_usuario;
    GRANT ALL PRIVILEGES ON DATABASE ibge_data TO seu_usuario;
    \q
    ```

#### Configurações do Django

1.  Abra o arquivo `ibge_data_project/settings.py`.

2.  Na seção `DATABASES`, configure os parâmetros de conexão do banco de dados criado:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'ibge_data',
            'USER': 'seu_usuario',
            'PASSWORD': 'sua_senha',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

### 3\. Importação dos Dados

Para popular o banco de dados, as migrações devem ser aplicadas e, em seguida, os comandos customizados do Django devem ser executados para a importação de dados.

1.  **Aplicação das Migrações do Django:**

    ```
    python manage.py makemigrations localities
    python manage.py migrate
    ```

2.  **Importação de dados da API do IBGE:**
    Este comando realiza a busca e a persistência de todas as Regiões, Estados, Municípios e Distritos no banco de dados. O processo pode ser demorado, mas a implementação de lógica de tratamento de erros e re-tentativas assegura a conclusão da importação.

    ```
    python manage.py populate_ibge_data
    ```

3.  **Importação de dados do arquivo CSV (Receita Federal):**

      * Baixe o arquivo `Empresas0.zip` do site da Receita Federal e descompacte-o, obtendo o arquivo `Empresas0.csv`.
      * Crie uma pasta chamada `data` na raiz do projeto e mova o arquivo CSV para este diretório.
      * Execute o comando de importação em massa:
        ```
        python manage.py import_empresas data/Empresas0.csv
        ```

    Este comando é otimizado para grandes volumes de dados, criando ou atualizando os registros de empresas de maneira eficiente.

### 4\. Acessando a Aplicação Web

Após a população do banco de dados, o servidor de desenvolvimento do Django pode ser iniciado para acessar a aplicação.

1.  Rode o servidor local:

    ```
    python manage.py runserver
    ```

2.  Abra um navegador web e acesse o seguinte URL: `http://127.0.0.1:8000/`.

### 5\. Funcionalidades

A aplicação web oferece as seguintes funcionalidades:

  * **Listagem de Estados:** Exibe todos os estados brasileiros com paginação.
  * **Listagem de Municípios:** Apresenta todos os municípios com paginação e um filtro por estado.
  * **Listagem de Distritos:** Mostra todos os distritos com paginação e um filtro por estado.
  * **Listagem de Empresas:** Exibe as empresas importadas com paginação e uma funcionalidade de busca por CNPJ.
  * **Estilização:** A interface foi estilizada com o framework CSS Bootstrap, resultando em uma melhor usabilidade e visual profissional.
