import os
import sys
import json
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QCoreApplication
from functools import partial
from enum import Enum
from GerenciamentoUI.ui_02_gerenteGUILayouts import GerenciadorInterface


def get_translated_legends():
    legends_winrar = {
        "0": f"0 - {QCoreApplication.translate('CompressLevels', 'Armazenar')}",
        "1": f"1 - {QCoreApplication.translate('CompressLevels', 'Mais Rápido')}",
        "2": f"2 - {QCoreApplication.translate('CompressLevels', 'Rápido')}",
        "3": f"3 - {QCoreApplication.translate('CompressLevels', 'Normal')}",
        "4": f"4 - {QCoreApplication.translate('CompressLevels', 'Bom')}",
        "5": f"5 - {QCoreApplication.translate('CompressLevels', 'Ótimo')}"
    }

    legends_7zip_zip = {
        "0": f"0 - {QCoreApplication.translate('CompressLevels', 'Armazenar')}",
        "1": f"1 - {QCoreApplication.translate('CompressLevels', 'Mais Rápido')}",
        "3": f"3 - {QCoreApplication.translate('CompressLevels', 'Rápido')}",
        "5": f"5 - {QCoreApplication.translate('CompressLevels', 'Normal')}",
        "7": f"7 - {QCoreApplication.translate('CompressLevels', 'Máximo')}",
        "9": f"9 - {QCoreApplication.translate('CompressLevels', 'Ultra')}"
    }

    legends_bzip2 = {
        "1": f"1 - {QCoreApplication.translate('CompressLevels', 'Mais Rápido')}",
        "3": f"3 - {QCoreApplication.translate('CompressLevels', 'Rápido')}",
        "5": f"5 - {QCoreApplication.translate('CompressLevels', 'Normal')}",
        "7": f"7 - {QCoreApplication.translate('CompressLevels', 'Máximo')}",
        "9": f"9 - {QCoreApplication.translate('CompressLevels', 'Ultra')}"
    }

    legends_tarxz_zipx_tgz_targz_lzh_iso = {
        "0": f"0 - {QCoreApplication.translate('CompressLevels', 'Armazenar')}",
        "1": f"1 - {QCoreApplication.translate('CompressLevels', 'Rápido')}",
        "5": f"5 - {QCoreApplication.translate('CompressLevels', 'Padrão')}",
        "9": f"9 - {QCoreApplication.translate('CompressLevels', 'Máximo')}"
    }

    legends_tar_wim = {
        "0": f"0 - {QCoreApplication.translate('CompressLevels', 'Armazenar')}"
    }
    
    return {
        'winrar': legends_winrar,
        '7z_zip': legends_7zip_zip,
        'bzip2': legends_bzip2,
        'tarxz': legends_tarxz_zipx_tgz_targz_lzh_iso,
        'tar_wim': legends_tar_wim
    }


class CompressType(Enum):
    RAR = 'rar'
    ZIP = 'zip'
    SEVEN_Z = '7z'
    BZIP2 = 'bzip2'
    ZIPX = 'zipx'
    TARXZ = 'tarxz'
    TGZ = 'tgz'
    TARGZ = 'targz'
    LZH = 'lzh'
    ISO = 'iso'
    TAR = 'tar'
    WIM = 'wim'


class MetodoCompressao:
    def __init__(self):
        self.gerenciador_interface = GerenciadorInterface()
        self.config_menu = QMenu()
        self.compression_method_action = QAction()
        self.compression_menu = None
        self.load_compression_method()

    def select_compression_method(self):
        if self.compression_menu and hasattr(self.compression_menu, 'deleteLater'):
            self.compression_menu.deleteLater()

        self.compression_menu = QMenu(self)
        self.compression_menu.setStyleSheet(self.config_menu.styleSheet())

        legends = get_translated_legends()

        self.add_submenu(self.compression_menu, 'RAR (0-5)', legends['winrar'], CompressType.RAR)
        self.add_submenu(self.compression_menu, 'ZIP (0-9)', legends['7z_zip'], CompressType.ZIP)
        self.add_submenu(self.compression_menu, '7Z (0-9)', legends['7z_zip'], CompressType.SEVEN_Z)
        self.add_submenu(self.compression_menu, 'Tar.BZ2 (1-9)', legends['bzip2'], CompressType.BZIP2)
        self.add_submenu(self.compression_menu, 'ZIPX (0-9)', legends['tarxz'], CompressType.ZIPX)
        self.add_submenu(self.compression_menu, 'Tar.XZ (0-9)', legends['tarxz'], CompressType.TARXZ)
        self.add_submenu(self.compression_menu, 'TGZ (0-9)', legends['tarxz'], CompressType.TGZ)
        self.add_submenu(self.compression_menu, 'Tar.GZ (0-9)', legends['tarxz'], CompressType.TARGZ)
        self.add_submenu(self.compression_menu, 'LZH (0-9)', legends['tarxz'], CompressType.LZH)
        self.add_submenu(self.compression_menu, 'ISO (0-9)', legends['tarxz'], CompressType.ISO)
        self.add_submenu(self.compression_menu, 'TAR (0)', legends['tar_wim'], CompressType.TAR)
        self.add_submenu(self.compression_menu, 'WIM (0)', legends['tar_wim'], CompressType.WIM)

        self.compression_method_action.setMenu(self.compression_menu)

    def add_submenu(self, parent_menu, title, legends, compress_type):
        submenu = QMenu(title, self)
        submenu.setStyleSheet(self.config_menu.styleSheet())
        for method, legend in legends.items():
            action = QAction(legend, self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type=compress_type))
            submenu.addAction(action)

        parent_menu.addMenu(submenu)

    def set_compression_method(self, method, compress_type):
        try:
            config_path = self.get_config_path()
            setattr(self.gerenciador_interface, f'compression_method_{compress_type.value}', method)
            self.save_compression_method(config_path)

        except Exception as e:
            print(f"Erro ao definir o método de compressão: {e}")

    def load_compression_method(self):
        config_path = self.get_config_path()
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

    def save_compression_method(self, config_path):
        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            config = {f'compress_type_{compress_type.value}': getattr(self.gerenciador_interface, f'compression_method_{compress_type.value}') for compress_type in CompressType}
            with open(config_path, 'w') as f:
                json.dump(config, f)

        except Exception as e:
            print(f"Erro ao salvar o método de compressão: {e}")

    def get_config_path(self):
        config_method = getattr(sys, '_MEIPASS', os.path.dirname(os.path.realpath(__file__)))
        config_path = os.path.join(config_method, "Config_Method")
        return os.path.join(config_path, 'config.json')
