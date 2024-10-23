from PyQt6.QtWidgets import (QMainWindow, QListWidget, QFileDialog, QWidget, QTreeView, QMessageBox)
from PyQt6.QtCore import QThread
from queue import Queue
from v003_4_motores_compressao import (buscar_winrar_executavel, buscar_sevenzip_executavel, buscar_bandizip_executavel,
                                       CompressaoRAR, CompressaoZIP, Compressao7Z, CompressaoBZip2, CompressaoTarXZ,
                                       CompressaoTarGZ, CompressaoZIPX, CompressaoTGZ, CompressaoLZH, CompressaoISO,
                                       CompressaoTAR, CompressaoWIM, TesteIntegridade, Extracao)


class GerenciadorInterface(QThread, QMainWindow):
    def __init__(self, main_window):
        super(GerenciadorInterface, self).__init__()
        self.main_window = main_window
        self.compress_queue = Queue()
        self.compress_thread_rar = None
        self.compress_thread_zip = None
        self.compress_thread_7z = None
        self.compress_thread_bzip2 = None
        self.compress_thread_zipx = None
        self.compress_thread_tarxz = None
        self.compress_thread_tgz = None
        self.compress_thread_targz = None
        self.compress_thread_lzh = None
        self.compress_thread_iso = None
        self.compress_thread_tar = None
        self.compress_thread_wim = None
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

        if not self.winrar_executable and not self.sevenzip_executable:
            print("Nenhum dos programas (WinRAR, 7-Zip ou Bandizip) encontrado. Por favor, instale um deles e tente novamente.")
            exit(1)

        self.output_listbox_rar = QListWidget()
        self.output_listbox_zip = QListWidget()
        self.output_listbox_7z = QListWidget()
        self.output_listbox_bzip2 = QListWidget()
        self.output_listbox_zipx = QListWidget()
        self.output_listbox_tarxz = QListWidget()
        self.output_listbox_tgz = QListWidget()
        self.output_listbox_targz = QListWidget()
        self.output_listbox_lzh = QListWidget()
        self.output_listbox_iso = QListWidget()
        self.output_listbox_tar = QListWidget()
        self.output_listbox_wim = QListWidget()
        self.output_listbox = QListWidget()
        self.folder_listbox = QListWidget()
        self.output_listbox_extract = QListWidget()
        self.compressed_files = []
        self.compress_threads = []

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

    def browse_folder(self, main_window):
        folder_dialog = QFileDialog(main_window, "Selecionar Pastas")
        folder_dialog.setFileMode(QFileDialog.FileMode.Directory)
        folder_dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        folder_dialog.setOption(QFileDialog.Option.ReadOnly, True)
        folder_dialog.setOption(QFileDialog.Option.HideNameFilterDetails, True)
        folder_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        folder_dialog.setOption(QFileDialog.Option.DontResolveSymlinks, True)
        folder_dialog.setLabelText(QFileDialog.DialogLabel.Accept, "Selecionar")
        folder_dialog.setLabelText(QFileDialog.DialogLabel.Reject, "Cancelar")
        folder_dialog.setSizeGripEnabled(False)

        tree_view = folder_dialog.findChild(QTreeView)

        if tree_view:
            assert isinstance(tree_view, QTreeView)
            tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)

        if folder_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_folders = folder_dialog.selectedFiles()
            self.folder_listbox.addItems(selected_folders)

    def browse_file(self, main_window):
        file_dialog = QFileDialog(main_window, "Selecionar Arquivos")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("Todos os Arquivos (*.*)")
        file_dialog.setOption(QFileDialog.Option.ReadOnly, True)
        file_dialog.setOption(QFileDialog.Option.HideNameFilterDetails, True)
        file_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        file_dialog.setOption(QFileDialog.Option.DontResolveSymlinks, True)
        file_dialog.setLabelText(QFileDialog.DialogLabel.Accept, "Selecionar")
        file_dialog.setLabelText(QFileDialog.DialogLabel.Reject, "Cancelar")
        file_dialog.setSizeGripEnabled(False)

        tree_view = file_dialog.findChild(QTreeView)

        if tree_view:
            assert isinstance(tree_view, QTreeView)
            tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            self.folder_listbox.addItems(selected_files)

    def clear_folders(self):
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

        tree_view = output_dialog.findChild(QTreeView)

        if tree_view:
            assert isinstance(tree_view, QTreeView)
            tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)

        if output_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_output = output_dialog.selectedFiles()
            self.output_listbox.addItems(selected_output)
            self.output_listbox_rar.addItems(selected_output)
            self.output_listbox_zip.addItems(selected_output)
            self.output_listbox_7z.addItems(selected_output)
            self.output_listbox_bzip2.addItems(selected_output)
            self.output_listbox_zipx.addItems(selected_output)
            self.output_listbox_tarxz.addItems(selected_output)
            self.output_listbox_tgz.addItems(selected_output)
            self.output_listbox_targz.addItems(selected_output)
            self.output_listbox_lzh.addItems(selected_output)
            self.output_listbox_iso.addItems(selected_output)
            self.output_listbox_tar.addItems(selected_output)
            self.output_listbox_wim.addItems(selected_output)
            self.output_listbox_extract.addItems(selected_output)

    def clear_output(self):
        self.output_listbox.clear()
        self.output_listbox_rar.clear()
        self.output_listbox_zip.clear()
        self.output_listbox_7z.clear()
        self.output_listbox_bzip2.clear()
        self.output_listbox_zipx.clear()
        self.output_listbox_tarxz.clear()
        self.output_listbox_tgz.clear()
        self.output_listbox_targz.clear()
        self.output_listbox_lzh.clear()
        self.output_listbox_iso.clear()
        self.output_listbox_tar.clear()
        self.output_listbox_wim.clear()
        self.output_listbox_extract.clear()

    def clear_output_listbox_rar(self):
        self.output_listbox_rar.clear()

    def clear_output_listbox_zip(self):
        self.output_listbox_zip.clear()

    def clear_output_listbox_7z(self):
        self.output_listbox_7z.clear()

    def clear_output_listbox_bzip2(self):
        self.output_listbox_bzip2.clear()

    def clear_output_listbox_zipx(self):
        self.output_listbox_zipx.clear()

    def clear_output_listbox_tarxz(self):
        self.output_listbox_tarxz.clear()

    def clear_output_listbox_tgz(self):
        self.output_listbox_tgz.clear()

    def clear_output_listbox_targz(self):
        self.output_listbox_targz.clear()

    def clear_output_listbox_lzh(self):
        self.output_listbox_lzh.clear()

    def clear_output_listbox_iso(self):
        self.output_listbox_iso.clear()

    def clear_output_listbox_tar(self):
        self.output_listbox_tar.clear()

    def clear_output_listbox_wim(self):
        self.output_listbox_wim.clear()

    def clear_output_listbox_extract(self):
        self.output_listbox_extract.clear()

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

        tree_view = output_dialog.findChild(QTreeView)
        
        if tree_view:
            assert isinstance(tree_view, QTreeView)
            tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)

        if output_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_output = output_dialog.selectedFiles()
            output_listbox.addItems(selected_output)

    def output_button_output_RAR_clicked(self):
        self.select_output_path(self.output_listbox_rar, self.main_window)

    def output_button_output_ZIP_clicked(self):
        self.select_output_path(self.output_listbox_zip, self.main_window)

    def output_button_output_7Z_clicked(self):
        self.select_output_path(self.output_listbox_7z, self.main_window)
    
    def output_button_output_BZIP2_clicked(self):
        self.select_output_path(self.output_listbox_bzip2, self.main_window)

    def output_button_output_ZIPX_clicked(self):
        self.select_output_path(self.output_listbox_zipx, self.main_window)

    def output_button_output_TarXZ_clicked(self):
        self.select_output_path(self.output_listbox_tarxz, self.main_window)

    def output_button_output_TGZ_clicked(self):
        self.select_output_path(self.output_listbox_tgz, self.main_window)

    def output_button_output_TarGZ_clicked(self):
        self.select_output_path(self.output_listbox_targz, self.main_window)

    def output_button_output_LZH_clicked(self):
        self.select_output_path(self.output_listbox_lzh, self.main_window)

    def output_button_output_ISO_clicked(self):
        self.select_output_path(self.output_listbox_iso, self.main_window)

    def output_button_output_TAR_clicked(self):
        self.select_output_path(self.output_listbox_tar, self.main_window)
    
    def output_button_output_WIM_clicked(self):
        self.select_output_path(self.output_listbox_wim, self.main_window)

    def output_button_output_EXTRACT_clicked(self):
        self.select_output_path(self.output_listbox_extract, self.main_window)

    def store_as_rar(self):
        if self.folder_listbox.count() == 0:
            self.show_selection_compression_warning()

        elif self.output_listbox_rar.count() == 0:
            self.show_selection_destination_warning()

        elif self.compression_method_rar is not None:
            new_compress_thread = CompressaoRAR(
                self.winrar_executable, self.update_existing, self.output_listbox_rar, self.folder_listbox,
                compress_as_rar=True, compression_method=self.compression_method_rar
            )
            new_compress_thread.finished.connect(self.on_compress_finished)
            self.start_compression_thread(new_compress_thread)

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
        
    def store_as_bzip2(self):
        if self.folder_listbox.count() == 0:
            self.show_selection_compression_warning()

        elif self.output_listbox_bzip2.count() == 0:
            self.show_selection_destination_warning()

        elif self.compression_method_bzip2 is not None:
            new_compress_thread = CompressaoBZip2(
                self.sevenzip_executable, self.update_existing, self.output_listbox_bzip2, self.folder_listbox,
                compress_as_bzip2=True, compression_method=self.compression_method_bzip2
            )
            new_compress_thread.finished.connect(self.on_compress_finished)
            self.start_compression_thread(new_compress_thread)

        else:
            self.show_method_warning()

    def store_as_zipx(self):
        if self.folder_listbox.count() == 0:
            self.show_selection_compression_warning()

        elif self.output_listbox_zipx.count() == 0:
            self.show_selection_destination_warning()

        elif self.compression_method_zipx is not None:
            new_compress_thread = CompressaoZIPX(
                self.bandizip_executable, self.update_existing, self.output_listbox_zipx, self.folder_listbox,
                compress_as_zipx=True, compression_method=self.compression_method_zipx
            )
            new_compress_thread.finished.connect(self.on_compress_finished)
            self.start_compression_thread(new_compress_thread)

        else:
            self.show_method_warning()

    def store_as_tarxz(self):
        if self.folder_listbox.count() == 0:
            self.show_selection_compression_warning()

        elif self.output_listbox_tarxz.count() == 0:
            self.show_selection_destination_warning()

        elif self.compression_method_tarxz is not None:
            new_compress_thread = CompressaoTarXZ(
                self.bandizip_executable, self.update_existing, self.output_listbox_tarxz, self.folder_listbox,
                compress_as_tarxz=True, compression_method=self.compression_method_tarxz
            )
            new_compress_thread.finished.connect(self.on_compress_finished)
            self.start_compression_thread(new_compress_thread)

        else:
            self.show_method_warning()

    def store_as_tgz(self):
        if self.folder_listbox.count() == 0:
            self.show_selection_compression_warning()

        elif self.output_listbox_tgz.count() == 0:
            self.show_selection_destination_warning()

        elif self.compression_method_tgz is not None:
            new_compress_thread = CompressaoTGZ(
                self.bandizip_executable, self.update_existing, self.output_listbox_tgz, self.folder_listbox,
                compress_as_tgz=True, compression_method=self.compression_method_tgz
            )
            new_compress_thread.finished.connect(self.on_compress_finished)
            self.start_compression_thread(new_compress_thread)

        else:
            self.show_method_warning()
    
    def store_as_targz(self):
        if self.folder_listbox.count() == 0:
            self.show_selection_compression_warning()

        elif self.output_listbox_targz.count() == 0:
            self.show_selection_destination_warning()

        elif self.compression_method_targz is not None:
            new_compress_thread = CompressaoTarGZ(
                self.bandizip_executable, self.update_existing, self.output_listbox_targz, self.folder_listbox,
                compress_as_targz=True, compression_method=self.compression_method_targz
            )
            new_compress_thread.finished.connect(self.on_compress_finished)
            self.start_compression_thread(new_compress_thread)

        else:
            self.show_method_warning()

    def store_as_lzh(self):
        if self.folder_listbox.count() == 0:
            self.show_selection_compression_warning()

        elif self.output_listbox_lzh.count() == 0:
            self.show_selection_destination_warning()

        elif self.compression_method_lzh is not None:
            new_compress_thread = CompressaoLZH(
                self.bandizip_executable, self.update_existing, self.output_listbox_lzh, self.folder_listbox,
                compress_as_lzh=True, compression_method=self.compression_method_lzh
            )
            new_compress_thread.finished.connect(self.on_compress_finished)
            self.start_compression_thread(new_compress_thread)

        else:
            self.show_method_warning()

    def store_as_iso(self):
        if self.folder_listbox.count() == 0:
            self.show_selection_compression_warning()

        elif self.output_listbox_iso.count() == 0:
            self.show_selection_destination_warning()

        elif self.compression_method_iso is not None:
            new_compress_thread = CompressaoISO(
                self.bandizip_executable, self.update_existing, self.output_listbox_iso, self.folder_listbox,
                compress_as_iso=True, compression_method=self.compression_method_iso
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
    
    def store_as_wim(self):
        if self.folder_listbox.count() == 0:
            self.show_selection_compression_warning()

        elif self.output_listbox_wim.count() == 0:
            self.show_selection_destination_warning()

        elif self.compression_method_wim is not None:
            new_compress_thread = CompressaoWIM(
                self.sevenzip_executable, self.update_existing, self.output_listbox_wim, self.folder_listbox,
                compress_as_wim=True, compression_method=self.compression_method_wim
            )
            new_compress_thread.finished.connect(self.on_compress_finished)
            self.start_compression_thread(new_compress_thread)

        else:
            self.show_method_warning()

    def testar_integridade(self):
        selected_files = []
        for idx in range(self.folder_listbox.count()):
            item = self.folder_listbox.item(idx)
            if item is not None:
                selected_files.append(item.text())

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

        elif self.output_listbox_extract.count() == 0:
            self.show_selection_destination_warning()

        elif self.winrar_executable:
            self.extract_thread = Extracao(
                self.winrar_executable, self.sevenzip_executable, self.bandizip_executable,
                self.output_listbox_extract, self.folder_listbox
            )
            self.extract_thread.finished.connect(self.on_extract_finished)
            self.extract_thread.start()

        elif self.sevenzip_executable:
            self.extract_thread = Extracao(
                self.sevenzip_executable, self.winrar_executable, self.bandizip_executable,
                self.output_listbox_extract, self.folder_listbox
            )
            self.extract_thread.finished.connect(self.on_extract_finished)
            self.extract_thread.start()

        elif self.bandizip_executable:
            self.extract_thread = Extracao(
                self.bandizip_executable, self.winrar_executable, self.sevenzip_executable,
                self.output_listbox_extract, self.folder_listbox
            )
            self.extract_thread.finished.connect(self.on_extract_finished)
            self.extract_thread.start()

        else:
            self.show_extract_warning()

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
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Empacotamento Concluído")
            msg_box.setText("O Empacotamento dos arquivos foi concluído com sucesso!")
            msg_box.exec()

    def on_teste_integridade_finished(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Teste de Integridade Concluído")
        msg_box.setText("O teste de integridade dos arquivos foi concluído com sucesso!")
        msg_box.exec()

    def on_extract_finished(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Extração Concluída")
        msg_box.setText("A Extração dos arquivos foi concluída com sucesso!")
        msg_box.exec()

    def show_queue_warning(self):
        parent = self.parent() if isinstance(self.parent(), QWidget) else QWidget()
        self.show_warning(parent, "Aviso", "O processo solicitado foi colocado em fila, aguardando o anterior encerrar.")

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

    def show_warning(self, parent, title, message):
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()
