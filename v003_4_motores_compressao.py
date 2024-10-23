import os
import sys
import subprocess
import tempfile
from PyQt6.QtCore import QThread, pyqtSignal


def buscar_winrar_executavel():
    dir_atual = getattr(sys, '_MEIPASS', os.path.dirname(os.path.realpath(__file__)))

    winrar_path = os.path.join(dir_atual, "WinRAR")

    caminho_winrar = os.path.join(winrar_path, 'WinRAR.exe')

    if os.path.exists(caminho_winrar):
        return caminho_winrar

    possible_locations = [
        rf"C:\Program Files\WinRAR\WinRAR.exe",
        rf"C:\Program Files (x86)\WinRAR\WinRAR.exe",
    ]

    for location in possible_locations:
        if os.path.isfile(location):
            return location

    return None


def buscar_sevenzip_executavel():
    dir_atual = getattr(sys, '_MEIPASS', os.path.dirname(os.path.realpath(__file__)))

    sevenzip_path = os.path.join(dir_atual, "7-Zip")

    caminho_sevenzip = os.path.join(sevenzip_path, '7zG.exe')

    if os.path.exists(caminho_sevenzip):
        return caminho_sevenzip

    possible_locations = [
        rf"C:\Program Files\7-Zip\7zG.exe",
        rf"C:\Program Files (x86)\7-Zip\7zG.exe",
    ]

    for location in possible_locations:
        if os.path.isfile(location):
            return location

    return None


def buscar_bandizip_executavel():
    dir_atual = getattr(sys, '_MEIPASS', os.path.dirname(os.path.realpath(__file__)))

    bandizip_path = os.path.join(dir_atual, "Bandizip")

    caminho_bandizip = os.path.join(bandizip_path, 'Bandizip.exe')

    if os.path.exists(caminho_bandizip):
        return caminho_bandizip
    
    possible_locations = [
        rf"C:\Program Files\Bandizip\Bandizip.exe",
        rf"C:\Program Files (x86)\Bandizip\Bandizip.exe",
    ]

    for location in possible_locations:
        if os.path.isfile(location):
            return location
        
    return None


class CompressaoRAR(QThread):
    finished = pyqtSignal()

    def __init__(self, winrar_executable, update_existing, output_listbox, folder_listbox,
                 compress_as_rar=False, compression_method=None):

        super(CompressaoRAR, self).__init__()
        self.format = "rar"
        self.winrar_executable = winrar_executable
        self.update_existing = update_existing
        self.output_listbox = output_listbox
        self.folder_listbox = folder_listbox
        self.compress_as_rar = compress_as_rar
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
                compressed_file_rar = os.path.join(output_path, f"{folder_name}.rar")
                command = f'"{self.winrar_executable}" a -r -ep1 -m{self.compression_method} -afrar "{compressed_file_rar}" "{folder_path}"'

                if self.update_existing:
                    command = f'"{self.winrar_executable}" u -r -ep1 -m{self.compression_method} -afrar "{compressed_file_rar}" "{folder_path}"'

                subprocess.run(command, shell=True)
                compressed_files.append(compressed_file_rar)

        self.finished.emit()


class CompressaoZIP(QThread):
    finished = pyqtSignal()

    def __init__(self, sevenzip_executable, update_existing, output_listbox, folder_listbox,
                 compress_as_zip=False, compression_method=None):

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

    def __init__(self, sevenzip_executable, update_existing, output_listbox, folder_listbox,
                 compress_as_7z=False, compression_method=None):

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


