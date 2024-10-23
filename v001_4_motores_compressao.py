import os  # Importa o módulo os
import sys  # Importa o módulo sys
import subprocess  # Importa o módulo subprocess
# Importa as classes Qt, QThread, pyqtSignal do módulo QtCore
from PyQt6.QtCore import QThread, pyqtSignal

### AS LINHAS DE COMENTÁRIO SEMPRE FARÃO REFERÊNCIA A LINHA DE CÓDIGO QUE AS SUSCEDE, LOGO ABAIXO ###

# Define a função de chamada, que busca o executável. Essa função não recebe nenhum argumento.
def buscar_winrar_executavel():
    # Obter o caminho do diretório do executável
    dir_atual = getattr(sys, '_MEIPASS', os.path.dirname(os.path.realpath(__file__)))

    winrar_path = os.path.join(dir_atual, "WinRAR")

    # Construir o caminho para o executável do WinRAR
    # Ela usa a função os.path.join() para combinar o diretório atual (dir_atual) com o nome do arquivo (WinRAR.exe).
    caminho_winrar = os.path.join(winrar_path, 'WinRAR.exe')

    # Verificar se o executável do WinRAR existe
    if os.path.exists(caminho_winrar):
        return caminho_winrar

    # Esta linha define uma lista de possíveis localizações para o executável do WinRAR.
    # Essas localizações são caminhos absolutos para os diretórios onde o WinRAR pode estar instalado.
    possible_locations = [
        rf"C:\Program Files\WinRAR\WinRAR.exe",
        rf"C:\Program Files (x86)\WinRAR\WinRAR.exe",
    ]

    # Esta linha inicia um loop que percorre cada localização na lista possible_locations.
    for location in possible_locations:
        if os.path.isfile(location):
            return location

    # Se o arquivo do executável do WinRAR não for encontrado em nenhuma das localizações, ...
    # esta linha retorna None, indicando que o executável não foi encontrado.
    return None


# Define a função de chamada, que busca o executável. Essa função não recebe nenhum argumento.
def buscar_sevenzip_executavel():
    # Obter o caminho do diretório do executável
    dir_atual = getattr(sys, '_MEIPASS', os.path.dirname(os.path.realpath(__file__)))

    sevenzip_path = os.path.join(dir_atual, "7-Zip")

    # Construir o caminho para o executável do 7-Zip
    # Ela usa a função os.path.join() para combinar o diretório atual (dir_atual) com o nome do arquivo (7zG.exe).
    caminho_sevenzip = os.path.join(sevenzip_path, '7zG.exe')

    # Verificar se o executável do 7-Zip existe
    if os.path.exists(caminho_sevenzip):
        return caminho_sevenzip

    # Esta linha define uma lista de possíveis localizações para o executável do 7-Zip.
    # Essas localizações são caminhos absolutos para os diretórios onde o WinRAR pode estar instalado.
    possible_locations = [
        rf"C:\Program Files\7-Zip\7zG.exe",
        rf"C:\Program Files (x86)\7-Zip\7zG.exe",
    ]

    # Esta linha inicia um loop que percorre cada localização na lista possible_locations.
    for location in possible_locations:
        if os.path.isfile(location):
            return location

    # Se o arquivo do executável do WinRAR não for encontrado em nenhuma das localizações, ...
    # esta linha retorna None, indicando que o executável não foi encontrado.
    return None


