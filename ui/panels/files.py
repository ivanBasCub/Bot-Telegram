from pathlib import Path
import shutil

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
)


class FilesPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.documents_dir = Path("data/documents")
        self.documents_dir.mkdir(parents=True, exist_ok=True)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Documentos a adjuntar"))

        # CV
        cv_row = QHBoxLayout()

        self.cv_path_input = QLineEdit()
        self.cv_path_input.setPlaceholderText("CV")
        self.cv_path_input.setReadOnly(True)

        self.cv_button = QPushButton("Seleccionar CV")
        self.cv_button.clicked.connect(self.on_select_cv)

        cv_row.addWidget(self.cv_path_input)
        cv_row.addWidget(self.cv_button)

        # Certificado
        cert_row = QHBoxLayout()

        self.cert_path_input = QLineEdit()
        self.cert_path_input.setPlaceholderText("Certificado")
        self.cert_path_input.setReadOnly(True)

        self.cert_button = QPushButton("Seleccionar certificado")
        self.cert_button.clicked.connect(self.on_select_cert)

        cert_row.addWidget(self.cert_path_input)
        cert_row.addWidget(self.cert_button)

        layout.addLayout(cv_row)
        layout.addLayout(cert_row)
        layout.addStretch()

    def _copy_document(self, source_path, destination_name):
        """
        Copia un documento seleccionado por el usuario
        a data/documents/.
        """

        source = Path(source_path)
        destination = self.documents_dir / destination_name

        try:
            shutil.copy2(source, destination)
            return destination

        except OSError as e:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo copiar el archivo:\n\n{e}"
            )
            return None

    def on_select_cv(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar CV",
            "",
            "PDF (*.pdf)"
        )

        if not path:
            return

        destination = self._copy_document(
            path,
            "cv.pdf"
        )

        if destination:
            self.cv_path_input.setText(str(destination))


    def on_select_cert(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar certificado",
            "",
            "PDF (*.pdf)"
        )

        if not path:
            return

        destination = self._copy_document(
            path,
            "certificado.pdf"
        )

        if destination:
            self.cert_path_input.setText(str(destination))



    def get_paths(self):
        return {
            "cv_path": self.cv_path_input.text() or None,
            "cert_path": self.cert_path_input.text() or None,
        }