class CompressaoBZip2(QThread):
    finished = pyqtSignal()

    def __init__(self, sevenzip_executable, update_existing, output_listbox, folder_listbox,
                 compress_as_bzip2=False, compression_method=None):
        
        super(CompressaoBZip2, self).__init__()
        self.format = "tar.bz2"
        self.sevenzip_executable = sevenzip_executable
        self.update_existing = update_existing
        self.output_listbox = output_listbox
        self.folder_listbox = folder_listbox
        self.compress_as_bzip2 = compress_as_bzip2
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
                try:
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_tar_path = os.path.join(temp_dir, f"{folder_name}.tar")
                        compressed_file_bz2 = os.path.join(output_path, f"{folder_name}.tar.bz2")

                        tar_command = [self.sevenzip_executable, "a", "-r", "-ttar", temp_tar_path, folder_path]
                        subprocess.run(tar_command, shell=True)

                        if self.compress_as_bzip2:
                            command = [self.sevenzip_executable, "a", "-r", "-tbzip2", f"-mx={self.compression_method}", compressed_file_bz2, temp_tar_path]
                            subprocess.run(command, shell=True)
                            os.remove(temp_tar_path)

                        elif self.update_existing:
                            command = [self.sevenzip_executable, "u", "-r", "-tbzip2", f"-mx={self.compression_method}", compressed_file_bz2, folder_path]
                            subprocess.run(command, shell=True)

                        compressed_files.append(compressed_file_bz2)

                except (PermissionError, subprocess.CalledProcessError) as e:
                    print(f"Erro ao processar {folder_path}: {e}")

        self.finished.emit()


class CompressaoZIPX(QThread):
    finished = pyqtSignal()

    def __init__(self, bandizip_executable, update_existing, output_listbox, folder_listbox,
                 compress_as_zipx=False, compression_method=None):
            
            super(CompressaoZIPX, self).__init__()
            self.format = "zipx"
            self.bandizip_executable = bandizip_executable
            self.update_existing = update_existing
            self.output_listbox = output_listbox
            self.folder_listbox = folder_listbox
            self.compress_as_zipx = compress_as_zipx
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
                compressed_file_zipx = os.path.join(output_path, f"{folder_name}.zipx")
                command = f'"{self.bandizip_executable}" c -fmt:zipx -r -y -l:{self.compression_method} -storeroot:yes "{compressed_file_zipx}" "{folder_path}"'

                if self.update_existing:
                    command = f'"{self.bandizip_executable}" a -fmt:zipx -r -l:{self.compression_method} -storeroot:yes "{compressed_file_zipx}" "{folder_path}"'

                subprocess.run(command, shell=True)
                compressed_files.append(compressed_file_zipx)

        self.finished.emit()


class CompressaoTarXZ(QThread):
    finished = pyqtSignal()

    def __init__(self, bandizip_executable, update_existing, output_listbox, folder_listbox,
                 compress_as_tarxz=False, compression_method=None):
        
        super(CompressaoTarXZ, self).__init__()
        self.format = "tar.xz"
        self.bandizip_executable = bandizip_executable
        self.update_existing = update_existing
        self.output_listbox = output_listbox
        self.folder_listbox = folder_listbox
        self.compress_as_tarxz = compress_as_tarxz
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
                try:
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_tar_path = os.path.join(temp_dir, f"{folder_name}.tar")
                        compressed_file_tarxz = os.path.join(output_path, f"{folder_name}.tar.xz")

                        tar_command = [self.bandizip_executable, "c", '-fmt:tar', "-r", '-y', f'-l:{self.compression_method}', '-storeroot:yes', temp_tar_path, folder_path]
                        subprocess.run(tar_command, shell=True)

                        if self.compress_as_tarxz:
                            command = [self.bandizip_executable, 'c', '-fmt:xz', '-r', '-y', f'-l:{self.compression_method}', '-storeroot:yes', compressed_file_tarxz, temp_tar_path]
                            subprocess.run(command, shell=True)
                            os.remove(temp_tar_path)

                        elif self.update_existing:
                            command = [self.bandizip_executable, 'a', '-fmt:xz', '-r', '-y', f'-l:{self.compression_method}', '-storeroot:yes', compressed_file_tarxz, folder_path]
                            subprocess.run(command, shell=False)

                        compressed_files.append(compressed_file_tarxz)

                except (PermissionError, subprocess.CalledProcessError) as e:
                    print(f"Erro ao processar {folder_path}: {e}")
        
        self.finished.emit()


