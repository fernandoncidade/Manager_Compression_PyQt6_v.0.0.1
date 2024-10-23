import os
import sys
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QListWidget, QPushButton, QScrollArea,
                             QWidget, QLabel, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction, QFont
from v002_2_gerente_GUI_layouts import GerenciadorInterface
from v002_3_metodos_compressao import MetodoCompressao


class InterfaceGrafica(QMainWindow, MetodoCompressao):
    def __init__(self):
        super(InterfaceGrafica, self).__init__()
        self.gerenciador_interface = GerenciadorInterface(self)

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
                self.set_compression_method(config['compress_type_tar'], 'tar')
                self.set_compression_method(config['compress_type_gzip'], 'gz')
                self.set_compression_method(config['compress_type_bzip2'], 'bz2')
                self.set_compression_method(config['compress_type_xz'], 'xz')
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
        folder_button.clicked.connect(lambda: self.gerenciador_interface.browse_folder(self))
        primeiro_quadrante_layout.addWidget(folder_button)

        file_button = self.create_button("Adicionar Arquivos")
        file_button.clicked.connect(lambda: self.gerenciador_interface.browse_file(self))
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
            'rar': self.create_rar_layout,
            'zip': self.create_zip_layout,
            '7z': self.create_7z_layout,
            'gz': self.create_gzip_layout,
            'bz2': self.create_bzip2_layout,
            'xz': self.create_xz_layout,
            'tar': self.create_tar_layout,
            'wim': self.create_wim_layout,
            'extração': self.create_extract_layout
        }

        self.current_layouts = {}

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setMinimumSize(600, 300)

        self.method_layouts_container = QVBoxLayout()
        self.scroll_area_layout.addLayout(self.method_layouts_container)

        main_layout = QVBoxLayout()

        main_layout_1_widget = QWidget(self)
        main_layout_2_widget = QWidget(self)
        main_layout_1_widget.setLayout(main_layout_1)
        main_layout_1_widget.setMaximumHeight(185)
        main_layout_2_widget.setLayout(main_layout_2)
        
        main_layout.addWidget(main_layout_1_widget)
        main_layout.addWidget(main_layout_2_widget)
        main_layout.addWidget(self.scroll_area)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_button(self, text):
        button = QPushButton(text)
        button.setMinimumWidth(22 * button.fontMetrics().horizontalAdvance('m'))
        button.setMaximumWidth(22 * button.fontMetrics().horizontalAdvance('m'))
        button.setFont(QFont('Arial', 9))
        return button

    def create_method_checkboxes(self, layout):
        checkbox_layout = QHBoxLayout()

        methods = ['rar', 'zip', '7z', 'gz', 'bz2', 'xz', 'tar', 'wim', 'extração']
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

    def remove_layout_widgets(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.remove_layout_widgets(item.layout())

    def create_rar_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_rar = self.create_button("Especificar Diretório(s) de Saída .RAR")
        output_button_output_rar.clicked.connect(self.gerenciador_interface.output_button_output_RAR_clicked)
        layout_1.addWidget(output_button_output_rar)

        create_rar_button = self.create_button("Armazenar como .RAR")
        rar_icon_path = os.path.join(icon_path, "winrar3.png")
        create_rar_button.setIcon(QIcon(rar_icon_path))
        create_rar_button.clicked.connect(self.gerenciador_interface.store_as_rar)
        layout_1.addWidget(create_rar_button)

        create_clear_rar_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_rar_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_rar_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_rar)
        layout_1.addWidget(create_clear_rar_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_rar = QLabel("Diretório(s) de saída .RAR:")
        layout_2.addWidget(output_label_rar)
        self.gerenciador_interface.output_listbox_rar = QListWidget()
        self.gerenciador_interface.output_listbox_rar.setMinimumHeight(95)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_rar)
        layout.addLayout(layout_2)

        return layout

    def create_zip_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_zip = self.create_button("Especificar Diretório(s) de Saída .ZIP")
        output_button_output_zip.clicked.connect(self.gerenciador_interface.output_button_output_ZIP_clicked)
        layout_1.addWidget(output_button_output_zip)

        create_zip_button = self.create_button("Armazenar como .ZIP")
        zip_icon_path = os.path.join(icon_path, "winzip4.png")
        create_zip_button.setIcon(QIcon(zip_icon_path))
        create_zip_button.clicked.connect(self.gerenciador_interface.store_as_zip)
        layout_1.addWidget(create_zip_button)

        create_clear_zip_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_zip_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_zip_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_zip)
        layout_1.addWidget(create_clear_zip_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_zip = QLabel("Diretório(s) de saída .ZIP:")
        layout_2.addWidget(output_label_zip)
        self.gerenciador_interface.output_listbox_zip = QListWidget()
        self.gerenciador_interface.output_listbox_zip.setMinimumHeight(95)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_zip)
        layout.addLayout(layout_2)

        return layout

    def create_7z_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_7z = self.create_button("Especificar Diretório(s) de Saída .7Z")
        output_button_output_7z.clicked.connect(self.gerenciador_interface.output_button_output_7Z_clicked)
        layout_1.addWidget(output_button_output_7z)

        create_7z_button = self.create_button("Armazenar como .7Z")
        sevenzip_icon_path = os.path.join(icon_path, "sevenzip4.png")
        create_7z_button.setIcon(QIcon(sevenzip_icon_path))
        create_7z_button.clicked.connect(self.gerenciador_interface.store_as_7z)
        layout_1.addWidget(create_7z_button)

        create_clear_7z_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_7z_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_7z_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_7z)
        layout_1.addWidget(create_clear_7z_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_7z = QLabel("Diretório(s) de saída .7Z:")
        layout_2.addWidget(output_label_7z)
        self.gerenciador_interface.output_listbox_7z = QListWidget()
        self.gerenciador_interface.output_listbox_7z.setMinimumHeight(95)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_7z)
        layout.addLayout(layout_2)

        return layout

    def create_tar_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_tar = self.create_button("Especificar Diretório(s) de Saída .TAR")
        output_button_output_tar.clicked.connect(self.gerenciador_interface.output_button_output_TAR_clicked)
        layout_1.addWidget(output_button_output_tar)

        create_tar_button = self.create_button("Armazenar como .TAR")
        tar_icon_path = os.path.join(icon_path, "tar1.png")
        create_tar_button.setIcon(QIcon(tar_icon_path))
        create_tar_button.clicked.connect(self.gerenciador_interface.store_as_tar)
        layout_1.addWidget(create_tar_button)

        create_clear_tar_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_tar_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_tar_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_tar)
        layout_1.addWidget(create_clear_tar_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_tar = QLabel("Diretório(s) de saída .TAR:")
        layout_2.addWidget(output_label_tar)
        self.gerenciador_interface.output_listbox_tar = QListWidget()
        self.gerenciador_interface.output_listbox_tar.setMinimumHeight(95)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_tar)
        layout.addLayout(layout_2)

        return layout

    def create_gzip_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_gzip = self.create_button("Especificar Diretório(s) de Saída .GZ")
        output_button_output_gzip.clicked.connect(self.gerenciador_interface.output_button_output_GZIP_clicked)
        layout_1.addWidget(output_button_output_gzip)

        create_gzip_button = self.create_button("Armazenar como .GZ")
        gzip_icon_path = os.path.join(icon_path, "gzip1.png")
        create_gzip_button.setIcon(QIcon(gzip_icon_path))
        create_gzip_button.clicked.connect(self.gerenciador_interface.store_as_gzip)
        layout_1.addWidget(create_gzip_button)

        create_clear_gzip_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_gzip_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_gzip_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_gzip)
        layout_1.addWidget(create_clear_gzip_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_gzip = QLabel("Diretório(s) de saída .GZ:")
        layout_2.addWidget(output_label_gzip)
        self.gerenciador_interface.output_listbox_gzip = QListWidget()
        self.gerenciador_interface.output_listbox_gzip.setMinimumHeight(95)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_gzip)
        layout.addLayout(layout_2)

        return layout

    def create_bzip2_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_bzip2 = self.create_button("Especificar Diretório(s) de Saída .BZ2")
        output_button_output_bzip2.clicked.connect(self.gerenciador_interface.output_button_output_BZIP2_clicked)
        layout_1.addWidget(output_button_output_bzip2)

        create_bzip2_button = self.create_button("Armazenar como .BZ2")
        bzip2_icon_path = os.path.join(icon_path, "bz2.png")
        create_bzip2_button.setIcon(QIcon(bzip2_icon_path))
        create_bzip2_button.clicked.connect(self.gerenciador_interface.store_as_bzip2)
        layout_1.addWidget(create_bzip2_button)

        create_clear_bzip2_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_bzip2_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_bzip2_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_bzip2)
        layout_1.addWidget(create_clear_bzip2_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_bzip2 = QLabel("Diretório(s) de saída .BZ2:")
        layout_2.addWidget(output_label_bzip2)
        self.gerenciador_interface.output_listbox_bzip2 = QListWidget()
        self.gerenciador_interface.output_listbox_bzip2.setMinimumHeight(95)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_bzip2)
        layout.addLayout(layout_2)

        return layout

    def create_xz_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_xz = self.create_button("Especificar Diretório(s) de Saída .XZ")
        output_button_output_xz.clicked.connect(self.gerenciador_interface.output_button_output_XZ_clicked)
        layout_1.addWidget(output_button_output_xz)

        create_xz_button = self.create_button("Armazenar como .XZ")
        xz_icon_path = os.path.join(icon_path, "xz.png")
        create_xz_button.setIcon(QIcon(xz_icon_path))
        create_xz_button.clicked.connect(self.gerenciador_interface.store_as_xz)
        layout_1.addWidget(create_xz_button)

        create_clear_xz_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_xz_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_xz_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_xz)
        layout_1.addWidget(create_clear_xz_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_xz = QLabel("Diretório(s) de saída .XZ:")
        layout_2.addWidget(output_label_xz)
        self.gerenciador_interface.output_listbox_xz = QListWidget()
        self.gerenciador_interface.output_listbox_xz.setMinimumHeight(95)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_xz)
        layout.addLayout(layout_2)

        return layout

    def create_wim_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_wim = self.create_button("Especificar Diretório(s) de Saída .WIM")
        output_button_output_wim.clicked.connect(self.gerenciador_interface.output_button_output_WIM_clicked)
        layout_1.addWidget(output_button_output_wim)

        create_wim_button = self.create_button("Armazenar como .WIM")
        wim_icon_path = os.path.join(icon_path, "wim.png")
        create_wim_button.setIcon(QIcon(wim_icon_path))
        create_wim_button.clicked.connect(self.gerenciador_interface.store_as_wim)
        layout_1.addWidget(create_wim_button)

        create_clear_wim_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_wim_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_wim_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_wim)
        layout_1.addWidget(create_clear_wim_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_wim = QLabel("Diretório(s) de saída .WIM:")
        layout_2.addWidget(output_label_wim)
        self.gerenciador_interface.output_listbox_wim = QListWidget()
        self.gerenciador_interface.output_listbox_wim.setMinimumHeight(95)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_wim)
        layout.addLayout(layout_2)

        return layout

    def create_extract_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_extract = self.create_button("Especificar Diretório(s) de Extração")
        output_button_output_extract.clicked.connect(self.gerenciador_interface.output_button_output_EXTRACT_clicked)
        layout_1.addWidget(output_button_output_extract)

        extract_button = self.create_button("Extrair Arquivos e Pastas")
        extracao_icon_path = os.path.join(icon_path, "extracao4.png")
        extract_button.setIcon(QIcon(extracao_icon_path))
        extract_button.clicked.connect(self.gerenciador_interface.extract_files)
        layout_1.addWidget(extract_button)

        create_clear_extract_button = self.create_button("Limpar Saída de EXTRAÇÃO")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_extract_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_extract_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_extract)
        layout_1.addWidget(create_clear_extract_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_extract = QLabel("Diretório(s) para Extração:")
        layout_2.addWidget(output_label_extract)
        self.gerenciador_interface.output_listbox_extract = QListWidget()
        self.gerenciador_interface.output_listbox_extract.setMinimumHeight(95)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_extract)
        layout.addLayout(layout_2)

        return layout


def main():
    app = QApplication(sys.argv)
    window = InterfaceGrafica()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
