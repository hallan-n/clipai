from loguru import logger


logger.remove()

logger.add(
    sink=lambda msg: print(msg, end=''), 
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>"
)