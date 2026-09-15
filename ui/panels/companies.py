from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLineEdit, QPushButton, QLabel
)


class CompaniesPanel(QWidget):
    """Panel para añadir/quitar las empresas que le interesan al cliente."""

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

    def on_add_clicked(self):
        # TODO: guardar en data/config.json para que el matching de ofertas lo use
        text = self.company_input.text().strip()
        if text:
            self.company_list.addItem(text)
            self.company_input.clear()

    def on_remove_clicked(self):
        # TODO: eliminar también de data/config.json al confirmar
        row = self.company_list.currentRow()
        if row >= 0:
            self.company_list.takeItem(row)

    def get_companies(self):
        return [self.company_list.item(i).text() for i in range(self.company_list.count())]