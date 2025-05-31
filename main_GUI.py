import os
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QWidget, QLabel, QCheckBox, QSpacerItem, QSizePolicy)
from PyQt6.QtGui import QIcon, QAction, QFont
from PyQt6.QtCore import QCoreApplication
from GerenciamentoUI.ui_01_layoutsCompressao import LayoutsCompressao
from GerenciamentoUI.ui_02_gerenteGUILayouts import GerenciadorInterface
from GerenciamentoUI.ui_03_dragDrop import DragDropListWidget
from MotoresCompressao.mtcomp_01_metodosCompressao import MetodoCompressao, MenuPersistente
from Traducao.tr_01_gerenciadorTraducao import GerenciadorTraducao


class InterfaceGrafica(QMainWindow, MetodoCompressao):
    def __init__(self):
        super().__init__()
        self.gerenciador_interface = GerenciadorInterface()
        self.layouts_compressao = LayoutsCompressao(self.gerenciador_interface, self.create_button)
        self.compression_method_layouts = self.layouts_compressao.create_compression_method_layouts()
        self.current_layouts = {}

        self.gerenciador_traducao = GerenciadorTraducao()
        self.gerenciador_traducao.idioma_alterado.connect(self.retranslateUi)
        self.gerenciador_traducao.aplicar_traducao()

        self.traduzir_widgets = {}

        self.init_menu()
        self.init_ui()
        MetodoCompressao.load_compression_method(self)

    def init_menu(self):
        self.menu_bar = self.menuBar()

        self.config_menu = self.menu_bar.addMenu(QCoreApplication.translate("InterfaceGrafica", "Configurações"))

        self.compression_method_action = QAction(QCoreApplication.translate("InterfaceGrafica", "Selecionar Método de Compressão"), self)
        self.compression_method_action.triggered.connect(self.select_compression_method)
        self.config_menu.addAction(self.compression_method_action)

        self.idiomas_menu = MenuPersistente(QCoreApplication.translate("InterfaceGrafica", "Idiomas"), self)
        self.config_menu.addMenu(self.idiomas_menu)

        self.pt_br_action = QAction("Português (Brasil)", self)
        self.pt_br_action.triggered.connect(lambda: self.mudar_idioma("pt_BR"))
        self.pt_br_action.setCheckable(True)
        self.pt_br_action.setChecked(self.gerenciador_traducao.idioma_atual == "pt_BR")
        self.idiomas_menu.addAction(self.pt_br_action)

        self.en_us_action = QAction("English (United States)", self)
        self.en_us_action.triggered.connect(lambda: self.mudar_idioma("en_US"))
        self.en_us_action.setCheckable(True)
        self.en_us_action.setChecked(self.gerenciador_traducao.idioma_atual == "en_US")
        self.idiomas_menu.addAction(self.en_us_action)

        self.config_menu.aboutToShow.connect(self.update_compression_menus)

    def update_compression_menus(self):
        self.select_compression_method()

    def mudar_idioma(self, codigo_idioma):
        self.pt_br_action.setChecked(codigo_idioma == "pt_BR")
        self.en_us_action.setChecked(codigo_idioma == "en_US")

        self.gerenciador_traducao.definir_idioma(codigo_idioma)

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("InterfaceGrafica", "Gerenciador de BackUp"))

        self.config_menu.setTitle(QCoreApplication.translate("InterfaceGrafica", "Configurações"))
        self.idiomas_menu.setTitle(QCoreApplication.translate("InterfaceGrafica", "Idiomas"))
        self.compression_method_action.setText(QCoreApplication.translate("InterfaceGrafica", "Selecionar Método de Compressão"))

        for button, text in self.main_buttons.items():
            button.setText(QCoreApplication.translate("InterfaceGrafica", text))

        self.folder_label.setText(QCoreApplication.translate("InterfaceGrafica", "Diretório(s) Pastas e Arquivos:"))

        for method, checkbox in self.checkboxes.items():
            if method == 'extracao':
                checkbox.setText(QCoreApplication.translate("InterfaceGrafica", "EXTRAÇÃO"))

            else:
                checkbox.setText(method.upper())

        self.rebuild_method_layouts()

        self.gerenciador_interface.atualizar_traducoes_dialogos()

        self.update_compression_menus()

    def init_ui(self):
        self.setWindowTitle(QCoreApplication.translate("InterfaceGrafica", "Gerenciador de BackUp"))
        self.setWindowIcon(QIcon(os.path.join(getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))), "icones", "Manager-BackUp.ico")))

        self.main_buttons = {}
        self.folder_label = None

        main_layout = QVBoxLayout()
        self.main_layout_1_widget = self.create_widget_with_layout(self.create_main_layout_1())
        self.main_layout_1_widget.setMinimumHeight(152)
        self.main_layout_1_widget.setMaximumHeight(304)
        main_layout.addWidget(self.main_layout_1_widget)
        main_layout.addWidget(self.create_widget_with_layout(self.create_main_layout_2()))
        main_layout.addWidget(self.create_scroll_area())

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_widget_with_layout(self, layout):
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def create_main_layout_1(self):
        layout = QHBoxLayout()
        layout.addLayout(self.create_first_quadrant())
        layout.addLayout(self.create_second_quadrant())
        return layout

    def create_first_quadrant(self):
        layout = QVBoxLayout()
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        add_folders_button = self.create_button(QCoreApplication.translate("InterfaceGrafica", "Adicionar Pastas"), self.gerenciador_interface.browse_folder)
        add_files_button = self.create_button(QCoreApplication.translate("InterfaceGrafica", "Adicionar Arquivos"), self.gerenciador_interface.browse_file)
        test_integrity_button = self.create_button(QCoreApplication.translate("InterfaceGrafica", "Testar Integridade"), self.gerenciador_interface.testar_integridade, "interrogacao.png")

        self.main_buttons[add_folders_button] = "Adicionar Pastas"
        self.main_buttons[add_files_button] = "Adicionar Arquivos"
        self.main_buttons[test_integrity_button] = "Testar Integridade"

        layout.addWidget(add_folders_button)
        layout.addWidget(add_files_button)
        layout.addWidget(test_integrity_button)
        return layout

    def create_second_quadrant(self):
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.folder_label = QLabel(QCoreApplication.translate("InterfaceGrafica", "Diretório(s) Pastas e Arquivos:"))
        button_layout.addWidget(self.folder_label)

        button_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        clear_input_button = self.create_button(QCoreApplication.translate("InterfaceGrafica", "Limpar Entrada"), self.gerenciador_interface.clear_folders, "clear_button3.png")
        clear_outputs_button = self.create_button(QCoreApplication.translate("InterfaceGrafica", "Limpar Todas Saídas"), self.gerenciador_interface.clear_output, "clear_button2.png")

        self.main_buttons[clear_input_button] = "Limpar Entrada"
        self.main_buttons[clear_outputs_button] = "Limpar Todas Saídas"

        button_layout.addWidget(clear_input_button)
        button_layout.addWidget(clear_outputs_button)
        layout.addLayout(button_layout)
        self.gerenciador_interface.folder_listbox = DragDropListWidget()
        layout.addWidget(self.gerenciador_interface.folder_listbox)
        return layout

    def rebuild_method_layouts(self):
        for method in list(self.current_layouts.keys()):
            layout_to_remove = self.current_layouts.pop(method)
            self.remove_layout_widgets(layout_to_remove)
            self.method_layouts_container.removeItem(layout_to_remove)
            layout_to_remove.deleteLater()

        for method, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                new_layout = self.compression_method_layouts[method]()
                self.current_layouts[method] = new_layout
                self.method_layouts_container.addLayout(new_layout)

        self.adjust_scroll_area()

    def create_main_layout_2(self):
        layout = QHBoxLayout()
        layout.addLayout(self.create_third_quadrant())
        return layout

    def create_third_quadrant(self):
        layout = QVBoxLayout()
        self.create_method_checkboxes(layout)
        return layout

    def create_scroll_area(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setMinimumSize(600, 347)
        self.method_layouts_container = QVBoxLayout()
        self.scroll_area_layout.addLayout(self.method_layouts_container)
        return self.scroll_area

    def create_button(self, text, callback=None, icon=None):
        button = QPushButton(text)
        button.setMinimumWidth(20 * button.fontMetrics().horizontalAdvance('m'))
        button.setMaximumWidth(20 * button.fontMetrics().horizontalAdvance('m'))
        button.setMinimumHeight(int(1.45 * button.fontMetrics().height()))
        button.setMaximumHeight(int(1.45 * button.fontMetrics().height()))
        button.setFont(QFont('Arial', 9))
        if icon:
            button.setIcon(QIcon(os.path.join(getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))), "icones", icon)))

        if callback:
            button.clicked.connect(callback)

        return button

    def create_method_checkboxes(self, layout):
        checkbox_layout = QHBoxLayout()
        checkbox_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        methods = ['rar', 'zip', '7z', 'tar.bz2', 'zipx', 'tar.xz', 'tgz', 'tar.gz', 'lzh', 'iso', 'tar', 'wim', 'extracao']
        method_display_names = {}

        for method in methods:
            if method == 'extracao':
                method_display_names[method] = QCoreApplication.translate("InterfaceGrafica", "EXTRAÇÃO")

            else:
                method_display_names[method] = method.upper()

        self.checkboxes = {method: QCheckBox(method_display_names[method]) for method in methods}

        for method, checkbox in self.checkboxes.items():
            checkbox.method = method
            checkbox.toggled.connect(self.on_method_toggled)
            checkbox_layout.addWidget(checkbox)

        layout.addLayout(checkbox_layout)

    def on_method_toggled(self):
        for method, checkbox in self.checkboxes.items():
            if checkbox.isChecked() and method not in self.current_layouts:
                new_layout = self.compression_method_layouts[method]()
                self.current_layouts[method] = new_layout
                self.method_layouts_container.addLayout(new_layout)

            elif not checkbox.isChecked() and method in self.current_layouts:
                layout_to_remove = self.current_layouts.pop(method)
                self.remove_layout_widgets(layout_to_remove)
                self.method_layouts_container.removeItem(layout_to_remove)
                layout_to_remove.deleteLater()

        self.adjust_scroll_area()

    def adjust_scroll_area(self):
        num_layouts = len(self.current_layouts)
        max_layouts = min(num_layouts, 4)
        self.scroll_area.setMinimumHeight(347 + max_layouts * 10)
        self.main_layout_1_widget.setMaximumHeight(304 - max_layouts * 20)

    def remove_layout_widgets(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

                else:
                    self.remove_layout_widgets(item.layout())

    def closeEvent(self, event):
        if hasattr(self, 'gerenciador_traducao') and self.gerenciador_traducao.tradutor:
            self.gerenciador_traducao.app.removeTranslator(self.gerenciador_traducao.tradutor)

        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gerenciador_traducao = GerenciadorTraducao()
    window = InterfaceGrafica()
    window.show()
    sys.exit(app.exec())