# Define uma nova classe chamada class CompressaoRAR(QThread): que herda de QThread, uma classe do PyQt que permite a criação de threads.
class CompressaoRAR(QThread):
    # Define um sinal chamado finished que pode ser emitido quando a thread terminar.
    finished = pyqtSignal()

    #Esta linha define o método especial __init__, que é o construtor da classe.
    # Ele é chamado quando um novo objeto da classe é criado.
    # O construtor recebe vários parâmetros: winrar_executable, output_listbox, folder_listbox, compress_as_rar e compression_method.
    def __init__(self, winrar_executable, update_existing, output_listbox, folder_listbox, compress_as_rar=False, compression_method=None):

        # Esta linha chama o construtor da classe pai.
        # Ela garante que o construtor da classe pai seja executado antes do código no construtor da classe atual.
        super(CompressaoRAR, self).__init__()
        self.format = "rar"
        # Esta linha atribui o valor do parâmetro winrar_executable ao atributo winrar_executable do objeto atual.
        # O atributo self.winrar_executable será usado posteriormente no código.
        # O mesmo vale para os outros atributos.
        self.winrar_executable = winrar_executable
        self.update_existing = update_existing
        self.output_listbox = output_listbox
        self.folder_listbox = folder_listbox
        self.compress_as_rar = compress_as_rar
        self.compression_method = compression_method

    # Define o método run, que é chamado quando a thread é iniciada. Este método não recebe argumentos além de self.
    def run(self):
        # Nesta linha, uma lista chamada output_paths é criada.
        # Ela contém os textos de cada item da output_listbox, que é uma caixa de listagem de saída.
        # O loop for percorre os índices de 0 até o número de itens na output_listbox, e o método text() é usado para obter o texto de cada item.
        output_paths = [self.output_listbox.item(idx).text() for idx in range(self.output_listbox.count())]
        # Esta linha verifica se a lista output_paths está vazia. Se estiver vazia, o código retorna imediatamente, interrompendo a execução do método.
        if not output_paths:
            return

        # Aqui, uma lista vazia chamada compressed_files é criada.
        # Essa lista será usada para armazenar os caminhos dos arquivos comprimidos.
        compressed_files = []

        # Este loop for percorre os índices de 0 até o número de itens na folder_listbox, que é outra caixa de listagem.
        for idx in range(self.folder_listbox.count()):
            # Nesta linha, o texto do item da folder_listbox correspondente ao índice atual é obtido e atribuído à variável folder_path.
            # Essa variável representa o caminho da pasta.
            folder_path = self.folder_listbox.item(idx).text()
            # Aqui, o nome da pasta é extraído do caminho completo da pasta usando a função basename do módulo os.
            # O nome da pasta é armazenado na variável folder_name.
            folder_name = os.path.basename(folder_path)

            # Este loop for percorre cada caminho de saída na lista output_paths.
            for output_path in output_paths:
                # Nesta linha, o caminho completo do arquivo comprimido é construído usando a função join do módulo os.
                # O caminho de saída e o nome da pasta são combinados com a extensão .rar para formar o caminho completo do arquivo comprimido.
                # O caminho é armazenado na variável compressed_file_rar.
                compressed_file_rar = os.path.join(output_path, f"{folder_name}.rar")
                # Aqui, uma string command é construída para representar o comando que será executado para comprimir a pasta.
                # O comando inclui o executável do WinRAR, opções de compressão e os caminhos do arquivo comprimido e da pasta.
                command = f'"{self.winrar_executable}" a -r -ep1 -m{self.compression_method} -md32 -afrar "{compressed_file_rar}" "{folder_path}"'

                # Se a opção de atualização estiver marcada, o comando é modificado para adicionar a opção -u.
                if self.update_existing:
                    # Adiciona a opção -o+ para atualizar arquivos existentes
                    command = f'"{self.winrar_executable}" u -r -ep1 -m{self.compression_method} -md32 -afrar -o+ "{compressed_file_rar}" "{folder_path}"'
                    
                # Nesta linha, o comando construído anteriormente é executado usando o módulo subprocess.
                # O parâmetro shell=True indica que o comando deve ser executado em um shell.
                subprocess.run(command, shell=True)
                # Aqui, o caminho do arquivo comprimido é adicionado à lista compressed_files.
                compressed_files.append(compressed_file_rar)

        # Por fim, o sinal finished é emitido.
        # Isso indica que o método run foi concluído e pode ser usado para notificar outros componentes ou partes do código sobre o término da execução.
        self.finished.emit()


class CompressaoZIP(QThread):
    finished = pyqtSignal()

    def __init__(self, sevenzip_executable, update_existing, output_listbox, folder_listbox, compress_as_zip=False, compression_method=None):

        super(CompressaoZIP, self).__init__()
        self.format = "zip"
        self.sevenzip_executable = sevenzip_executable
        self.update_existing = update_existing
        self.output_listbox = output_listbox
        self.folder_listbox = folder_listbox
        self.compress_as_zip = compress_as_zip
        self.compression_method = compression_method

    def run(self):
        output_paths = [self.output_listbox.item(idx).text() for idx in range(self.output_listbox.count())]
        if not output_paths:
            return

        compressed_files = []

        for idx in range(self.folder_listbox.count()):
            folder_path = self.folder_listbox.item(idx).text()
            folder_name = os.path.basename(folder_path)

            for output_path in output_paths:
                compressed_file_zip = os.path.join(output_path, f"{folder_name}.zip")
                command = f'"{self.sevenzip_executable}" a -r -tzip -mx={self.compression_method} "{compressed_file_zip}" "{folder_path}"'
                if self.update_existing:
                    command = f'"{self.sevenzip_executable}" u -r -tzip -mx={self.compression_method} "{compressed_file_zip}" "{folder_path}"'
                subprocess.run(command, shell=True)
                compressed_files.append(compressed_file_zip)

        self.finished.emit()


