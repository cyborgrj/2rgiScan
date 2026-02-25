from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation
from PySide6.QtGui import QFont


class Toast(QWidget):
    def __init__(self, parent=None, mensagem="Mensagem", duracao=1000):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.ToolTip)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet(
            """
            background-color: rgba(44, 123, 229, 230);
            color: white;
            border-radius: 6px;
            padding: 12px 20px;
            font-size: 10pt;
        """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        label = QLabel(mensagem)
        label.setWordWrap(True)
        label.setFont(QFont("Segoe UI", 10))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.setMinimumWidth(300)
        self.adjustSize()

        if parent:
            x = parent.geometry().right() - self.width() - 30
            y = parent.geometry().bottom() - self.height() - 30
            self.move(x, y)

        self.show()
        self.fade_out = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out.setDuration(500)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)

        QTimer.singleShot(duracao, self.iniciar_fade)

    def iniciar_fade(self):
        self.fade_out.start()
        self.fade_out.finished.connect(self.close)
