import sys
import math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QLineEdit, QTextEdit, QLabel, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence


class CalculadoraAvanzadaPySide6(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pract 3 - Calculadora Multi-Modo (PySide6)")
        self.setFixedSize(380, 480)

        self.historial = []
        self.en_estado_error = False
        self.modo_cientifico = False

        self.iniciar_ui()
        self.crear_menus()
        self.aplicar_tema_oscuro()

    def iniciar_ui(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        self.layout_principal = QVBoxLayout(widget_central)
        self.layout_principal.setSpacing(2)
        self.layout_principal.setContentsMargins(12, 10, 12, 10)

        # 1. Display
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(45)
        self.display.setStyleSheet("font-size: 22px; padding: 4px;")
        self.layout_principal.addWidget(self.display)

        # 2. Etiqueta Historial
        self.lbl_historial = QLabel("Últimas 5 operaciones:")
        self.lbl_historial.setStyleSheet("font-weight: bold; margin-top: 2px;")
        self.layout_principal.addWidget(self.lbl_historial)

        # 3. Caja de Texto Historial
        self.txt_historial = QTextEdit()
        self.txt_historial.setReadOnly(True)
        self.txt_historial.setFixedHeight(60)
        self.txt_historial.setStyleSheet("font-family: Consolas; font-size: 11px;")
        self.layout_principal.addWidget(self.txt_historial)

        # 4. Botones Científicos
        self.widget_cientifico = QWidget()
        grid_cientifico = QGridLayout(self.widget_cientifico)
        grid_cientifico.setContentsMargins(0, 2, 0, 2)
        grid_cientifico.setSpacing(3)

        botones_cientificos = [
            ('√', 0, 0), ('^', 0, 1), ('π', 0, 2),
            ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2)
        ]

        for texto, fila, col in botones_cientificos:
            btn = QPushButton(texto)
            btn.setStyleSheet("font-size: 13px; font-weight: bold; min-height: 28px; background-color: #2b5b84;")
            self.conectar_boton(btn, texto)
            grid_cientifico.addWidget(btn, fila, col)

        self.widget_cientifico.setVisible(False)
        self.layout_principal.addWidget(self.widget_cientifico)

        # 5. Botones Estándar
        self.grid_botones = QGridLayout()
        self.grid_botones.setSpacing(3)
        self.grid_botones.setContentsMargins(0, 2, 0, 0)
        
        botones_estandar = [
            ('C', 0, 0), ('CE', 0, 1), ('/', 0, 2), ('*', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('-', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('+', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('=', 3, 3, 2, 1),
            ('0', 4, 0), ('.', 4, 1), ('Info', 4, 2)
        ]

        for item in botones_estandar:
            texto, fila, col = item[0], item[1], item[2]
            r_span = item[3] if len(item) > 3 else 1
            c_span = item[4] if len(item) > 4 else 1

            btn = QPushButton(texto)
            btn.setStyleSheet("font-size: 15px; font-weight: bold; min-height: 38px;")
            self.conectar_boton(btn, texto)
            self.grid_botones.addWidget(btn, fila, col, r_span, c_span)

        self.layout_principal.addLayout(self.grid_botones)

    def crear_menus(self):
        menu_bar = self.menuBar()

        # --- MENÚ MODO ---
        menu_modo = menu_bar.addMenu("&Modo")
        
        act_estandar = QAction("Estándar", self)
        act_estandar.triggered.connect(lambda: self.cambiar_modo(False))
        menu_modo.addAction(act_estandar)

        act_cientifico = QAction("Científico", self)
        act_cientifico.triggered.connect(lambda: self.cambiar_modo(True))
        menu_modo.addAction(act_cientifico)

        # --- MENÚ EDICIÓN ---
        menu_edicion = menu_bar.addMenu("&Edición")

        act_copiar = QAction("Copiar resultado", self)
        act_copiar.setShortcut(QKeySequence.StandardKey.Copy)
        act_copiar.triggered.connect(self.copiar_resultado)
        menu_edicion.addAction(act_copiar)

        act_limpiar_hist = QAction("Borrar historial", self)
        act_limpiar_hist.triggered.connect(self.limpiar_historial)
        menu_edicion.addAction(act_limpiar_hist)

        # --- MENÚ VER (TEMAS) ---
        menu_ver = menu_bar.addMenu("&Ver")
        
        act_oscuro = QAction("Tema Oscuro", self)
        act_oscuro.triggered.connect(self.aplicar_tema_oscuro)
        menu_ver.addAction(act_oscuro)

        act_claro = QAction("Tema Claro", self)
        act_claro.triggered.connect(self.aplicar_tema_claro)
        menu_ver.addAction(act_claro)

        # --- MENÚ AYUDA ---
        menu_ayuda = menu_bar.addMenu("&Ayuda")
        act_info = QAction("Acerca de...", self)
        act_info.triggered.connect(self.abrir_info)
        menu_ayuda.addAction(act_info)

    def cambiar_modo(self, cientifico: bool):
        self.modo_cientifico = cientifico
        self.widget_cientifico.setVisible(cientifico)
        if cientifico:
            self.setFixedSize(380, 550)
        else:
            self.setFixedSize(380, 480)

    def conectar_boton(self, btn, texto):
        if texto == 'Info':
            btn.clicked.connect(self.abrir_info)
        elif texto == '=':
            btn.clicked.connect(self.calcular)
        elif texto == 'C':
            btn.clicked.connect(self.limpiar)
        elif texto == 'CE':
            btn.clicked.connect(self.borrar_ultimo)
        elif texto == '√':
            btn.clicked.connect(lambda: self.agregar_caracter("math.sqrt("))
        elif texto == '^':
            btn.clicked.connect(lambda: self.agregar_caracter("**"))
        elif texto == 'π':
            btn.clicked.connect(lambda: self.agregar_caracter("math.pi"))
        elif texto in ['sin', 'cos', 'tan']:
            btn.clicked.connect(lambda t=texto: self.agregar_caracter(f"math.{t}(math.radians("))
        else:
            btn.clicked.connect(lambda _, t=texto: self.agregar_caracter(t))

    def agregar_caracter(self, char):
        if self.en_estado_error:
            return
        self.display.setText(self.display.text() + char)

    def limpiar(self):
        self.display.setText("")
        self.en_estado_error = False

    def borrar_ultimo(self):
        if self.en_estado_error:
            return
        texto = self.display.text()
        if texto:
            self.display.setText(texto[:-1])

    def calcular(self):
        if self.en_estado_error:
            return

        expr = self.display.text()
        if not expr:
            return

        try:
            res = eval(expr, {"__builtins__": None, "math": math}, {})
            if isinstance(res, float) and res.is_integer():
                res = int(res)

            res_str = str(res)
            self.actualizar_historial(f"{expr} = {res_str}")
            self.display.setText(res_str)
        except Exception:
            self.display.setText("Error")
            self.en_estado_error = True

    def actualizar_historial(self, operacion):
        self.historial.append(operacion)
        if len(self.historial) > 5:
            self.historial.pop(0)
        self.txt_historial.setText("\n".join(self.historial))

    def copiar_resultado(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.display.text())

    def limpiar_historial(self):
        self.historial.clear()
        self.txt_historial.clear()

    def aplicar_tema_oscuro(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; color: #ffffff; }
            QLabel { color: #ffffff; }
            QLineEdit { background-color: #2d2d2d; color: #ffffff; border: 1px solid #3d3d3d; border-radius: 4px; }
            QTextEdit { background-color: #121212; color: #00ffcc; border: 1px solid #3d3d3d; }
            QPushButton { background-color: #333333; color: #ffffff; border-radius: 4px; }
            QPushButton:hover { background-color: #444444; }
            QMenuBar { background-color: #2d2d2d; color: #ffffff; }
            QMenuBar::item:selected { background-color: #3d3d3d; }
            QMenu { background-color: #2d2d2d; color: #ffffff; }
            QMenu::item:selected { background-color: #007acc; }
            QMessageBox { background-color: #2d2d2d; }
            QMessageBox QLabel { color: #ffffff; }
            QMessageBox QPushButton { background-color: #333333; color: #ffffff; padding: 5px 15px; border-radius: 4px; }
            QMessageBox QPushButton:hover { background-color: #444444; }
        """)

    def aplicar_tema_claro(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0f0; color: #000000; }
            QLabel { color: #000000; }
            QLineEdit { background-color: #ffffff; color: #000000; border: 1px solid #cccccc; border-radius: 4px; }
            QTextEdit { background-color: #ffffff; color: #005588; border: 1px solid #cccccc; }
            QPushButton { background-color: #e1e1e1; color: #000000; border-radius: 4px; }
            QPushButton:hover { background-color: #d0d0d0; }
            QMenuBar { background-color: #e1e1e1; color: #000000; }
            QMenuBar::item:selected { background-color: #cccccc; }
            QMenu { background-color: #ffffff; color: #000000; }
            QMenu::item:selected { background-color: #0078d7; color: #ffffff; }
            QMessageBox { background-color: #f0f0f0; }
            QMessageBox QLabel { color: #000000; }
            QMessageBox QPushButton { background-color: #e1e1e1; color: #000000; padding: 5px 15px; border-radius: 4px; }
            QMessageBox QPushButton:hover { background-color: #d0d0d0; }
        """)

    def abrir_info(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Información")
        msg.setText("Calculadora Avanzada v3.0\nAutor: Desarrollador\nLibrería: PySide6 (Qt)")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculadoraAvanzadaPySide6()
    window.show()
    sys.exit(app.exec())