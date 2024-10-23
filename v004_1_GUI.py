import os
import sys
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QListWidget, QPushButton, QScrollArea,
                             QWidget, QLabel, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction, QFont
from v004_2_layouts_compressao import LayoutsCompressao
from v004_3_gerente_GUI_layouts import GerenciadorInterface
from v004_4_metodos_compressao import MetodoCompressao


class InterfaceGrafica(QMainWindow, MetodoCompressao):
    def __init__(self):
        super(InterfaceGrafica, self).__init__()
        self.gerenciador_interface = GerenciadorInterface(self)
        self.layouts_compressao = LayoutsCompressao(self.gerenciador_interface, self.create_button)

        self.menu_bar = self.menuBar()

        self.config_menu = self.menu_bar.addMenu('Configurações')
        
        self.compression_method_action = QAction('Selecionar Método de Compressão', self)
        self.compression_method_action.triggered.connect(self.select_compression_method)
        self.config_menu.addAction(self.compression_method_action)
        self.config_menu.aboutToShow.connect(self.select_compression_method)

        self.init_ui()
        self.load_compression_method()

    def load_compression_method(self):
        config_method = getattr(sys, '_MEIPASS', os.path.dirname(os.path.realpath(__file__)))
        config_path = os.path.join(config_method, "Config_Method")
        caminho_metodo = os.path.join(config_path, 'config.json')

        try:
            with open(caminho_metodo, 'r') as f:
                config = json.load(f)
                self.set_compression_method(config['compress_type_rar'], 'rar')
                self.set_compression_method(config['compress_type_zip'], 'zip')
                self.set_compression_method(config['compress_type_7z'], '7z')
                self.set_compression_method(config['compress_type_bzip2'], 'tar.bz2')
                self.set_compression_method(config['compress_type_zipx'], 'zipx')
                self.set_compression_method(config['compress_type_tarxz'], 'tar.xz')
                self.set_compression_method(config['compress_type_tgz'], 'tgz')
                self.set_compression_method(config['compress_type_targz'], 'tar.gz')
                self.set_compression_method(config['compress_type_lzh'], 'lzh')
                self.set_compression_method(config['compress_type_iso'], 'iso')
                self.set_compression_method(config['compress_type_tar'], 'tar')
                self.set_compression_method(config['compress_type_wim'], 'wim')

        except FileNotFoundError:
            pass

    def init_ui(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")
        self.setWindowTitle("Gerenciador de BackUp")
        icon_title_path = os.path.join(icon_path, "Manager-BackUp.ico")
        self.setWindowIcon(QIcon(icon_title_path))

        # Primeiro Layout Horizontal
        main_layout_1 = QHBoxLayout()

        # Primeiro Quadrante
        primeiro_quadrante_layout = QVBoxLayout()

        folder_button = self.create_button("Adicionar Pastas")
        folder_button.clicked.connect(lambda: self.gerenciador_interface.browse_folder())
        primeiro_quadrante_layout.addWidget(folder_button)

        file_button = self.create_button("Adicionar Arquivos")
        file_button.clicked.connect(lambda: self.gerenciador_interface.browse_file())
        primeiro_quadrante_layout.addWidget(file_button)

        test_button = self.create_button("Testar Integridade")
        test_icon_path = os.path.join(icon_path, "interrogacao.png")
        test_button.setIcon(QIcon(test_icon_path))
        test_button.clicked.connect(self.gerenciador_interface.testar_integridade)
        primeiro_quadrante_layout.addWidget(test_button)

        main_layout_1.addLayout(primeiro_quadrante_layout)
        main_layout_1.setAlignment(primeiro_quadrante_layout, Qt.AlignmentFlag.AlignBottom)

        # Segundo Quadrante
        segundo_quadrante_layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        clear_button_folders = self.create_button("Limpar Entrada")
        limpar_folders_icon_path = os.path.join(icon_path, "clear_button3.png")
        clear_button_folders.setIcon(QIcon(limpar_folders_icon_path))
        clear_button_folders.clicked.connect(self.gerenciador_interface.clear_folders)
        button_layout.addWidget(clear_button_folders)
        button_layout.setAlignment(clear_button_folders ,Qt.AlignmentFlag.AlignLeft)

        clear_button_output = self.create_button("Limpar Todas Saídas")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        clear_button_output.setIcon(QIcon(limpar_output_icon_path))
        clear_button_output.clicked.connect(self.gerenciador_interface.clear_output)
        button_layout.addWidget(clear_button_output)
        button_layout.setAlignment(clear_button_output, Qt.AlignmentFlag.AlignRight)

        segundo_quadrante_layout.addLayout(button_layout)

        folder_label = QLabel("Diretório(s) Pastas e Arquivos:")
        segundo_quadrante_layout.addWidget(folder_label)
        self.gerenciador_interface.folder_listbox = QListWidget()
        segundo_quadrante_layout.addWidget(self.gerenciador_interface.folder_listbox)

        main_layout_1.addLayout(segundo_quadrante_layout)
        main_layout_1.setAlignment(segundo_quadrante_layout, Qt.AlignmentFlag.AlignTop)

        # Segundo Layout Horizontal
        main_layout_2 = QHBoxLayout()

        # Terceiro Quadrante
        terceiro_quadrante_layout = QVBoxLayout()

        main_layout_2.addLayout(terceiro_quadrante_layout)
        main_layout_2.setAlignment(terceiro_quadrante_layout, Qt.AlignmentFlag.AlignRight)
        self.create_method_checkboxes(terceiro_quadrante_layout)

        self.compression_method_layouts = {
            'rar': self.layouts_compressao.create_rar_layout,
            'zip': self.layouts_compressao.create_zip_layout,
            '7z': self.layouts_compressao.create_7z_layout,
            'tar.bz2': self.layouts_compressao.create_bzip2_layout,
            'zipx': self.layouts_compressao.create_zipx_layout,
            'tar.xz': self.layouts_compressao.create_tarxz_layout,
            'tgz': self.layouts_compressao.create_tgz_layout,
            'tar.gz': self.layouts_compressao.create_targz_layout,
            'lzh': self.layouts_compressao.create_lzh_layout,
            'iso': self.layouts_compressao.create_iso_layout,
            'tar': self.layouts_compressao.create_tar_layout,
            'wim': self.layouts_compressao.create_wim_layout,
            'extração': self.layouts_compressao.create_extract_layout
        }

        self.current_layouts = {}

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setMinimumSize(600, 347)

        self.method_layouts_container = QVBoxLayout()
        self.scroll_area_layout.addLayout(self.method_layouts_container)

        main_layout = QVBoxLayout()

        self.main_layout_1_widget = QWidget(self)
        main_layout_2_widget = QWidget(self)
        self.main_layout_1_widget.setLayout(main_layout_1)
        self.main_layout_1_widget.setMinimumHeight(152)
        self.main_layout_1_widget.setMaximumHeight(304)
        main_layout_2_widget.setLayout(main_layout_2)
        
        main_layout.addWidget(self.main_layout_1_widget)
        main_layout.addWidget(main_layout_2_widget)
        main_layout.addWidget(self.scroll_area)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_button(self, text):
        button = QPushButton(text)
        button.setMinimumWidth(24 * button.fontMetrics().horizontalAdvance('m'))
        button.setMaximumWidth(24 * button.fontMetrics().horizontalAdvance('m'))
        button.setFont(QFont('Arial', 9))
        return button

    def create_method_checkboxes(self, layout):
        checkbox_layout = QHBoxLayout()

        methods = ['rar', 'zip', '7z', 'tar.bz2', 'zipx', 'tar.xz', 'tgz', 'tar.gz', 'lzh', 'iso', 'tar', 'wim', 'extração']
        self.checkboxes = {}

        for method in methods:
            checkbox = QCheckBox(method.upper())
            checkbox.method = method
            checkbox.toggled.connect(self.on_method_toggled)
            self.checkboxes[method] = checkbox
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
