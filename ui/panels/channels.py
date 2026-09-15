from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLineEdit,QPushButton, QLabel, QMessageBox
from qasync import asyncSlot

from core.telegram.user_client import client
from core.config_bd import load_bd, save_bd
from middleware.telegram_middleware import save_valid_channels


class ChannelsPanel(QWidget):
    """Panel para añadir/quitar los canales de Telegram que el bot debe vigilar."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self._load_existing_channels()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Canales vigilados"))
        self.channel_list = QListWidget()
        layout.addWidget(self.channel_list)

        input_row = QHBoxLayout()
        self.channel_input = QLineEdit()
        self.channel_input.setPlaceholderText("ID o @usuario del canal")
        self.add_button = QPushButton("Añadir")
        self.remove_button = QPushButton("Quitar seleccionado")

        self.add_button.clicked.connect(self.on_add_clicked)
        self.remove_button.clicked.connect(self.on_remove_clicked)

        input_row.addWidget(self.channel_input)
        input_row.addWidget(self.add_button)

        layout.addLayout(input_row)
        layout.addWidget(self.remove_button)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

    def _load_existing_channels(self):
        """Rellena la lista con lo que ya haya guardado en data/config.json."""
        config = load_bd()
        for canal in config.get("channels", []):
            self.channel_list.addItem(canal)

    @asyncSlot()
    async def on_add_clicked(self):
        text = self.channel_input.text().strip()
        if not text:
            return

        self.add_button.setEnabled(False)
        self.status_label.setText(f"Comprobando {text}...")

        canales_a_probar = self.get_channels() + [text]
        resultado = await save_valid_channels(client, canales_a_probar)

        self.channel_list.clear()
        for canal in resultado["validos"]:
            self.channel_list.addItem(canal)

        if text in resultado["invalidos"]:
            self.status_label.setText(f"⚠️ No se pudo acceder a '{text}'")
            QMessageBox.warning(
                self,
                "Canal no válido",
                f"No se pudo acceder al canal '{text}'.\n"
                "Comprueba que el ID/usuario es correcto y que la cuenta ya es miembro.",
            )
        else:
            self.status_label.setText(f"Canal '{text}' añadido correctamente.")
            self.channel_input.clear()

        self.add_button.setEnabled(True)

    def on_remove_clicked(self):
        row = self.channel_list.currentRow()
        if row < 0:
            return
        canal = self.channel_list.item(row).text()
        self.channel_list.takeItem(row)

        config = load_bd()
        canales = config.get("channels", [])
        if canal in canales:
            canales.remove(canal)
        config["channels"] = canales
        save_bd(config)

    def get_channels(self):
        return [self.channel_list.item(i).text() for i in range(self.channel_list.count())]