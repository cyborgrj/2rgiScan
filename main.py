########################################################################
## IMPORTS
########################################################################

########################################################################
## Sistema/Úteis
########################################################################
import sys
import shutil
import os
from subprocess import Popen, CalledProcessError, run
import re
from datetime import datetime, time, date
import locale
import configparser
import unicodedata

########################################################################
## GUI
########################################################################
from PySide6.QtCore import QDate, Qt, QThread, Signal, QEvent, QTimer, QCoreApplication
from PySide6.QtGui import QFont, QIcon, QPixmap, QWheelEvent, QAction, QStatusTipEvent
from PySide6.QtWidgets import (
    QLabel,
    QDialog,
    QVBoxLayout,
    QWidget,
    QMainWindow,
    QScrollArea,
    QMenuBar,
    QMessageBox,
    QApplication,
    QSystemTrayIcon,
    QMenu,
    QHeaderView,
    QProgressBar,
    QTableWidgetItem,
    QAbstractItemView,
)
from gui import *
from gui.toast import Toast

########################################################################
## Banco de dados
########################################################################
from db.db import DataBaseUsers
from db.db_handler import DBHandler

########################################################################
## Utilitários
########################################################################
from utils.logger import logger
from utils.loading import LoadingDialog
from utils.helpers import contar_paginas_tiff
from utils.scanner_utils import processar_digitalizacao, processar_digitalizacao_simples

########################################################################
## Relatórios/PDF
########################################################################
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from PyPDF2 import PdfReader, PdfWriter

########################################################################
## E-Mail
########################################################################
from email_rgi.mail import envia_email

########################################################################
# Criar objeto de janela para "system tray" global
window_obj = []
########################################################################

# nomes de documentos comums para referência e uso no sistema
nomes_documentos = [
    "Matrícula",
    "Protocolo",
    "Certidão",
    "Registro Auxiliar",
    "Certidão Cancelada",
    "Protocolo Cancelado",
]

# nomes de pastas para conferência de erro
nomes_conferencia = [
    "matricula",
    "procotolo",
    "certidao",
    "auxiliar",
    "certidao",
    "protocolo",
]

# Dicionário com nomes de tabelas e variáveis da tabela pra cada tipo de documento
tab_doc = {
    0: ["Matricula", "nummat"],
    1: ["Protocolo", "numprot"],
    2: ["Certidao", "numcert", "anocert"],
    3: ["RegistroAuxiliar", "numreg"],
    4: ["CertidaoCancelada", "numcertcanc", "anocertcanc"],
    5: ["ProtocoloCancelado", "numprotcanc"],
}


########################################################################
#### Validação do banco de dados DataBaseUsers


def validar_sqlite(users_db: DataBaseUsers):
    try:
        users_db.get_sigla_users()
    except Exception as e:
        print(f"Erro ao verificar/criar tabela users: {e}")
        logger.error(f"Erro ao verificar/criar tabela users: {e}")


def validar_postgresql(db_handler: DBHandler):
    try:
        db_handler.cursor.execute("SELECT 1")
        print("Conexão com o PostgreSQL estabelecida com sucesso.")
    except Exception as e:
        print(f"Erro ao conectar com o banco PostgreSQL: {e}")
        logger.error(f"Erro ao conectar com o banco PostgreSQL: {e}")


########################################################################


def dia_corrente():
    data = datetime.today()
    strData = data.strftime("%d/%m/%Y")
    dia, mes, ano = strData.split("/")
    # print(f'Dia: {dia}, mês: {mes}, ano: {ano}')
    return int(ano), int(mes), int(dia)


def abrir_com_visualizador_classico(caminho_arquivo):
    run(
        [
            "rundll32.exe",
            "C:\\Windows\\System32\\shimgvw.dll,ImageView_Fullscreen",
            caminho_arquivo,
        ],
        shell=True,
    )


class ExemploDocumentoDialog(QDialog):
    def __init__(self, tipo_documento, parent=None):
        super().__init__(parent)
        self.tipo_documento = tipo_documento
        self.zoom_factor = 0.8
        self._dragging = False
        self._last_mouse_pos = None

        self.setWindowTitle(f"Exemplo de documento: {tipo_documento}")
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )

        layout = QVBoxLayout(self)

        self.menu_bar = QMenuBar()
        ajuda_action = QAction(f"Mais informações sobre o {tipo_documento}?", self)
        ajuda_action.triggered.connect(self.exibir_ajuda)
        self.menu_bar.addAction(ajuda_action)
        layout.setMenuBar(self.menu_bar)

        self.setup_visual_ajuda()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setCursor(Qt.CursorShape.OpenHandCursor)

        self.scroll_area.setWidget(self.label)
        layout.addWidget(self.scroll_area)

        self.setLayout(layout)
        self.carregar_imagem()

        self.label.installEventFilter(self)

    def setup_visual_ajuda(self):
        self.setStyleSheet(
            """
            QDialog { background-color: #2e2e2e; }
            QLabel { background-color: #2e2e2e; color: white; }
            QScrollArea { background-color: #2e2e2e; border: none; }
            QMenuBar { background-color: #444; color: white; }
            QMenuBar::item { background: transparent; padding: 4px 10px; }
            QMenuBar::item:selected { background-color: #666; }
        """
        )

    def carregar_imagem(self):
        caminho = os.path.join("src", f"{self.tipo_documento}.png")
        if not os.path.exists(caminho):
            QMessageBox.warning(
                self, "Imagem não encontrada", f"Imagem {caminho} não encontrada."
            )
            self.close()
            return

        self.pixmap_original = QPixmap(caminho)
        self.atualizar_imagem()

    def atualizar_imagem(self):
        if self.pixmap_original:
            pixmap = self.pixmap_original.scaled(
                self.zoom_factor * self.pixmap_original.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.label.setPixmap(pixmap)

    # Verificar zoom, scrool, pela roda do mouse etc.
    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.HelpRequest:
            self.exibir_ajuda()
            return True

        if source == self.label:
            if event.type() == QEvent.Type.Wheel:
                angle = event.angleDelta().y()
                self.zoom_factor += 0.1 if angle > 0 else -0.1
                self.zoom_factor = max(0.1, min(5.0, self.zoom_factor))
                self.atualizar_imagem()
                return True

            elif event.type() == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.LeftButton:
                    self._dragging = True
                    self._last_mouse_pos = event.globalPos()
                    self.label.setCursor(Qt.CursorShape.ClosedHandCursor)
                    return True

            elif event.type() == QEvent.Type.MouseMove and self._dragging:
                delta = event.globalPos() - self._last_mouse_pos
                self._last_mouse_pos = event.globalPos()

                self.scroll_area.horizontalScrollBar().setValue(
                    self.scroll_area.horizontalScrollBar().value() - delta.x()
                )
                self.scroll_area.verticalScrollBar().setValue(
                    self.scroll_area.verticalScrollBar().value() - delta.y()
                )
                return True

            elif event.type() == QEvent.Type.MouseButtonRelease:
                self._dragging = False
                self.label.setCursor(Qt.CursorShape.OpenHandCursor)
                return True

        return super().eventFilter(source, event)

    def exibir_ajuda(self):
        caminho_txt = os.path.join("src", f"{self.tipo_documento}.txt")
        if os.path.exists(caminho_txt):
            with open(caminho_txt, encoding="utf-8") as f:
                conteudo = f.read()
            QMessageBox.information(self, f"Sobre o {self.tipo_documento}", conteudo)
        else:
            QMessageBox.information(
                self,
                "Ajuda não disponível",
                f"Não há descrição disponível para {self.tipo_documento}.",
            )


# Classe com métodos referente às configurações do usuário
class Configuracoes:
    def __init__(self, arquivo="config.ini"):
        self.arquivo = arquivo
        self.config = configparser.ConfigParser()
        self.config.optionxform = str  # preserva maiúsculas/minúsculas se necessário
        self.config.read(arquivo)

    def get_servidor(self):
        return self.config["REDES"]["servidor"].rstrip("\\")

    def _join_path(self, *partes):
        """Junta partes do caminho e normaliza para evitar barras duplicadas ou caminhos quebrados."""
        return os.path.normpath(os.path.join(*partes))

    def get_locais_de_rede(self):
        locais_raw = self.config.get("REDES", "locais_de_rede")
        locais = [
            self._join_path(self.get_servidor(), c.strip().lstrip("\\"))
            for c in locais_raw.split(",")
        ]
        return locais

    def get_caminho_por_indice(self, indice):
        return self.get_locais_de_rede()[indice]

    def get_caminho_temp_index(self):
        caminho = self.config["REDES"]["caminho_temp_index"].lstrip("\\")
        return self._join_path(self.get_servidor(), caminho)

    def get_caminho_base(self):
        caminho = self.config["REDES"]["caminho_base"].lstrip("\\")
        return self._join_path(self.get_servidor(), caminho)

    def get_caminho_backup(self):
        caminho = self.config["REDES"]["caminho_backup"].lstrip("\\")
        return self._join_path(self.get_servidor(), caminho)

    def get_temp_index_usuario(self):
        # Este caminho não está baseado no servidor, então só normaliza
        return os.path.normpath(self.config["REDES"]["temp_index_usuario"])

    def get_caminho_naps2(self):
        return os.path.normpath(self.config["NAPS2"]["caminho_naps2"])

    def salvar_config(self, servidor, caminho_temp_index_usuario, caminho_naps2):
        self.config["REDES"]["servidor"] = servidor
        self.config["REDES"]["temp_index_usuario"] = caminho_temp_index_usuario
        self.config["NAPS2"]["caminho_naps2"] = caminho_naps2

        with open(self.arquivo, "w") as arquivo:
            self.config.write(arquivo)

        # Recarrega para garantir que a nova config seja usada a seguir
        self.config.read(self.arquivo)

    def get_tipos_digitalizacao_simples(self):
        tipos_raw = self.config.get("REDES", "tipos_digitalizacao_simples")
        itens = [i.strip() for i in tipos_raw.split(",") if i.strip()]
        resultado = {}

        for item in itens:
            try:
                nome, caminho, formato = item.split(":", 2)
                resultado[nome.strip()] = {
                    "caminho": os.path.normpath(
                        os.path.join(self.get_servidor(), caminho.strip())
                    ),
                    "formato": formato.strip(),
                }
            except ValueError as e:
                print(f"[ERRO] Configuração inválida no item: {item} - {e}")

        return resultado


class NAPS2Thread(QThread):
    finished = Signal()

    def __init__(self, caminho_arquivo):
        super().__init__()
        self.configuracoes = Configuracoes()
        self.caminho_arquivo = caminho_arquivo

    def run(self):
        if self.caminho_arquivo:
            Popen([self.configuracoes.get_caminho_naps2(), self.caminho_arquivo]).wait()
        else:
            Popen([self.configuracoes.get_caminho_naps2()]).wait()
        self.finished.emit()


class LoadingDialog(QDialog):
    def __init__(self, parent=None, mensagem="Carregando..."):
        super().__init__(parent)
        self.setWindowTitle("Aguarde")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(400, 120)
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )

        layout = QVBoxLayout(self)

        label = QLabel(mensagem, alignment=Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)
        label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)  # Modo indeterminado
        self.progress_bar.setTextVisible(False)
        layout.addWidget(self.progress_bar)

        self.setStyleSheet(
            """
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                color: white;
            }
            QProgressBar {
                height: 18px;
                border: 1px solid #aaa;
                border-radius: 5px;
                background-color: #eee;
            }
            QProgressBar::chunk {
                background-color: #2c7be5;
                width: 20px;
                margin: 1px;
            }
        """
        )


