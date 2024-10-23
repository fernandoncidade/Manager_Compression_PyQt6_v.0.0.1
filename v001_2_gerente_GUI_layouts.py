# Importa as classes QListWidget, QFileDialog, QWidget, QTreeView, QMessageBox do módulo QtWidgets
from PyQt6.QtWidgets import (QListWidget, QFileDialog, QWidget, QTreeView, QMessageBox)
# Importa a classe Qt do módulo QtCore
from PyQt6.QtCore import QThread
# Importa a classe Queue do módulo queue
from queue import Queue
# Importa as classes CompressaoRAR, CompressaoZIP, Compressao7Z, CompressaoTAR, TesteIntegridade, Extracao do módulo CompressionMotors_7Zip
from v001_4_motores_compressao import (buscar_sevenzip_executavel, buscar_winrar_executavel, CompressaoRAR,
                                       CompressaoZIP, Compressao7Z, CompressaoTAR, TesteIntegridade, Extracao)
from v001_5_colors import apply_dialog_box_theme


# Define uma nova classe chamada GerenciadorInterface que herda de QThread, uma classe do PyQt que permite a criação de threads.
class GerenciadorInterface(QThread):
    # Define o método inicializador da classe, que é chamado quando um objeto da classe é criado.
    def __init__(self, main_window):
        # Chama o método inicializador da classe pai (QThread), que é necessário para a correta inicialização da thread.
        super(GerenciadorInterface, self).__init__()
        # Armazena uma referência à janela principal passada como argumento.
        self.main_window = main_window
        # Cria uma fila para armazenar os arquivos a serem comprimidos.
        self.compress_queue = Queue()

            # Cria uma fila para armazenar os arquivos a serem extraídos.
        self.compress_thread_rar = None # Thread de compressão para arquivos RAR
        self.compress_thread_zip = None
        self.compress_thread_7z = None
        self.compress_thread_tar = None

            # Definir variáveis para armazenar o método de compressão selecionado para cada tipo de arquivo.
        self.compression_method_rar = None # Método de compressão para arquivos RAR
        self.compression_method_zip = None
        self.compression_method_7z = None
        self.compression_method_tar = None

            # Atualizar arquivos existentes
        self.update_existing = None

        # Atribuir o caminho do executável do WinRAR à variável winrar_executable.
        self.winrar_executable = buscar_winrar_executavel()
        # Atribuir o caminho do executável do 7zip à variável sevenzip_executable.
        self.sevenzip_executable = buscar_sevenzip_executavel()

        # Verificar se o executável do WinRAR ou do 7zip foi encontrado.
        if not self.winrar_executable and not self.sevenzip_executable:
            print("Nenhum dos programas (WinRAR ou 7-Zip) encontrado. Por favor, instale um deles e tente novamente.")
            # Se nenhum dos executáveis for encontrado, o programa é encerrado.
            exit(1)

            # Crie listas separadas para cada tipo de compressão
        self.output_listbox_rar = QListWidget() # Lista de saída para arquivos RAR
        self.output_listbox_zip = QListWidget()
        self.output_listbox_7z = QListWidget()
        self.output_listbox_tar = QListWidget()
        self.output_listbox = QListWidget() # Lista de saída para arquivos a serem comprimidos
        self.folder_listbox = QListWidget() # Lista de entrada para arquivos a serem comprimidos
        self.output_listbox_extract = QListWidget() # Lista de saída para extração de arquivos
        self.compressed_files = [] # Lista de arquivos comprimidos
        self.compress_threads = [] # Lista de threads de compressão

        # Esta linha está criando uma nova instância da classe CompressaoRAR, passando três argumentos para o construtor:
        # self.winrar_executable (o caminho para o executável do WinRAR);
        # self.output_listbox (um objeto ListBox que contém os caminhos de saída) e;
        # self.folder_listbox (um objeto ListBox que contém os caminhos dos arquivos a serem comprimidos).
        # A nova instância é armazenada na variável self.compress_thread_rar.
        self.compress_thread_rar = CompressaoRAR(self.winrar_executable, self.update_existing, self.output_listbox, self.folder_listbox)
        # Esta linha está conectando o sinal finished da instância CompressaoRAR ao método self.on_compress_finished.
        # Isso significa que quando o sinal finished for emitido (ou seja, quando a compressão estiver concluída);
        # o método self.on_compress_finished será chamado automaticamente.
        self.compress_thread_rar.finished.connect(self.on_compress_finished)

        self.compress_thread_zip = CompressaoZIP(self.sevenzip_executable, self.update_existing, self.output_listbox, self.folder_listbox)
        self.compress_thread_zip.finished.connect(self.on_compress_finished)

        self.compress_thread_7z = Compressao7Z(self.sevenzip_executable, self.update_existing, self.output_listbox, self.folder_listbox)
        self.compress_thread_7z.finished.connect(self.on_compress_finished)

        self.compress_thread_tar = CompressaoTAR(self.sevenzip_executable, self.update_existing, self.output_listbox, self.folder_listbox)
        self.compress_thread_tar.finished.connect(self.on_compress_finished)

        self.teste_integridade_thread = TesteIntegridade(self.sevenzip_executable, self.compressed_files)
        self.teste_integridade_thread.finished.connect(self.on_teste_integridade_finished)

        self.extract_thread = Extracao(self.winrar_executable, self.sevenzip_executable, self.output_listbox, self.folder_listbox)
        self.extract_thread.finished.connect(self.on_extract_finished)

    # Define um método chamado browse_folder.
    # Este método não recebe argumentos além de self (uma referência ao objeto que o método foi chamado).
    def browse_folder(self, main_window):
        # Cria um novo diálogo de seleção de arquivos com o título "Selecionar Pastas". O diálogo é filho da janela principal.
        folder_dialog = QFileDialog(main_window, "Selecionar Pastas")
        # Define o modo do diálogo para permitir apenas a seleção de diretórios.
        folder_dialog.setFileMode(QFileDialog.FileMode.Directory)
        # Define a opção para mostrar apenas diretórios no diálogo.
        folder_dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        # Define a opção para tornar o diálogo somente leitura.
        folder_dialog.setOption(QFileDialog.Option.ReadOnly, True)
        # Define a opção para ocultar detalhes do filtro de nome no diálogo.
        folder_dialog.setOption(QFileDialog.Option.HideNameFilterDetails, True)
        # Define a opção para não usar o diálogo nativo do sistema operacional.
        folder_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        # Define a opção para não resolver links simbólicos no diálogo.
        folder_dialog.setOption(QFileDialog.Option.DontResolveSymlinks, True)
        # Define o texto do botão de aceitação do diálogo para "Selecionar".
        folder_dialog.setLabelText(QFileDialog.DialogLabel.Accept, "Selecionar")
        # Define o texto do botão de rejeição do diálogo para "Cancelar".
        folder_dialog.setLabelText(QFileDialog.DialogLabel.Reject, "Cancelar")
        # Desabilita a alça de redimensionamento do diálogo.
        folder_dialog.setSizeGripEnabled(False)

        apply_dialog_box_theme(folder_dialog)

        # Procura por um objeto QTreeView filho do diálogo e armazena em tree_view.
        tree_view = folder_dialog.findChild(QTreeView)

        # Verifica se tree_view não é None (ou seja, se um objeto QTreeView foi encontrado).
        if tree_view:
            # Define o modo de seleção do QTreeView para permitir a seleção de múltiplos itens.
            tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)

        # Exibe o diálogo e verifica se o usuário clicou no botão de aceitar.
        if folder_dialog.exec() == QFileDialog.DialogCode.Accepted:
            # Obtém a lista de diretórios selecionados pelo usuário.
            selected_folders = folder_dialog.selectedFiles()
            # Adiciona os diretórios selecionados ao ListBox de pastas.
            self.folder_listbox.addItems(selected_folders)

    def browse_file(self, main_window):
        file_dialog = QFileDialog(main_window, "Selecionar Arquivos")
        # Define o modo do diálogo para permitir a seleção de arquivos.
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        # Define o filtro de nome do diálogo para "Todos os Arquivos (*.*)".
        file_dialog.setNameFilter("Todos os Arquivos (*.*)")
        file_dialog.setOption(QFileDialog.Option.ReadOnly, True)
        file_dialog.setOption(QFileDialog.Option.HideNameFilterDetails, True)
        file_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        file_dialog.setOption(QFileDialog.Option.DontResolveSymlinks, True)
        file_dialog.setLabelText(QFileDialog.DialogLabel.Accept, "Selecionar")
        file_dialog.setLabelText(QFileDialog.DialogLabel.Reject, "Cancelar")
        file_dialog.setSizeGripEnabled(False)

        apply_dialog_box_theme(file_dialog)

        tree_view = file_dialog.findChild(QTreeView)

        if tree_view:
            tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            # Obtém a lista de arquivos selecionados pelo usuário.
            selected_files = file_dialog.selectedFiles()
            # Adiciona os arquivos selecionados ao ListBox de pastas.
            self.folder_listbox.addItems(selected_files)

    # Define um método chamado clear_folders.
    def clear_folders(self):
        # Limpa o conteúdo do ListBox de pastas.
        self.folder_listbox.clear()

    def browse_output(self, main_window):
        output_dialog = QFileDialog(main_window, "Selecionar Pasta de Saída")
        output_dialog.setFileMode(QFileDialog.FileMode.Directory)
        output_dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        output_dialog.setOption(QFileDialog.Option.ReadOnly, True)
        output_dialog.setOption(QFileDialog.Option.HideNameFilterDetails, True)
        output_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        output_dialog.setOption(QFileDialog.Option.DontResolveSymlinks, True)
        output_dialog.setLabelText(QFileDialog.DialogLabel.Accept, "Selecionar")
        output_dialog.setLabelText(QFileDialog.DialogLabel.Reject, "Cancelar")
        output_dialog.setSizeGripEnabled(False)

        apply_dialog_box_theme(output_dialog)

        tree_view = output_dialog.findChild(QTreeView)

        if tree_view:
            tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)

        if output_dialog.exec() == QFileDialog.DialogCode.Accepted:
            # Obtém a lista de diretórios selecionados pelo usuário.
            selected_output = output_dialog.selectedFiles()
            # Adiciona os diretórios selecionados ao ListBox de saída.
            self.output_listbox.addItems(selected_output)
            # Adiciona os diretórios selecionados aos ListBox de saída para cada tipo de compressão.
            self.output_listbox_rar.addItems(selected_output)
            self.output_listbox_zip.addItems(selected_output)
            self.output_listbox_7z.addItems(selected_output)
            self.output_listbox_tar.addItems(selected_output)
            # Adiciona os diretórios selecionados ao ListBox de saída para extração.
            self.output_listbox_extract.addItems(selected_output)

    # Define um método chamado clear_output.
    def clear_output(self):
        # Limpa o conteúdo do ListBox de saída.
        self.output_listbox.clear()
        self.output_listbox_rar.clear()
        self.output_listbox_zip.clear()
        self.output_listbox_7z.clear()
        self.output_listbox_tar.clear()
        self.output_listbox_extract.clear()

    # Define um método chamado select_output_path.
    def select_output_path(self, output_listbox, main_window):
        output_dialog = QFileDialog(main_window, "Selecionar Pasta de Saída")
        output_dialog.setFileMode(QFileDialog.FileMode.Directory)
        output_dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        output_dialog.setOption(QFileDialog.Option.ReadOnly, True)
        output_dialog.setOption(QFileDialog.Option.HideNameFilterDetails, True)
        output_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        output_dialog.setOption(QFileDialog.Option.DontResolveSymlinks, True)
        output_dialog.setLabelText(QFileDialog.DialogLabel.Accept, "Selecionar")
        output_dialog.setLabelText(QFileDialog.DialogLabel.Reject, "Cancelar")
        output_dialog.setSizeGripEnabled(False)

        apply_dialog_box_theme(output_dialog)

        tree_view = output_dialog.findChild(QTreeView)
        
        if tree_view:
            tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)

        if output_dialog.exec() == QFileDialog.DialogCode.Accepted:
            # Obtém a lista de diretórios selecionados pelo usuário.
            selected_output = output_dialog.selectedFiles()
            # Adiciona os diretórios selecionados ao ListBox de saída correspondente.
            output_listbox.addItems(selected_output)

    # Define um método chamado output_button_output_RAR_clicked.
    def output_button_output_RAR_clicked(self):
        # Chama o método select_output_path, passando o ListBox de saída correspondente como argumento.
        self.select_output_path(self.output_listbox_rar, self.main_window)

    def output_button_output_ZIP_clicked(self):
        self.select_output_path(self.output_listbox_zip, self.main_window)

    def output_button_output_7Z_clicked(self):
        self.select_output_path(self.output_listbox_7z, self.main_window)

    def output_button_output_TAR_clicked(self):
        self.select_output_path(self.output_listbox_tar, self.main_window)

    def output_button_output_EXTRACT_clicked(self):
        self.select_output_path(self.output_listbox_extract, self.main_window)

    # Define um método chamado store_as_rar.
    def store_as_rar(self):
        if self.folder_listbox.count() == 0: # Verifica se o ListBox de pastas está vazio.
            self.show_selection_compression_warning() # Exibe uma mensagem de aviso.

        elif self.output_listbox_rar.count() == 0: # Verifica se o ListBox de saída para arquivos RAR está vazio.
            self.show_selection_destination_warning() # Exibe uma mensagem de aviso.

        # Verifica se um método de compressão foi selecionado.
        elif self.compression_method_rar is not None:
            # Cria uma nova instância da classe CompressaoRAR, passando os argumentos necessários para o construtor.
            new_compress_thread = CompressaoRAR(
                # O caminho para o executável do WinRAR.
                # O ListBox de saída correspondente.
                # O ListBox de pastas.
                # O valor True para o parâmetro compress_as_rar.
                # O método de compressão selecionado.
                self.winrar_executable, self.update_existing, self.output_listbox_rar, self.folder_listbox,
                compress_as_rar=True, compression_method=self.compression_method_rar
            )
            # Conecta o sinal finished da instância CompressaoRAR ao método self.on_compress_finished.
            new_compress_thread.finished.connect(self.on_compress_finished)
            # Inicia a thread.
            self.start_compression_thread(new_compress_thread)
        # Se nenhum método de compressão foi selecionado, exibe uma mensagem de aviso.
        else:
            self.show_method_warning()

    def store_as_zip(self):
        if self.folder_listbox.count() == 0:
            self.show_selection_compression_warning()

        elif self.output_listbox_zip.count() == 0:
            self.show_selection_destination_warning()

        elif self.compression_method_zip is not None:
            new_compress_thread = CompressaoZIP(
                self.sevenzip_executable, self.update_existing, self.output_listbox_zip, self.folder_listbox,
                compress_as_zip=True, compression_method=self.compression_method_zip
            )
            new_compress_thread.finished.connect(self.on_compress_finished)
            self.start_compression_thread(new_compress_thread)
        else:
            self.show_method_warning()

    def store_as_7z(self):
        if self.folder_listbox.count() == 0:
            self.show_selection_compression_warning()

        elif self.output_listbox_7z.count() == 0:
            self.show_selection_destination_warning()

        elif self.compression_method_7z is not None:
            new_compress_thread = Compressao7Z(
                self.sevenzip_executable, self.update_existing, self.output_listbox_7z, self.folder_listbox,
                compress_as_7z=True, compression_method=self.compression_method_7z
            )
            new_compress_thread.finished.connect(self.on_compress_finished)
            self.start_compression_thread(new_compress_thread)
        else:
            self.show_method_warning()

    def store_as_tar(self):
        if self.folder_listbox.count() == 0:
            self.show_selection_compression_warning()

        elif self.output_listbox_tar.count() == 0:
            self.show_selection_destination_warning()

        elif self.compression_method_tar is not None:
            new_compress_thread = CompressaoTAR(
                self.sevenzip_executable, self.update_existing, self.output_listbox_tar, self.folder_listbox,
                compress_as_tar=True, compression_method=self.compression_method_tar
            )
            new_compress_thread.finished.connect(self.on_compress_finished)
            self.start_compression_thread(new_compress_thread)
        else:
            self.show_method_warning()

    # Define um método chamado testar_integridade.
    def testar_integridade(self):
        # Obtém a lista de arquivos selecionados pelo usuário.
        selected_files = []
        for idx in range(self.folder_listbox.count()):
            item = self.folder_listbox.item(idx)
            if item is not None:
                selected_files.append(item.text())

        # Filtra a lista de arquivos selecionados para incluir apenas arquivos comprimidos.
        compressed_files = [file for file in selected_files if file.lower().endswith(('.rar', '.zip', '.7z', '.tar'))]

        # Verifica se a lista de arquivos comprimidos não está vazia.
        if not compressed_files:
            self.show_extension_warning()
            return

        # Verifica se a lista de arquivos selecionados não está vazia.
        if self.sevenzip_executable and compressed_files:
            # Cria uma nova instância da classe TesteIntegridade, passando os argumentos necessários para o construtor.
            self.teste_integridade_thread = TesteIntegridade(self.sevenzip_executable, compressed_files)
            # Conecta o sinal finished da instância TesteIntegridade ao método self.on_teste_integridade_finished.
            self.teste_integridade_thread.finished.connect(self.on_teste_integridade_finished)
            # Inicia a thread.
            self.teste_integridade_thread.start()
        # Se a lista de arquivos selecionados estiver vazia, exibe uma mensagem de aviso.
        else:
            self.show_integridade_warning()

    # Define um método chamado extract_files.
    def extract_files(self):
        if self.folder_listbox.count() == 0: # Verifica se o ListBox de pastas está vazio.
            self.show_selection_descompression_warning() # Exibe uma mensagem de aviso.

        elif self.output_listbox_extract.count() == 0: # Verifica se o ListBox de saída para extração está vazio.
            self.show_selection_destination_warning() # Exibe uma mensagem de aviso.

        # Verifica se o executável do WinRAR foi encontrado.
        elif self.winrar_executable:
            # Cria uma nova instância da classe Extracao, passando os argumentos necessários para o construtor.
            self.extract_thread = Extracao(
                self.winrar_executable, self.sevenzip_executable,
                self.output_listbox_extract, self.folder_listbox
            )
            # Conecta o sinal finished da instância Extracao ao método self.on_extract_finished.
            self.extract_thread.finished.connect(self.on_extract_finished)
            # Inicia a thread.
            self.extract_thread.start()

        # Verifica se o executável do 7zip foi encontrado.
        elif self.sevenzip_executable:
            self.extract_thread = Extracao(
                self.sevenzip_executable, self.winrar_executable,
                self.output_listbox_extract, self.folder_listbox
            )
            self.extract_thread.finished.connect(self.on_extract_finished)
            self.extract_thread.start()
        # Se nenhum dos programas for encontrado, exibe uma mensagem de aviso.
        else:
            self.show_extract_warning()

    def start_compression_thread(self, new_thread):
        # Verifica se há alguma thread em execução com o mesmo formato de compressão.
        new_format = new_thread.format

        # Se houver uma thread em execução com o mesmo formato de compressão, coloque a nova thread na fila.
        if any(thread.isRunning() and thread.format == new_format for thread in self.compress_threads):
            self.compress_queue.put(new_thread) # Adiciona a nova thread à fila.
            self.show_queue_warning() # Exibe uma mensagem de aviso.

        # Se não houver threads em execução com o mesmo formato de compressão, inicie a nova thread.
        else:
            new_thread.start() # Inicia a nova thread.
            self.compress_threads.append(new_thread) # Adiciona a nova thread à lista de threads de compressão.

    # Define um método chamado on_compress_finished.
    def on_compress_finished(self):
        finished_thread = self.sender() # Obtém a thread que emitiu o sinal finished.
        self.compress_threads.remove(finished_thread) # Remove a thread da lista de threads de compressão.

        if not self.compress_queue.empty(): # Verifica se a fila de compressão não está vazia.
            next_thread = self.compress_queue.get() # Obtém a próxima thread da fila.
            self.start_compression_thread(next_thread) # Inicia a próxima thread.

        elif not self.compress_threads:
            # Cria uma nova instância da classe QMessageBox.
            msg_box = QMessageBox()
            # Define o ícone da caixa de mensagem como um ícone de informação.
            msg_box.setIcon(QMessageBox.Icon.Information)
            # Define o título da caixa de mensagem como "Empacotamento Concluído".
            msg_box.setWindowTitle("Empacotamento Concluído")
            # Define o texto da caixa de mensagem como "O Empacotamento dos arquivos foi concluído com sucesso!".
            msg_box.setText("O Empacotamento dos arquivos foi concluído com sucesso!")
            # Exibe a caixa de mensagem.
            msg_box.exec()

    # Define um método chamado on_teste_integridade_finished.
    def on_teste_integridade_finished(self):
        msg_box = QMessageBox() # Cria uma nova instância da classe QMessageBox.
        msg_box.setIcon(QMessageBox.Icon.Information) # Define o ícone da caixa de mensagem como um ícone de informação.
        msg_box.setWindowTitle("Teste de Integridade Concluído") # Define o título da caixa de mensagem como "Teste de Integridade Concluído".
        msg_box.setText("O teste de integridade dos arquivos foi concluído com sucesso!") # Define o texto da caixa de mensagem como "O teste de integridade dos arquivos foi concluído com sucesso!".
        msg_box.exec() # Exibe a caixa de mensagem.

    def on_extract_finished(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Extração Concluída")
        msg_box.setText("A Extração dos arquivos foi concluída com sucesso!")
        msg_box.exec()

    # Define um método chamado show_queue_warning.
    def show_queue_warning(self):
        parent = self.parent() if isinstance(self.parent(), QWidget) else QWidget() # Obtém a janela pai do objeto.
        self.show_warning(parent, "Aviso", "O processo solicitado foi colocado em fila, aguardando o anterior encerrar.") # Exibe uma mensagem de aviso.

    def show_method_warning(self):
        parent = self.parent() if isinstance(self.parent(), QWidget) else QWidget()
        self.show_warning(parent, "Aviso", "Por favor, selecione um método de compressão antes de prosseguir.")

    def show_integridade_warning(self):
        parent = self.parent()if isinstance(self.parent(), QWidget) else QWidget()
        self.show_warning(parent, "Aviso", "Por favor, selecione um arquivo para testar a integridade.")

    def show_extension_warning(self):
        parent = self.parent()if isinstance(self.parent(), QWidget) else QWidget()
        self.show_warning(parent, "Aviso", "Por favor, selecione um arquivo RAR, ZIP, 7Z ou TAR para prosseguir.")

    def show_extract_warning(self):
        parent = self.parent() if isinstance(self.parent(), QWidget) else QWidget()
        self.show_warning(parent, "Aviso", "Nenhum dos programas (WinRAR ou 7-Zip) encontrado. Por favor, instale um deles e tente novamente.")

    def show_selection_compression_warning(self):
        parent = self.parent()if isinstance(self.parent(), QWidget) else QWidget()
        self.show_warning(parent, "Aviso", "Por favor, selecione uma pasta antes de prosseguir.")

    def show_selection_descompression_warning(self):
        parent = self.parent()if isinstance(self.parent(), QWidget) else QWidget()
        self.show_warning(parent, "Aviso", "Por favor, selecione um arquivo antes de prosseguir.")

    def show_selection_destination_warning(self):
        parent = self.parent()if isinstance(self.parent(), QWidget) else QWidget()
        self.show_warning(parent, "Aviso", "Por favor, selecione um diretório de saída antes de prosseguir.")

    # Define um método chamado show_warning.
    def show_warning(self, parent, title, message):
        msg_box = QMessageBox(parent) # Cria uma nova instância da classe QMessageBox, passando a janela pai como argumento.
        msg_box.setIcon(QMessageBox.Icon.Warning) # Define o ícone da caixa de mensagem como um ícone de aviso.
        msg_box.setWindowTitle(title) # Define o título da caixa de mensagem como o título fornecido.
        msg_box.setText(message) # Define o texto da caixa de mensagem como a mensagem fornecida.
        msg_box.exec() # Exibe a caixa de mensagem.
