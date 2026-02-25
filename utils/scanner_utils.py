import os
import shutil
from utils.logger import logger
from PIL import Image

def processar_digitalizacao_simples(configuracoes, caminho_destino_pdf):
    """
    Processa a digitalização simples: converte 0001.TIF da pasta temp_index para PDF e salva no caminho especificado.
    
    :param configuracoes: Instância da classe Configuracoes
    :param caminho_destino_pdf: Caminho completo de onde salvar o PDF final (inclui nome do arquivo)
    """

    # Monta o caminho completo da imagem TIF na pasta temp_index do usuário
    caminho_temp_index = os.path.join(
        configuracoes.get_caminho_temp_index(),
        configuracoes.get_temp_index_usuario()
    )
    arquivo_tif = os.path.join(caminho_temp_index, '0001.TIF')

    if not os.path.exists(arquivo_tif):
        logger.error(f"Arquivo TIFF da digitalização não encontrado: {arquivo_tif}")
        raise FileNotFoundError(f"Arquivo TIFF da digitalização não encontrado: {arquivo_tif}")

    try:
        # Converte o TIFF para PDF usando PIL
        with Image.open(arquivo_tif) as img:
            img.convert('RGB').save(caminho_destino_pdf, "PDF")
            logger.info(f"PDF gerado em: {caminho_destino_pdf}")
            print(f"PDF gerado em: {caminho_destino_pdf}")
    except Exception as e:
        logger.error(f"Erro ao converter TIFF em PDF: {str(e)}")
        raise Exception(f"Erro ao converter TIFF em PDF: {e}")

    try:
        os.remove(arquivo_tif)
        logger.info(f"Arquivo TIFF removido de {arquivo_tif}")
    except Exception as e:
        logger.error(f"Erro ao remover arquivo TIFF temporário: {str(e)}")
        raise Exception(f"Erro ao remover arquivo TIFF temporário: {e}")


def processar_digitalizacao(tipo_documento: int, num_documento, caminho_temp, caminho_base, caminho_backup, pasta_usuario, ano_cert=None, num_cert=None, tipo_operacao="novo nocumento") :

    tipos_de_documento = ['matricula', 
                        'Protocolo',
                        'CERTIDAO',
                        'auxiliar',
                        'CERTIDAO',
                        'Protocolo'
    ]
    nome_arquivo_temp = '0001.TIF'
    # Construção do caminho do arquivo original
    caminho_original = os.path.normpath(os.path.join(caminho_base, tipos_de_documento[tipo_documento]))

    if tipo_documento in [2, 4]:
        if not (ano_cert and num_cert):
            raise ValueError("Ano da certidão e número da certidão são obrigatórios para este tipo de documento.")

        subpasta = f"L00020{ano_cert}"
        nome_arquivo = f"{str(num_cert).zfill(6)}.TIF"
    else:
        if not num_documento:
            raise ValueError("Número do documento é obrigatório para este tipo de documento.")

        num_documento = str(num_documento).zfill(6)
        subpasta = num_documento[:3]
        nome_arquivo = f"{num_documento[-3:]}.TIF"

    caminho_arquivo_backup = os.path.normpath(os.path.join(caminho_backup,
        tipos_de_documento[tipo_documento],
        subpasta,
        nome_arquivo
    ))

    caminho_novo = os.path.normpath(os.path.join(caminho_original, subpasta, nome_arquivo))
    caminho_temp_arquivo = os.path.normpath(os.path.join(caminho_temp, pasta_usuario, nome_arquivo_temp))

    # Verificação de existência dos caminhos, se não existe o caminho original, e for um documento novo
    # levantar exceção de filenot found
    if not os.path.exists(caminho_original) and tipo_operacao != "novo documento":
        logger.error(f"Arquivo original não encontrado: {caminho_original}")
        raise FileNotFoundError(f"Arquivo original não encontrado: {caminho_original}")

    if not os.path.exists(caminho_temp_arquivo):
        logger.error(f"Arquivo digitalizado não encontrado: {caminho_temp_arquivo}")
        raise FileNotFoundError(f"Arquivo digitalizado não encontrado: {caminho_temp_arquivo}")

    # Criação de diretório para backup, se não existir
    os.makedirs(os.path.dirname(caminho_arquivo_backup), exist_ok=True)

    try:
        # Realiza o backup
        if tipo_operacao != "novo documento":
            shutil.copy2(caminho_novo, caminho_arquivo_backup)
            print(f"Backup realizado: {caminho_arquivo_backup}")
        else:
            shutil.copy2(caminho_temp_arquivo, caminho_arquivo_backup)
            print(f"Backup realizado: {caminho_arquivo_backup}")

        # Substituição da nova digitalização
        os.makedirs(os.path.dirname(caminho_novo), exist_ok=True)
        shutil.move(caminho_temp_arquivo, caminho_novo)
        print(f"Arquivo substituído: {caminho_novo}")

    except Exception as e:
        logger.error(f"Erro ao processar digitalização: {str(e)}")
        raise Exception(f"Erro ao processar digitalização: {e}")
    
    if os.path.exists(caminho_temp_arquivo):
        try:
            # Apaga arquivo digitalizado em temp_index caso não tenha sido movido
            os.remove(caminho_temp_arquivo)
        except Exception as e:
            logger.error(f"Erro ao remover o arquivo de digitalização temporário! {str(e)}")
            raise Exception(f"Erro ao remover o arquivo de digitalização temporário! {e}")

if __name__ == "__main__":
    pass