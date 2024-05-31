import hashlib


class SessionsService:
    @staticmethod
    def generate_session_id_by_jwt_token(jwt_token: str) -> str:
        """Получить идентификатор сессии по JWT токену"""

        return hashlib.sha256(jwt_token.encode("utf-8")).hexdigest()
