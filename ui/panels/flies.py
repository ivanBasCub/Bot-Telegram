from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog
)


class FilesPanel(QWidget):
    """Panel para seleccionar el CV y el certificado a adjuntar en los correos."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Documentos a adjuntar"))

        cv_row = QHBoxLayout()
        self.cv_path_input = QLineEdit()
        self.cv_path_input.setPlaceholderText("Ruta al CV (PDF)")
        self.cv_path_input.setReadOnly(True)
        self.cv_button = QPushButton("Seleccionar CV")
        self.cv_button.clicked.connect(self.on_select_cv)
        cv_row.addWidget(self.cv_path_input)
        cv_row.addWidget(self.cv_button)

        cert_row = QHBoxLayout()
        self.cert_path_input = QLineEdit()
        self.cert_path_input.setPlaceholderText("Ruta al certificado (PDF)")
        self.cert_path_input.setReadOnly(True)
        self.cert_button = QPushButton("Seleccionar certificado")
        self.cert_button.clicked.connect(self.on_select_cert)
        cert_row.addWidget(self.cert_path_input)
        cert_row.addWidget(self.cert_button)

        layout.addLayout(cv_row)
        layout.addLayout(cert_row)
        layout.addStretch()

    def on_select_cv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Seleccionar CV", filter="PDF (*.pdf)")
        if path:
            self.cv_path_input.setText(path)
            # TODO: guardar la ruta en data/config.json (CV_PATH)

    def on_select_cert(self):
        path, _ = QFileDialog.getOpenFileName(self, "Seleccionar certificado", filter="PDF (*.pdf)")
        if path:
            self.cert_path_input.setText(path)
            # TODO: guardar la ruta en data/config.json (CERT_PATH)

    def get_paths(self):
        return {
            "cv_path": self.cv_path_input.text() or None,
            "cert_path": self.cert_path_input.text() or None,
        }