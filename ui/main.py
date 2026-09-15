from PySide6.QtWidgets import QMainWindow, QTabWidget

from ui.panels.bot import BotPanel
from ui.panels.channels import ChannelsPanel
from ui.panels.companies import CompaniesPanel
from ui.panels.files import FilesPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PY_BOT_EMPR")
        self.resize(600, 400)

        tabs = QTabWidget()
        self.bot_panel = BotPanel()
        self.channels_panel = ChannelsPanel()
        self.companies_panel = CompaniesPanel()
        self.files_panel = FilesPanel()

        tabs.addTab(self.bot_panel, "Bot")
        tabs.addTab(self.channels_panel, "Canales")
        tabs.addTab(self.companies_panel, "Empresas")
        tabs.addTab(self.files_panel, "Documentos")

        self.setCentralWidget(tabs)