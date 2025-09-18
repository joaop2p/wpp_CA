from os import getenv
from dotenv import load_dotenv
from configparser import ConfigParser
# --- Carregamento das variavies de ambiente
load_dotenv()
data_path = getenv('DATA_FILE')
driver_cache = getenv('CACHE_DRIVER_PATH')

# --- Carregamento das Configurações do aplicativo
config = ConfigParser()
with open('config.ini', 'r', encoding='utf-8') as f:
    config.read_file(f)