class CompressaoTGZ(QThread):
    finished = pyqtSignal()

    def __init__(self, bandizip_executable, update_existing, output_listbox, folder_listbox,
                 compress_as_tgz=False, compression_method=None):
    
            super(CompressaoTGZ, self).__init__()
            self.format = "tgz"
            self.bandizip_executable = bandizip_executable
            self.update_existing = update_existing
            self.output_listbox = output_listbox
            self.folder_listbox = folder_listbox
            self.compress_as_tgz = compress_as_tgz
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
                compressed_file_tgz = os.path.join(output_path, f"{folder_name}.tgz")
                command = f'"{self.bandizip_executable}" c -fmt:tgz -r -y -l:{self.compression_method} -storeroot:yes "{compressed_file_tgz}" "{folder_path}"'

                if self.update_existing:
                    command = f'"{self.bandizip_executable}" a -fmt:tgz -r -l:{self.compression_method} -storeroot:yes "{compressed_file_tgz}" "{folder_path}"'

                subprocess.run(command, shell=True)
                compressed_files.append(compressed_file_tgz)

        self.finished.emit()


class CompressaoTarGZ(QThread):
    finished = pyqtSignal()

    def __init__(self, bandizip_executable, update_existing, output_listbox, folder_listbox,
                 compress_as_targz=False, compression_method=None):
        
        super(CompressaoTarGZ, self).__init__()
        self.format = "tar.gz"
        self.bandizip_executable = bandizip_executable
        self.update_existing = update_existing
        self.output_listbox = output_listbox
        self.folder_listbox = folder_listbox
        self.compress_as_targz = compress_as_targz
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
                try:
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_tar_path = os.path.join(temp_dir, f"{folder_name}.tar")
                        compressed_file_targz = os.path.join(output_path, f"{folder_name}.tar.gz")

                        tar_command = [self.bandizip_executable, "c", '-fmt:tar', "-r", '-y', f'-l:{self.compression_method}', '-storeroot:yes', temp_tar_path, folder_path]
                        subprocess.run(tar_command, shell=True)

                        if self.compress_as_targz:
                            command = [self.bandizip_executable, 'c', '-fmt:gz', '-r', '-y', f'-l:{self.compression_method}', '-storeroot:yes', compressed_file_targz, temp_tar_path]
                            subprocess.run(command, shell=True)
                            os.remove(temp_tar_path)

                        elif self.update_existing:
                            command = [self.bandizip_executable, 'a', '-fmt:gz', '-r', '-y', f'-l:{self.compression_method}', '-storeroot:yes', compressed_file_targz, folder_path]
                            subprocess.run(command, shell=False)

                        compressed_files.append(compressed_file_targz)

                except (PermissionError, subprocess.CalledProcessError) as e:
                    print(f"Erro ao processar {folder_path}: {e}")
        
        self.finished.emit()


class CompressaoLZH(QThread):
    finished = pyqtSignal()

    def __init__(self, bandizip_executable, update_existing, output_listbox, folder_listbox,
                 compress_as_lzh=False, compression_method=None):
            
            super(CompressaoLZH, self).__init__()
            self.format = "lzh"
            self.bandizip_executable = bandizip_executable
            self.update_existing = update_existing
            self.output_listbox = output_listbox
            self.folder_listbox = folder_listbox
            self.compress_as_lzh = compress_as_lzh
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
                compressed_file_lzh = os.path.join(output_path, f"{folder_name}.lzh")
                command = f'"{self.bandizip_executable}" c -fmt:lzh -r -y -l:{self.compression_method} -storeroot:yes "{compressed_file_lzh}" "{folder_path}"'

                if self.update_existing:
                    command = f'"{self.bandizip_executable}" a -fmt:lzh -r -l:{self.compression_method} -storeroot:yes "{compressed_file_lzh}" "{folder_path}"'

                subprocess.run(command, shell=True)
                compressed_files.append(compressed_file_lzh)

        self.finished.emit()


