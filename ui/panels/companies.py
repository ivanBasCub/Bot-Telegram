from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QLineEdit, QPushButton, QLabel

from core.config_bd import load_bd, save_bd


class CompaniesPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Empresas de interés"))
        self.company_list = QListWidget()
        layout.addWidget(self.company_list)

        input_row = QHBoxLayout()
        self.company_input = QLineEdit()
        self.company_input.setPlaceholderText("Nombre de la empresa")
        self.add_button = QPushButton("Añadir")
        self.remove_button = QPushButton("Quitar seleccionada")

        self.add_button.clicked.connect(self.on_add_clicked)
        self.remove_button.clicked.connect(self.on_remove_clicked)

        input_row.addWidget(self.company_input)
        input_row.addWidget(self.add_button)

        layout.addLayout(input_row)
        layout.addWidget(self.remove_button)
        self._load_companies(set(load_bd().get("companies", [])))


    def on_add_clicked(self):
        text = self.company_input.text().strip()
        self.company_input.clear()

        if not text:
            return

        companies_saved = set(load_bd().get("companies", []))
        companies_saved.add(text)

        bd = load_bd()
        bd["companies"] = list(companies_saved)
        save_bd(bd)

        self.company_list.clear()
        self._load_companies(companies_saved)


    def on_remove_clicked(self):
        row = self.company_list.currentRow()
        company = self.company_list.currentItem().text()
        if company:
            bd = load_bd()

            companies_saved = bd.get("companies", [])
            companies_saved.remove(company)

            bd["companies"] = companies_saved
            save_bd(bd)
            self.company_list.takeItem(row)


    def _load_companies(self, companies: set):
        for company in companies:
            item = QListWidgetItem(company)
            self.company_list.addItem(item)