class LoginWindow(QWidget):
    def __init__(self, parent=None):
        self.db = DataBaseUsers()
        QWidget.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.show()

        self.ui.label_incorrect_user.hide()  # Oculta a mensagem de erro inicialmente
        self.ui.label_correct_user.hide()

        self.ui.campo_usuario.returnPressed.connect(
            lambda: self.ui.campo_senha.setFocus()
        )
        self.ui.campo_senha.returnPressed.connect(lambda: self.efetuar_login())
        self.ui.sair.clicked.connect(lambda: self.sair_login())
        self.ui.btn_login.clicked.connect(lambda: self.efetuar_login())

    def sair_login(self):
        self.close()
        app.exit()

    def efetuar_login(self):
        self.ui.btn_login.setEnabled(False)
        self.ui.label_incorrect_user.clear()
        self.ui.label_incorrect_user.hide()

        usuario = self.ui.campo_usuario.text().lower()
        senha = self.ui.campo_senha.text()

        if not usuario or not senha:
            self.ui.label_incorrect_user.setText("Preencha todos os campos!")
            self.ui.label_incorrect_user.show()
            self.ui.btn_login.setEnabled(True)
            return

        username, acesso = self.db.check_users(usuario, senha)

        if acesso == "incorretas":
            self.ui.label_incorrect_user.setText("Senha ou usuário incorreto!")
            self.ui.label_incorrect_user.show()
            self.ui.btn_login.setEnabled(True)
        else:
            logger.info(f"Usuário {username} com acesso: {acesso}, logado com sucesso!")
            self.ui.label_incorrect_user.hide()
            self.window = MainWindow(usuario=username, acesso=acesso, sigla=usuario)
            self.window.show()
            self.close()