class Compressao7Z(QThread):
    finished = pyqtSignal()

    def __init__(self, sevenzip_executable, update_existing, output_listbox, folder_listbox, compress_as_7z=False, compression_method=None):

        super(Compressao7Z, self).__init__()
        self.format = "7z"
        self.sevenzip_executable = sevenzip_executable
        self.update_existing = update_existing
        self.output_listbox = output_listbox
        self.folder_listbox = folder_listbox
        self.compress_as_7z = compress_as_7z
        self.compression_method = compression_method

    def run(self):
        output_paths = [self.output_listbox.item(idx).text() for idx in range(self.output_listbox.count())]
        if not output_paths:
            return

        compressed_files = []

        for idx in range(self.folder_listbox.count()):
            folder_path = self.folder_listbox.item(idx).text()
            folder_name = os.path.basename(folder_path)

            for output_path in output_paths:
                compressed_file_7z = os.path.join(output_path, f"{folder_name}.7z")
                command = f'"{self.sevenzip_executable}" a -r -t7z -mx={self.compression_method} "{compressed_file_7z}" "{folder_path}"'
                if self.update_existing:
                    command = f'"{self.sevenzip_executable}" u -r -t7z -mx={self.compression_method} "{compressed_file_7z}" "{folder_path}"'
                subprocess.run(command, shell=True)
                compressed_files.append(compressed_file_7z)

        self.finished.emit()


class CompressaoTAR(QThread):
    finished = pyqtSignal()

    def __init__(self, sevenzip_executable, update_existing, output_listbox, folder_listbox, compress_as_tar=False, compression_method=None):

        super(CompressaoTAR, self).__init__()
        self.format = "tar"
        self.sevenzip_executable = sevenzip_executable
        self.update_existing = update_existing
        self.output_listbox = output_listbox
        self.folder_listbox = folder_listbox
        self.compress_as_tar = compress_as_tar
        self.compression_method = compression_method

    def run(self):
        output_paths = [self.output_listbox.item(idx).text() for idx in range(self.output_listbox.count())]
        if not output_paths:
            return

        compressed_files = []

        for idx in range(self.folder_listbox.count()):
            folder_path = self.folder_listbox.item(idx).text()
            folder_name = os.path.basename(folder_path)

            for output_path in output_paths:
                compressed_file_tar = os.path.join(output_path, f"{folder_name}.tar")
                command = f'"{self.sevenzip_executable}" a -r -ttar "{compressed_file_tar}" "{folder_path}"'
                if self.update_existing:
                    command = f'"{self.sevenzip_executable}" u -r -ttar "{compressed_file_tar}" "{folder_path}"'
                subprocess.run(command, shell=True)
                compressed_files.append(compressed_file_tar)

        self.finished.emit()

# Define uma nova classe chamada TesteIntegridade que herda de QThread, uma classe do PyQt que permite a criação de threads.
class TesteIntegridade(QThread):
    # Define um sinal chamado finished que pode ser emitido quando a thread terminar.
    finished = pyqtSignal()

    # Define o método inicializador da classe, que é chamado quando um objeto da classe é criado.
    # Ele recebe três argumentos:
    # self (uma referência ao objeto sendo criado),\;
    # sevenzip_executable (o caminho para o executável do 7zip), e;
    # compressed_files (uma lista de arquivos comprimidos para verificar).
    def __init__(self, sevenzip_executable, compressed_files):
        # Chama o método inicializador da classe pai (QThread), que é necessário para a correta inicialização da thread.
        super(TesteIntegridade, self).__init__()
        # Armazena o caminho para o executável do 7zip no objeto.
        self.sevenzip_executable = sevenzip_executable
        # Armazena a lista de arquivos comprimidos no objeto.
        self.compressed_files = compressed_files

    # Define o método run, que é chamado quando a thread é iniciada. Este método não recebe argumentos além de self.
    def run(self):
        # Inicia um loop que itera sobre cada arquivo na lista de arquivos comprimidos.
        for compressed_file in self.compressed_files:
            # Verifica se o nome do arquivo termina com ".rar", indicando que é um arquivo RAR.
            if compressed_file.endswith(".rar"):
                # Define o comando que será executado para verificar a integridade do arquivo.
                # O comando usa o executável do 7zip e o nome do arquivo.
                command = f'"{self.sevenzip_executable}" t "{compressed_file}"'
                # Executa o comando definido na linha anterior.
                # O argumento shell=True permite que o comando seja executado em um shell,
                # enquanto check=True faz com que uma exceção seja lançada se o comando falhar.
                result = subprocess.run(command, shell=True, check=True)
                # Verifica se o comando retornou um código de erro (qualquer coisa diferente de 0).
                if result.returncode != 0:
                    # Se o comando retornou um código de erro, ...
                    # uma exceção é lançada com uma mensagem indicando ...
                    # que a verificação da integridade do arquivo falhou.
                    raise Exception("A verificação da integridade do arquivo falhou")
                
            # Verifica se o nome do arquivo termina com ".zip", indicando que é um arquivo ZIP.
            elif compressed_file.endswith(".zip"):
                command = f'"{self.sevenzip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")

            # Verifica se o nome do arquivo termina com ".7z", indicando que é um arquivo 7z.
            elif compressed_file.endswith(".7z"):
                command = f'"{self.sevenzip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")

            # Verifica se o nome do arquivo termina com ".tar", indicando que é um arquivo TAR.
            elif compressed_file.endswith(".tar"):
                command = f'"{self.sevenzip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")

        # Emite o sinal finished, indicando que a thread terminou.
        self.finished.emit()


