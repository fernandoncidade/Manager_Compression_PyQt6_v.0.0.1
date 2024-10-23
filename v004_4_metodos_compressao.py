import os
import sys
import json
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from functools import partial
from v004_3_gerente_GUI_layouts import GerenciadorInterface


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
        legends_7zip_zip = {
            "0": "0 - Armazenar",
            "1": "1 - Mais Rápido",
            "3": "3 - Rápido",
            "5": "5 - Normal",
            "7": "7 - Máximo",
            "9": "9 - Ultra"
        }
        legends_bzip2 = {
            "1": "1 - Mais Rápido",
            "3": "3 - Rápido",
            "5": "5 - Normal",
            "7": "7 - Máximo",
            "9": "9 - Ultra"
        }
        legends_tarxz_zipx_tgz_targz_lzh_iso = {
            "0": "0 - Armazenar",
            "1": "1 - Rápido",
            "5": "5 - Padrão",
            "9": "9 - Máximo"
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

        bzip2_submenu = QMenu('BZip2 (1-9)', self)
        bzip2_submenu.setStyleSheet(self.config_menu.styleSheet())
        bzip2_methods = ["1", "3", "5", "7", "9"]

        zipx_submenu = QMenu('ZIPX (0-9)', self)
        zipx_submenu.setStyleSheet(self.config_menu.styleSheet())
        zipx_methods = ["0", "1", "5", "9"]

        txz_submenu = QMenu('Tar.XZ (0-9)', self)
        txz_submenu.setStyleSheet(self.config_menu.styleSheet())
        txz_methods = ["0", "1", "5", "9"]

        tgz_submenu = QMenu('TGZ (0-9)', self)
        tgz_submenu.setStyleSheet(self.config_menu.styleSheet())
        tgz_methods = ["0", "1", "5", "9"]

        targz_submenu = QMenu('Tar.GZ (0-9)', self)
        targz_submenu.setStyleSheet(self.config_menu.styleSheet())
        targz_methods = ["0", "1", "5", "9"]

        lzh_submenu = QMenu('LZH (0-9)', self)
        lzh_submenu.setStyleSheet(self.config_menu.styleSheet())
        lzh_methods = ["0", "1", "5", "9"]

        iso_submenu = QMenu('ISO (0-9)', self)
        iso_submenu.setStyleSheet(self.config_menu.styleSheet())
        iso_methods = ["0", "1", "5", "9"]

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
            action = QAction(legends_7zip_zip[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='zip'))
            zip_submenu.addAction(action)
        compression_menu.addMenu(zip_submenu)

        for method in seven_methods:
            action = QAction(legends_7zip_zip[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='7z'))
            seven_submenu.addAction(action)
        compression_menu.addMenu(seven_submenu)

        for method in bzip2_methods:
            action = QAction(legends_bzip2[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='tar.bz2'))
            bzip2_submenu.addAction(action)
        compression_menu.addMenu(bzip2_submenu)

        for method in zipx_methods:
            action = QAction(legends_tarxz_zipx_tgz_targz_lzh_iso[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='zipx'))
            zipx_submenu.addAction(action)
        compression_menu.addMenu(zipx_submenu)

        for method in txz_methods:
            action = QAction(legends_tarxz_zipx_tgz_targz_lzh_iso[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='tar.xz'))
            txz_submenu.addAction(action)
        compression_menu.addMenu(txz_submenu)

        for method in tgz_methods:
            action = QAction(legends_tarxz_zipx_tgz_targz_lzh_iso[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='tgz'))
            tgz_submenu.addAction(action)
        compression_menu.addMenu(tgz_submenu)

        for method in targz_methods:
            action = QAction(legends_tarxz_zipx_tgz_targz_lzh_iso[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='tar.gz'))
            targz_submenu.addAction(action)
        compression_menu.addMenu(targz_submenu)

        for method in lzh_methods:
            action = QAction(legends_tarxz_zipx_tgz_targz_lzh_iso[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='lzh'))
            lzh_submenu.addAction(action)
        compression_menu.addMenu(lzh_submenu)

        for method in iso_methods:
            action = QAction(legends_tarxz_zipx_tgz_targz_lzh_iso[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='iso'))
            iso_submenu.addAction(action)
        compression_menu.addMenu(iso_submenu)

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
        elif compress_type == 'tar.bz2':
            self.gerenciador_interface.compression_method_bzip2 = method
        elif compress_type == 'zipx':
            self.gerenciador_interface.compression_method_zipx = method
        elif compress_type == 'tar.xz':
            self.gerenciador_interface.compression_method_tarxz = method
        elif compress_type == 'tgz':
            self.gerenciador_interface.compression_method_tgz = method
        elif compress_type == 'tar.gz':
            self.gerenciador_interface.compression_method_targz = method
        elif compress_type == 'lzh':
            self.gerenciador_interface.compression_method_lzh = method
        elif compress_type == 'iso':
            self.gerenciador_interface.compression_method_iso = method
        elif compress_type == 'tar':
            self.gerenciador_interface.compression_method_tar = method
        elif compress_type == 'wim':
            self.gerenciador_interface.compression_method_wim = method

        os.makedirs(os.path.dirname(caminho_metodo), exist_ok=True)

        with open(caminho_metodo, 'w') as f:
            json.dump({
                'compress_type_rar': self.gerenciador_interface.compression_method_rar,
                'compress_type_zip': self.gerenciador_interface.compression_method_zip,
                'compress_type_7z': self.gerenciador_interface.compression_method_7z,
                'compress_type_bzip2': self.gerenciador_interface.compression_method_bzip2,
                'compress_type_zipx': self.gerenciador_interface.compression_method_zipx,
                'compress_type_tarxz': self.gerenciador_interface.compression_method_tarxz,
                'compress_type_tgz': self.gerenciador_interface.compression_method_tgz,
                'compress_type_targz': self.gerenciador_interface.compression_method_targz,
                'compress_type_lzh': self.gerenciador_interface.compression_method_lzh,
                'compress_type_iso': self.gerenciador_interface.compression_method_iso,
                'compress_type_tar': self.gerenciador_interface.compression_method_tar,
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