#  Passar a classe __init__ com self, user
#  Se user for caixa, self.ui.btn_cadastrar.setVisible(False)
class MainWindow(QMainWindow):
    def __init__(self, usuario, acesso, sigla):
        self.usuario = usuario
        self.acesso = acesso
        self.sigla = sigla

        self.db_auditoria = DBHandler()

        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("2rgiScan - Eduardo Rossini (2025)")
        # nome_fonte, tamanho_fonte = carrega_fonte_config()
        # self.fontTable = QFont(nome_fonte, tamanho_fonte)
        ##########################
        global window_obj
        window_obj = self.ui
        ##########################
        self.dbUsers = DataBaseUsers()
        dia = QDate()
        try:
            aa, mm, dd = dia_corrente()
        except Exception as error:
            print(f"Erro ao recuperar dia{error}")
            aa = 2023
            mm = 1
            dd = 1
        finally:
            dia.setDate(aa, mm, dd)
            self.data_padrão = str(dd) + "/" + str(mm) + "/" + str(aa)
            self.ano_corrente = str(aa)[2:]
        self.tipo_operacao = "novo documento"
        self.setCertidaoVisible(False)

        # Módulo de consulta de documentos, começa em false e habilita se for usuário de consulta
        self.ui.buttonConsultarDocumento.setVisible(False)

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.hideStatusTip())

        self.ui.setTrabalhoCB.currentIndexChanged.connect(lambda: self.alteraTrabalho())

        self.ui.campoNumAnoCertidao.setText(self.ano_corrente)
        self.ui.lineEditAnoCert.setText(self.ano_corrente)

        self.ui.buttonDigitalizar.clicked.connect(
            lambda: self.showStatusTip("Digitalizar")
        )
        self.ui.buttonDigitalizar.clicked.connect(
            lambda: self.iniciaDigitalizacao(somente_visualizar=False)
        )
        self.ui.buttonConsultarDocumento.clicked.connect(
            lambda: self.iniciaDigitalizacao(somente_visualizar=True)
        )
        self.ui.buttonGravar.clicked.connect(self.gravarDocumentoDigitalizado)
        self.ui.buttonGravar.clicked.connect(lambda: self.showStatusTip("Gravar"))
        self.ui.buttonLimpar.clicked.connect(lambda: self.showStatusTip("Limpar"))
        self.ui.buttonLimparDocumentosSimples.clicked.connect(
            lambda: self.showStatusTip("Limpar")
        )
        self.ui.buttonLimpar.clicked.connect(lambda: self.limpaCampos())
        self.ui.buttonLimparDocumentosSimples.clicked.connect(
            lambda: self.limpaCampos()
        )
        self.ui.tabela_dinamica_conf.cellDoubleClicked.connect(
            self.abrir_para_conferencia
        )
        self.ui.buttonLimpar.clicked.connect(
            lambda: self.habilitaDigitarDocumento(True)
        )
        self.ui.buttonLimparDocumentosSimples.clicked.connect(
            lambda: self.habilitaDigitarDocumento(True)
        )
        self.ui.button_listar_conf.clicked.connect(
            lambda: self.listar_digitalizacoes_para_conferencia()
        )
        self.ui.buttonAumentar.clicked.connect(lambda: self.incrementaNumDocumento(1))
        self.ui.buttonDiminuir.clicked.connect(lambda: self.incrementaNumDocumento(-1))

        # Inicialização dos campos de configuração usuário
        self.configuracoes = Configuracoes()
        self.ui.campo_temp_index.setText(self.configuracoes.get_temp_index_usuario())
        self.ui.campo_servidor.setText(self.configuracoes.get_servidor())
        self.ui.campo_caminho_naps2.setText(self.configuracoes.get_caminho_naps2())
        self.ui.button_testar_email.clicked.connect(lambda: self.testarEmail())
        self.ui.button_salvar_config.clicked.connect(lambda: self.gravarConfig())

        # Não é a conferência de documentos da aba conferências.
        self.ui.buttonVerificar.clicked.connect(lambda: self.iniciaVerificarDoc())
        self.ui.buttonConferenciaErro.clicked.connect(
            lambda: self.iniciaVerificarDoc(verifica_erro=True)
        )
        self.ui.button_cancelar_config.clicked.connect(lambda: self.cancelaConfig())
        self.habilitaDigitarDocumento(True)
        self.setupAuditoria()
        self.atualizarCamposAuditoria()
        self.verificaAcessos(self.acesso)

        # Área de gerenciamento de usuários
        self.ui.button_verificar_sigla.clicked.connect(lambda: self.verifica_sigla())
        self.ui.button_criar_atualizar.clicked.connect(lambda: self.gravar_usuario())
        self.ui.button_cancelar_usuario.clicked.connect(
            lambda: self.cancela_alteracao_usuario()
        )

        self.ui.buttonDigitalizarDocumentosSimples.clicked.connect(
            lambda: self.on_buttonDigitalizarDocumentosSimples_clicked()
        )
        self.ui.buttonGravarDocumentosSimples.clicked.connect(
            lambda: self.on_buttonGravarDocumentosSimples_clicked()
        )
        self.ui.buttonDocumentInfo.clicked.connect(
            self.exibir_exemplo_documento_simples
        )

        self.ui.comboBoxTipoSimples.currentIndexChanged.connect(
            self.setupDigitalizacaoSimples
        )

        self.ui.tabela_dinamica_conf.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.ui.tabela_dinamica_conf.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.ui.tableWidget.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.ui.tableWidget.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.ui.tabWidget.currentChanged.connect(self.verificar_aba_conferencia)

        self.tipos_simples = self.configuracoes.get_tipos_digitalizacao_simples()
        self.ui.comboBoxTipoSimples.clear()
        for i, tipo in enumerate(self.tipos_simples.keys(), start=1):
            self.ui.comboBoxTipoSimples.addItem(f"{i} - {tipo}", userData=tipo)
        self.setupDigitalizacaoSimples()

        self.ui.campoNumDocumento.setFocus()

    def exibir_exemplo_documento_simples(self):
        tipo = self.ui.comboBoxTipoSimples.currentData()
        dialog = ExemploDocumentoDialog(tipo, self)
        dialog.resize(1300, 680)
        dialog.exec()

    def setupDigitalizacaoSimples(self):
        # Inicializar data
        hoje = QDate.currentDate()
        self.ui.dateEditDataSimples.setDate(hoje)
        self.ui.dateEditDataSimples.setCalendarPopup(True)

        # Aplica estilo para o calendário popup
        calendar = self.ui.dateEditDataSimples.calendarWidget()
        calendar.setStyleSheet(
            """
            QCalendarWidget QAbstractItemView {
                color: black;
                font-size: 12px;
            }
            QCalendarWidget QWidget {
                background-color: white;
            }
            QCalendarWidget QToolButton {
                color: black;
            }
            QCalendarWidget QTableView {
                selection-background-color: #A0C4FF;
                selection-color: black;
            }
        """
        )
        tipo = self.ui.comboBoxTipoSimples.currentData()
        formato = self.tipos_simples[tipo]["formato"]

        if "numero_documento" in formato:
            self.ui.lineEditNumeroDocumento.show()
            self.ui.labelNumeroDocumentoSimples.show()
        else:
            self.ui.lineEditNumeroDocumento.hide()
            self.ui.labelNumeroDocumentoSimples.hide()

    def onComboBoxTipoSimplesChanged(self):
        self.setupDigitalizacaoSimples()

    def gerar_caminho_final_simples(self):
        tipo = self.ui.comboBoxTipoSimples.currentData()
        info = self.tipos_simples[tipo]
        caminho_base = info["caminho"]
        formato = info["formato"]

        # Dados do formulário
        data = date(
            self.ui.dateEditDataSimples.date().year(),
            self.ui.dateEditDataSimples.date().month(),
            self.ui.dateEditDataSimples.date().day(),
        )
        numero_doc = self.ui.lineEditNumeroDocumento.text().strip()

        # Substituições no formato
        path_formatado = (
            formato.replace("aaaa", str(data.year))
            .replace("mm", f"{data.month:02d}")
            .replace("dd", f"{data.day:02d}")
            .replace("ddmmaaaa", f"{data.day:02d}{data.month:02d}{data.year}")
            .replace("numero_documento", numero_doc)
        )

        caminho_completo = os.path.normpath(os.path.join(caminho_base, path_formatado))
        return caminho_completo

    def on_buttonDigitalizarDocumentosSimples_clicked(self):
        # Verifica se já existem arquivos reais (não pastas) na pasta
        conf = Configuracoes()
        caminho_arquivo_temp = os.path.join(
            conf.get_caminho_temp_index(), conf.get_temp_index_usuario()
        )
        if os.path.exists(caminho_arquivo_temp):
            arquivos_temporarios = [
                f
                for f in os.listdir(caminho_arquivo_temp)
                if os.path.isfile(os.path.join(caminho_arquivo_temp, f))
                and (f.lower().endswith(".tiff") or f.lower().endswith(".tif"))
            ]
            if arquivos_temporarios:
                QMessageBox.warning(
                    self,
                    "Aviso",
                    "A pasta temporária de digitalização já contém arquivos. Por favor, esvazie-a antes de iniciar uma nova digitalização.",
                )
                return

        self.abrirNAPS2(
            caminho_arquivo="", somente_visualizar=False, digitalizacao_simples=True
        )

    # erro gravar documento simples
    def on_buttonGravarDocumentosSimples_clicked(self):
        from PIL import Image, ImageSequence

        tipo_label = self.ui.comboBoxTipoSimples.currentData()
        if not tipo_label:
            QMessageBox.warning(self, "Erro", "Selecione um tipo de documento.")
            return

        tipos = self.configuracoes.get_tipos_digitalizacao_simples()
        if tipo_label not in tipos:
            QMessageBox.warning(
                self,
                "Erro",
                f"Tipo de documento '{tipo_label}' não encontrado no config.ini.",
            )
            return

        caminho_rede = tipos[tipo_label]["caminho"]
        padrao_nome = tipos[tipo_label]["formato"]

        data = date(
            self.ui.dateEditDataSimples.date().year(),
            self.ui.dateEditDataSimples.date().month(),
            self.ui.dateEditDataSimples.date().day(),
        )
        if self.ui.labelNumeroDocumentoSimples.isVisible():
            numero = self.ui.lineEditNumeroDocumento.text().strip()
        else:
            numero = ""

        if "numero_documento" in padrao_nome and not numero:
            QMessageBox.warning(self, "Erro", "Informe o número do documento.")
            return

        # Substitui os marcadores no padrão do nome
        nome_arquivo = (
            padrao_nome.replace("aaaa", str(data.year))
            .replace("mm", f"{data.month:02}")
            .replace("dd", f"{data.day:02}")
            .replace("ddmmaaaa", f"{data.day:02}{data.month:02}{data.year}")
            .replace("numero_documento", numero)
        )

        caminho_destino = os.path.normpath(
            os.path.join(self.configuracoes.get_servidor(), caminho_rede, nome_arquivo)
        )

        # Caminho da imagem TIFF digitalizada
        tiff_path = os.path.join(
            self.configuracoes.get_caminho_temp_index(),
            self.configuracoes.get_temp_index_usuario(),
            "0001.tif",
        )

        if not os.path.exists(tiff_path):
            QMessageBox.warning(
                self, "Erro", f"Arquivo de digitalização não encontrado: {tiff_path}"
            )
            return

        # Garante que as pastas de destino existam
        os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)

        # Verifica se já existe e pergunta
        if os.path.exists(caminho_destino):
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Question)
            msg_box.setWindowTitle("Arquivo já existe")
            msg_box.setText(
                f"O arquivo já existe:\n\n{caminho_destino}\n\nDeseja substituir ou adicionar como arquivo'A'?"
            )
            substituir_btn = msg_box.addButton(
                "Substituir", QMessageBox.ButtonRole.AcceptRole
            )
            adicionar_btn = msg_box.addButton(
                "Adicionar", QMessageBox.ButtonRole.RejectRole
            )
            msg_box.exec()

            if msg_box.clickedButton() == adicionar_btn:
                base, ext = os.path.splitext(caminho_destino)
                caminho_destino = base + "A" + ext  # Adiciona 'A' antes da extensão

        try:

            img = Image.open(tiff_path)
            pages = [p.convert("RGB") for p in ImageSequence.Iterator(img)]

            if pages:
                pages[0].save(
                    caminho_destino,
                    save_all=True,
                    append_images=pages[1:],
                    resolution=100.0,
                    format="PDF",
                )
            else:
                raise Exception(
                    "Nenhuma página encontrada no TIFF, entrar em contato com o setor de TI"
                )

            try:
                img.close()  # Fecha o arquivo de Imagem TIFF para posteriormente poder apagar
            except Exception as e:
                QMessageBox.critical(
                    self, "Erro", f"Erro ao fechar o arquivo TIFF:\n{e}"
                )

            # Apaga o arquivo TIFF temporário
            try:
                os.remove(tiff_path)
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Aviso",
                    f"O PDF foi salvo, mas houve um erro ao remover o arquivo temporário:\n{e}",
                )

            QMessageBox.information(
                self, "Sucesso", f"Arquivo salvo em:\n{caminho_destino}"
            )

            # Nome do arquivo (extraindo só o nome final)
            nome_final_arquivo = os.path.basename(caminho_destino)
            agora = datetime.now().replace(microsecond=0)

            try:
                colunas = "tipo_documento, nome_documento, usuario, data_hora"
                valores = (tipo_label, nome_final_arquivo, self.sigla, agora)
                self.db_auditoria.inserir_dado("documentos_simples", colunas, valores)
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Aviso",
                    f"O PDF foi salvo, mas houve um erro ao registrar no banco:\n{e}",
                )

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao converter TIFF para PDF:\n{e}")

        self.habilitaDigitarDocumento(habilita=True)

    def cancela_alteracao_usuario(self):
        self.ui.campo_sigla.setText("")
        self.ui.campo_nome_usuario.setText("")
        self.ui.campo_senha_usuario.setText("")
        self.ui.campo_confirma_senha.setText("")
        self.ui.combo_acesso_usuario.setCurrentIndex(0)

    def gravar_usuario(self):
        self.dbUsers.connect_users()

        acesso = {
            0: "digitalização",
            1: "administrador",
            2: "documentos",
            3: "consulta",
            4: "digitalização_simples",
        }

        sigla = self.ui.campo_sigla.text().strip().lower()
        nome_usuario = self.ui.campo_nome_usuario.text().strip()
        senha = self.ui.campo_senha_usuario.text()
        confirma_senha = self.ui.campo_confirma_senha.text()
        acesso_usuario = acesso.get(self.ui.combo_acesso_usuario.currentIndex())

        if not sigla:
            QMessageBox.information(
                self,
                "Sigla não informada",
                "É necessário informar a sigla para criar ou atualizar um usuário!",
            )
            return

        if not nome_usuario:
            QMessageBox.information(
                self,
                "Nome não informado",
                "É necessário informar o nome completo do usuário!",
            )
            return

        if not senha or not confirma_senha:
            QMessageBox.information(
                self,
                "Senha obrigatória",
                "A senha e a confirmação são obrigatórias para gravar ou atualizar o usuário!",
            )
            return

        if senha != confirma_senha:
            QMessageBox.information(
                self, "Senha incorreta", "As senhas digitadas não coincidem!"
            )
            return

        # Verifica se o usuário já existe
        usuario = self.dbUsers.get_user_info(sigla)

        if usuario["existe"]:
            # Atualizar usuário
            try:
                self.dbUsers.update_user(sigla, senha, acesso_usuario, nome_usuario)
                QMessageBox.information(
                    self, "Sucesso", f"Usuário '{nome_usuario}' atualizado com sucesso!"
                )
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao atualizar o usuário: {e}")
        else:
            # Criar novo usuário
            try:
                resultado = self.dbUsers.insert_users(
                    sigla, senha, acesso_usuario, nome_usuario
                )
                if resultado == "sucesso":
                    QMessageBox.information(
                        self, "Sucesso", f"Usuário '{nome_usuario}' criado com sucesso!"
                    )
                elif resultado == "existente":
                    QMessageBox.warning(
                        self, "Aviso", f"O usuário '{nome_usuario}' já está cadastrado."
                    )
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao criar o usuário: {e}")

    def verifica_sigla(self):
        self.dbUsers.connect_users()
        acesso = {
            "digitalização": 0,
            "administrador": 1,
            "documentos": 2,
            "consulta": 3,
            "digitalizacao_simples": 4,
        }
        sigla = self.ui.campo_sigla.text()
        if sigla == "":
            QMessageBox.information(
                self,
                "Sigla não informada",
                "É necessário informar a sigla para criar ou atualizar um usuário!",
            )
            return
        usuario = self.dbUsers.get_user_info(sigla)
        if usuario["existe"]:
            self.ui.campo_nome_usuario.setText(usuario["nome_usuario"])
            self.ui.combo_acesso_usuario.setCurrentIndex(acesso[usuario["acesso"]])
            self.ui.button_criar_atualizar.setText("Atualizar")
        else:
            self.ui.button_criar_atualizar.setText("Criar")
            self.ui.campo_nome_usuario.setText("")
            self.ui.combo_acesso_usuario.setCurrentIndex(0)
            self.ui.campo_senha_usuario.setText("")
            self.ui.campo_confirma_senha.setText("")

    def cancelaConfig(self):
        self.configuracoes = Configuracoes()
        self.ui.campo_temp_index.setText(self.configuracoes.get_temp_index_usuario())
        self.ui.campo_servidor.setText(self.configuracoes.get_servidor())
        self.ui.campo_caminho_naps2.setText(self.configuracoes.get_caminho_naps2())

    def gravarConfig(self):
        self.configuracoes = Configuracoes()
        try:
            self.configuracoes.salvar_config(
                servidor=self.ui.campo_servidor.text(),
                caminho_temp_index_usuario=self.ui.campo_temp_index.text(),
                caminho_naps2=self.ui.campo_caminho_naps2.text(),
            )
            QMessageBox.information(
                self, "Sucesso", "Configurações salvas com sucesso!"
            )
            logger.info("Configurações salvas com sucesso!")
        except Exception as erro:
            QMessageBox.information(
                self, "Erro", f"Falha ao gravar no arquivo 'config.ini' \n{erro}"
            )
            logger.exception(f"Falha ao gravar no arquivo 'config.ini'")

    def testarEmail(self):
        try:
            status = envia_email(
                email_dest="cartorio@2rgi-rj.com.br",
                nome_documento="Protocolo",
                numero_doc="540200",
                data_hora_tabela="15/05/2023 10:13",
                usuario_logado=self.usuario,
                usuario_digitalizacao="edu",
            )
            if status == "sucesso":
                QMessageBox.information(self, "Sucesso", f"E-mail enviado com sucesso!")
                logger.info(f"E-mail enviado com sucesso!")
            else:
                QMessageBox.warning(self, "Erro", f"Erro ao enviar e-mail: {err}")
                logger.error(f"Erro ao enviar e-mail: {err}")
        except Exception as err:
            logger.error(f"Erro ao enviar e-mail: {err}")
        finally:
            logger.info(f"E-mail enviado com sucesso!")

    def verificar_aba_conferencia(self, index):
        if self.ui.tabWidget.widget(index) == self.ui.tab_3:
            self.listar_digitalizacoes_para_conferencia(mostrar_mensagem=True)

    def verificaAcessos(self, acesso: str):
        if acesso == "digitalização":
            self.liberarDigitalizar()
        elif acesso == "administrador":
            pass
        elif acesso == "documentos":
            self.liberaDocumentos()
        elif acesso == "consulta":
            self.liberaConsulta()
        elif acesso == "digitalização_simples":
            self.liberaDigitalizacaoSimples()
        else:
            QMessageBox.warning(self, "Erro", f"Acesso inválido: {acesso}")
            logger.error(f"Acesso inválido: {acesso}")

    # Controlar acessos para usuário de digitalização geral ou digitalização somente de documentos
    def liberaDocumentos(self):
        self.ui.tabWidget.removeTab(3)
        self.ui.tabWidget.removeTab(1)
        self.ui.tabWidget.removeTab(2)

    def liberaDigitalizacaoSimples(self):
        self.ui.tabWidget.removeTab(0)
        self.ui.tabWidget.removeTab(2)
        self.ui.tabWidget.removeTab(1)
        self.ui.tabWidget.removeTab(1)

    def liberarDigitalizar(self):
        self.ui.tabWidget.removeTab(4)
        self.ui.tabWidget.removeTab(3)

    def liberaConsulta(self):
        self.ui.tabWidget.removeTab(3)
        self.ui.tabWidget.removeTab(1)
        self.ui.tabWidget.removeTab(2)
        self.ui.tabWidget.removeTab(1)
        self.ui.tabWidget.setTabText(0, "Consulta de Documentos")
        self.ui.label.setText("Consulta de documentos do Cartório")
        self.ui.buttonDigitalizar.setVisible(False)
        self.ui.buttonGravar.setVisible(False)
        self.ui.buttonVerificar.setVisible(False)
        self.ui.buttonConsultarDocumento.setVisible(True)

    def setupAuditoria(self):
        # Filtro principal
        self.ui.comboBoxFiltro.addItems(["Usuário", "Documento"])
        self.ui.comboBoxFiltro.currentIndexChanged.connect(
            self.atualizarCamposAuditoria
        )

        # Datas
        hoje = QDate.currentDate()
        tres_meses_atras = hoje.addMonths(-3)

        self.ui.dateEditInicio.setDate(tres_meses_atras)
        self.ui.dateEditFinal.setDate(hoje)

        self.ui.dateEditInicio.setCalendarPopup(True)
        self.ui.dateEditFinal.setCalendarPopup(True)

        # Inicialmente esconder todos os inputs específicos
        self.ui.lineEditAnoCert.hide()
        self.ui.lineEditNumCert.hide()
        self.ui.lineEditNumDocumento.hide()

        # Botão Listar e responsividade ao enter nos campos de digitação
        self.ui.buttonListar.clicked.connect(self.filtrarAuditoria)
        self.ui.lineEditNumDocumento.returnPressed.connect(self.filtrarAuditoria)
        self.ui.lineEditAnoCert.returnPressed.connect(self.filtrarAuditoria)
        self.ui.lineEditNumCert.returnPressed.connect(self.filtrarAuditoria)

        # Botão Cancelar
        self.ui.buttonCancelar.clicked.connect(self.resetarFiltrosAuditoria)
        self.ui.buttonCancelar.clicked.connect(self.atualizarCamposAuditoria)

        # # Botões Imprimir/Salvar
        self.ui.buttonImprimir.clicked.connect(self.gerar_pdf_auditoria)
        # self.ui.buttonSalvar.clicked.connect(self.salvarRelatorioPDF)

    def atualizarCamposAuditoria(self):
        filtro = self.ui.comboBoxFiltro.currentText()

        self.ui.comboBoxDinamica.clear()
        self.ui.lineEditAnoCert.hide()
        self.ui.lineEditNumCert.hide()
        self.ui.lineEditNumDocumento.hide()

        if filtro == "Usuário":
            siglas = self.dbUsers.get_sigla_users()
            usuarios = self.dbUsers.listar_nomes_usuarios([s[0] for s in siglas])
            self.ui.comboBoxDinamica.addItems(usuarios)
            self.ui.lineEditAnoCert.hide()
            self.ui.lineEditNumCert.hide()
            self.ui.label_certidao.hide()
            self.ui.label_documento.hide()
            self.ui.lineEditNumDocumento.hide()
            self.ui.comboBoxDinamica.setFixedWidth(391)

        elif filtro == "Documento":
            self.ui.comboBoxDinamica.setFixedWidth(221)
            self.ui.comboBoxDinamica.addItems(
                nomes_documentos
            )  # lista com nomes dos documentos
            self.ui.comboBoxDinamica.currentIndexChanged.connect(
                self.atualizarCamposDocumento
            )
            self.atualizarCamposDocumento()  # força atualizar o que for exibido

    def atualizarCamposDocumento(self):
        tipo = self.ui.comboBoxDinamica.currentIndex()
        item = self.ui.comboBoxDinamica.currentText()
        if tipo in (2, 4):  # Certidão ou Certidão Cancelada
            self.ui.lineEditAnoCert.show()
            self.ui.lineEditNumCert.show()
            self.ui.label_certidao.show()
            self.ui.label_documento.hide()
            self.ui.lineEditNumDocumento.hide()
            self.ui.lineEditAnoCert.setText(self.ano_corrente)
        else:
            self.ui.lineEditAnoCert.hide()
            self.ui.lineEditNumCert.hide()
            self.ui.label_certidao.hide()
            self.ui.label_documento.show()
            self.ui.lineEditNumDocumento.show()

        if item not in nomes_documentos:
            self.ui.lineEditAnoCert.hide()
            self.ui.lineEditNumCert.hide()
            self.ui.label_certidao.hide()
            self.ui.label_documento.hide()
            self.ui.lineEditNumDocumento.hide()

    def resetarFiltrosAuditoria(self):
        self.ui.comboBoxFiltro.setCurrentIndex(0)
        self.ui.comboBoxDinamica.clear()
        self.ui.lineEditAnoCert.clear()
        self.ui.lineEditNumCert.clear()
        self.ui.lineEditNumDocumento.clear()
        self.ui.lineEditAnoCert.setText(self.ano_corrente)

        hoje = QDate.currentDate()
        tres_meses_atras = hoje.addMonths(-3)
        self.ui.dateEditInicio.setDate(tres_meses_atras)
        self.ui.dateEditFinal.setDate(hoje)

        self.ui.tableWidget.setRowCount(0)

    def abrir_para_conferencia(self, row):
        try:
            # Obter tipo de documento e número da linha clicada
            tipo_documento = self.ui.tabela_dinamica_conf.item(row, 0).text()
            numero = self.ui.tabela_dinamica_conf.item(row, 1).text()
            data_hora_tabela = self.ui.tabela_dinamica_conf.item(row, 5).text()
            usuario_digitalizacao = self.ui.tabela_dinamica_conf.item(row, 2).text()

            # Normalizar nomes para evitar erros de acento/maiúsculas
            def normalizar(texto):
                return (
                    unicodedata.normalize("NFKD", texto)
                    .encode("ASCII", "ignore")
                    .decode()
                    .lower()
                )

            tipo_normalizado = normalizar(tipo_documento)
            nomes_normalizados = [normalizar(n) for n in nomes_documentos]

            # Obter índice e caminho base
            try:
                indice = nomes_normalizados.index(tipo_normalizado)
                caminho_base = self.configuracoes.get_caminho_por_indice(indice)
            except ValueError:
                caminho_base = None

            # Montar caminho do TIFF com base no tipo de documento
            if tipo_documento in ("Certidão", "Certidão Cancelada"):
                try:
                    ano, num = numero.split("/")
                    nome_arquivo = f"{int(num):06}.TIF"
                    subpasta = f"L00020{ano}"
                    caminho_arquivo = os.path.normpath(
                        os.path.join(caminho_base, subpasta, nome_arquivo)
                    )
                    if not os.path.exists(caminho_arquivo):
                        nome_arquivo = f"{int(num):06}.TIFF"
                        caminho_arquivo = os.path.normpath(
                            os.path.join(caminho_base, subpasta, nome_arquivo)
                        )
                except ValueError:
                    QMessageBox.warning(
                        self, "Erro", f"Número de certidão inválido: {numero}"
                    )
                    return
            else:
                num_pasta = numero.zfill(6)[:3]
                nome_arquivo = f"{numero.zfill(6)[-3:]}.TIF"
                caminho_arquivo = os.path.normpath(
                    os.path.join(caminho_base, num_pasta, nome_arquivo)
                )
                if not os.path.exists(caminho_arquivo):
                    nome_arquivo = f"{numero.zfill(6)[-3:]}.TIFF"
                    caminho_arquivo = os.path.normpath(
                        os.path.join(caminho_base, num_pasta, nome_arquivo)
                    )

            # Abrir imagem com visualizador padrão
            if os.path.exists(caminho_arquivo):
                if tipo_documento in ("Certidão", "Certidão Cancelada"):
                    abrir_com_visualizador_classico(caminho_arquivo)
                else:
                    comando = f'start /wait "" "{caminho_arquivo}"'
                    run(comando, shell=True)
                # Aqui depois você chama a confirmação
                self.finalizar_conferencia(
                    caminho_arquivo=caminho_arquivo,
                    nome_documento=tipo_documento,
                    numero_doc=numero,
                    usuario_logado=self.sigla,
                    usuario_digitalizacao=usuario_digitalizacao,
                    data_hora_tabela=data_hora_tabela,
                )
                return caminho_arquivo, tipo_normalizado, numero
            else:
                msg = QMessageBox()
                msg.setWindowTitle("O arquivo não foi encontrado!!!")
                msg.setText("Sinalizar o arquivo como 'digitalizado incorretamente'?")
                msg.setIcon(QMessageBox.Icon.Question)
                msg.setStandardButtons(
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )

                # Alterar texto dos botões
                yes_button = msg.button(QMessageBox.StandardButton.Yes)
                yes_button.setText("Sim")
                no_button = msg.button(QMessageBox.StandardButton.No)
                no_button.setText("Não")

                resposta = msg.exec()
                if resposta == QMessageBox.StandardButton.Yes:
                    self.finalizar_conferencia(
                        caminho_arquivo="ausente",
                        nome_documento=tipo_documento,
                        numero_doc=numero,
                        usuario_logado=self.sigla,
                        usuario_digitalizacao=usuario_digitalizacao,
                        data_hora_tabela=data_hora_tabela,
                    )
                    logger.error(f"Arquivo não encontrado:\n{caminho_arquivo}")

        except Exception as e:
            QMessageBox.critical(
                self, "Erro", f"Erro ao abrir documento para conferência:\n{e}"
            )
            logger.error(f"Erro ao abrir documento para conferência:\n{e}")
            return "Erro", tipo_normalizado, numero

    def listar_digitalizacoes_para_conferencia(self, mostrar_mensagem=True):
        self.ui.tabela_dinamica_conf.setSortingEnabled(False)
        self.ui.tabela_dinamica_conf.setRowCount(0)
        self.ui.tabela_dinamica_conf.setColumnCount(6)
        self.ui.tabela_dinamica_conf.setHorizontalHeaderLabels(
            [
                "Documento",
                " Número ",
                "Usuário",
                "   Ação Efetuada   ",
                "Páginas",
                "Data/Hora",
            ]
        )

        self.ui.tabela_dinamica_conf.setAlternatingRowColors(True)
        self.ui.tabela_dinamica_conf.setStyleSheet(
            """
                QTableWidget {
                    background-color: rgb(150, 150, 150);
                    alternate-background-color: rgb(42, 42, 42);  /* cinza claro */
                    color: rgb(42, 42, 42); /* texto padrão: cinza escuro */
                }
                QTableWidget::item:alternate {
                    color: rgb(150, 150, 150);  /* texto cinza na linha alternada */
                }
                QHeaderView::section {
                    background-color: #f0f0f0;  /* cabeçalho cinza claro */
                    color: rgb(42, 42, 42);     /* texto cinza escuro */
                    padding: 4px;
                    font-weight: bold;
                    border: 1px solid #ccc;
                }
            """
        )

        self.ui.tabela_dinamica_conf.resizeColumnsToContents()
        self.ui.tabela_dinamica_conf.resizeRowsToContents()
        self.ui.tabela_dinamica_conf.horizontalHeader().setStretchLastSection(True)
        self.ui.tabela_dinamica_conf.horizontalHeader().setSectionResizeMode(
            QHeaderView.Interactive
        )

        try:
            conn = self.db_auditoria.get_conn()
            cursor = conn.cursor()
            usuario_atual = self.sigla  # Ex: "ABC"

            for tipo_doc, valores in tab_doc.items():
                tabela = valores[0]
                if len(valores) == 3:
                    # Caso especial: certidão ou certidão cancelada
                    campo_ano = valores[1]
                    campo_num = valores[2]
                    select_sql = f"""
                        SELECT '{nomes_documentos[tipo_doc]}' AS tipo_doc,
                            {campo_ano}, {campo_num},
                            usuario, tipo_alteracao, qtd_paginas, data_hora
                        FROM {tabela}
                        WHERE usuario != %s AND (usuario_conf IS NULL OR usuario_conf = '')
                        AND (data_conf IS NULL)
                        ORDER BY data_hora DESC
                    """
                    cursor.execute(select_sql, (usuario_atual,))
                    registros = cursor.fetchall()

                else:
                    # Demais tipos de documento
                    coluna_doc = valores[1]

                    select_sql = f"""
                        SELECT '{nomes_documentos[tipo_doc]}' AS tipo_doc,
                            {coluna_doc},
                            usuario, tipo_alteracao, qtd_paginas, data_hora
                        FROM {tabela}
                        WHERE usuario != %s AND (usuario_conf IS NULL OR usuario_conf = '')
                        AND (data_conf IS NULL)
                        ORDER BY data_hora DESC
                    """
                    cursor.execute(select_sql, (usuario_atual,))
                    registros = cursor.fetchall()

                for linha in registros:
                    row = self.ui.tabela_dinamica_conf.rowCount()
                    self.ui.tabela_dinamica_conf.insertRow(row)

                    if linha[0] in ("Certidão", "Certidão Cancelada"):
                        tipo_doc_fmt = linha[0]
                        numero_fmt = f"{linha[2]}/{linha[1]}"  # ano/numero
                        valores = [
                            tipo_doc_fmt,
                            numero_fmt,
                            linha[3],
                            linha[4],
                            linha[5],
                            linha[6],
                        ]
                    else:
                        valores = linha  # já está na ordem correta

                    for col, val in enumerate(valores):
                        item = QTableWidgetItem(str(val) if val is not None else "")

                        # Centralizar "Usuário" (coluna 1) e "Qtd. Páginas" (coluna 3)
                        if col in (2, 4):
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                        # Se for data formatar conforme esquema 02/05/2025 11:35
                        if isinstance(val, datetime):
                            val = val.strftime("%d/%m/%Y %H:%M:%S")
                            item = QTableWidgetItem(str(val))
                        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        self.ui.tabela_dinamica_conf.setItem(row, col, item)

            total = self.ui.tabela_dinamica_conf.rowCount()
            if mostrar_mensagem:
                QMessageBox.information(
                    self, "Conferência", f"{total} documentos aguardando conferência."
                )
            # Ativa ordenação
            self.ui.tabela_dinamica_conf.setSortingEnabled(True)
        except Exception as e:
            logger.error(f"Erro ao buscar documentos para conferência: {e}")
            QMessageBox.critical(
                self, "Erro", "Ocorreu um erro ao listar os documentos."
            )
        finally:
            cursor.close()
            conn.close()

    def filtrarAuditoria(self):
        # Bloqueia o sorting da tabela para popular com dados
        self.ui.tableWidget.setSortingEnabled(False)

        # Carrega mapeamento nome completo -> sigla
        usuarios = self.dbUsers.get_sigla_users()
        mapa_siglas = {nome: user for user, nome in usuarios}

        filtro_listar_documentos = self.ui.filtro_listar_documentos.currentText()
        condicao_correto = ""

        if filtro_listar_documentos == "Corretos":
            condicao_correto = " AND correto = 'S'"
        elif filtro_listar_documentos == "Incorretos":
            condicao_correto = " AND correto = 'N'"

        tipo_filtro = self.ui.comboBoxFiltro.currentText()
        filtro_dinamico = self.ui.comboBoxDinamica.currentText()
        qdate_inicio = self.ui.dateEditInicio.date()
        qdate_fim = self.ui.dateEditFinal.date()
        data_inicio = datetime.combine(qdate_inicio.toPython(), time.min)  # 00:00:00
        data_fim = datetime.combine(qdate_fim.toPython(), time.max)  # 23:59:59.999999

        filtros_sql = []

        if tipo_filtro == "Usuário" and filtro_dinamico:
            sigla = mapa_siglas.get(filtro_dinamico)
            if not sigla:
                QMessageBox.warning(
                    self,
                    "Aviso",
                    f"Sigla não encontrada para o usuário '{filtro_dinamico}'",
                )
                return

            for tipo_documento, (tabela, coluna_doc, *extra) in tab_doc.items():
                if tabela.lower() == "certidao":
                    sql = f"""SELECT '{nomes_documentos[tipo_documento]}' AS tipo_doc, 
                                    numcert, anocert, tipo_alteracao, qtd_paginas,
                                    data_hora, usuario_conf, data_conf, correto
                                FROM {tabela} 
                                WHERE usuario = %s AND data_hora BETWEEN %s AND %s
                                {condicao_correto}
                                ORDER BY data_hora DESC"""
                elif tabela.lower() == "certidaocancelada":
                    sql = f"""SELECT '{nomes_documentos[tipo_documento]}' AS tipo_doc, 
                                    numcertcanc, anocertcanc, tipo_alteracao, qtd_paginas, 
                                    data_hora, usuario_conf, data_conf, correto
                                FROM {tabela} 
                                WHERE usuario = %s AND data_hora BETWEEN %s AND %s
                                {condicao_correto}
                                ORDER BY data_hora DESC"""
                else:
                    sql = f"""SELECT '{nomes_documentos[tipo_documento]}' AS tipo_doc, 
                                    {coluna_doc}, tipo_alteracao, qtd_paginas, 
                                    data_hora, usuario_conf, data_conf, correto 
                                FROM {tabela} 
                                WHERE usuario = %s AND data_hora BETWEEN %s AND %s
                                {condicao_correto}
                                ORDER BY data_hora DESC"""

                filtros_sql.append((sql, [sigla, data_inicio, data_fim]))

        elif tipo_filtro == "Documento" and filtro_dinamico:
            tipo_doc = self.ui.comboBoxDinamica.currentIndex()
            tabela, coluna_doc, *extra = tab_doc[tipo_doc]

            if tipo_doc in (2, 4):  # Certidão ou Cancelada
                num_cert = self.ui.lineEditNumCert.text().zfill(6)
                ano_cert = self.ui.lineEditAnoCert.text()
                if not (num_cert and ano_cert):
                    QMessageBox.warning(
                        self, "Aviso", "Informe o número e o ano da certidão."
                    )
                    return
                col_num, col_ano = coluna_doc, extra[0]
                sql = f"""SELECT {col_num}, {col_ano}, tipo_alteracao, qtd_paginas, usuario,
                        data_hora, usuario_conf, data_conf, correto
                    FROM {tabela} 
                    WHERE {col_num} = %s AND {col_ano} = %s AND data_hora BETWEEN %s AND %s
                    {condicao_correto}
                    ORDER BY data_hora DESC"""
                valores = [num_cert, ano_cert, data_inicio, data_fim]
            else:
                num_doc = self.ui.lineEditNumDocumento.text().zfill(6)
                if not num_doc:
                    QMessageBox.warning(self, "Aviso", "Informe o número do documento.")
                    return
                sql = f"""SELECT {coluna_doc}, tipo_alteracao, qtd_paginas, usuario, 
                             data_hora, usuario_conf, data_conf, correto
                      FROM {tabela} 
                      WHERE {coluna_doc} = %s AND data_hora BETWEEN %s AND %s
                      {condicao_correto}
                      ORDER BY data_hora DESC"""
                valores = [num_doc, data_inicio, data_fim]

            filtros_sql.append((sql, valores))
            print(f"SQL: {sql} \n\n e \n\n Valores: {valores}")
        # Limpa a tabela
        self.ui.tableWidget.setRowCount(0)

        try:
            conn = self.db_auditoria.get_conn()
            cursor = conn.cursor()

            # Define colunas de acordo com o tipo de filtro
            if tipo_filtro == "Documento":
                self.ui.tableWidget.setColumnCount(8)
                self.ui.tableWidget.setHorizontalHeaderLabels(
                    [
                        "Número",
                        "   Ação Efetuada   ",
                        "Páginas",
                        "Usuário",
                        "Data/Hora",
                        "Usuário Conf.",
                        "Data Conf.",
                        "Correto?",
                    ]
                )
            else:
                self.ui.tableWidget.setColumnCount(8)
                self.ui.tableWidget.setHorizontalHeaderLabels(
                    [
                        " Tipo Documento ",
                        "Número",
                        "   Ação Efetuada   ",
                        "Páginas",
                        "Data/Hora",
                        "Usuário Conf.",
                        "Data Conf.",
                        "Correto?",
                    ]
                )

            self.ui.tableWidget.setAlternatingRowColors(True)
            self.ui.tableWidget.setStyleSheet(
                """
                QTableWidget {
                    background-color: rgb(150, 150, 150);
                    alternate-background-color: rgb(42, 42, 42);  /* cinza claro */
                    color: rgb(42, 42, 42); /* texto padrão: cinza escuro */
                }
                QTableWidget::item:alternate {
                    color: rgb(150, 150, 150);  /* texto cinza na linha alternada */
                }
                QHeaderView::section {
                    background-color: #f0f0f0;  /* cabeçalho cinza claro */
                    color: rgb(42, 42, 42);     /* texto cinza escuro */
                    padding: 4px;
                    font-weight: bold;
                    border: 1px solid #ccc;
                }
            """
            )

            self.ui.tableWidget.resizeColumnsToContents()
            self.ui.tableWidget.resizeRowsToContents()
            self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(
                QHeaderView.Interactive
            )

            for sql, vals in filtros_sql:
                print(f"SQL: {sql}")
                print(f"Valores: {vals}")

                cursor.execute(sql, vals)
                resultados = cursor.fetchall()

                for row_data in resultados:
                    row = self.ui.tableWidget.rowCount()
                    self.ui.tableWidget.insertRow(row)

                    tipo_doc = row_data[0]

                    if tipo_filtro == "Documento":
                        valores = [
                            row_data[0],  # tipo doc
                            row_data[1],  # número
                            row_data[2],  # ação
                            row_data[3],  # páginas
                            row_data[4],  # data/hora
                            row_data[5],  # usuario_conf
                            row_data[6],  # data_conf
                            row_data[7],  # correto
                        ]
                    else:
                        if row_data[0] in ("Certidão", "Certidão Cancelada"):
                            numero_formatado = f"{row_data[2]}/{row_data[1]}"
                            valores = [
                                row_data[0],  # tipo doc
                                numero_formatado,  # número
                                row_data[3],  # ação
                                row_data[4],  # páginas
                                row_data[5],  # data/hora
                                row_data[6],  # usuario_conf
                                row_data[7],  # data_conf
                                row_data[8],  # correto
                            ]
                        else:
                            valores = list(
                                row_data
                            )  # já inclui as 8 colunas na ordem correta

                    for col, value in enumerate(valores):
                        if isinstance(value, datetime):
                            value = value.strftime("%d/%m/%Y %H:%M:%S")
                        self.ui.tableWidget.setItem(
                            row,
                            col,
                            QTableWidgetItem(str(value) if value is not None else ""),
                        )

            if self.ui.tableWidget.rowCount() == 0:
                QMessageBox.information(
                    self,
                    "Auditoria",
                    "Nenhum resultado encontrado para os filtros aplicados.",
                )

            # Após popular a tabela, habilita novamente a ordenação...
            self.ui.tableWidget.setSortingEnabled(True)
        except Exception as e:
            logger.error(f"Erro ao filtrar auditoria: {e}")
            QMessageBox.critical(
                self, "Erro", "Ocorreu um erro ao tentar consultar os dados."
            )

        finally:
            cursor.close()
            conn.close()

    def gravar_conferencia(
        self,
        tipo_documento,
        numero_documento,
        usuario,
        data_hora_conf,
        data_hora_tabela,
        conf_correta="S",
    ):
        data_hora_query = datetime.strptime(data_hora_tabela, "%d/%m/%Y %H:%M:%S")
        conn = self.db_auditoria.get_conn()
        cursor = conn.cursor()
        try:
            # Mapeia nome da tabela e coluna de número
            mapeamento = {
                "Protocolo": ("Protocolo", "numprot"),
                "Matrícula": ("Matricula", "nummat"),
                "Registro Auxiliar": ("RegistroAuxiliar", "numreg"),
                "Protocolo Cancelado": ("ProtocoloCancelado", "numprotcanc"),
                "Certidão": ("Certidao", ("anocert", "numcert")),
                "Certidão Cancelada": (
                    "CertidaoCancelada",
                    ("anocertcanc", "numcertcanc"),
                ),
            }

            tabela, colunas = mapeamento[tipo_documento]

            if isinstance(colunas, tuple):
                # Certidão ou Certidão Cancelada – extrai ano e número
                num_doc = numero_documento.split("/")
                ano = num_doc[0]
                num = num_doc[1]
                condicoes = (
                    f"{colunas[0]} = %s AND {colunas[1]} = %s AND data_hora = %s"
                )
                valores = (
                    usuario,
                    data_hora_conf,
                    conf_correta,
                    ano,
                    num,
                    data_hora_query,
                )
            else:
                condicoes = f"{colunas} = %s AND data_hora = %s"
                valores = (
                    usuario,
                    data_hora_conf,
                    conf_correta,
                    numero_documento,
                    data_hora_query,
                )

            # Monta a query
            query = f"""
                UPDATE {tabela}
                SET usuario_conf = %s, data_conf = %s, correto = %s
                WHERE {condicoes}
            """
            cursor.execute(query, valores)
            conn.commit()
            if cursor.rowcount == 0:
                print("⚠️ Nenhum registro foi atualizado. Verifique os parâmetros.")
        except Exception as e:
            print(f"Erro ao gravar conferência no banco: {e}")
            logger.error(f"Erro ao gravar conferência no banco: {e}")
        finally:
            cursor.close()
            conn.close()

    def finalizar_conferencia(
        self,
        caminho_arquivo,
        nome_documento,
        numero_doc,
        usuario_logado,
        usuario_digitalizacao,
        data_hora_tabela,
    ):
        agora = datetime.now().replace(microsecond=0)

        if caminho_arquivo == "ausente":
            # Gravar conferência no banco para o arquivo ausente e sair da rotina.
            self.gravar_conferencia(
                nome_documento,
                numero_doc,
                usuario_logado,
                agora,
                data_hora_tabela,
                conf_correta="N",
            )
            self.listar_digitalizacoes_para_conferencia(mostrar_mensagem=False)
            return  # Não faz rollback apenas grava que foi digitalizado incorretamente

        conf_correta = "S"
        # 1. Pergunta se a imagem está correta
        msg = QMessageBox()
        msg.setWindowTitle("Confirmação")
        msg.setText("O documento está correto?")
        msg.setIcon(QMessageBox.QueIcon.Questionstion)
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        # Alterar texto dos botões
        yes_button = msg.button(QMessageBox.StandardButton.Yes)
        yes_button.setText("Sim")
        no_button = msg.button(QMessageBox.StandardButton.No)
        no_button.setText("Não")

        resposta = msg.exec()

        if resposta == QMessageBox.StandardButton.Yes:
            # Gravar conferência no banco
            self.gravar_conferencia(
                nome_documento,
                numero_doc,
                usuario_logado,
                agora,
                data_hora_tabela,
                conf_correta=conf_correta,
            )
            QMessageBox.information(
                self, "Conferência Finalizada", "Imagem confirmada como correta."
            )
            self.listar_digitalizacoes_para_conferencia(mostrar_mensagem=False)
            return

        # 2. Usuário disse que não está correta, pede confirmação
        msg = QMessageBox(self)
        msg.setWindowTitle("Confirmar Erro")
        msg.setText(
            "Tem certeza que o arquivo está incorreto? A imagem será restaurada do backup."
        )
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        # Traduz os botões
        msg.button(QMessageBox.StandardButton.Yes).setText("Sim")
        msg.button(QMessageBox.StandardButton.No).setText("Não")

        confirmar = msg.exec()

        if confirmar == QMessageBox.StandardButton.No:
            self.listar_digitalizacoes_para_conferencia(mostrar_mensagem=False)
            return  # cancela o rollback

        # 3. Envia e-mail
        nome_usuario_conferente = self.dbUsers.get_user_info(usuario_logado)[
            "nome_usuario"
        ]
        nome_usuario_digitalizacao = self.dbUsers.get_user_info(usuario_digitalizacao)[
            "nome_usuario"
        ]
        try:
            envio = envia_email(
                email_dest="cartorio@2rgi-rj.com.br",
                nome_documento=nome_documento,
                numero_doc=numero_doc,
                data_hora_tabela=data_hora_tabela,
                usuario_logado=nome_usuario_conferente,
                usuario_digitalizacao=nome_usuario_digitalizacao,
            )
            print(envio)
        except Exception as err:
            print(f"Erro ao enviar e-mail {err}")

        # 4. Realiza o rollback da imagem
        try:
            # Backup do arquivo incorreto para análise futura
            pasta_backup = os.path.dirname(caminho_arquivo.lower()).replace(
                "imagens", "digitalizacao\\CONFERENCIA DIGITALIZACAO"
            )
            nome_arquivo = os.path.basename(caminho_arquivo.lower())
            nome_erro = (
                nome_arquivo.lower()
                .replace(".tif", "_conferir_erro.tif")
                .replace(".tiff", "_conferir_erro.tiff")
            )
            destino_erro = os.path.normpath(os.path.join(pasta_backup, nome_erro))

            shutil.copy2(caminho_arquivo.lower(), destino_erro)

            # Restaurar o backup original
            pasta_original = os.path.dirname(caminho_arquivo.lower())
            nome_original = os.path.basename(caminho_arquivo.lower())

            arquivo_backup = os.path.normpath(os.path.join(pasta_backup, nome_original))
            arquivo_original = os.path.normpath(
                os.path.join(pasta_original, nome_original)
            )

            shutil.copy2(arquivo_backup, arquivo_original)

            conf_correta = "N"

            # Grava conferência mesmo assim para marcar como "conferido"
            self.gravar_conferencia(
                nome_documento,
                numero_doc,
                usuario_logado,
                agora,
                data_hora_tabela,
                conf_correta=conf_correta,
            )

            QMessageBox.information(
                self, "Imagem Restaurada", "Imagem incorreta foi restaurada do backup."
            )
            self.listar_digitalizacoes_para_conferencia(mostrar_mensagem=False)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao restaurar imagem: {str(e)}")
            logger.error(f"Erro ao restaurar imagem: {str(e)}")
            self.listar_digitalizacoes_para_conferencia(mostrar_mensagem=False)

    def gerar_pdf_auditoria(self):
        try:
            # Pasta temporária e nomes dos arquivos
            pasta_temp = os.path.normpath(os.path.join(os.getcwd(), "temp_relatorios"))
            os.makedirs(pasta_temp, exist_ok=True)
            caminho_temp = os.path.normpath(
                os.path.join(pasta_temp, "relatorio_temp.pdf")
            )
            caminho_final = os.path.normpath(
                os.path.join(pasta_temp, "relatorio_auditoria.pdf")
            )

            # Criação inicial do PDF (sem número de páginas ainda)
            c = canvas.Canvas(caminho_temp, pagesize=landscape(A4))
            largura, altura = landscape(A4)
            paginas = []

            # Cabeçalho de filtros
            tipo_filtro = self.ui.comboBoxFiltro.currentText()
            filtro_dinamico = self.ui.comboBoxDinamica.currentText()
            data_ini = self.ui.dateEditInicio.date().toString("dd/MM/yyyy")
            data_fim = self.ui.dateEditFinal.date().toString("dd/MM/yyyy")
            usuario = self.usuario if hasattr(self, "usuario") else "Desconhecido"
            gerado_em = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            # Cabeçalho da tabela
            col_titles = [
                self.ui.tableWidget.horizontalHeaderItem(i).text()
                for i in range(self.ui.tableWidget.columnCount())
            ]

            footer_y = 1.5 * cm

            if tipo_filtro == "Usuário":
                col_widths = [
                    3.8 * cm,  # Tipo Documento
                    2.8 * cm,  # Número Documento
                    3.8 * cm,  # Ação Efetuada
                    2.8 * cm,  # Páginas
                    3.8 * cm,  # Data/Hora
                    2.8 * cm,  # Usuário Conferente
                    3.8 * cm,  # Data da Conferência
                    2.8 * cm,
                ]  # Digitalizaçaõ Correta?
            else:
                col_widths = [
                    3 * cm,  # Tipo Documento
                    2 * cm,  # Número Documento
                    2.5 * cm,  # Ação Efetuada
                    2 * cm,  # Páginas
                    3 * cm,  # Data/Hora
                    1 * cm,
                    2 * cm,
                    2 * cm,
                ]

            def desenhar_cabecalho():
                nonlocal y
                c.setFont("Helvetica-Bold", 15)
                c.drawString(2 * cm, y, "Relatório de Auditoria")
                y -= 1.2 * cm

                c.setFont("Helvetica", 11)
                if tipo_filtro == "Usuário":
                    c.drawString(2 * cm, y, f"Filtro: Usuário - {filtro_dinamico}")
                elif tipo_filtro == "Documento":
                    c.drawString(
                        2 * cm, y, f"Filtro: Tipo Documento - {filtro_dinamico}"
                    )
                    y -= 0.7 * cm
                    if filtro_dinamico in ("Certidão", "Certidão Cancelada"):
                        numero = (
                            self.ui.lineEditAnoCert.text()
                            + "/"
                            + self.ui.lineEditNumCert.text().zfill(6)
                        )
                        c.drawString(2 * cm, y, f"Número: {numero}")
                    else:
                        numero = self.ui.lineEditNumDocumento.text().zfill(6)
                        c.drawString(2 * cm, y, f"Número: {numero}")
                y -= 0.7 * cm
                c.drawString(2 * cm, y, f"Período: {data_ini} a {data_fim}")
                y -= 1.2 * cm

                # Títulos da tabela
                c.setFont("Helvetica-Bold", 11)
                for i, title in enumerate(col_titles):
                    x = 2 * cm + sum(col_widths[:i]) + col_widths[i] / 2
                    c.drawCentredString(x, y, title)
                y -= 0.4 * cm
                c.setLineWidth(0.3)
                c.line(2 * cm, y + 0.3 * cm, largura - 2 * cm, y + 0.3 * cm)
                y -= 0.3 * cm

            # Conteúdo
            y = altura - 2 * cm
            desenhar_cabecalho()

            c.setFont("Helvetica", 11)
            alterna = False
            for row in range(self.ui.tableWidget.rowCount()):
                if y < 2.5 * cm:
                    c.showPage()
                    paginas.append(c.getPageNumber())
                    y = altura - 2 * cm
                    desenhar_cabecalho()
                    c.setFont("Helvetica", 11)  # <- Retorna à fonte regular
                if alterna:
                    c.setFillColor(colors.lightgrey)
                    c.rect(
                        2 * cm,
                        y - 0.1 * cm,
                        sum(col_widths),
                        0.4 * cm,
                        stroke=0,
                        fill=1,
                    )
                c.setFillColor(colors.black)

                for col in range(self.ui.tableWidget.columnCount()):
                    item = self.ui.tableWidget.item(row, col)
                    if item:
                        texto = item.text()
                        x = 2 * cm + sum(col_widths[:col]) + col_widths[col] / 2
                        c.drawCentredString(x, y, texto)

                # altura da linha
                y -= 0.55 * cm
                alterna = not alterna

            # Última página
            paginas.append(c.getPageNumber())

            c.save()

            # Adicionar rodapé com número de página em cada página
            reader = PdfReader(caminho_temp)
            writer = PdfWriter()

            total = len(reader.pages)
            for i, page in enumerate(reader.pages):
                # Textos
                texto_gerado = f"Gerado por: {usuario}"
                texto_data = f"Gerado em: {gerado_em}"
                texto_pagina = f"Página {i+1} de {total}"

                packet = canvas.Canvas(
                    os.path.normpath(os.path.join(pasta_temp, f"pagina_temp_{i}.pdf")),
                    pagesize=landscape(A4),
                )
                packet.setFont("Helvetica-Oblique", 9)
                packet.setFillColor(colors.gray)

                # Linha separadora (acima do rodapé)
                packet.setStrokeColor(colors.lightgrey)
                packet.setLineWidth(0.5)
                packet.line(
                    2 * cm, footer_y + 0.4 * cm, largura - 2 * cm, footer_y + 0.4 * cm
                )

                packet.drawString(2 * cm, 1.5 * cm, texto_gerado)  # Esquerda
                packet.drawCentredString(largura / 2, 1.5 * cm, texto_data)  # Centro
                packet.drawRightString(
                    largura - 2 * cm, 1.5 * cm, texto_pagina
                )  # Direita
                packet.save()

                # Mesclar rodapé na página original
                footer_pdf = PdfReader(
                    os.path.normpath(os.path.join(pasta_temp, f"pagina_temp_{i}.pdf"))
                )
                page.merge_page(footer_pdf.pages[0])
                writer.add_page(page)

            with open(caminho_final, "wb") as f:
                writer.write(f)

            QMessageBox.information(
                self, "PDF Gerado", "Relatório PDF gerado com sucesso!"
            )

            # Abrir no visualizador padrão ou
            if sys.platform == "win32":
                os.startfile(caminho_final)
            elif sys.platform == "darwin":
                Popen(["open", caminho_final])
            else:
                Popen(["xdg-open", caminho_final])

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao gerar relatório: {str(e)}")
            logger.error(f"Erro ao gerar relatório: {str(e)}")

    def limpaCampos(self):
        self.ui.campoNumAnoCertidao.setText(self.ano_corrente)
        self.ui.campoNumCertidao.setText("")
        self.ui.campoNumDocumento.setText("")
        self.ui.lineEditNumeroDocumento.clear()
        self.ui.dateEditDataSimples.setDate(QDate.currentDate())

        if self.ui.campoNumDocumento.isVisible():
            self.ui.campoNumDocumento.setFocus()
        else:
            self.ui.campoNumCertidao.setFocus()

        if self.ui.lineEditNumeroDocumento.isVisible():
            self.ui.lineEditNumeroDocumento.setFocus()

    def abrirNAPS2(
        self, caminho_arquivo="", somente_visualizar=False, digitalizacao_simples=False
    ):
        try:
            if not os.path.isfile(self.configuracoes.get_caminho_naps2()):
                logger.error(
                    f"O executável do NAPS2 não foi encontrado em: {self.configuracoes.get_caminho_naps2()}"
                )
                raise FileNotFoundError(
                    f"O executável do NAPS2 não foi encontrado em: {self.configuracoes.get_caminho_naps2()}"
                )

            self.loading = LoadingDialog(
                self,
                "Aguarde...\n\nO programa de digitalização (NAPS2) foi aberto.\nFeche-o para continuar usando o sistema.",
            )
            self.loading.show()

            self.thread = NAPS2Thread(caminho_arquivo)
            self.thread.finished.connect(self.loading.close)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.finished.connect(lambda: self.setEnabled(True))
            if not somente_visualizar and not digitalizacao_simples:
                self.thread.finished.connect(
                    lambda: self.on_digitalizacao_concluida(digitalizacao_simples=False)
                )
            if not somente_visualizar and digitalizacao_simples:
                self.thread.finished.connect(
                    lambda: self.on_digitalizacao_concluida(digitalizacao_simples=True)
                )
            self.thread.start()

        except FileNotFoundError as e:
            logger.error(str(e))
            QMessageBox.critical(
                self,
                "NAPS2 não encontrado",
                "O programa de digitalização (NAPS2) não foi encontrado.\n\nVerifique o caminho configurado no sistema.",
            )
        except Exception as e:
            logger.error(f"Erro inesperado ao tentar abrir o NAPS2: {e}")
            QMessageBox.critical(
                self,
                "Erro ao abrir o NAPS2",
                "Ocorreu um erro inesperado ao tentar abrir o programa de digitalização.",
            )

    def digitalizaDocumento(
        self,
        tipo_documento: int,
        num_documento="",
        ano_certidao="",
        num_certidao="",
        somente_visualizar=False,
    ):

        # Antes de começar, verificar se o NAPS2 está instalado
        if not os.path.isfile(self.configuracoes.get_caminho_naps2()):
            QMessageBox.critical(
                self, "Erro", "Programa de digitalização (NAPS2) não encontrado."
            )
            logger.error("Programa de digitalização (NAPS2) não encontrado.")
            return

        if num_documento == "" and (ano_certidao == "" or num_certidao == ""):
            QMessageBox.critical(
                self, "Erro", "É obrigatório informar um número de documento!"
            )
            return

        if tipo_documento != 2 and tipo_documento != 4:
            protocolo = f"{num_documento:0>6}"
            pasta_num = f"{protocolo[0]}{protocolo[1]}{protocolo[2]}"
            doc_num = f"{protocolo[3]}{protocolo[4]}{protocolo[5]}"
            local_documento = os.path.normpath(
                os.path.join(
                    self.configuracoes.get_caminho_por_indice(tipo_documento),
                    pasta_num,
                    f"{doc_num}.tif",
                )
            )
        else:
            ano = ano_certidao
            num_cert = f"{num_certidao:0>6}"
            pasta_ano = f"L00020{ano}"
            local_documento = os.path.normpath(
                os.path.join(
                    self.configuracoes.get_caminho_por_indice(tipo_documento),
                    pasta_ano,
                    f"{num_cert}.tif",
                )
            )

        local_doc_index = os.path.normpath(
            os.path.join(
                self.configuracoes.get_caminho_temp_index(),
                self.configuracoes.get_temp_index_usuario(),
                f"0001.TIF",
            )
        )
        try:
            if os.path.isfile(local_documento):
                self.local_documento = local_documento
                self.local_doc_index = local_doc_index
                self.paginas_antes = contar_paginas_tiff(local_documento)
                self.tipo_documento = tipo_documento
                self.abrirNAPS2(local_documento, somente_visualizar=somente_visualizar)

            else:
                msg = QMessageBox()
                msg.setWindowTitle("Documento não encontrado")
                if not somente_visualizar:
                    msg.setText(
                        f"{nomes_documentos[tipo_documento]} não existe.\nDeseja criar um(a) novo(a)?"
                    )
                else:
                    msg.setText(
                        f"{nomes_documentos[tipo_documento]} não existe.\nFavor verificar o número digitado e tentar novamente!"
                    )
                    msg.exec()
                    return
                msg.setIcon(QMessageBox.Icon.Question)
                msg.setStandardButtons(
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )

                # Alterar texto dos botões
                yes_button = msg.button(QMessageBox.StandardButton.Yes)
                yes_button.setText("Sim")
                no_button = msg.button(QMessageBox.StandardButton.No)
                no_button.setText("Não")

                resposta = msg.exec()
                if resposta == QMessageBox.StandardButton.Yes:
                    self.local_doc_index = local_doc_index
                    self.tipo_documento = tipo_documento
                    self.paginas_antes = 0
                    self.abrirNAPS2()
                    self.tipo_operacao = "novo documento"
                else:
                    self.tipo_operacao = "Cancelado"

        except Exception as e:
            logger.error(f"Erro ao tentar abrir o NAPS2: {e}")
            QMessageBox.critical(
                self, "Erro", "Houve um problema ao abrir o programa de digitalização."
            )

    def incrementaNumDocumento(self, quant: int):
        textoNumCertidao = self.ui.campoNumCertidao.text()
        textoNumProtocolo = self.ui.campoNumDocumento.text()
        if self.ui.campoNumCertidao.isVisible():
            if textoNumCertidao != "":
                try:
                    numDocInformado = int(textoNumCertidao)
                except Exception as err:
                    show_message("Informe um número válido", "Erro!")
            else:
                numDocInformado = 0
            # Não há números de documentos negativos, então se for 0 ou menor
            # (aumentando ou diminuindo) passa para 1, se chegar a 999999 também
            if numDocInformado > 0 and numDocInformado < 999999:
                numDocInformado += quant
            else:
                numDocInformado = 1
            self.ui.campoNumCertidao.setText(str(numDocInformado))
        elif self.ui.campoNumDocumento.isVisible():
            if textoNumProtocolo != "":
                try:
                    numDocInformado = int(textoNumProtocolo)
                except Exception as err:
                    show_message("Informe um número válido", "Erro!")
            else:
                numDocInformado = 0
            # Não há números de documentos negativos, então se for 0 ou menor
            # (aumentando ou diminuindo) passa para 1, se chegar a 999999 também
            if numDocInformado > 0 and numDocInformado < 999999:
                numDocInformado += quant
            else:
                numDocInformado = 1
            self.ui.campoNumDocumento.setText(str(numDocInformado))

    def habilitaDigitarDocumento(self, habilita: bool):
        self.ui.campoNumAnoCertidao.setEnabled(habilita)
        self.ui.campoNumCertidao.setEnabled(habilita)
        self.ui.campoNumDocumento.setEnabled(habilita)
        self.ui.buttonDigitalizar.setEnabled(habilita)
        self.ui.buttonDigitalizarDocumentosSimples.setEnabled(habilita)
        self.ui.lineEditNumeroDocumento.setEnabled(habilita)
        self.ui.dateEditDataSimples.setEnabled(habilita)
        self.ui.comboBoxTipoSimples.setEnabled(habilita)
        self.ui.setTrabalhoCB.setEnabled(habilita)
        self.ui.buttonGravar.setEnabled(not habilita)
        self.ui.buttonGravarDocumentosSimples.setEnabled(not habilita)
        self.ui.buttonAumentar.setEnabled(habilita)
        self.ui.buttonDiminuir.setEnabled(habilita)
        self.ui.buttonDigitalizar.setEnabled(habilita)
        self.ui.buttonVerificar.setEnabled(habilita)
        self.ui.buttonConferenciaErro.setEnabled(habilita)
        # if self.acesso == 'digitalização':
        #     self.ui.tabWidget.setTabEnabled(1, habilita)
        #     self.ui.tabWidget.setTabEnabled(2, habilita)
        # elif self.acesso == 'administrador':
        #     self.ui.tabWidget.setTabEnabled(1, habilita)
        #     self.ui.tabWidget.setTabEnabled(2, habilita)
        #     self.ui.tabWidget.setTabEnabled(3, habilita)
        #     self.ui.tabWidget.setTabEnabled(4, habilita)

    def gravaBanco(
        self,
        tipo_documento: int,
        tipo_alteracao: str,
        usuario: str,
        quant_paginas: int = 0,
        num_documento: str = "",
        ano_certidao: str = "",
        num_certidao: str = "",
    ):
        """
        Insere dados em uma tabela do banco com base no tipo de documento.

        Parâmetros:
            tipo_documento (int): Código que define o tipo do documento.
            tipo_alteracao (str): Tipo de operação realizada.
            quant_paginas (int): Quantidade de páginas que foram criadas(novo), inseridas ou removidas
            usuario (str): Nome do usuário que realizou a operação.
            num_documento (str, opcional): Número do documento (usado para tipos diferentes de 2 e 4).
            ano_certidao (str, opcional): Ano da certidão (usado para tipo 2 ou 4).
            num_certidao (str, opcional): Número da certidão (usado para tipo 2 ou 4).
        """
        agora = datetime.now().replace(microsecond=0)
        tabela = tab_doc[tipo_documento][0]
        documento = tab_doc[tipo_documento][1]
        num_cert_completo = (
            f"{num_certidao:0>6}"  # preenche com zeros até completar 6 dígitos
        )
        num_doc_completo = f"{num_documento:0>6}"
        # Tipos diferentes de 2 e 4: usa apenas o número do documento
        if tipo_documento not in (2, 4):
            colunas = f"{documento}, tipo_alteracao, usuario, qtd_paginas, data_hora"
            valores = (num_doc_completo, tipo_alteracao, usuario, quant_paginas, agora)

        # Tipos 2 e 4: exige ano e número de certidão
        else:
            ano_documento = tab_doc[tipo_documento][2]
            colunas = f"{documento}, {ano_documento}, tipo_alteracao, usuario, qtd_paginas, data_hora"
            valores = (
                num_cert_completo,
                ano_certidao,
                tipo_alteracao,
                usuario,
                quant_paginas,
                agora,
            )

        try:
            self.db_auditoria.inserir_dado(tabela, colunas, valores)
        except ConnectionError as e:
            QMessageBox.critical(
                self,
                "Erro de Conexão",
                "A conexão com o banco foi perdida. O sistema será encerrado.",
            )
            QCoreApplication.quit()
            return

    # Não é a conferência de documento, apenas um meio de o usuário que acabou de digitalizar
    # algo e tem dúvida do que fez, abrir para verificar se está correto antes de avançar para o
    # próximo documento, só é possível verificar quando não está no passo de gravação...
    def iniciaVerificarDoc(self, verifica_erro=False):
        tipo_documento = self.ui.setTrabalhoCB.currentIndex()
        num_documento = self.ui.campoNumDocumento.text()
        ano_certidao = self.ui.campoNumAnoCertidao.text()
        num_certidao = self.ui.campoNumCertidao.text()

        if num_documento == "" and (ano_certidao == "" or num_certidao == ""):
            QMessageBox.critical(
                self, "Erro", "É obrigatório informar um número de documento!"
            )
            return

        if tipo_documento != 2 and tipo_documento != 4:
            protocolo = f"{num_documento:0>6}"
            pasta_num = f"{protocolo[0]}{protocolo[1]}{protocolo[2]}"
            doc_num = f"{protocolo[3]}{protocolo[4]}{protocolo[5]}"
            if not verifica_erro:
                nome_arquivo = f"{doc_num}.tif"
                caminho_base = self.configuracoes.get_caminho_por_indice(tipo_documento)
            else:
                nome_arquivo = f"{doc_num}_conferir_erro.tif"
                caminho_base = os.path.join(
                    self.configuracoes.get_caminho_backup(),
                    nomes_conferencia[tipo_documento],
                )
            local_documento = os.path.normpath(
                os.path.join(caminho_base, pasta_num, nome_arquivo)
            )
            try:
                if os.path.isfile(local_documento):
                    comando = f'start /wait "" "{local_documento}"'
                    run(comando, shell=True)

                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("Documento não encontrado")
                    msg.setText(
                        f"{nomes_documentos[tipo_documento]} não existe.\nVerifique o número e tente novamente!"
                    )
                    msg.setIcon(QMessageBox.Information)
                    msg.exec()

            except Exception as e:
                logger.error(f"Erro ao tentar abrir o Documento: {e}")
                QMessageBox.critical(
                    self,
                    "Erro",
                    "Houve um problema ao abrir o documento para visualização.",
                )
        else:
            ano = ano_certidao
            num_cert = f"{num_certidao:0>6}"
            pasta_ano = f"L00020{ano}"
            if not verifica_erro:
                nome_arquivo = f"{num_cert}.tif"
                caminho_base = self.configuracoes.get_caminho_por_indice(tipo_documento)
            else:
                nome_arquivo = f"{num_cert}_conferir_erro.tif"
                caminho_base = os.path.join(
                    self.configuracoes.get_caminho_backup(),
                    nomes_conferencia[tipo_documento],
                )
            local_documento = os.path.normpath(
                os.path.join(caminho_base, pasta_ano, nome_arquivo)
            )

            try:
                if os.path.isfile(local_documento):
                    abrir_com_visualizador_classico(local_documento)

                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("Documento não encontrado")
                    msg.setText(
                        f"{nomes_documentos[tipo_documento]} não existe.\nVerifique o número e tente novamente!"
                    )
                    msg.setIcon(QMessageBox.Information)
                    msg.exec()

            except Exception as e:
                logger.error(f"Erro ao tentar abrir o Documento: {e}")
                QMessageBox.critical(
                    self,
                    "Erro",
                    "Houve um problema ao abrir o documento para visualização.",
                )

    def iniciaDigitalizacao(self, somente_visualizar=False):
        if not self.db_auditoria.conexao_ativa():
            QMessageBox.critical(
                self,
                "Erro de Conexão",
                "A conexão com o banco de dados foi perdida. O sistema será fechado.",
            )
            QCoreApplication.quit()
            return

        # Caminho completo da pasta temp_index do usuário
        temp_index_path = os.path.join(
            self.configuracoes.get_caminho_temp_index(),
            self.configuracoes.get_temp_index_usuario(),
        )

        # Verifica se já existem arquivos reais (não pastas) na pasta
        if os.path.exists(temp_index_path):
            arquivos_visiveis = [
                f
                for f in os.listdir(temp_index_path)
                if os.path.isfile(os.path.join(temp_index_path, f))
                and (f.lower().endswith(".tiff") or f.lower().endswith(".tif"))
            ]
            if arquivos_visiveis:
                QMessageBox.warning(
                    self,
                    "Aviso",
                    "A pasta temporária de digitalização já contém arquivos. Por favor, esvazie-a antes de iniciar uma nova digitalização.",
                )
                return

        indice = self.ui.setTrabalhoCB.currentIndex()
        num_doc = self.ui.campoNumDocumento.text()
        ano_cert = self.ui.campoNumAnoCertidao.text()
        num_cert = self.ui.campoNumCertidao.text()
        self.digitalizaDocumento(
            tipo_documento=indice,
            num_documento=num_doc,
            ano_certidao=ano_cert,
            num_certidao=num_cert,
            somente_visualizar=somente_visualizar,
        )

    def alteraTrabalho(self):
        indice = self.ui.setTrabalhoCB.currentIndex()
        if indice in (2, 4):
            self.setCertidaoVisible(True)
        else:
            self.setCertidaoVisible(False)

        self.limpaCampos()

    def setCertidaoVisible(self, visivel: bool):
        if visivel:
            self.ui.campoNumAnoCertidao.setVisible(True)
            self.ui.campoNumCertidao.setVisible(True)
            self.ui.lblAnoCertidao.setVisible(True)
            self.ui.lblNumCertidao.setVisible(True)
            self.ui.lblDocumento.setVisible(False)
            self.ui.campoNumDocumento.setVisible(False)
        else:
            self.ui.campoNumAnoCertidao.setVisible(False)
            self.ui.campoNumCertidao.setVisible(False)
            self.ui.lblAnoCertidao.setVisible(False)
            self.ui.lblNumCertidao.setVisible(False)
            self.ui.lblDocumento.setVisible(True)
            self.ui.campoNumDocumento.setVisible(True)

    def gravarDocumentoDigitalizado(self):
        print(f"Sigla do usuário: {self.sigla}")
        try:
            tipo_documento = self.ui.setTrabalhoCB.currentIndex()
            num_documento = self.ui.campoNumDocumento.text().strip()
            ano_cert = self.ui.campoNumAnoCertidao.text().strip()
            num_cert = self.ui.campoNumCertidao.text().strip()

            if (num_cert == "" or ano_cert == "") and num_documento == "":
                QMessageBox.warning(
                    self,
                    "Atenção",
                    "Preencha todos os campos obrigatórios antes de gravar.",
                )
                return

            processar_digitalizacao(
                tipo_documento=tipo_documento,
                num_documento=num_documento,
                caminho_temp=self.configuracoes.get_caminho_temp_index(),
                caminho_base=self.configuracoes.get_caminho_base(),
                caminho_backup=self.configuracoes.get_caminho_backup(),
                ano_cert=ano_cert,
                num_cert=num_cert,
                pasta_usuario=self.configuracoes.get_temp_index_usuario(),
                tipo_operacao=self.tipo_operacao,
            )

            QMessageBox.information(
                self, "Sucesso", "Digitalização gravada e substituída com sucesso."
            )
            self.habilitaDigitarDocumento(True)

            # Grava as informações da digitalização efetuada no banco
            if self.tipo_operacao not in ("Erro", "Cancelado"):
                self.gravaBanco(
                    tipo_documento=tipo_documento,
                    tipo_alteracao=self.tipo_operacao,
                    usuario=self.sigla,
                    quant_paginas=self.quant_paginas,
                    num_documento=num_documento,
                    ano_certidao=ano_cert,
                    num_certidao=num_cert,
                )
            else:
                print("Erro na operação!")

        except Exception as e:
            QMessageBox.critical(
                self, "Erro", f"Ocorreu um erro ao gravar a digitalização:\n{e}"
            )
            logger.error(f"Ocorreu um erro ao gravar a digitalização:\n{e}")

    def on_digitalizacao_concluida(self, digitalizacao_simples=False):
        if not digitalizacao_simples:
            try:
                paginas_depois = contar_paginas_tiff(self.local_doc_index)
                tipo_alteracao = "Erro"

                if self.paginas_antes == paginas_depois:
                    tipo_alteracao = "edição de páginas"
                elif self.paginas_antes > paginas_depois:
                    tipo_alteracao = "exclusão de páginas"
                elif (self.paginas_antes < paginas_depois) and (
                    self.paginas_antes != 0
                ):
                    tipo_alteracao = "inclusão de páginas"
                elif self.paginas_antes == 0 and paginas_depois > 0:
                    tipo_alteracao = "novo documento"

                self.tipo_operacao = tipo_alteracao
                self.quant_paginas = abs(paginas_depois - self.paginas_antes)

                print(
                    f"Tipo de operação: {self.tipo_operacao}, páginas: {self.quant_paginas}"
                )

            except Exception as e:
                logger.error(f"Erro ao processar digitalização: {e}")
                self.habilitaDigitarDocumento(True)

            finally:
                toast = Toast(self, "✅ Digitalização concluída com sucesso.")
                self.habilitaDigitarDocumento(False)
        else:
            toast = Toast(self, "✅ Digitalização concluída com sucesso.")
            self.habilitaDigitarDocumento(False)

    def showStatusTip(self, botao: str):
        if botao == "Digitalizar":
            tip = "Iniciando a digitalização do documento..."
        elif botao == "Gravar":
            tip = "Iniciando a gravação para a SERVCOM"
        else:
            tip = "Limpando campos"

        QApplication.sendEvent(self, QStatusTipEvent(tip))
        self.timer.start(3000)

    def hideStatusTip(self):
        QApplication.sendEvent(self, QStatusTipEvent(""))


