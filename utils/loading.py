# utils/loading.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class LoadingDialog(QDialog):
    def __init__(self, parent=None, mensagem="Carregando..."):
        super().__init__(parent)
        self.setWindowTitle("Aguarde")
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(300, 100)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)

        label = QLabel(mensagem, alignment=Qt.AlignCenter)
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
                color: #333;
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
