import os
import sys
import json
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from functools import partial
from v002_2_gerente_GUI_layouts import GerenciadorInterface


class MetodoCompressao:
    def __init__(self):
        self.gerenciador_interface = GerenciadorInterface(self)
        self.load_compression_method()

    def select_compression_method(self):
        legends_winrar = {
            "0": "0 - Armazenar",
            "1": "1 - Mais Rápido",
            "2": "2 - Rápido",
            "3": "3 - Normal",
            "4": "4 - Bom",
            "5": "5 - Ótimo"
        }
        legends_7zip_gzip_zip = {
            "0": "0 - Armazenar",
            "1": "1 - Mais Rápido",
            "3": "3 - Rápido",
            "5": "5 - Normal",
            "7": "7 - Máximo",
            "9": "9 - Ultra"
        }
        legends_bzip2_xz = {
            "1": "1 - Mais Rápido",
            "3": "3 - Rápido",
            "5": "5 - Normal",
            "7": "7 - Máximo",
            "9": "9 - Ultra"
        }
        legends_tar_wim = {
            "0": "0 - Armazenar"
        }

        compression_menu = QMenu(self)
        compression_menu.setStyleSheet(self.config_menu.styleSheet())	

        rar_submenu = QMenu('RAR (0-5)', self)
        rar_submenu.setStyleSheet(self.config_menu.styleSheet())
        rar_methods = ["0", "1", "2", "3", "4", "5"]

        zip_submenu = QMenu('ZIP (0-9)', self)
        zip_submenu.setStyleSheet(self.config_menu.styleSheet())
        zip_methods = ["0", "1", "3", "5", "7", "9"]

        seven_submenu = QMenu('7Z (0-9)', self)
        seven_submenu.setStyleSheet(self.config_menu.styleSheet())
        seven_methods = ["0", "1", "3", "5", "7", "9"]

        gzip_submenu = QMenu('GZip (0-9)', self)
        gzip_submenu.setStyleSheet(self.config_menu.styleSheet())
        gzip_methods = ["0", "1", "3", "5", "7", "9"]

        bzip2_submenu = QMenu('BZip2 (1-9)', self)
        bzip2_submenu.setStyleSheet(self.config_menu.styleSheet())
        bzip2_methods = ["1", "3", "5", "7", "9"]

        xz_submenu = QMenu('XZ (1-9)', self)
        xz_submenu.setStyleSheet(self.config_menu.styleSheet())
        xz_methods = ["1", "3", "5", "7", "9"]

        tar_submenu = QMenu('TAR (0)', self)
        tar_submenu.setStyleSheet(self.config_menu.styleSheet())
        tar_methods = ["0"]

        wim_submenu = QMenu('WIM (0)', self)
        wim_submenu.setStyleSheet(self.config_menu.styleSheet())
        wim_methods = ["0"]
        
        for method in rar_methods:
            action = QAction(legends_winrar[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='rar'))
            rar_submenu.addAction(action)
        compression_menu.addMenu(rar_submenu)
        
        for method in zip_methods:
            action = QAction(legends_7zip_gzip_zip[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='zip'))
            zip_submenu.addAction(action)
        compression_menu.addMenu(zip_submenu)

        for method in seven_methods:
            action = QAction(legends_7zip_gzip_zip[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='7z'))
            seven_submenu.addAction(action)
        compression_menu.addMenu(seven_submenu)

        for method in gzip_methods:
            action = QAction(legends_7zip_gzip_zip[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='gz'))
            gzip_submenu.addAction(action)
        compression_menu.addMenu(gzip_submenu)

        for method in bzip2_methods:
            action = QAction(legends_bzip2_xz[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='bz2'))
            bzip2_submenu.addAction(action)
        compression_menu.addMenu(bzip2_submenu)

        for method in xz_methods:
            action = QAction(legends_bzip2_xz[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='xz'))
            xz_submenu.addAction(action)
        compression_menu.addMenu(xz_submenu)

        for method in tar_methods:
            action = QAction(legends_tar_wim[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='tar'))
            tar_submenu.addAction(action)
        compression_menu.addMenu(tar_submenu)

        for method in wim_methods:
            action = QAction(legends_tar_wim[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='wim'))
            wim_submenu.addAction(action)
        compression_menu.addMenu(wim_submenu)

        self.compression_method_action.setMenu(compression_menu)

    def set_compression_method(self, method, compress_type):
        config_method = getattr(sys, '_MEIPASS', os.path.dirname(os.path.realpath(__file__)))
        config_path = os.path.join(config_method, "Config_Method")
        caminho_metodo = os.path.join(config_path, 'config.json')

        if compress_type == 'rar':
            self.gerenciador_interface.compression_method_rar = method
        elif compress_type == 'zip':
            self.gerenciador_interface.compression_method_zip = method
        elif compress_type == '7z':
            self.gerenciador_interface.compression_method_7z = method
        elif compress_type == 'tar':
            self.gerenciador_interface.compression_method_tar = method
        elif compress_type == 'gz':
            self.gerenciador_interface.compression_method_gzip = method
        elif compress_type == 'bz2':
            self.gerenciador_interface.compression_method_bzip2 = method
        elif compress_type == 'xz':
            self.gerenciador_interface.compression_method_xz = method
        elif compress_type == 'wim':
            self.gerenciador_interface.compression_method_wim = method

        os.makedirs(os.path.dirname(caminho_metodo), exist_ok=True)

        with open(caminho_metodo, 'w') as f:
            json.dump({
                'compress_type_rar': self.gerenciador_interface.compression_method_rar,
                'compress_type_zip': self.gerenciador_interface.compression_method_zip,
                'compress_type_7z': self.gerenciador_interface.compression_method_7z,
                'compress_type_tar': self.gerenciador_interface.compression_method_tar,
                'compress_type_gzip': self.gerenciador_interface.compression_method_gzip,
                'compress_type_bzip2': self.gerenciador_interface.compression_method_bzip2,
                'compress_type_xz': self.gerenciador_interface.compression_method_xz,
                'compress_type_wim': self.gerenciador_interface.compression_method_wim
            }, f)

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
