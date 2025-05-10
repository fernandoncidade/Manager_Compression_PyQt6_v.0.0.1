import os
import sys
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QScrollArea, QWidget, QLabel, QCheckBox, QSpacerItem, QSizePolicy)
from PyQt6.QtGui import QIcon, QAction, QFont
from v005_2_layouts_compressao import LayoutsCompressao
from v005_3_gerente_GUI_layouts import GerenciadorInterface
from v005_4_metodos_compressao import MetodoCompressao, CompressType
from v005_6_drag_drop import DragDropListWidget


class InterfaceGrafica(QMainWindow, MetodoCompressao):
    def __init__(self):
        super().__init__()
        self.gerenciador_interface = GerenciadorInterface()
        self.layouts_compressao = LayoutsCompressao(self.gerenciador_interface, self.create_button)
        self.compression_method_layouts = self.layouts_compressao.create_compression_method_layouts()
        self.current_layouts = {}
        self.init_menu()
        self.init_ui()
        self.load_compression_method()

    def init_menu(self):
        self.menu_bar = self.menuBar()
        self.config_menu = self.menu_bar.addMenu('Configurações')
        self.compression_method_action = QAction('Selecionar Método de Compressão', self)
        self.compression_method_action.triggered.connect(self.select_compression_method)
        self.config_menu.addAction(self.compression_method_action)
        self.config_menu.aboutToShow.connect(self.select_compression_method)

    def load_compression_method(self):
        config_path = os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.realpath(__file__))), "Config_Method", 'config.json')
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                for compress_type in CompressType:
                    if f'compress_type_{compress_type.value}' in config:
                        self.set_compression_method(config[f'compress_type_{compress_type.value}'], compress_type)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Erro ao carregar o método de compressão: {e}")

    def init_ui(self):
        self.setWindowTitle("Gerenciador de BackUp")
        self.setWindowIcon(QIcon(os.path.join(getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))), "icones", "Manager-BackUp.ico")))

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
        layout.addWidget(self.create_button("Adicionar Pastas", self.gerenciador_interface.browse_folder))
        layout.addWidget(self.create_button("Adicionar Arquivos", self.gerenciador_interface.browse_file))
        layout.addWidget(self.create_button("Testar Integridade", self.gerenciador_interface.testar_integridade, "interrogacao.png"))
        return layout

    def create_second_quadrant(self):
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.addWidget(QLabel("Diretório(s) Pastas e Arquivos:"))
        button_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        button_layout.addWidget(self.create_button("Limpar Entrada", self.gerenciador_interface.clear_folders, "clear_button3.png"))
        button_layout.addWidget(self.create_button("Limpar Todas Saídas", self.gerenciador_interface.clear_output, "clear_button2.png"))
        layout.addLayout(button_layout)
        self.gerenciador_interface.folder_listbox = DragDropListWidget()
        layout.addWidget(self.gerenciador_interface.folder_listbox)
        return layout

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
        self.checkboxes = {method: QCheckBox(method.upper()) for method in methods}
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InterfaceGrafica()
    window.show()
    sys.exit(app.exec())
