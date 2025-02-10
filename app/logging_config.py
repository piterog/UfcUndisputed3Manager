import logging
from logging.handlers import TimedRotatingFileHandler
import os


def setup_logging(app=None):
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_filename = os.path.join(log_directory, 'app.log')

    # Configura o handler para rotação diária
    handler = TimedRotatingFileHandler(
        log_filename,
        when="midnight",  # A rotação ocorre à meia-noite
        interval=1,  # Rotaciona a cada 1 dia
        backupCount=7  # Mantém os últimos 7 dias de logs
    )
    handler.suffix = "%Y-%m-%d"  # Formato do arquivo (data no nome)

    # Formatação dos logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    # Configura o logger global
    if app:
        app.logger.setLevel(logging.INFO)  # Define o nível de log
        app.logger.addHandler(handler)

    # Retorna o logger caso você precise usá-lo diretamente
    return handler
