import os
import sys
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QListWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class LayoutsCompressao:
    def __init__(self, gerenciador_interface, create_button):
        self.gerenciador_interface = gerenciador_interface
        self.create_button = create_button

    def create_rar_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_rar = self.create_button("Especificar Diretório(s) de Saída .RAR")
        output_button_output_rar.clicked.connect(self.gerenciador_interface.output_button_output_RAR_clicked)
        layout_1.addWidget(output_button_output_rar)

        create_rar_button = self.create_button("Armazenar como .RAR")
        rar_icon_path = os.path.join(icon_path, "winrar3.png")
        create_rar_button.setIcon(QIcon(rar_icon_path))
        create_rar_button.clicked.connect(self.gerenciador_interface.store_as_rar)
        layout_1.addWidget(create_rar_button)

        create_clear_rar_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_rar_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_rar_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_rar)
        layout_1.addWidget(create_clear_rar_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_rar = QLabel("Diretório(s) de saída .RAR:")
        layout_2.addWidget(output_label_rar)
        self.gerenciador_interface.output_listbox_rar = QListWidget()
        self.gerenciador_interface.output_listbox_rar.setMinimumHeight(82)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_rar)
        layout.addLayout(layout_2)

        return layout

    def create_zip_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_zip = self.create_button("Especificar Diretório(s) de Saída .ZIP")
        output_button_output_zip.clicked.connect(self.gerenciador_interface.output_button_output_ZIP_clicked)
        layout_1.addWidget(output_button_output_zip)

        create_zip_button = self.create_button("Armazenar como .ZIP")
        zip_icon_path = os.path.join(icon_path, "winzip4.png")
        create_zip_button.setIcon(QIcon(zip_icon_path))
        create_zip_button.clicked.connect(self.gerenciador_interface.store_as_zip)
        layout_1.addWidget(create_zip_button)

        create_clear_zip_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_zip_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_zip_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_zip)
        layout_1.addWidget(create_clear_zip_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_zip = QLabel("Diretório(s) de saída .ZIP:")
        layout_2.addWidget(output_label_zip)
        self.gerenciador_interface.output_listbox_zip = QListWidget()
        self.gerenciador_interface.output_listbox_zip.setMinimumHeight(82)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_zip)
        layout.addLayout(layout_2)

        return layout

    def create_7z_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_7z = self.create_button("Especificar Diretório(s) de Saída .7Z")
        output_button_output_7z.clicked.connect(self.gerenciador_interface.output_button_output_7Z_clicked)
        layout_1.addWidget(output_button_output_7z)

        create_7z_button = self.create_button("Armazenar como .7Z")
        sevenzip_icon_path = os.path.join(icon_path, "sevenzip4.png")
        create_7z_button.setIcon(QIcon(sevenzip_icon_path))
        create_7z_button.clicked.connect(self.gerenciador_interface.store_as_7z)
        layout_1.addWidget(create_7z_button)

        create_clear_7z_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_7z_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_7z_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_7z)
        layout_1.addWidget(create_clear_7z_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_7z = QLabel("Diretório(s) de saída .7Z:")
        layout_2.addWidget(output_label_7z)
        self.gerenciador_interface.output_listbox_7z = QListWidget()
        self.gerenciador_interface.output_listbox_7z.setMinimumHeight(82)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_7z)
        layout.addLayout(layout_2)

        return layout

    def create_bzip2_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_bzip2 = self.create_button("Especificar Diretório(s) de Saída .Tar.BZ2")
        output_button_output_bzip2.clicked.connect(self.gerenciador_interface.output_button_output_BZIP2_clicked)
        layout_1.addWidget(output_button_output_bzip2)

        create_bzip2_button = self.create_button("Armazenar como .Tar.BZ2")
        bzip2_icon_path = os.path.join(icon_path, "bz2.png")
        create_bzip2_button.setIcon(QIcon(bzip2_icon_path))
        create_bzip2_button.clicked.connect(self.gerenciador_interface.store_as_bzip2)
        layout_1.addWidget(create_bzip2_button)

        create_clear_bzip2_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_bzip2_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_bzip2_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_bzip2)
        layout_1.addWidget(create_clear_bzip2_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_bzip2 = QLabel("Diretório(s) de saída .Tar.BZ2:")
        layout_2.addWidget(output_label_bzip2)
        self.gerenciador_interface.output_listbox_bzip2 = QListWidget()
        self.gerenciador_interface.output_listbox_bzip2.setMinimumHeight(82)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_bzip2)
        layout.addLayout(layout_2)

        return layout

    def create_zipx_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_zipx = self.create_button("Especificar Diretório(s) de Saída .ZIPX")
        output_button_output_zipx.clicked.connect(self.gerenciador_interface.output_button_output_ZIPX_clicked)
        layout_1.addWidget(output_button_output_zipx)

        create_zipx_button = self.create_button("Armazenar como .ZIPX")
        zipx_icon_path = os.path.join(icon_path, "zipx.ico")
        create_zipx_button.setIcon(QIcon(zipx_icon_path))
        create_zipx_button.clicked.connect(self.gerenciador_interface.store_as_zipx)
        layout_1.addWidget(create_zipx_button)

        create_clear_zipx_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_zipx_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_zipx_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_zipx)
        layout_1.addWidget(create_clear_zipx_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_zipx = QLabel("Diretório(s) de saída .ZPIX:")
        layout_2.addWidget(output_label_zipx)
        self.gerenciador_interface.output_listbox_zipx = QListWidget()
        self.gerenciador_interface.output_listbox_zipx.setMinimumHeight(82)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_zipx)
        layout.addLayout(layout_2)

        return layout

    def create_tarxz_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_tarxz = self.create_button("Especificar Diretório(s) de Saída .Tar.XZ")
        output_button_output_tarxz.clicked.connect(self.gerenciador_interface.output_button_output_TarXZ_clicked)
        layout_1.addWidget(output_button_output_tarxz)

        create_tarxz_button = self.create_button("Armazenar como .Tar.XZ")
        tarxz_icon_path = os.path.join(icon_path, "txz.ico")
        create_tarxz_button.setIcon(QIcon(tarxz_icon_path))
        create_tarxz_button.clicked.connect(self.gerenciador_interface.store_as_tarxz)
        layout_1.addWidget(create_tarxz_button)

        create_clear_tarxz_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_tarxz_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_tarxz_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_tarxz)
        layout_1.addWidget(create_clear_tarxz_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_tarxz = QLabel("Diretório(s) de saída .Tar.XZ:")
        layout_2.addWidget(output_label_tarxz)
        self.gerenciador_interface.output_listbox_tarxz = QListWidget()
        self.gerenciador_interface.output_listbox_tarxz.setMinimumHeight(82)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_tarxz)
        layout.addLayout(layout_2)

        return layout

    def create_tgz_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_tgz = self.create_button("Especificar Diretório(s) de Saída .TGZ")
        output_button_output_tgz.clicked.connect(self.gerenciador_interface.output_button_output_TGZ_clicked)
        layout_1.addWidget(output_button_output_tgz)

        create_tgz_button = self.create_button("Armazenar como .TGZ")
        tgz_icon_path = os.path.join(icon_path, "tgz.ico")
        create_tgz_button.setIcon(QIcon(tgz_icon_path))
        create_tgz_button.clicked.connect(self.gerenciador_interface.store_as_tgz)
        layout_1.addWidget(create_tgz_button)

        create_clear_tgz_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_tgz_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_tgz_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_tgz)
        layout_1.addWidget(create_clear_tgz_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_tgz = QLabel("Diretório(s) de saída .TGZ:")
        layout_2.addWidget(output_label_tgz)
        self.gerenciador_interface.output_listbox_tgz = QListWidget()
        self.gerenciador_interface.output_listbox_tgz.setMinimumHeight(82)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_tgz)
        layout.addLayout(layout_2)

        return layout

    def create_targz_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_targz = self.create_button("Especificar Diretório(s) de Saída .Tar.GZ")
        output_button_output_targz.clicked.connect(self.gerenciador_interface.output_button_output_TarGZ_clicked)
        layout_1.addWidget(output_button_output_targz)

        create_targz_button = self.create_button("Armazenar como .Tar.GZ")
        targz_icon_path = os.path.join(icon_path, "gzip1.png")
        create_targz_button.setIcon(QIcon(targz_icon_path))
        create_targz_button.clicked.connect(self.gerenciador_interface.store_as_targz)
        layout_1.addWidget(create_targz_button)

        create_clear_targz_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_targz_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_targz_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_targz)
        layout_1.addWidget(create_clear_targz_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_targz = QLabel("Diretório(s) de saída .Tar.GZ:")
        layout_2.addWidget(output_label_targz)
        self.gerenciador_interface.output_listbox_targz = QListWidget()
        self.gerenciador_interface.output_listbox_targz.setMinimumHeight(82)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_targz)
        layout.addLayout(layout_2)

        return layout

    def create_lzh_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_lzh = self.create_button("Especificar Diretório(s) de Saída .LZH")
        output_button_output_lzh.clicked.connect(self.gerenciador_interface.output_button_output_LZH_clicked)
        layout_1.addWidget(output_button_output_lzh)

        create_lzh_button = self.create_button("Armazenar como .LZH")
        lzh_icon_path = os.path.join(icon_path, "lzh.ico")
        create_lzh_button.setIcon(QIcon(lzh_icon_path))
        create_lzh_button.clicked.connect(self.gerenciador_interface.store_as_lzh)
        layout_1.addWidget(create_lzh_button)

        create_clear_lzh_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_lzh_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_lzh_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_lzh)
        layout_1.addWidget(create_clear_lzh_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_lzh = QLabel("Diretório(s) de saída .LZH:")
        layout_2.addWidget(output_label_lzh)
        self.gerenciador_interface.output_listbox_lzh = QListWidget()
        self.gerenciador_interface.output_listbox_lzh.setMinimumHeight(82)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_lzh)
        layout.addLayout(layout_2)

        return layout

    def create_iso_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_iso = self.create_button("Especificar Diretório(s) de Saída .ISO")
        output_button_output_iso.clicked.connect(self.gerenciador_interface.output_button_output_ISO_clicked)
        layout_1.addWidget(output_button_output_iso)

        create_iso_button = self.create_button("Armazenar como .ISO")
        iso_icon_path = os.path.join(icon_path, "iso.ico")
        create_iso_button.setIcon(QIcon(iso_icon_path))
        create_iso_button.clicked.connect(self.gerenciador_interface.store_as_iso)
        layout_1.addWidget(create_iso_button)

        create_clear_iso_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_iso_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_iso_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_iso)
        layout_1.addWidget(create_clear_iso_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_iso = QLabel("Diretório(s) de saída .ISO:")
        layout_2.addWidget(output_label_iso)
        self.gerenciador_interface.output_listbox_iso = QListWidget()
        self.gerenciador_interface.output_listbox_iso.setMinimumHeight(82)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_iso)
        layout.addLayout(layout_2)

        return layout

    def create_tar_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_tar = self.create_button("Especificar Diretório(s) de Saída .TAR")
        output_button_output_tar.clicked.connect(self.gerenciador_interface.output_button_output_TAR_clicked)
        layout_1.addWidget(output_button_output_tar)

        create_tar_button = self.create_button("Armazenar como .TAR")
        tar_icon_path = os.path.join(icon_path, "tar1.png")
        create_tar_button.setIcon(QIcon(tar_icon_path))
        create_tar_button.clicked.connect(self.gerenciador_interface.store_as_tar)
        layout_1.addWidget(create_tar_button)

        create_clear_tar_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_tar_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_tar_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_tar)
        layout_1.addWidget(create_clear_tar_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_tar = QLabel("Diretório(s) de saída .TAR:")
        layout_2.addWidget(output_label_tar)
        self.gerenciador_interface.output_listbox_tar = QListWidget()
        self.gerenciador_interface.output_listbox_tar.setMinimumHeight(82)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_tar)
        layout.addLayout(layout_2)

        return layout

    def create_wim_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_wim = self.create_button("Especificar Diretório(s) de Saída .WIM")
        output_button_output_wim.clicked.connect(self.gerenciador_interface.output_button_output_WIM_clicked)
        layout_1.addWidget(output_button_output_wim)

        create_wim_button = self.create_button("Armazenar como .WIM")
        wim_icon_path = os.path.join(icon_path, "wim.png")
        create_wim_button.setIcon(QIcon(wim_icon_path))
        create_wim_button.clicked.connect(self.gerenciador_interface.store_as_wim)
        layout_1.addWidget(create_wim_button)

        create_clear_wim_button = self.create_button("Limpar Saída")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_wim_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_wim_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_wim)
        layout_1.addWidget(create_clear_wim_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_wim = QLabel("Diretório(s) de saída .WIM:")
        layout_2.addWidget(output_label_wim)
        self.gerenciador_interface.output_listbox_wim = QListWidget()
        self.gerenciador_interface.output_listbox_wim.setMinimumHeight(82)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_wim)
        layout.addLayout(layout_2)

        return layout

    def create_extract_layout(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()

        output_button_output_extract = self.create_button("Especificar Diretório(s) de Extração")
        output_button_output_extract.clicked.connect(self.gerenciador_interface.output_button_output_EXTRACT_clicked)
        layout_1.addWidget(output_button_output_extract)

        extract_button = self.create_button("Extrair Arquivos e Pastas")
        extracao_icon_path = os.path.join(icon_path, "extracao4.png")
        extract_button.setIcon(QIcon(extracao_icon_path))
        extract_button.clicked.connect(self.gerenciador_interface.extract_files)
        layout_1.addWidget(extract_button)

        create_clear_extract_button = self.create_button("Limpar Saída de EXTRAÇÃO")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        create_clear_extract_button.setIcon(QIcon(limpar_output_icon_path))
        create_clear_extract_button.clicked.connect(self.gerenciador_interface.clear_output_listbox_extract)
        layout_1.addWidget(create_clear_extract_button)

        layout.addLayout(layout_1)
        layout.setAlignment(layout_1, Qt.AlignmentFlag.AlignBottom)

        layout_2 = QVBoxLayout()

        output_label_extract = QLabel("Diretório(s) para Extração:")
        layout_2.addWidget(output_label_extract)
        self.gerenciador_interface.output_listbox_extract = QListWidget()
        self.gerenciador_interface.output_listbox_extract.setMinimumHeight(82)
        layout_2.addWidget(self.gerenciador_interface.output_listbox_extract)
        layout.addLayout(layout_2)

        return layout
