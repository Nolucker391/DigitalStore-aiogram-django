import logging

from aiogram import Router

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot_logs.txt"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

router = Router()