# Define uma nova classe chamada Extracao que herda de QThread, uma classe do PyQt que permite a criação de threads.
class Extracao(QThread):
    # Define um sinal chamado finished que pode ser emitido quando a thread terminar.
    finished = pyqtSignal()

    # Define o método inicializador da classe, que é chamado quando um objeto da classe é criado.
    # Ele recebe cinco argumentos:
    # self (uma referência ao objeto sendo criado);
    # winrar_executable (o caminho para o executável do WinRAR);
    # sevenzip_executable (o caminho para o executável do 7zip);
    # output_listbox (um objeto ListBox que contém os caminhos de saída);
    # e folder_listbox (um objeto ListBox que contém os caminhos dos arquivos a serem extraídos).
    def __init__(self, winrar_executable, sevenzip_executable, output_listbox, folder_listbox):
        # Chama o método inicializador da classe pai (QThread), que é necessário para a correta inicialização da thread.
        super(Extracao, self).__init__()
        # Armazena o caminho para o executável do WinRAR no objeto.
        self.winrar_executable = winrar_executable
        # Armazena o caminho para o executável do 7zip no objeto.
        self.sevenzip_executable = sevenzip_executable
        # Armazena o objeto ListBox que contém os caminhos de saída no objeto.
        self.output_listbox = output_listbox
        # Armazena o objeto ListBox que contém os caminhos dos arquivos a serem extraídos no objeto.
        self.folder_listbox = folder_listbox

    # Define o método run, que é chamado quando a thread é iniciada. Este método não recebe argumentos além de self.
    def run(self):
        # Cria uma lista de caminhos de saída, obtendo o texto de cada item no ListBox de saída.
        output_paths = [self.output_listbox.item(idx).text() for idx in range(self.output_listbox.count())]
        # Verifica se a lista de caminhos de saída está vazia.
        if not output_paths:
            # Se a lista de caminhos de saída está vazia, o método run é encerrado.
            return

        # Inicia um loop que itera sobre cada item no ListBox de pastas.
        for idx in range(self.folder_listbox.count()):
            # Obtém o caminho do arquivo a ser extraído do item atual no ListBox de pastas.
            archive_path = self.folder_listbox.item(idx).text()
            # Inicia um loop que itera sobre cada caminho de saída na lista de caminhos de saída.
            for output_path in output_paths:
                # Verifica se o nome do arquivo termina com ".rar", indicando que é um arquivo RAR.
                if archive_path.endswith(".rar"):
                    # Define o comando que será executado para extrair o arquivo.
                    # O comando usa o executável do WinRAR e o nome do arquivo.
                    command = f'"{self.winrar_executable}" x -y "{archive_path}" "{output_path}"'
                    # Executa o comando definido na linha anterior.
                    # O argumento shell=True permite que o comando seja executado em um shell.
                    subprocess.run(command, shell=True)

                elif archive_path.endswith(".zip"):
                    command = f'"{self.sevenzip_executable}" x -y "{archive_path}" -o"{output_path}"'
                    # Executa o comando definido na linha anterior.
                    # O argumento shell=True permite que o comando seja executado em um shell.
                    subprocess.run(command, shell=True)

                elif archive_path.endswith(".7z"):
                    # Define o comando que será executado para extrair o arquivo.
                    # O comando usa o executável do 7zip e o nome do arquivo.
                    command = f'"{self.sevenzip_executable}" x -y "{archive_path}" -o"{output_path}"'
                    # Executa o comando definido na linha anterior.
                    # O argumento shell=True permite que o comando seja executado em um shell.
                    subprocess.run(command, shell=True)

                elif archive_path.endswith(".tar"):
                    command = f'"{self.sevenzip_executable}" x -y "{archive_path}" -o"{output_path}"'
                    # Executa o comando definido na linha anterior.
                    # O argumento shell=True permite que o comando seja executado em um shell.
                    subprocess.run(command, shell=True)

        # Emite o sinal finished, indicando que a thread terminou.
        self.finished.emit()
