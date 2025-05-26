import os
import sys
import json
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from functools import partial
from enum import Enum
from GerenciamentoUI.ui_02_gerenteGUILayouts import GerenciadorInterface


LEGENDS_WINRAR = {
    "0": "0 - Armazenar",
    "1": "1 - Mais Rápido",
    "2": "2 - Rápido",
    "3": "3 - Normal",
    "4": "4 - Bom",
    "5": "5 - Ótimo"
}
LEGENDS_7ZIP_ZIP = {
    "0": "0 - Armazenar",
    "1": "1 - Mais Rápido",
    "3": "3 - Rápido",
    "5": "5 - Normal",
    "7": "7 - Máximo",
    "9": "9 - Ultra"
}
LEGENDS_BZIP2 = {
    "1": "1 - Mais Rápido",
    "3": "3 - Rápido",
    "5": "5 - Normal",
    "7": "7 - Máximo",
    "9": "9 - Ultra"
}
LEGENDS_TARXZ_ZIPX_TGZ_TARGZ_LZH_ISO = {
    "0": "0 - Armazenar",
    "1": "1 - Rápido",
    "5": "5 - Padrão",
    "9": "9 - Máximo"
}
LEGENDS_TAR_WIM = {
    "0": "0 - Armazenar"
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
        self.load_compression_method()

    def select_compression_method(self):
        compression_menu = QMenu(self)
        compression_menu.setStyleSheet(self.config_menu.styleSheet())

        self.add_submenu(compression_menu, 'RAR (0-5)', LEGENDS_WINRAR, CompressType.RAR)
        self.add_submenu(compression_menu, 'ZIP (0-9)', LEGENDS_7ZIP_ZIP, CompressType.ZIP)
        self.add_submenu(compression_menu, '7Z (0-9)', LEGENDS_7ZIP_ZIP, CompressType.SEVEN_Z)
        self.add_submenu(compression_menu, 'Tar.BZ2 (1-9)', LEGENDS_BZIP2, CompressType.BZIP2)
        self.add_submenu(compression_menu, 'ZIPX (0-9)', LEGENDS_TARXZ_ZIPX_TGZ_TARGZ_LZH_ISO, CompressType.ZIPX)
        self.add_submenu(compression_menu, 'Tar.XZ (0-9)', LEGENDS_TARXZ_ZIPX_TGZ_TARGZ_LZH_ISO, CompressType.TARXZ)
        self.add_submenu(compression_menu, 'TGZ (0-9)', LEGENDS_TARXZ_ZIPX_TGZ_TARGZ_LZH_ISO, CompressType.TGZ)
        self.add_submenu(compression_menu, 'Tar.GZ (0-9)', LEGENDS_TARXZ_ZIPX_TGZ_TARGZ_LZH_ISO, CompressType.TARGZ)
        self.add_submenu(compression_menu, 'LZH (0-9)', LEGENDS_TARXZ_ZIPX_TGZ_TARGZ_LZH_ISO, CompressType.LZH)
        self.add_submenu(compression_menu, 'ISO (0-9)', LEGENDS_TARXZ_ZIPX_TGZ_TARGZ_LZH_ISO, CompressType.ISO)
        self.add_submenu(compression_menu, 'TAR (0)', LEGENDS_TAR_WIM, CompressType.TAR)
        self.add_submenu(compression_menu, 'WIM (0)', LEGENDS_TAR_WIM, CompressType.WIM)

        self.compression_method_action.setMenu(compression_menu)

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
