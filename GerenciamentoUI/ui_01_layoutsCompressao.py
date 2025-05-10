import os
import sys
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class LayoutsCompressao:
    def __init__(self, gerenciador_interface, create_button):
        self.gerenciador_interface = gerenciador_interface
        self.create_button = create_button
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        self.icon_path = os.path.join(project_root, "icones")

        if hasattr(sys, "_MEIPASS"):
            self.icon_path = os.path.join(sys._MEIPASS, "icones")

    def create_compression_method_layouts(self):
        methods = ['rar', 'zip', '7z', 'tar.bz2', 'zipx', 'tar.xz', 'tgz', 'tar.gz', 'lzh', 'iso', 'tar', 'wim', 'extracao']
        return {method: getattr(self, f'create_{method.replace(".", "_")}_layout') for method in methods}

    def create_layout(self, method, icon_name, store_callback, clear_callback):
        layout = QHBoxLayout()
        layout_1 = QVBoxLayout()
        layout_2 = QVBoxLayout()

        output_button = self.create_button(f"Especificar Saída .{method.upper()}")
        output_button.clicked.connect(getattr(self.gerenciador_interface, f'output_button_output_{method.upper()}_clicked'))
        layout_1.addWidget(output_button)

        store_button = self.create_button(f"Armazenar .{method.upper()}")
        store_button.setIcon(QIcon(os.path.join(self.icon_path, icon_name)))
        store_button.clicked.connect(store_callback)
        layout_1.addWidget(store_button)

        clear_button = self.create_button("Limpar Saída")
        clear_button.setIcon(QIcon(os.path.join(self.icon_path, "clear_button2.png")))
        clear_button.clicked.connect(clear_callback)
        layout_1.addWidget(clear_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        output_label = QLabel(f"Diretório(s) de saída .{method.upper()}:")
        layout_2.addWidget(output_label)

        listbox = getattr(self.gerenciador_interface, f'output_listbox_{method}')
        listbox.setMinimumHeight(82)
        layout_2.addWidget(listbox)
        layout.addLayout(layout_2)

        return layout

    def create_rar_layout(self):
        return self.create_layout('rar', 'winrar3.png', self.gerenciador_interface.store_as_rar, self.gerenciador_interface.clear_output_listbox_rar)

    def create_zip_layout(self):
        return self.create_layout('zip', 'winzip4.png', self.gerenciador_interface.store_as_zip, self.gerenciador_interface.clear_output_listbox_zip)

    def create_7z_layout(self):
        return self.create_layout('7z', 'sevenzip4.png', self.gerenciador_interface.store_as_7z, self.gerenciador_interface.clear_output_listbox_7z)

    def create_tar_bz2_layout(self):
        return self.create_layout('tar_bz2', 'bz2.png', self.gerenciador_interface.store_as_bzip2, self.gerenciador_interface.clear_output_listbox_bzip2)

    def create_zipx_layout(self):
        return self.create_layout('zipx', 'zipx.ico', self.gerenciador_interface.store_as_zipx, self.gerenciador_interface.clear_output_listbox_zipx)

    def create_tar_xz_layout(self):
        return self.create_layout('tar_xz', 'txz.ico', self.gerenciador_interface.store_as_tarxz, self.gerenciador_interface.clear_output_listbox_tarxz)

    def create_tgz_layout(self):
        return self.create_layout('tgz', 'tgz.ico', self.gerenciador_interface.store_as_tgz, self.gerenciador_interface.clear_output_listbox_tgz)

    def create_tar_gz_layout(self):
        return self.create_layout('tar_gz', 'gzip1.png', self.gerenciador_interface.store_as_targz, self.gerenciador_interface.clear_output_listbox_targz)

    def create_lzh_layout(self):
        return self.create_layout('lzh', 'lzh.ico', self.gerenciador_interface.store_as_lzh, self.gerenciador_interface.clear_output_listbox_lzh)

    def create_iso_layout(self):
        return self.create_layout('iso', 'iso.ico', self.gerenciador_interface.store_as_iso, self.gerenciador_interface.clear_output_listbox_iso)

    def create_tar_layout(self):
        return self.create_layout('tar', 'tar1.png', self.gerenciador_interface.store_as_tar, self.gerenciador_interface.clear_output_listbox_tar)

    def create_wim_layout(self):
        return self.create_layout('wim', 'wim.png', self.gerenciador_interface.store_as_wim, self.gerenciador_interface.clear_output_listbox_wim)

    def create_extracao_layout(self):
        return self.create_layout('extracao', 'extracao4.png', self.gerenciador_interface.extract_files, self.gerenciador_interface.clear_output_listbox_extracao)
