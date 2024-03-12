from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    logging_file_name: str = "app.log"
    """Файл для логов"""
    mongo_url: str = "mongodb://mongodb:27017"
    """Ссылка для подключения к mongo"""

    # ключи, устанавливаемые в интерфейсе moodle для LTI протокола
    session_public_key: str = "publickey"
    """Публичный ключ"""
    session_secret_key: str = "secretkey"
    """Секретный ключ"""

    # для установки jwt-токена в куки, которую будет читать js приложение
    jwt_secret: str = "change_me_plz"
    """Секрет для генерации jwt"""
    jwt_algorithm: str = "HS256"
    """Алгоритм для генерации jwt"""
    jwt_cookie_name: str = "session_token"
    """Имя куки для jwt токена"""
    jwt_user_id_param_name: str = "user_id"
    """Имя параметра для user_id в jwt"""
    jwt_pass_back_params_param_name: str = "pass_back_params_json"
    """Имя параметра для pass_back_params"""
    jwt_task_id_param_name: str = "task_id"
    """Имя параметра для task_id в jwt"""
    jwt_is_tried_param_name: str = "is_tried"
    """Имя параметра для is_tried в jwt"""
    jwt_is_success_param_name: str = "is_success"
    """Имя параметра для is_success в jwt"""

    # для работы в docker-compose
    nginx_host_name: str = "localhost"
    """Хост nginx, с которого редиректим на приложение в контейнере"""
    nginx_host_port: str | None = None

    # для редиректа на задачу
    js_task_uri: str = "/js_app/task/"

    class Config:
        env_file = ".env.local"
        # env_file = "../.env"
        """Путь до файла с переменными окружения"""


settings = Settings()
