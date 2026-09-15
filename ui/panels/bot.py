from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt


class BotPanel(QWidget):
    """Panel para arrancar/parar el bot y ver su estado actual."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = False
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        self.status_label = QLabel("Estado: detenido")
        self.status_label.setAlignment(Qt.AlignCenter)

        buttons_row = QHBoxLayout()
        self.start_button = QPushButton("Iniciar bot")
        self.stop_button = QPushButton("Detener bot")
        self.stop_button.setEnabled(False)

        self.start_button.clicked.connect(self.on_start_clicked)
        self.stop_button.clicked.connect(self.on_stop_clicked)

        buttons_row.addWidget(self.start_button)
        buttons_row.addWidget(self.stop_button)

        layout.addWidget(self.status_label)
        layout.addLayout(buttons_row)
        layout.addStretch()

    def on_start_clicked(self):
        # TODO: arrancar aquí el listener de Telethon (core/telegram/user_client.py)
        self._running = True
        self.status_label.setText("Estado: en marcha")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def on_stop_clicked(self):
        # TODO: parar aquí el listener de Telethon de forma ordenada
        self._running = False
        self.status_label.setText("Estado: detenido")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)