from queue import Queue
from PyQt6.QtWidgets import (QMainWindow, QListWidget, QFileDialog, QTreeView, QMessageBox)
from v005_5_motores_compressao import (buscar_winrar_executavel, buscar_sevenzip_executavel, buscar_bandizip_executavel,
                                       CompressaoRAR, CompressaoZIP, Compressao7Z, CompressaoBZip2, CompressaoTarXZ,
                                       CompressaoTarGZ, CompressaoZIPX, CompressaoTGZ, CompressaoLZH, CompressaoISO,
                                       CompressaoTAR, CompressaoWIM, TesteIntegridade, Extracao)


class GerenciadorInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.compress_queue = Queue()
        self.compress_threads = []
        self.compression_method_rar = None
        self.compression_method_zip = None
        self.compression_method_7z = None
        self.compression_method_bzip2 = None
        self.compression_method_zipx = None
        self.compression_method_tarxz = None
        self.compression_method_tgz = None
        self.compression_method_targz = None
        self.compression_method_lzh = None
        self.compression_method_iso = None
        self.compression_method_tar = None
        self.compression_method_wim = None
        self.update_existing = None

        self.winrar_executable = buscar_winrar_executavel()
        self.sevenzip_executable = buscar_sevenzip_executavel()
        self.bandizip_executable = buscar_bandizip_executavel()

        if not self.winrar_executable and not self.sevenzip_executable and not self.bandizip_executable:
            print("Nenhum dos programas (WinRAR, 7-Zip ou Bandizip) encontrado. Por favor, instale um deles e tente novamente.")
            exit(1)

        self.output_listbox_rar = QListWidget()
        self.output_listbox_zip = QListWidget()
        self.output_listbox_7z = QListWidget()
        self.output_listbox_tar_bz2 = QListWidget()
        self.output_listbox_zipx = QListWidget()
        self.output_listbox_tar_xz = QListWidget()
        self.output_listbox_tgz = QListWidget()
        self.output_listbox_tar_gz = QListWidget()
        self.output_listbox_lzh = QListWidget()
        self.output_listbox_iso = QListWidget()
        self.output_listbox_tar = QListWidget()
        self.output_listbox_wim = QListWidget()
        self.output_listbox = QListWidget()
        self.folder_listbox = QListWidget()
        self.output_listbox_extracao = QListWidget()
        self.compressed_files = []

        self.init_threads()

    def init_threads(self):
        self.compress_thread_rar = CompressaoRAR(self.winrar_executable, self.update_existing, self.output_listbox, self.folder_listbox)
        self.compress_thread_rar.finished.connect(self.on_compress_finished)

        self.compress_thread_zip = CompressaoZIP(self.sevenzip_executable, self.update_existing, self.output_listbox, self.folder_listbox)
        self.compress_thread_zip.finished.connect(self.on_compress_finished)

        self.compress_thread_7z = Compressao7Z(self.sevenzip_executable, self.update_existing, self.output_listbox, self.folder_listbox)
        self.compress_thread_7z.finished.connect(self.on_compress_finished)

        self.compress_thread_bzip2 = CompressaoBZip2(self.sevenzip_executable, self.update_existing, self.output_listbox, self.folder_listbox)
        self.compress_thread_bzip2.finished.connect(self.on_compress_finished)

        self.compress_thread_zipx = CompressaoZIPX(self.bandizip_executable, self.update_existing, self.output_listbox, self.folder_listbox)
        self.compress_thread_zipx.finished.connect(self.on_compress_finished)

        self.compress_thread_tarxz = CompressaoTarXZ(self.bandizip_executable, self.update_existing, self.output_listbox, self.folder_listbox)
        self.compress_thread_tarxz.finished.connect(self.on_compress_finished)

        self.compress_thread_tgz = CompressaoTGZ(self.bandizip_executable, self.update_existing, self.output_listbox, self.folder_listbox)
        self.compress_thread_tgz.finished.connect(self.on_compress_finished)

        self.compress_thread_targz = CompressaoTarGZ(self.bandizip_executable, self.update_existing, self.output_listbox, self.folder_listbox)
        self.compress_thread_targz.finished.connect(self.on_compress_finished)

        self.compress_thread_lzh = CompressaoLZH(self.bandizip_executable, self.update_existing, self.output_listbox, self.folder_listbox)
        self.compress_thread_lzh.finished.connect(self.on_compress_finished)

        self.compress_thread_iso = CompressaoISO(self.bandizip_executable, self.update_existing, self.output_listbox, self.folder_listbox)
        self.compress_thread_iso.finished.connect(self.on_compress_finished)

        self.compress_thread_tar = CompressaoTAR(self.sevenzip_executable, self.update_existing, self.output_listbox, self.folder_listbox)
        self.compress_thread_tar.finished.connect(self.on_compress_finished)

        self.compress_thread_wim = CompressaoWIM(self.sevenzip_executable, self.update_existing, self.output_listbox, self.folder_listbox)
        self.compress_thread_wim.finished.connect(self.on_compress_finished)

        self.teste_integridade_thread = TesteIntegridade(self.sevenzip_executable, self.bandizip_executable, self.compressed_files)
        self.teste_integridade_thread.finished.connect(self.on_teste_integridade_finished)

        self.extract_thread = Extracao(self.winrar_executable, self.sevenzip_executable, self.bandizip_executable, self.output_listbox, self.folder_listbox)
        self.extract_thread.finished.connect(self.on_extract_finished)

    def browse_folder(self):
        self._browse(QFileDialog.FileMode.Directory, self.folder_listbox)

    def browse_file(self):
        self._browse(QFileDialog.FileMode.ExistingFiles, self.folder_listbox)

    def browse_output(self):
        self._browse(QFileDialog.FileMode.Directory, self.output_listbox)
        self._browse(QFileDialog.FileMode.Directory, self.output_listbox_rar)
        self._browse(QFileDialog.FileMode.Directory, self.output_listbox_zip)
        self._browse(QFileDialog.FileMode.Directory, self.output_listbox_7z)
        self._browse(QFileDialog.FileMode.Directory, self.output_listbox_tar_bz2)
        self._browse(QFileDialog.FileMode.Directory, self.output_listbox_zipx)
        self._browse(QFileDialog.FileMode.Directory, self.output_listbox_tar_xz)
        self._browse(QFileDialog.FileMode.Directory, self.output_listbox_tgz)
        self._browse(QFileDialog.FileMode.Directory, self.output_listbox_tar_gz)
        self._browse(QFileDialog.FileMode.Directory, self.output_listbox_lzh)
        self._browse(QFileDialog.FileMode.Directory, self.output_listbox_iso)
        self._browse(QFileDialog.FileMode.Directory, self.output_listbox_tar)
        self._browse(QFileDialog.FileMode.Directory, self.output_listbox_wim)
        self._browse(QFileDialog.FileMode.Directory, self.output_listbox_extracao)

    def _browse(self, file_mode, listbox):
        dialog = QFileDialog()
        dialog.setFileMode(file_mode)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)

        tree_view = dialog.findChild(QTreeView)
        if tree_view:
            tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)

        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_items = dialog.selectedFiles()
            listbox.addItems(selected_items)

    def select_output_path(self, output_listbox):
        self._browse(QFileDialog.FileMode.Directory, output_listbox)

    def output_button_output_RAR_clicked(self):
        self.select_output_path(self.output_listbox_rar)

    def output_button_output_ZIP_clicked(self):
        self.select_output_path(self.output_listbox_zip)

    def output_button_output_7Z_clicked(self):
        self.select_output_path(self.output_listbox_7z)
    
    def output_button_output_TAR_BZ2_clicked(self):
        self.select_output_path(self.output_listbox_tar_bz2)

    def output_button_output_ZIPX_clicked(self):
        self.select_output_path(self.output_listbox_zipx)

    def output_button_output_TAR_XZ_clicked(self):
        self.select_output_path(self.output_listbox_tar_xz)

    def output_button_output_TGZ_clicked(self):
        self.select_output_path(self.output_listbox_tgz)

    def output_button_output_TAR_GZ_clicked(self):
        self.select_output_path(self.output_listbox_tar_gz)

    def output_button_output_LZH_clicked(self):
        self.select_output_path(self.output_listbox_lzh)

    def output_button_output_ISO_clicked(self):
        self.select_output_path(self.output_listbox_iso)

    def output_button_output_TAR_clicked(self):
        self.select_output_path(self.output_listbox_tar)
    
    def output_button_output_WIM_clicked(self):
        self.select_output_path(self.output_listbox_wim)

    def output_button_output_EXTRACAO_clicked(self):
        self.select_output_path(self.output_listbox_extracao)

    def clear_folders(self):
        self.folder_listbox.clear()

    def clear_output(self):
        self.output_listbox.clear()
        self.output_listbox_rar.clear()
        self.output_listbox_zip.clear()
        self.output_listbox_7z.clear()
        self.output_listbox_tar_bz2.clear()
        self.output_listbox_zipx.clear()
        self.output_listbox_tar_xz.clear()
        self.output_listbox_tgz.clear()
        self.output_listbox_tar_gz.clear()
        self.output_listbox_lzh.clear()
        self.output_listbox_iso.clear()
        self.output_listbox_tar.clear()
        self.output_listbox_wim.clear()
        self.output_listbox_extracao.clear()

    def clear_output_listbox_rar(self):
        self.output_listbox_rar.clear()

    def clear_output_listbox_zip(self):
        self.output_listbox_zip.clear()

    def clear_output_listbox_7z(self):
        self.output_listbox_7z.clear()

    def clear_output_listbox_bzip2(self):
        self.output_listbox_tar_bz2.clear()

    def clear_output_listbox_zipx(self):
        self.output_listbox_zipx.clear()

    def clear_output_listbox_tarxz(self):
        self.output_listbox_tar_xz.clear()

    def clear_output_listbox_tgz(self):
        self.output_listbox_tgz.clear()

    def clear_output_listbox_targz(self):
        self.output_listbox_tar_gz.clear()

    def clear_output_listbox_lzh(self):
        self.output_listbox_lzh.clear()

    def clear_output_listbox_iso(self):
        self.output_listbox_iso.clear()

    def clear_output_listbox_tar(self):
        self.output_listbox_tar.clear()

    def clear_output_listbox_wim(self):
        self.output_listbox_wim.clear()

    def clear_output_listbox_extracao(self):
        self.output_listbox_extracao.clear()

    def store_as_rar(self):
        self._store_as(self.compress_thread_rar, self.output_listbox_rar, self.compression_method_rar)

    def store_as_zip(self):
        self._store_as(self.compress_thread_zip, self.output_listbox_zip, self.compression_method_zip)

    def store_as_7z(self):
        self._store_as(self.compress_thread_7z, self.output_listbox_7z, self.compression_method_7z)
    
    def store_as_bzip2(self):
        self._store_as(self.compress_thread_bzip2, self.output_listbox_tar_bz2, self.compression_method_bzip2)

    def store_as_zipx(self):
        self._store_as(self.compress_thread_zipx, self.output_listbox_zipx, self.compression_method_zipx)

    def store_as_tarxz(self):
        self._store_as(self.compress_thread_tarxz, self.output_listbox_tar_xz, self.compression_method_tarxz)
    
    def store_as_tgz(self):
        self._store_as(self.compress_thread_tgz, self.output_listbox_tgz, self.compression_method_tgz)

    def store_as_targz(self):
        self._store_as(self.compress_thread_targz, self.output_listbox_tar_gz, self.compression_method_targz)

    def store_as_lzh(self):
        self._store_as(self.compress_thread_lzh, self.output_listbox_lzh, self.compression_method_lzh)

    def store_as_iso(self):
        self._store_as(self.compress_thread_iso, self.output_listbox_iso, self.compression_method_iso)

    def store_as_tar(self):
        self._store_as(self.compress_thread_tar, self.output_listbox_tar, self.compression_method_tar)

    def store_as_wim(self):
        self._store_as(self.compress_thread_wim, self.output_listbox_wim, self.compression_method_wim)

    def _store_as(self, thread, output_listbox, compression_method):
        if self.folder_listbox.count() == 0:
            self.show_selection_compression_warning()
        elif output_listbox.count() == 0:
            self.show_selection_destination_warning()
            
        elif compression_method is not None:
            new_thread = thread.__class__(thread.executable, self.update_existing, output_listbox, self.folder_listbox, compress_as=True, compression_method=compression_method)
            new_thread.finished.connect(self.on_compress_finished)
            self.start_compression_thread(new_thread)
        else:
            self.show_method_warning()

    def testar_integridade(self):
        selected_files = [self.folder_listbox.item(idx).text() for idx in range(self.folder_listbox.count())]
        compressed_files = [file for file in selected_files if file.lower().endswith(('.rar', '.zip', '.7z', '.tar.bz2', '.zipx', '.tar.xz', '.tgz', '.tar.gz', '.lzh', '.iso', '.tar', '.wim'))]

        if not compressed_files:
            self.show_extension_warning()
            return

        if self.sevenzip_executable and compressed_files:
            self.teste_integridade_thread = TesteIntegridade(self.sevenzip_executable, self.bandizip_executable, compressed_files)
            self.teste_integridade_thread.finished.connect(self.on_teste_integridade_finished)
            self.teste_integridade_thread.start()
        elif self.bandizip_executable and compressed_files:
            self.teste_integridade_thread = TesteIntegridade(self.bandizip_executable, self.sevenzip_executable, compressed_files)
            self.teste_integridade_thread.finished.connect(self.on_teste_integridade_finished)
            self.teste_integridade_thread.start()
        else:
            self.show_integridade_warning()

    def extract_files(self):
        if self.folder_listbox.count() == 0:
            self.show_selection_descompression_warning()
        elif self.output_listbox_extracao.count() == 0:
            self.show_selection_destination_warning()
        else:
            self._start_extraction_thread()

    def _start_extraction_thread(self):
        if self.winrar_executable:
            self.extract_thread = Extracao(self.winrar_executable, self.sevenzip_executable, self.bandizip_executable, self.output_listbox_extracao, self.folder_listbox)
        elif self.sevenzip_executable:
            self.extract_thread = Extracao(self.sevenzip_executable, self.winrar_executable, self.bandizip_executable, self.output_listbox_extracao, self.folder_listbox)
        elif self.bandizip_executable:
            self.extract_thread = Extracao(self.bandizip_executable, self.winrar_executable, self.sevenzip_executable, self.output_listbox_extracao, self.folder_listbox)
        else:
            self.show_extract_warning()
            return

        self.extract_thread.finished.connect(self.on_extract_finished)
        self.extract_thread.start()

    def start_compression_thread(self, new_thread):
        new_format = new_thread.format

        if any(thread.isRunning() and thread.format == new_format for thread in self.compress_threads):
            self.compress_queue.put(new_thread)
            self.show_queue_warning()
        else:
            new_thread.start()
            self.compress_threads.append(new_thread)

    def on_compress_finished(self):
        finished_thread = self.sender()
        self.compress_threads.remove(finished_thread)

        if not self.compress_queue.empty():
            next_thread = self.compress_queue.get()
            self.start_compression_thread(next_thread)
        elif not self.compress_threads:
            self.show_info_message("Empacotamento Concluído", "O Empacotamento dos arquivos foi concluído com sucesso!")

    def on_teste_integridade_finished(self):
        self.show_info_message("Teste de Integridade Concluído", "O teste de integridade dos arquivos foi concluído com sucesso!")

    def on_extract_finished(self):
        self.show_info_message("Extração Concluída", "A Extração dos arquivos foi concluída com sucesso!")

    def show_queue_warning(self):
        self.show_warning("Aviso", "O processo solicitado foi colocado em fila, aguardando o anterior encerrar.")

    def show_method_warning(self):
        self.show_warning("Aviso", "Por favor, selecione um método de compressão antes de prosseguir.")

    def show_integridade_warning(self):
        self.show_warning("Aviso", "Por favor, selecione um arquivo para testar a integridade.")

    def show_extension_warning(self):
        self.show_warning("Aviso", "Por favor, selecione um arquivo COMPACTADO para prosseguir.")

    def show_extract_warning(self):
        self.show_warning("Aviso", "Nenhum dos programas (WinRAR, 7-Zip ou BandiZip) encontrado. Por favor, instale um deles e tente novamente.")

    def show_selection_compression_warning(self):
        self.show_warning("Aviso", "Por favor, selecione uma pasta antes de prosseguir.")

    def show_selection_descompression_warning(self):
        self.show_warning("Aviso", "Por favor, selecione um arquivo antes de prosseguir.")

    def show_selection_destination_warning(self):
        self.show_warning("Aviso", "Por favor, selecione um diretório de saída antes de prosseguir.")

    def show_warning(self, title, message):
        self.show_message(QMessageBox.Icon.Warning, title, message)

    def show_info_message(self, title, message):
        self.show_message(QMessageBox.Icon.Information, title, message)

    def show_message(self, icon, title, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()