def show_message(mensagem, titulo):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowIcon(QIcon(r"info.svg"))

    msg.setWindowTitle(titulo)
    msg.setText(mensagem)

    msg.setInformativeText("Informações adicionais podem ser inseridas aqui...")
    msg.setDetailedText("Ainda mais detalhes nessa parte")
    msg.exec()


if __name__ == "__main__":
    import sys

    # SQLite (usuários)
    users_db = DataBaseUsers()
    validar_sqlite(users_db)

    # PostgreSQL (auditoria digitalizações)
    db_handler = DBHandler()
    validar_postgresql(db_handler)

    app = QApplication(sys.argv)
    # Verificar se o sistema permite uso de notificações
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "System Tray", "System tray was not detected!")
        sys.exit(1)

    app.setWindowIcon(QIcon(r"scan_icon.png"))

    # Em vez de fechar o app minimizar para a system tray
    app.setQuitOnLastWindowClosed(True)

    # Criar o ícone do app e exibir na "system tray"
    tray = QSystemTrayIcon(QIcon(r"scan_icon.png"), app)
    tray.show()

    tray.setToolTip("2rgi Scan - v1.0")

    # # Criar o menu da system tray
    menu = QMenu()

    # Somente para teste de funcionamento das notificações
    # action_message_box = QAction("Mostrar caixa de mensagem")
    # action_message_box.triggered.connect(lambda: show_message('Teste de Mensagem ao clicar no Tray','Caixa de Mensagem'))
    # menu.addAction(action_message_box)

    # # Mostrar uma notificação no sistema
    # Somente para teste de funcionamento das notificações
    # action_tray_message = QAction("Mostrar notificação")
    # action_tray_message.triggered.connect(lambda: show_tray_message(window_obj, tray, 'Teste', 'Mensagem de teste'))
    # menu.addAction(action_tray_message)

    # Esconder ou exibir a janela para a system tray
    action_show_hide = QAction("Exibir/ocultar a janela principal")
    menu.addAction(action_show_hide)

    # Mostrar a janela a partir da system tray
    action_exit = QAction("Sair")
    action_exit.triggered.connect(app.exit)
    menu.addAction(action_exit)

    # Adicionar o menu ao contexto da system tray
    tray.setContextMenu(menu)

    login_form = LoginWindow()
    login_form.show()
    sys.exit(app.exec())
