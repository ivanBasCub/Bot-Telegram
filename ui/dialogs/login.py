from PySide6.QtWidgets import QInputDialog, QLineEdit

def ask_code(parent=None) -> str:
    code, ok = QInputDialog.getText(
        parent,
        "Código de verificación",
        "Introduce el código que has recibido por telegram:"
    )
    if not ok or not code.strip():
        raise RuntimeError("Inicio de sesión cancelado: No se introdujo el codigo")
    return code.strip()

def ask_password(parent=None) -> str:
    password, ok = QInputDialog.getText(
        parent,
        "Verificación de dos pasos",
        "Introduce tu contraseña de Telegram (2FA):",
        QLineEdit.Password
    )
    if not ok or not password:
        raise RuntimeError("Inicio de sesión cancelado: No se introdujo contraseña 2FA")
    return password