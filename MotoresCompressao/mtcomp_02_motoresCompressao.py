import os
import sys
import subprocess
import tempfile
from PyQt6.QtCore import QThread, pyqtSignal


WINRAR_PATHS = [
    rf"C:\Program Files\WinRAR\WinRAR.exe",
    rf"C:\Program Files (x86)\WinRAR\WinRAR.exe",
]

SEVENZIP_PATHS = [
    rf"C:\Program Files\7-Zip\7zG.exe",
    rf"C:\Program Files (x86)\7-Zip\7zG.exe",
]

BANDIZIP_PATHS = [
    rf"C:\Program Files\Bandizip\Bandizip.exe",
    rf"C:\Program Files (x86)\Bandizip\Bandizip.exe",
]

def buscar_executavel(nome_pasta, nome_executavel, possiveis_caminhos):
    """Busca o executável em diretórios conhecidos."""
    dir_atual = getattr(sys, '_MEIPASS', os.path.dirname(os.path.realpath(__file__)))
    caminho_executavel = os.path.join(dir_atual, nome_pasta, nome_executavel)

    if os.path.exists(caminho_executavel):
        return caminho_executavel

    for caminho in possiveis_caminhos:
        if os.path.isfile(caminho):
            return caminho

    return None

def buscar_winrar_executavel():
    return buscar_executavel("WinRAR", "WinRAR.exe", WINRAR_PATHS)

def buscar_sevenzip_executavel():
    return buscar_executavel("7-Zip", "7zG.exe", SEVENZIP_PATHS)

def buscar_bandizip_executavel():
    return buscar_executavel("Bandizip", "Bandizip.exe", BANDIZIP_PATHS)


class CompressaoBase(QThread):
    finished = pyqtSignal()

    def __init__(self, executable, update_existing, output_listbox, folder_listbox, compress_as=False, compression_method=None):
        super().__init__()
        self.executable = executable
        self.update_existing = update_existing
        self.output_listbox = output_listbox
        self.folder_listbox = folder_listbox
        self.compress_as = compress_as
        self.compression_method = compression_method
        self.format = None

    def run(self):
        output_paths = [self.output_listbox.item(idx).text() for idx in range(self.output_listbox.count())]
        if not output_paths:
            return

        for idx in range(self.folder_listbox.count()):
            folder_path = self.folder_listbox.item(idx).text()
            folder_name = os.path.basename(folder_path)

            for output_path in output_paths:
                self.comprimir(output_path, folder_path, folder_name)

        self.finished.emit()