class CompressaoISO(QThread):
    finished = pyqtSignal()

    def __init__(self, bandizip_executable, update_existing, output_listbox, folder_listbox,
                 compress_as_iso=False, compression_method=None):
                
                super(CompressaoISO, self).__init__()
                self.format = "iso"
                self.bandizip_executable = bandizip_executable
                self.update_existing = update_existing
                self.output_listbox = output_listbox
                self.folder_listbox = folder_listbox
                self.compress_as_iso = compress_as_iso
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
                compressed_file_iso = os.path.join(output_path, f"{folder_name}.iso")
                command = f'"{self.bandizip_executable}" c -fmt:iso -r -y -l:{self.compression_method} -storeroot:yes "{compressed_file_iso}" "{folder_path}"'

                if self.update_existing:
                    command = f'"{self.bandizip_executable}" a -fmt:iso -r -l:{self.compression_method} -storeroot:yes "{compressed_file_iso}" "{folder_path}"'

                subprocess.run(command, shell=True)
                compressed_files.append(compressed_file_iso)

        self.finished.emit()


class CompressaoTAR(QThread):
    finished = pyqtSignal()

    def __init__(self, sevenzip_executable, update_existing, output_listbox, folder_listbox,
                 compress_as_tar=False, compression_method=None):

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


class CompressaoWIM(QThread):
    finished = pyqtSignal()

    def __init__(self, sevenzip_executable, update_existing, output_listbox, folder_listbox, 
                 compress_as_wim=False, compression_method=None):
        
        super(CompressaoWIM, self).__init__()
        self.format = "wim"
        self.sevenzip_executable = sevenzip_executable
        self.update_existing = update_existing
        self.output_listbox = output_listbox
        self.folder_listbox = folder_listbox
        self.compress_as_wim = compress_as_wim
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
                compressed_file_wim = os.path.join(output_path, f"{folder_name}.wim")
                command = f'"{self.sevenzip_executable}" a -r -twim "{compressed_file_wim}" "{folder_path}"'

                if self.update_existing:
                    command = f'"{self.sevenzip_executable}" u -r -twim "{compressed_file_wim}" "{folder_path}"'

                subprocess.run(command, shell=True)
                compressed_files.append(compressed_file_wim)

        self.finished.emit()


class TesteIntegridade(QThread):
    finished = pyqtSignal()

    def __init__(self, sevenzip_executable, bandizip_executable, compressed_files):

        super(TesteIntegridade, self).__init__()
        self.sevenzip_executable = sevenzip_executable
        self.bandizip_executable = bandizip_executable
        self.compressed_files = compressed_files

    def run(self):
        for compressed_file in self.compressed_files:
            
            if compressed_file.endswith(".rar"):
                command = f'"{self.sevenzip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")
                
            elif compressed_file.endswith(".zip"):
                command = f'"{self.sevenzip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")

            elif compressed_file.endswith(".7z"):
                command = f'"{self.sevenzip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")
            
            elif compressed_file.endswith(".bz2"):
                command = f'"{self.sevenzip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")
            
            elif compressed_file.endswith(".tar.xz"):
                command = f'"{self.bandizip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")
                
            elif compressed_file.endswith(".zipx"):
                command = f'"{self.bandizip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")
                
            elif compressed_file.endswith(".tgz"):
                command = f'"{self.bandizip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")
                
            elif compressed_file.endswith(".tar.gz"):
                command = f'"{self.bandizip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")
                
            elif compressed_file.endswith(".lzh"):
                command = f'"{self.bandizip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")
                
            elif compressed_file.endswith(".iso"):
                command = f'"{self.bandizip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")

            elif compressed_file.endswith(".tar"):
                command = f'"{self.sevenzip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")
            
            elif compressed_file.endswith(".wim"):
                command = f'"{self.sevenzip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")

        self.finished.emit()


