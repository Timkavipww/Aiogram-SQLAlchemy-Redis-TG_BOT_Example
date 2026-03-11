import os

class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    ADMIN_IDS: list = []
 
    @classmethod
    def _parse_admin_ids(cls):
        admin_ids_str = os.getenv("ADMIN_IDS", "")
        if admin_ids_str:
            admin_ids = [int(x.strip()) for x in admin_ids_str.split(",") if x.strip()]
            return admin_ids
        
        return []

    @classmethod
    def validate_config(cls):

        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не найден в .env файле")
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL не найден в .env файле")
        
        cls.ADMIN_IDS = cls._parse_admin_ids()
        
        if not cls.ADMIN_IDS:
            print("⚠️ ADMIN_IDS не установлен или пуст. Админские функции будут недоступны.")

