# MediLeaf-backend
This repository is actually a production ready admin dashboard consist of several REST APIs to access the knowledge base and user authentication of the MediLeaf project.

## Live Preview
[Click Here](https://medi-leaf-backend.vercel.app)

## Local Preview

### A. Using Docker
1. Clone the repository
   ```bash
    git clone  https://github.com/surajkarki66/MediLeaf_backend
    ``` 
2. Make sure that the Docker and docker-compose is installed in your local computer. If not installed, you can install it using this [link](https://docs.docker.com/engine/install/).
3. Create a `.env` file in a project root directory and set all the environment variables based on the provided `.env.sample` example. Remember one thing while setting the environment variables in `.env`, keep the database configuration variables as it is.
   
4. Now, go to `settings.py` which is inside `MediLeaf_backend` and then find two variables: `CSRF_COOKIE_HTTPONLY` and `CSRF_COOKIE_SAMESITE`, and set them as:
   ```python
    CSRF_COOKIE_HTTPONLY = False
    CSRF_COOKIE_SAMESITE = "None"
   ```
5. Run the following docker command.

   ```bash
    docker-compose up --build
    ```

To access the APIs: http://127.0.0.1:8000/

To access the APIs documentations: http://127.0.0.1:8000/docs/

To access the admin panel click here: http://127.0.0.1:8000/admin


### B. Locally
1. Clone the repository
   ```bash
    git clone  https://github.com/surajkarki66/MediLeaf_backend
    ```

2. Create a Python virtual environment and activate the environment based on your machine(Linux, MacOS, and Windows)

3. Install the dependencies
   ```bash
    make install
   ```
4. Create a `.env` file in a project root directory and set all the environment variables based on the provided `.env.sample` example.

5. Now, go to `settings.py` which is inside `MediLeaf_backend` and then find two variables: `CSRF_COOKIE_HTTPONLY` and `CSRF_COOKIE_SAMESITE`, and set them as:
   ```python
    CSRF_COOKIE_HTTPONLY = False
    CSRF_COOKIE_SAMESITE = "None"
   ```

6. Migrate the database
   ```bash
    make migrate
    ```

7. If you want to create a super user then enter the following command.
    ```bash
    make superuser
    ```

8. Run the development server
    ```bash
    make run
    ```

To access the APIs: http://127.0.0.1:8000/

To access the APIs documentations: http://127.0.0.1:8000/docs/

To access the admin panel click here: http://127.0.0.1:8000/admin


Happy coding!!