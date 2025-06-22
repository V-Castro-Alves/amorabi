## Como rodar o projeto

### Usando Docker

1. **Certifique-se de ter o Docker e o Docker Compose instalados.**
2. No terminal, navegue até a raiz do projeto (onde está o arquivo `docker-compose.yml`).
3. Execute o comando:

   ```sh
   docker-compose up --build
   ```

4. O serviço estará disponível em [http://localhost:8000](http://localhost:8000).

---

### Rodando localmente (sem Docker)

1. **Pré-requisitos:** Python 3.12+, pip e virtualenv.
2. No terminal, navegue até a pasta `amorabi/amorabi` (onde está o `manage.py`).
3. Crie e ative um ambiente virtual:

   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

4. Instale as dependências:

   ```sh
   pip install -r requirements.txt
   ```

5. Aplique as migrações e colete os arquivos estáticos:

   ```sh
   python manage.py makemigrations
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

6. Rode o servidor de desenvolvimento:

   ```sh
   python manage.py runserver
   ```

7. Acesse [http://localhost:8000](http://localhost:8000) no navegador.

---

**Obs:** O usuário admin pode ser criado com:

```sh
python manage.py createsuperuser
```