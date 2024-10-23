import os  # Importa o módulo os
import sys  # Importa o módulo sys
import json  # Importa o módulo json
# Importa as classes QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, ...
# QFileDialog, QWidget, QTreeView, QMessageBox do módulo QtWidgets
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel,
                             QListWidget, QPushButton, QWidget)
# Importa a classe Qt do módulo QtCore
from PyQt6.QtCore import Qt
# Importa a classe QAction do módulo QtGui
from PyQt6.QtGui import QAction
# Importa a classe QtGui do módulo PyQt6
from PyQt6 import QtGui
# Importa a classe GerenciadorInterface do módulo ManagerInterface_7Zip
from v001_2_gerente_GUI_layouts import GerenciadorInterface
# Importa a classe MetodoCompressao do módulo CompressionMethod
from v001_3_metodos_compressao import MetodoCompressao
# Importa a função apply_neutral_standart_theme_2 do módulo Colors
from v001_5_colors import apply_neutral_standart_theme


# Define uma nova classe chamada InterfaceGrafica que herda de QMainWindow, uma classe do PyQt que representa uma janela.
class InterfaceGrafica(QMainWindow, MetodoCompressao):
    def __init__(self):
        super(InterfaceGrafica, self).__init__()
        # Cria o gerenciador de interface
        self.gerenciador_interface = GerenciadorInterface(self)

        # Cria a barra de menus
        self.menu_bar = self.menuBar()
        if self.menu_bar is None:
            raise Exception("MenuBar não pôde ser criado")

        # Cria a barra de menus
        self.config_menu = self.menu_bar.addMenu('Configurações')
        if self.config_menu is None:
            raise Exception("Menu de Configurações não pôde ser criado")
        
            # Adicionar ação para selecionar método de compressão
        self.compression_method_action = QAction('Selecionar Método de Compressão', self)
            # Conectar a ação a um método
        self.compression_method_action.triggered.connect(self.select_compression_method)
            # Adicionar a ação ao menu
        self.config_menu.addAction(self.compression_method_action)
            # Adiciona evento de entrada e saída para ativar o menu
        self.config_menu.aboutToShow.connect(self.select_compression_method)

        # Chama o método init_ui
        self.init_ui()
        # Chama e carrega o método de compressão
        self.load_compression_method()

    # Define um método chamado load_compression_method
    def load_compression_method(self):
        # Define o caminho do método de configuração
        config_method = getattr(sys, '_MEIPASS', os.path.dirname(os.path.realpath(__file__)))
        config_path = os.path.join(config_method, "Config_Method")
        caminho_metodo = os.path.join(config_path, 'config.json')

        # Tenta abrir o arquivo de configuração
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

    # Define um método chamado init_ui
    def init_ui(self):
        # Esta linha está definindo o caminho base para buscar arquivos.
        # Se o programa estiver sendo executado como um executável PyInstaller, ...
        # o atributo sys._MEIPASS será definido, que é o caminho para os recursos empacotados.
        # Se não estiver sendo executado como um executável, ele usará o diretório do script atual.
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        # Esta linha está definindo o caminho para a pasta "icones", ...
        # que está localizada no mesmo diretório que o script atual ou no diretório de recursos do PyInstaller, ...
        # dependendo de como o programa está sendo executado.
        icon_path = os.path.join(base_path, "icones")

        # Define o título da janela
        self.setWindowTitle("Gerenciador de BackUp")
        # Esta linha está definindo o caminho completo para o arquivo de ícone "Manager-BackUp.ico", que está localizado na pasta "icones".
        icon_title_path = os.path.join(icon_path, "Manager-BackUp.ico")
        # Esta linha está definindo o ícone da janela para o ícone especificado pelo caminho icon_title_path.
        # O método setWindowIcon é um método de um objeto de janela PyQt, e QtGui.QIcon é uma classe que encapsula um ícone.
        self.setWindowIcon(QtGui.QIcon(icon_title_path))

        ### Primeiro layout horizontal ###
        main_layout_1 = QHBoxLayout()  # Cria um novo layout horizontal

        ## Primeiro quadrante (topo esquerdo)
        primeiro_quadrante_layout = QVBoxLayout()  # Cria um novo layout vertical

            # Cria um botão para adicionar pastas
        folder_button = QPushButton("Adicionar Pastas")
            # Conecta o botão a um método (browse_folder) da classe GerenciadorInterface
        folder_button.clicked.connect(lambda: self.gerenciador_interface.browse_folder(self))
            # Adiciona o botão ao layout vertical
        primeiro_quadrante_layout.addWidget(folder_button)
            # Cria um botão para adicionar arquivos
        file_button = QPushButton("Adicionar Arquivos")
            # Conecta o botão a um método (browse_file) da classe GerenciadorInterface
        file_button.clicked.connect(lambda: self.gerenciador_interface.browse_file(self))
            # Adiciona o botão ao layout vertical
        primeiro_quadrante_layout.addWidget(file_button)

            # Cria um botão para limpar a entrada
        output_button_output_EXTRACT = QPushButton("Especificar Diretório(s) de Extração")
            # Conecta o botão a um método (output_button_output_EXTRACT_clicked) da classe GerenciadorInterface
        output_button_output_EXTRACT.clicked.connect(self.gerenciador_interface.output_button_output_EXTRACT_clicked)
            # Adiciona o botão ao layout vertical
        primeiro_quadrante_layout.addWidget(output_button_output_EXTRACT)

            # Cria um botão para extrair arquivos e pastas
        extract_button = QPushButton("Extrair Arquivos e Pastas")
            # Define o caminho completo para o arquivo de ícone "extracao4.png", que está localizado na pasta "icones".
        extracao_icon_path = os.path.join(icon_path, "extracao4.png")
            # Define o ícone do botão para o ícone especificado pelo caminho extracao_icon_path.
        extract_button.setIcon(QtGui.QIcon(extracao_icon_path))
            # Conecta o botão a um método (extract_files) da classe GerenciadorInterface
        extract_button.clicked.connect(self.gerenciador_interface.extract_files)
            # Adiciona o botão ao layout vertical
        primeiro_quadrante_layout.addWidget(extract_button)

            # Cria um botão para testar a integridade dos arquivos
        test_button = QPushButton("Testar Integridade")
            # Define o caminho completo para o arquivo de ícone "teste_integridade2.png", que está localizado na pasta "icones".
        test_icon_path = os.path.join(icon_path, "teste_integridade2.png")
            # Define o ícone do botão para o ícone especificado pelo caminho test_icon_path.
        test_button.setIcon(QtGui.QIcon(test_icon_path))
            # Conecta o botão a um método (testar_integridade) da classe GerenciadorInterface
        test_button.clicked.connect(self.gerenciador_interface.testar_integridade)
            # Adiciona o botão ao layout vertical
        primeiro_quadrante_layout.addWidget(test_button)

            # Adiciona o layout vertical ao layout horizontal
        main_layout_1.addLayout(primeiro_quadrante_layout)
            # Alinha o layout vertical ao fundo do layout horizontal
        main_layout_1.setAlignment(primeiro_quadrante_layout, Qt.AlignmentFlag.AlignBottom)

        ## Segundo quadrante (topo centro)
        segundo_quadrante_layout = QVBoxLayout()  # Cria um novo layout vertical

            # Cria um botão para limpar a entrada
        clear_button_folders = QPushButton("Limpar Entrada")
            # Define o caminho completo para o arquivo de ícone "clear_button3.png", que está localizado na pasta "icones".
        limpar_folders_icon_path = os.path.join(icon_path, "clear_button3.png")
            # Define o ícone do botão para o ícone especificado pelo caminho limpar_folders_icon_path.
        clear_button_folders.setIcon(QtGui.QIcon(limpar_folders_icon_path))
            # Conecta o botão a um método (clear_folders) da classe GerenciadorInterface
        clear_button_folders.clicked.connect(self.gerenciador_interface.clear_folders)
            # Adiciona o botão ao layout vertical
        segundo_quadrante_layout.addWidget(clear_button_folders)

            # Cria um rótulo para o ListBox de pastas e arquivos
        folder_label = QLabel("Diretório(s) Pastas e Arquivos:")
            # Adiciona o rótulo ao layout vertical
        segundo_quadrante_layout.addWidget(folder_label)
            # Cria um novo ListBox para armazenar pastas e arquivos
        self.gerenciador_interface.folder_listbox = QListWidget()
            # Adiciona o ListBox ao layout vertical
        segundo_quadrante_layout.addWidget(self.gerenciador_interface.folder_listbox)
            # Adiciona o layout vertical ao layout horizontal
        main_layout_1.addLayout(segundo_quadrante_layout)

        ## Terceiro quadrante (topo direito)
        terceiro_quadrante_layout = QVBoxLayout()  # Cria um novo layout vertical

            # Cria um botão para limpar a saída
        clear_button_output = QPushButton("Limpar Saídas")
            # Define o caminho completo para o arquivo de ícone "clear_button2.png", que está localizado na pasta "icones".
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
            # Define o ícone do botão para o ícone especificado pelo caminho limpar_output_icon_path.
        clear_button_output.setIcon(QtGui.QIcon(limpar_output_icon_path))
            # Conecta o botão a um método (clear_output) da classe GerenciadorInterface
        clear_button_output.clicked.connect(self.gerenciador_interface.clear_output)
            # Adiciona o botão ao layout vertical
        terceiro_quadrante_layout.addWidget(clear_button_output)

            # Cria um rótulo para o ListBox de pastas de extração
        output_label_extract = QLabel("Diretório(s) para Extração:")
            # Adiciona o rótulo ao layout vertical
        terceiro_quadrante_layout.addWidget(output_label_extract)
            # Cria um novo ListBox para armazenar pastas de extração
        self.gerenciador_interface.output_listbox_extract = QListWidget()
            # Adiciona o ListBox ao layout vertical
        terceiro_quadrante_layout.addWidget(self.gerenciador_interface.output_listbox_extract)
            # Adiciona o layout vertical ao layout horizontal
        main_layout_1.addLayout(terceiro_quadrante_layout)

        ### Segundo layout horizontal ###
        main_layout_2 = QHBoxLayout()

        ## Quarto quadrante (centro esquerdo)
        quarto_quadrante_layout = QVBoxLayout()  # Cria um novo layout vertical

            # Cria um botão para especificar o diretório de saída .RAR
        output_button_output_RAR = QPushButton("Especificar Diretório(s) de Saída .RAR")
            # Conecta o botão a um método (output_button_output_RAR_clicked) da classe GerenciadorInterface
        output_button_output_RAR.clicked.connect(self.gerenciador_interface.output_button_output_RAR_clicked)
            # Adiciona o botão ao layout vertical
        quarto_quadrante_layout.addWidget(output_button_output_RAR)

            # Cria um botão para armazenar como .RAR
        create_rar_button = QPushButton("Armazenar como .RAR")
            # Define o caminho completo para o arquivo de ícone "winrar3.png", que está localizado na pasta "icones".
        rar_icon_path = os.path.join(icon_path, "winrar3.png")
            # Define o ícone do botão para o ícone especificado pelo caminho rar_icon_path.
        create_rar_button.setIcon(QtGui.QIcon(rar_icon_path))
            # Conecta o botão a um método (store_as_rar) da classe GerenciadorInterface
        create_rar_button.clicked.connect(self.gerenciador_interface.store_as_rar)
            # Adiciona o botão ao layout vertical
        quarto_quadrante_layout.addWidget(create_rar_button)

            # Cria um botão para especificar o diretório de saída .ZIP
        output_button_output_ZIP = QPushButton("Especificar Diretório(s) de Saída .ZIP")
            # Conecta o botão a um método (output_button_output_ZIP_clicked) da classe GerenciadorInterface
        output_button_output_ZIP.clicked.connect(self.gerenciador_interface.output_button_output_ZIP_clicked)
            # Adiciona o botão ao layout vertical
        quarto_quadrante_layout.addWidget(output_button_output_ZIP)

            # Cria um botão para armazenar como .ZIP
        create_zip_button = QPushButton("Armazenar como .ZIP")
            # Define o caminho completo para o arquivo de ícone "winzip4.png", que está localizado na pasta "icones".
        zip_icon_path = os.path.join(icon_path, "winzip4.png")
            # Define o ícone do botão para o ícone especificado pelo caminho zip_icon_path.
        create_zip_button.setIcon(QtGui.QIcon(zip_icon_path))
            # Conecta o botão a um método (store_as_zip) da classe GerenciadorInterface
        create_zip_button.clicked.connect(self.gerenciador_interface.store_as_zip)
            # Adiciona o botão ao layout vertical
        quarto_quadrante_layout.addWidget(create_zip_button)

            # Adiciona o layout vertical ao layout horizontal
        main_layout_2.addLayout(quarto_quadrante_layout)
            # Alinha o layout vertical ao fundo do layout horizontal
        main_layout_2.setAlignment(quarto_quadrante_layout, Qt.AlignmentFlag.AlignBottom)

        ## Quinto quadrante (centro centro)
        quinto_quadrante_layout = QVBoxLayout()  # Cria um novo layout vertical

            # Cria um rótulo para o ListBox de pastas de saída .RAR
        output_label_rar = QLabel("Diretório(s) de saída .RAR:")
            # Adiciona o rótulo ao layout vertical
        quinto_quadrante_layout.addWidget(output_label_rar)
            # Cria um novo ListBox para armazenar pastas de saída .RAR
        self.gerenciador_interface.output_listbox_rar = QListWidget()
            # Adiciona o ListBox ao layout vertical
        quinto_quadrante_layout.addWidget(self.gerenciador_interface.output_listbox_rar)
            # Adiciona o layout vertical ao layout horizontal
        main_layout_2.addLayout(quinto_quadrante_layout)

        ## Sexto quadrante (centro direito)
        sexto_quadrante_layout = QVBoxLayout()  # Cria um novo layout vertical

            # Cria um rótulo para o ListBox de pastas de saída .ZIP
        output_label_zip = QLabel("Diretório(s) de saída .ZIP:")
            # Adiciona o rótulo ao layout vertical
        sexto_quadrante_layout.addWidget(output_label_zip)
            # Cria um novo ListBox para armazenar pastas de saída .ZIP
        self.gerenciador_interface.output_listbox_zip = QListWidget()
            # Adiciona o ListBox ao layout vertical
        sexto_quadrante_layout.addWidget(self.gerenciador_interface.output_listbox_zip)
            # Adiciona o layout vertical ao layout horizontal
        main_layout_2.addLayout(sexto_quadrante_layout)

        ### Terceiro layout horizontal ###
        main_layout_3 = QHBoxLayout()

        ## Sétimo quadrante (inferior esquerdo)
        setimo_quadrante_layout = QVBoxLayout()

        output_button_output_7Z = QPushButton("Especificar Diretório(s) de Saída .7Z")
        output_button_output_7Z.clicked.connect(self.gerenciador_interface.output_button_output_7Z_clicked)
        setimo_quadrante_layout.addWidget(output_button_output_7Z)

        create_7z_button = QPushButton("Armazenar como .7Z")
        sevenzip_icon_path = os.path.join(icon_path, "sevenzip4.png")
        create_7z_button.setIcon(QtGui.QIcon(sevenzip_icon_path))
        create_7z_button.clicked.connect(self.gerenciador_interface.store_as_7z)
        setimo_quadrante_layout.addWidget(create_7z_button)

        output_button_output_TAR = QPushButton("Especificar Diretório(s) de Saída .TAR")
        output_button_output_TAR.clicked.connect(self.gerenciador_interface.output_button_output_TAR_clicked)
        setimo_quadrante_layout.addWidget(output_button_output_TAR)

        create_tar_button = QPushButton("Armazenar como .TAR")
        tar_icon_path = os.path.join(icon_path, "tar1.png")
        create_tar_button.setIcon(QtGui.QIcon(tar_icon_path))
        create_tar_button.clicked.connect(self.gerenciador_interface.store_as_tar)
        setimo_quadrante_layout.addWidget(create_tar_button)

        main_layout_3.addLayout(setimo_quadrante_layout)
        main_layout_3.setAlignment(setimo_quadrante_layout, Qt.AlignmentFlag.AlignBottom)

        ## Oitavo quadrante (inferior centro)
        setimo_quadrante_layout = QVBoxLayout()

        output_label_7z = QLabel("Diretório(s) de saída .7Z:")
        setimo_quadrante_layout.addWidget(output_label_7z)
        self.gerenciador_interface.output_listbox_7z = QListWidget()
        setimo_quadrante_layout.addWidget(self.gerenciador_interface.output_listbox_7z)
        main_layout_3.addLayout(setimo_quadrante_layout)

        ## Nono quadrante (inferior direito)
        nono_quadrante_layout = QVBoxLayout()

        output_label_tar = QLabel("Diretório(s) de saída .TAR:")
        nono_quadrante_layout.addWidget(output_label_tar)
        self.gerenciador_interface.output_listbox_tar = QListWidget()
        nono_quadrante_layout.addWidget(self.gerenciador_interface.output_listbox_tar)
        main_layout_3.addLayout(nono_quadrante_layout)

        ### Criar três widgets para acomodar os layouts horizontais ###
            # Esta linha está criando uma nova instância de QWidget, que é uma classe base para todos os objetos de interface do usuário no PyQt.
            # O argumento self indica que este widget será um filho do objeto atual, que é provavelmente uma janela ou outro widget.
        widget_1 = QWidget(self)
            # Esta linha está definindo o layout do widget_2 para ser main_layout_1.
            # Um layout é uma maneira de organizar widgets dentro de um widget pai.
            # O objeto main_layout_1 provavelmente é uma instância de uma das classes de layout do PyQt, ...
            # como QVBoxLayout, QHBoxLayout ou QGridLayout, que foi definida anteriormente no código.
        widget_1.setLayout(main_layout_1)

        widget_2 = QWidget(self)
        widget_2.setLayout(main_layout_2)

        widget_3 = QWidget(self)
        widget_3.setLayout(main_layout_3)

        ### Adicionar os widgets ao layout principal ###
            # Esta linha está criando uma nova instância de QVBoxLayout, que é uma classe que fornece um layout vertical de widgets.
        main_layout = QVBoxLayout()
            # Essas linhas estão adicionando três widgets (widget_1, widget_2, widget_3) ao layout vertical.
            # Os widgets serão dispostos de cima para baixo na ordem em que foram adicionados.
        main_layout.addWidget(widget_1)
        main_layout.addWidget(widget_2)
        main_layout.addWidget(widget_3)

            # Esta linha está criando uma nova instância de QWidget, que é uma classe base para todos os objetos de interface do usuário no PyQt.
            # O argumento self indica que este widget será um filho do objeto atual, que é provavelmente uma janela ou outro widget.
        central_widget = QWidget(self)
            # Esta linha está definindo o layout do central_widget para ser main_layout.
            # Isso significa que o central_widget terá os três widgets dispostos verticalmente.
        central_widget.setLayout(main_layout)
            # Esta linha está definindo o central_widget como o widget central da janela.
            # Em uma janela do QMainWindow, o widget central é o widget principal que ocupa a maior parte do espaço da janela.
        self.setCentralWidget(central_widget)

        self.aplicacao_tema_padrao_neutro()

    def aplicacao_tema_padrao_neutro(self):
        apply_neutral_standart_theme(self)


