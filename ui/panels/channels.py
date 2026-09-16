from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QLabel
from PySide6.QtCore import Qt
from qasync import asyncSlot

from core.telegram.user_client import client, connect_client, is_listener_running, restart_listener
from core.config_bd import load_bd, save_bd

class ChannelsPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Canales disponibles"))
        self.channel_list = QListWidget()
        layout.addWidget(self.channel_list)

        buttons_row = QHBoxLayout()
        self.refresh_button = QPushButton("Actualizar lista")
        self.save_button = QPushButton("Guardar selección")

        self.refresh_button.clicked.connect(self.on_refresh_clicked)
        self.save_button.clicked.connect(self.on_save_clicked)

        buttons_row.addWidget(self.refresh_button)
        buttons_row.addWidget(self.save_button)
        layout.addLayout(buttons_row)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

    def showEvent(self, event):
        super().showEvent(event)
        if self.channel_list.count() == 0:
            self.on_refresh_clicked()

    @asyncSlot()
    async def on_refresh_clicked(self):
        self.refresh_button.setEnabled(False)
        self.status_label.setText("Cargando canales...")

        try:
            await connect_client()
            dialogs = await client.get_dialogs()
        except Exception as e:
            self.status_label.setText(f"⚠️ Error al cargar canales: {e}")
            self.refresh_button.setEnabled(True)
            return

        canales_guardados = set(load_bd().get("channels", []))

        self.channel_list.clear()
        for dialog in dialogs:
            if not (dialog.is_channel or dialog.is_group):
                continue

            item = QListWidgetItem(f"{dialog.name} ({dialog.id})")
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setData(Qt.UserRole, dialog.id)
            item.setCheckState(
                Qt.Checked if dialog.id in canales_guardados else Qt.Unchecked
            )
            self.channel_list.addItem(item)

        self.status_label.setText(f"{self.channel_list.count()} canales encontrados.")
        self.refresh_button.setEnabled(True)

    @asyncSlot()
    async def on_save_clicked(self):
        seleccionados = [
            self.channel_list.item(i).data(Qt.UserRole)
            for i in range(self.channel_list.count())
            if self.channel_list.item(i).checkState() == Qt.Checked
        ]

        config = load_bd()
        config["channels"] = seleccionados
        save_bd(config)

        self.status_label.setText(f"Guardados {len(seleccionados)} canales.")

        if seleccionados and is_listener_running():
            self.status_label.setText(
                f"Guardados {len(seleccionados)} canales. Reiniciando vigilancia..."
            )
            self.save_button.setEnabled(False)
            try:
                await restart_listener()
                self.status_label.setText(f"Vigilando {len(seleccionados)} canales.")
            except Exception as e:
                self.status_label.setText(f"⚠️ Error al reiniciar: {e}")
            finally:
                self.save_button.setEnabled(True)