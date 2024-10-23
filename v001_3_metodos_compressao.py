import os  # Importa o módulo os
import sys  # Importa o módulo sys
import json  # Importa o módulo json
# Importa a classe QMenu do módulo QtWidgets
from PyQt6.QtWidgets import QMenu
# Importa a classe QAction do módulo QtGui
from PyQt6.QtGui import QAction
# Importa a classe partial do módulo functools
from functools import partial
# Importa a classe GerenciadorInterface do módulo ManagerInterface_7Zip
from v001_2_gerente_GUI_layouts import GerenciadorInterface


# Cria a classe MetodoCompressao
class MetodoCompressao:
    # Inicializa a classe
    def __init__(self):
        # Cria o gerenciador de interface
        self.gerenciador_interface = GerenciadorInterface(self)
        # Carrega o método de compressão
        self.load_compression_method()

    # Define um método chamado select_compression_method
    def select_compression_method(self):
        # Dicionário com as legendas para os métodos de compressão
        legends_winrar = {
            "0": "0 - Armazenar",
            "1": "1 - Mais Rápido",
            "2": "2 - Rápido",
            "3": "3 - Normal",
            "4": "4 - Bom",
            "5": "5 - Ótimo"
        }
        # Dicionário com as legendas para os métodos de compressão
        legends_sevenzip = {
            "0": "0 - Armazenar",
            "1": "1 - Mais Rápido",
            "3": "3 - Rápido",
            "5": "5 - Normal",
            "7": "7 - Máximo",
            "9": "9 - Ultra"
        }

        # Cria um menu para selecionar o método de compressão
        compression_menu = QMenu(self)
        compression_menu.setStyleSheet(self.config_menu.styleSheet())	

        # Adicione submenus para cada método de compressão do WinRAR
        rar_submenu = QMenu('RAR (0-5)', self)
        rar_submenu.setStyleSheet(self.config_menu.styleSheet())
        rar_methods = ["0", "1", "2", "3", "4", "5"]

        # Adicione submenus para cada método de compressão do WinRAR
        zip_submenu = QMenu('ZIP (0-9)', self)
        zip_submenu.setStyleSheet(self.config_menu.styleSheet())
        zip_methods = ["0", "1", "3", "5", "7", "9"]

        # Adicione submenus para cada método de compressão do 7-Zip
        seven_submenu = QMenu('7Z (0-9)', self)
        seven_submenu.setStyleSheet(self.config_menu.styleSheet())
        seven_methods = ["0", "1", "3", "5", "7", "9"]

        # Adicione submenus para cada método de compressão do 7-Zip
        tar_submenu = QMenu('TAR (0)', self)
        tar_submenu.setStyleSheet(self.config_menu.styleSheet())
        tar_methods = ["0"]
        
        # Adicione ação para cada método de compressão
        for method in rar_methods:
            # Crie uma ação para o método de compressão
            action = QAction(legends_winrar[method], self)
            # Conecte a ação a um método, passando o método de compressão como argumento
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='rar'))
            # Adicione a ação ao submenu do WinRAR
            rar_submenu.addAction(action)
        # Adicione o submenu do WinRAR ao menu de compressão
        compression_menu.addMenu(rar_submenu)
        
        for method in zip_methods:
            action = QAction(legends_sevenzip[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='zip'))
            zip_submenu.addAction(action)
        compression_menu.addMenu(zip_submenu)

        for method in seven_methods:
            action = QAction(legends_sevenzip[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='7z'))
            seven_submenu.addAction(action)
        compression_menu.addMenu(seven_submenu)

        for method in tar_methods:
            action = QAction(legends_sevenzip[method], self)
            action.triggered.connect(partial(self.set_compression_method, method=method, compress_type='tar'))
            tar_submenu.addAction(action)
        compression_menu.addMenu(tar_submenu)

        # Adicione o menu de compressão como submenu do menu principal
        self.compression_method_action.setMenu(compression_menu)

    # Define um método chamado set_compression_method
    def set_compression_method(self, method, compress_type):
        # Busca o caminho do arquivo de configuração
        config_method = getattr(sys, '_MEIPASS', os.path.dirname(os.path.realpath(__file__)))
        config_path = os.path.join(config_method, "Config_Method")
        caminho_metodo = os.path.join(config_path, 'config.json')

        # Verifica o tipo de compressão
        if compress_type == 'rar':
            # Define o método de compressão para arquivos RAR
            self.gerenciador_interface.compression_method_rar = method
        elif compress_type == 'zip':
            self.gerenciador_interface.compression_method_zip = method
        elif compress_type == '7z':
            self.gerenciador_interface.compression_method_7z = method
        elif compress_type == 'tar':
            self.gerenciador_interface.compression_method_tar = method

        # Cria o diretório para o arquivo de configuração
        os.makedirs(os.path.dirname(caminho_metodo), exist_ok=True)

        # Salva o método de compressão no arquivo de configuração
        with open(caminho_metodo, 'w') as f:
            json.dump({
                'compress_type_rar': self.gerenciador_interface.compression_method_rar,
                'compress_type_zip': self.gerenciador_interface.compression_method_zip,
                'compress_type_7z': self.gerenciador_interface.compression_method_7z,
                'compress_type_tar': self.gerenciador_interface.compression_method_tar
            }, f)

    # Define um método chamado load_compression_method
    def load_compression_method(self):
        # Busca o caminho do arquivo de configuração
        config_method = getattr(sys, '_MEIPASS', os.path.dirname(os.path.realpath(__file__)))
        config_path = os.path.join(config_method, "Config_Method")
        caminho_metodo = os.path.join(config_path, 'config.json')

        # Verifica se o arquivo de configuração existe
        try:
            # Carrega o método de compressão do arquivo de configuração
            with open(caminho_metodo, 'r') as f:
                config = json.load(f)
                self.set_compression_method(config['compress_type_rar'], 'rar')
                self.set_compression_method(config['compress_type_zip'], 'zip')
                self.set_compression_method(config['compress_type_7z'], '7z')
                self.set_compression_method(config['compress_type_tar'], 'tar')
                
        # Verifica se o arquivo de configuração não existe
        except FileNotFoundError:
            pass