class CompressaoRAR(CompressaoBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format = 'rar'

    def comprimir(self, output_path, folder_path, folder_name):
        compressed_file = os.path.join(output_path, f"{folder_name}.rar")
        command = f'"{self.executable}" a -r -ep1 -m{self.compression_method} -afrar "{compressed_file}" "{folder_path}"'
        if self.update_existing:
            command = f'"{self.executable}" u -r -ep1 -m{self.compression_method} -afrar "{compressed_file}" "{folder_path}"'
        subprocess.run(command, shell=True)


class CompressaoZIP(CompressaoBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format = 'zip'

    def comprimir(self, output_path, folder_path, folder_name):
        compressed_file = os.path.join(output_path, f"{folder_name}.zip")
        command = f'"{self.executable}" a -r -tzip -mx={self.compression_method} "{compressed_file}" "{folder_path}"'
        if self.update_existing:
            command = f'"{self.executable}" u -r -tzip -mx={self.compression_method} "{compressed_file}" "{folder_path}"'
        subprocess.run(command, shell=True)


class Compressao7Z(CompressaoBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format = '7z'

    def comprimir(self, output_path, folder_path, folder_name):
        compressed_file = os.path.join(output_path, f"{folder_name}.7z")
        command = f'"{self.executable}" a -r -t7z -mx={self.compression_method} "{compressed_file}" "{folder_path}"'
        if self.update_existing:
            command = f'"{self.executable}" u -r -t7z -mx={self.compression_method} "{compressed_file}" "{folder_path}"'
        subprocess.run(command, shell=True)


class CompressaoBZip2(CompressaoBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format = 'tar.bz2'

    def comprimir(self, output_path, folder_path, folder_name):
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_tar_path = os.path.join(temp_dir, f"{folder_name}.tar")
                compressed_file = os.path.join(output_path, f"{folder_name}.tar.bz2")

                tar_command = [self.executable, "a", "-r", "-ttar", temp_tar_path, folder_path]
                subprocess.run(tar_command, shell=True)

                if self.compress_as:
                    command = [self.executable, "a", "-r", "-tbzip2", f"-mx={self.compression_method}", compressed_file, temp_tar_path]
                    subprocess.run(command, shell=True)
                    os.remove(temp_tar_path)
                elif self.update_existing:
                    command = [self.executable, "u", "-r", "-tbzip2", f"-mx={self.compression_method}", compressed_file, folder_path]
                    subprocess.run(command, shell=True)
        except (PermissionError, subprocess.CalledProcessError) as e:
            print(f"Erro ao processar {folder_path}: {e}")


class CompressaoZIPX(CompressaoBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format = 'zipx'

    def comprimir(self, output_path, folder_path, folder_name):
        compressed_file = os.path.join(output_path, f"{folder_name}.zipx")
        command = f'"{self.executable}" c -fmt:zipx -r -y -l:{self.compression_method} -storeroot:yes "{compressed_file}" "{folder_path}"'
        if self.update_existing:
            command = f'"{self.executable}" a -fmt:zipx -r -l:{self.compression_method} -storeroot:yes "{compressed_file}" "{folder_path}"'
        subprocess.run(command, shell=True)


class CompressaoTarXZ(CompressaoBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format = 'tar.xz'

    def comprimir(self, output_path, folder_path, folder_name):
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_tar_path = os.path.join(temp_dir, f"{folder_name}.tar")
                compressed_file = os.path.join(output_path, f"{folder_name}.tar.xz")

                tar_command = [self.executable, "c", '-fmt:tar', "-r", '-y', f'-l:{self.compression_method}', '-storeroot:yes', temp_tar_path, folder_path]
                subprocess.run(tar_command, shell=True)

                if self.compress_as:
                    command = [self.executable, "c", '-fmt:xz', "-r", '-y', f'-l:{self.compression_method}', '-storeroot:yes', compressed_file, temp_tar_path]
                    subprocess.run(command, shell=True)
                    os.remove(temp_tar_path)
                elif self.update_existing:
                    command = [self.executable, 'a', '-fmt:xz', '-r', '-y', f'-l:{self.compression_method}', '-storeroot:yes', compressed_file, folder_path]
                    subprocess.run(command, shell=True)
        except (PermissionError, subprocess.CalledProcessError) as e:
            print(f"Erro ao processar {folder_path}: {e}")


class CompressaoTGZ(CompressaoBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format = 'tgz'

    def comprimir (self, output_path, folder_path, folder_name):
        compressed_file = os.path.join(output_path, f"{folder_name}.tgz")
        command = f'"{self.executable}" c -fmt:tgz -r -y -l:{self.compression_method} -storeroot:yes "{compressed_file}" "{folder_path}"'
        if self.update_existing:
            command = f'"{self.executable}" a -fmt:tgz -r -l:{self.compression_method} -storeroot:yes "{compressed_file}" "{folder_path}"'
        subprocess.run(command, shell=True)


class CompressaoTarGZ(CompressaoBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format = 'tar.gz'

    def comprimir(self, output_path, folder_path, folder_name):
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_tar_path = os.path.join(temp_dir, f"{folder_name}.tar")
                compressed_file = os.path.join(output_path, f"{folder_name}.tar.gz")

                tar_command = [self.executable, "c", '-fmt:tar', "-r", '-y', f'-l:{self.compression_method}', '-storeroot:yes', temp_tar_path, folder_path]
                subprocess.run(tar_command, shell=True)

                if self.compress_as:
                    command = [self.executable, "c", '-fmt:gz', "-r", '-y', f'-l:{self.compression_method}', '-storeroot:yes', compressed_file, temp_tar_path]
                    subprocess.run(command, shell=True)
                    os.remove(temp_tar_path)
                elif self.update_existing:
                    command = [self.executable, 'a', '-fmt:gz', '-r', '-y', f'-l:{self.compression_method}', '-storeroot:yes', compressed_file, folder_path]
                    subprocess.run(command, shell=True)
        except (PermissionError, subprocess.CalledProcessError) as e:
            print(f"Erro ao processar {folder_path}: {e}")


class CompressaoLZH(CompressaoBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format = 'lzh'

    def comprimir(self, output_path, folder_path, folder_name):
        compressed_file = os.path.join(output_path, f"{folder_name}.lzh")
        command = f'"{self.executable}" c -fmt:lzh -r -y -l:{self.compression_method} -storeroot:yes "{compressed_file}" "{folder_path}"'
        if self.update_existing:
            command = f'"{self.executable}" a -fmt:lzh -r -l:{self.compression_method} -storeroot:yes "{compressed_file}" "{folder_path}"'
        subprocess.run(command, shell=True)


class CompressaoISO(CompressaoBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format = 'iso'

    def comprimir(self, output_path, folder_path, folder_name):
        compressed_file = os.path.join(output_path, f"{folder_name}.iso")
        command = f'"{self.executable}" c -fmt:iso -r -y -l:{self.compression_method} -storeroot:yes "{compressed_file}" "{folder_path}"'
        if self.update_existing:
            command = f'"{self.executable}" a -fmt:iso -r -l:{self.compression_method} -storeroot:yes "{compressed_file}" "{folder_path}"'
        subprocess.run(command, shell=True)


class CompressaoTAR(CompressaoBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format = 'tar'

    def comprimir(self, output_path, folder_path, folder_name):
        compressed_file = os.path.join(output_path, f"{folder_name}.tar")
        command = f'"{self.executable}" a -r -ttar "{compressed_file}" "{folder_path}"'
        if self.update_existing:
            command = f'"{self.executable}" u -r -ttar "{compressed_file}" "{folder_path}"'
        subprocess.run(command, shell=True)


class CompressaoWIM(CompressaoBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format = 'wim'

    def comprimir(self, output_path, folder_path, folder_name):
        compressed_file = os.path.join(output_path, f"{folder_name}.wim")
        command = f'"{self.executable}" a -r -twim "{compressed_file}" "{folder_path}"'
        if self.update_existing:
            command = f'"{self.executable}" u -r -twim "{compressed_file}" "{folder_path}"'
        subprocess.run(command, shell=True)


class TesteIntegridade(QThread):
    finished = pyqtSignal()

    def __init__(self, sevenzip_executable, bandizip_executable, compressed_files):

        super(TesteIntegridade, self).__init__()
        self.sevenzip_executable = sevenzip_executable
        self.bandizip_executable = bandizip_executable
        self.compressed_files = compressed_files

    def run(self):
        for compressed_file in self.compressed_files:
            
            if compressed_file.endswith(".rar") or compressed_file.endswith(".zip") or compressed_file.endswith(".7z") or compressed_file.endswith(".bz2") or compressed_file.endswith(".tar") or compressed_file.endswith(".wim"):
                command = f'"{self.sevenzip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")
            
            elif compressed_file.endswith(".tar.xz") or compressed_file.endswith(".zipx") or compressed_file.endswith(".tgz") or compressed_file.endswith(".tar.gz") or compressed_file.endswith(".lzh") or compressed_file.endswith(".iso"):
                command = f'"{self.bandizip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")

        self.finished.emit()


class Extracao(QThread):
    finished = pyqtSignal()

    def __init__(self, winrar_executable, sevenzip_executable, bandizip_executable, output_listbox, folder_listbox):
        super().__init__()
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
                self.extrair(archive_path, output_path)

    def extrair(self, archive_path, output_path):
        if archive_path.endswith(".rar"):
            command = f'"{self.winrar_executable}" x -y "{archive_path}" "{output_path}"'
            subprocess.run(command, shell=True)

        elif archive_path.endswith(".zip") or archive_path.endswith(".7z") or archive_path.endswith(".tar") or archive_path.endswith(".wim"):
            command = f'"{self.sevenzip_executable}" x -y "{archive_path}" -o"{output_path}"'
            subprocess.run(command, shell=True)

        elif archive_path.endswith(".bz2"):
            with tempfile.TemporaryDirectory() as temp_dir:

                temp_tar_path = os.path.join(temp_dir, os.path.basename(archive_path).replace('.bz2', ''))
                command = f'"{self.sevenzip_executable}" x -y "{archive_path}" -o"{temp_dir}"'
                subprocess.run(command, shell=True)

                command = f'"{self.sevenzip_executable}" x -y "{temp_tar_path}" -o"{output_path}"'
                subprocess.run(command, shell=True)

        elif archive_path.endswith(".tar.xz") or archive_path.endswith(".tgz") or archive_path.endswith(".tar.gz"):
            with tempfile.TemporaryDirectory() as temp_dir:
                
                temp_tar_path = os.path.join(temp_dir, os.path.basename(archive_path).replace('.xz', '').replace('.tgz', '.tar').replace('.gz', ''))
                command = f'"{self.bandizip_executable}" x -o:"{temp_dir}" "{archive_path}"'
                subprocess.run(command, shell=True)
                
                command = f'"{self.bandizip_executable}" x -o:"{output_path}" "{temp_tar_path}"'
                subprocess.run(command, shell=True)

        elif archive_path.endswith(".zipx") or archive_path.endswith(".lzh") or archive_path.endswith(".iso"):
            command = f'"{self.bandizip_executable}" x -o:"{output_path}" "{archive_path}"'
            subprocess.run(command, shell=True)

        self.finished.emit()
