from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from qasync import asyncSlot

from core.config_bd import load_bd
from core.telegram.user_client import (
    client, connect_client, start_listener_task, stop_listener, is_listener_running,
)


class BotPanel(QWidget):

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

    def showEvent(self, event):
        super().showEvent(event)
        self._refresh_status()

    def _refresh_status(self):
        """Sincroniza label y botones con el estado real del cliente/listener."""
        num_canales = len(load_bd().get("channels", []))

        if is_listener_running():
            self.status_label.setText(f"Estado: en marcha (vigilando {num_canales} canales)")
            self._running = True
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        elif client.is_connected():
            self.status_label.setText("Estado: conectado (sin canales seleccionados)")
            self._running = True
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else:
            self.status_label.setText("Estado: detenido")
            self._running = False
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    @asyncSlot()
    async def on_start_clicked(self):
        self.start_button.setEnabled(False)
        self.status_label.setText("Estado: conectando...")

        try:
            await connect_client(parent=self)
        except Exception as e:
            self.status_label.setText(f"⚠️ Error al conectar: {e}")
            self.start_button.setEnabled(True)
            return

        canales = load_bd().get("channels", [])
        if canales:
            start_listener_task()
            self.status_label.setText(f"Estado: en marcha (vigilando {len(canales)} canales)")
        else:
            self.status_label.setText("Estado: conectado (sin canales seleccionados)")

        self._running = True
        self.stop_button.setEnabled(True)

    @asyncSlot()
    async def on_stop_clicked(self):
        self.stop_button.setEnabled(False)
        self.status_label.setText("Estado: deteniendo...")

        await stop_listener()

        self._running = False
        self.status_label.setText("Estado: detenido")
        self.start_button.setEnabled(True)