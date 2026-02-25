import re
from datetime import datetime
from configparser import ConfigParser
from utils.logger import logger
from PIL import Image


def contar_paginas_tiff(caminho_arquivo):
    try:
        with Image.open(caminho_arquivo) as img:
            return getattr(img, "n_frames", 1)
    except Exception as e:
        print(f"Erro ao contar páginas: {e}")
        logger.error(f"Erro ao contar páginas: {e}")
        return 0

# Função que retorna data atual em dia, mês e ano
def dia_corrente():
    try:
        data = datetime.today()
        strData = data.strftime('%d/%m/%Y')
        dia, mes, ano = strData.split('/')
        return int(ano), int(mes), int(dia)
    except Exception as e:
        logger.error("Erro ao calcular o dia corrente", exc_info=True)
        return 2023, 1, 1  # fallback

# Função para carregar a fonte do arquivo de config
def carrega_fonte_config(config_path='config.ini'):
    nome_fonte = 'MS Shell Dlg 2'
    tamanho_fonte = 11

    try:
        config = ConfigParser()
        config.read(config_path)
        fonte_str = config['APARENCIA']['FONTE']
        match = re.search(r'(?<=\().*,\d\d', fonte_str)
        if match:
            nome_fonte, tamanho = match.group().split(',')
            return nome_fonte.strip(), int(tamanho)
    except Exception as e:
        logger.warning("Erro ao carregar fonte do config.ini, usando fonte padrão", exc_info=True)

    return nome_fonte, tamanho_fonte


if __name__ == "__main__":
    pass