class Extracao(QThread):
    finished = pyqtSignal()

    def __init__(self, winrar_executable, sevenzip_executable, bandizip_executable,
                 output_listbox, folder_listbox):
        
        super(Extracao, self).__init__()
        self.winrar_executable = winrar_executable
        self.sevenzip_executable = sevenzip_executable
        self.bandizip_executable = bandizip_executable
        self.output_listbox = output_listbox
        self.folder_listbox = folder_listbox

    def run(self):
        output_paths = [self.output_listbox.item(idx).text() for idx in range(self.output_listbox.count())]
        if not output_paths:
            return

        for idx in range(self.folder_listbox.count()):
            archive_path = self.folder_listbox.item(idx).text()

            for output_path in output_paths:
                if archive_path.endswith(".rar"):
                    command = f'"{self.winrar_executable}" x -y "{archive_path}" "{output_path}"'
                    subprocess.run(command, shell=True)

                elif archive_path.endswith(".zip"):
                    command = f'"{self.sevenzip_executable}" x -y "{archive_path}" -o"{output_path}"'
                    subprocess.run(command, shell=True)

                elif archive_path.endswith(".7z"):
                    command = f'"{self.sevenzip_executable}" x -y "{archive_path}" -o"{output_path}"'
                    subprocess.run(command, shell=True)
                
                elif archive_path.endswith(".bz2"):
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_tar_path = os.path.join(temp_dir, os.path.basename(archive_path).replace('.bz2', ''))
                        command = f'"{self.sevenzip_executable}" x -y "{archive_path}" -o"{temp_dir}"'
                        subprocess.run(command, shell=True)
                        
                        command = f'"{self.sevenzip_executable}" x -y "{temp_tar_path}" -o"{output_path}"'
                        subprocess.run(command, shell=True)
                
                elif archive_path.endswith(".tar.xz"):
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_tar_path = os.path.join(temp_dir, os.path.basename(archive_path).replace('.xz', ''))
                        command = f'"{self.bandizip_executable}" x -o:"{temp_dir}" "{archive_path}"'
                        subprocess.run(command, shell=True)
                        
                        command = f'"{self.bandizip_executable}" x -o:"{output_path}" "{temp_tar_path}"'
                        subprocess.run(command, shell=True)

                elif archive_path.endswith(".zipx"):
                    command = f'"{self.bandizip_executable}" x -o:"{output_path}" "{archive_path}"'
                    subprocess.run(command, shell=True)

                elif archive_path.endswith(".tgz"):
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_tar_path = os.path.join(temp_dir, os.path.basename(archive_path).replace('.tgz', '.tar'))
                        command = f'"{self.bandizip_executable}" x -o:"{temp_dir}" "{archive_path}"'
                        subprocess.run(command, shell=True)
                        
                        command = f'"{self.bandizip_executable}" x -o:"{output_path}" "{temp_tar_path}"'
                        subprocess.run(command, shell=True)

                elif archive_path.endswith(".tar.gz"):
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_tar_path = os.path.join(temp_dir, os.path.basename(archive_path).replace('.gz', ''))
                        command = f'"{self.bandizip_executable}" x -o:"{temp_dir}" "{archive_path}"'
                        subprocess.run(command, shell=True)
                        
                        command = f'"{self.bandizip_executable}" x -o:"{output_path}" "{temp_tar_path}"'
                        subprocess.run(command, shell=True)

                elif archive_path.endswith(".lzh"):
                    command = f'"{self.bandizip_executable}" x -o:"{output_path}" "{archive_path}"'
                    subprocess.run(command, shell=True)

                elif archive_path.endswith(".iso"):
                    command = f'"{self.bandizip_executable}" x -o:"{output_path}" "{archive_path}"'
                    subprocess.run(command, shell=True)

                elif archive_path.endswith(".tar"):
                    command = f'"{self.sevenzip_executable}" x -y "{archive_path}" -o"{output_path}"'
                    subprocess.run(command, shell=True)
                
                elif archive_path.endswith(".wim"):
                    command = f'"{self.sevenzip_executable}" x -y "{archive_path}" -o"{output_path}"'
                    subprocess.run(command, shell=True)

        self.finished.emit()