# Esta linha verifica se o script atual está sendo executado diretamente, e não sendo importado como um módulo.
# Se o script está sendo executado diretamente, o valor de __name__ será "__main__".
if __name__ == "__main__":
    # Esta linha cria uma instância de QApplication, que é a classe principal de qualquer aplicação PyQt.
    # Ela recebe como argumento uma lista de argumentos de linha de comando.
    # Neste caso, uma lista vazia é passada, o que significa que nenhum argumento de linha de comando é usado.
    app = QApplication([])
    # Esta linha cria uma instância da classe InterfaceGrafica.
    # Presumivelmente, esta é uma subclasse de uma das classes de janela do PyQt, ...
    # como QMainWindow ou QWidget, e define a interface do usuário da aplicação.
    window = InterfaceGrafica()
    # Esta linha exibe a janela na tela. Até que este método seja chamado, a janela não será visível.
    window.show()
    # Esta linha inicia o loop de eventos da aplicação.
    # Um loop de eventos é um loop infinito que espera por eventos do sistema, ...
    # como cliques de mouse ou pressionamentos de teclas, e os envia para os objetos apropriados.
    # Este método não retornará até que a aplicação seja encerrada.
    app.exec()

"""
Este código utiliza as seguintes bibliotecas:

- `os`: Uma biblioteca padrão do Python para interagir com o sistema operacional. Permite realizar várias operações no sistema de arquivos e no ambiente do sistema operacional.
- `subprocess`: Uma biblioteca padrão do Python para gerenciar novos processos, conectar a seus pipes de entrada/saída/erro e obter seus códigos de retorno.
- `PyQt6.QtWidgets`: Uma biblioteca de terceiros para criar interfaces gráficas de usuário (GUIs) no Python.
- `Nesta versão`: O empacotamento de compressão e descompressão é feito pelo WinRAR e pelo 7-Zip, fora da Thread Principal.
        Deixando a GUI livre, sem bloquea-la, até que o processo seja concluído.
- `Nesta versão`: Os botões e caixas de texto estão organizados em grade, em três colunas e três linhas.
- `Nesta versão`: O tema é aplicado o tema padrão da biblioteca PyQt6 - Neutral Standart.

Agradecemos aos desenvolvedores e contribuidores dessas bibliotecas por seu trabalho duro e dedicação, que tornaram possível a criação deste projeto.
"""
