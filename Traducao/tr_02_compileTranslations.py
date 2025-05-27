import os
import sys
import xml.etree.ElementTree as ET
import struct
from typing import List, Dict, Tuple

def compilar_traducoes():
    diretorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    diretorio_traducoes = os.path.join(diretorio_base, "Traducao", "translations")

    if not os.path.exists(diretorio_traducoes):
        print(f"Diretório de traduções não encontrado: {diretorio_traducoes}")
        return

    for arquivo in os.listdir(diretorio_traducoes):
        if arquivo.endswith('.ts'):
            arquivo_ts = os.path.join(diretorio_traducoes, arquivo)
            arquivo_qm = os.path.join(diretorio_traducoes, arquivo.replace('.ts', '.qm'))

            print(f"Compilando: {arquivo}")
            try:
                if compilar_ts_para_qm_alternativo(arquivo_ts, arquivo_qm):
                    print(f"Sucesso: {arquivo} compilado para {os.path.basename(arquivo_qm)}")

                else:
                    print(f"Erro: Falha ao compilar {arquivo}")

            except Exception as e:
                print(f"Erro ao compilar {arquivo}: {e}")

def compilar_ts_para_qm_alternativo(arquivo_ts: str, arquivo_qm: str) -> bool:
    try:
        tree = ET.parse(arquivo_ts)
        root = tree.getroot()

        traducoes = extrair_traducoes(root)

        criar_qm_alternativo(traducoes, arquivo_qm)

        return True

    except Exception as e:
        print(f"Erro durante a compilação: {e}")
        return False

def extrair_traducoes(root: ET.Element) -> Dict[str, Dict[str, str]]:
    traducoes = {}

    for context in root.findall('context'):
        nome_contexto = context.find('name')
        if nome_contexto is not None:
            nome_contexto = nome_contexto.text

        else:
            nome_contexto = "default"

        traducoes[nome_contexto] = {}

        for message in context.findall('message'):
            source_elem = message.find('source')
            translation_elem = message.find('translation')

            if source_elem is not None and translation_elem is not None:
                source_text = source_elem.text or ""
                translation_text = translation_elem.text or ""

                if translation_text and not translation_elem.get('type') == 'unfinished':
                    traducoes[nome_contexto][source_text] = translation_text

    return traducoes

def criar_qm_alternativo(traducoes: Dict[str, Dict[str, str]], arquivo_qm: str):
    import pickle
    import base64

    traducoes_flat = {}
    for contexto, msgs in traducoes.items():
        for source, translation in msgs.items():
            if contexto and contexto != "default":
                key = f"{contexto}::{source}"

            else:
                key = source

            traducoes_flat[key] = translation

    dados = {
        'magic': b'PyQt6QM',
        'version': 1,
        'translations': traducoes_flat
    }

    with open(arquivo_qm, 'wb') as f:
        f.write(b'PyQt6QM\x00')
        pickle.dump(dados, f)

def compilar_ts_para_qm(arquivo_ts: str, arquivo_qm: str) -> bool:
    try:
        tree = ET.parse(arquivo_ts)
        root = tree.getroot()

        traducoes = extrair_traducoes(root)

        criar_arquivo_qm(traducoes, arquivo_qm)

        return True

    except Exception as e:
        print(f"Erro durante a compilação: {e}")
        return False

def criar_arquivo_qm(traducoes: Dict[str, Dict[str, str]], arquivo_qm: str):
    qm_data = bytearray()
    qm_data.extend(b'\x3c\xb8\x64\x18')
    qm_data.extend(struct.pack('<I', 11))
    message_data = bytearray()
    hash_table = {}

    for contexto, msgs in traducoes.items():
        for source, translation in msgs.items():
            if contexto and contexto != "default":
                key = f"{contexto}\x00{source}"

            else:
                key = source

            key_bytes = key.encode('utf-8')
            translation_bytes = translation.encode('utf-8')

            hash_value = hash_string(key) & 0xFFFFFFFF

            pos = len(message_data)

            message_data.extend(struct.pack('<I', len(translation_bytes)))
            message_data.extend(translation_bytes)

            while len(message_data) % 4 != 0:
                message_data.extend(b'\x00')

            hash_table[hash_value] = (pos, len(translation_bytes), key_bytes)

    hash_data = bytearray()
    num_entries = len(hash_table)

    hash_data.extend(struct.pack('<I', num_entries))

    for hash_val, (pos, length, key_bytes) in hash_table.items():
        hash_data.extend(struct.pack('<I', hash_val))
        hash_data.extend(struct.pack('<I', pos))
        hash_data.extend(struct.pack('<I', length))

    final_data = bytearray()
    final_data.extend(qm_data)

    final_data.extend(struct.pack('<B', 0x42))
    final_data.extend(struct.pack('<I', len(hash_data)))
    final_data.extend(hash_data)

    final_data.extend(struct.pack('<B', 0x69))
    final_data.extend(struct.pack('<I', len(message_data)))
    final_data.extend(message_data)

    final_data.extend(struct.pack('<B', 0x00))

    with open(arquivo_qm, 'wb') as f:
        f.write(final_data)

def hash_string(s: str) -> int:
    h = 0
    for char in s:
        h = ((h << 4) + ord(char)) & 0xFFFFFFFF
        g = h & 0xF0000000
        if g:
            h ^= g >> 24
            h &= ~g

    return h

def verificar_arquivo_qm(arquivo_qm: str) -> bool:
    try:
        if not os.path.exists(arquivo_qm):
            return False

        if os.path.getsize(arquivo_qm) == 0:
            return False

        with open(arquivo_qm, 'rb') as f:
            header = f.read(8)
            if header.startswith(b'PyQt6QM'):
                return True

        return False

    except Exception:
        return False

def testar_traducao():
    try:
        from PyQt6.QtCore import QCoreApplication, QTranslator
        import sys

        if QCoreApplication.instance() is None:
            app = QCoreApplication(sys.argv)

        else:
            app = QCoreApplication.instance()

        diretorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        diretorio_traducoes = os.path.join(diretorio_base, "Traducao", "translations")

        for arquivo in os.listdir(diretorio_traducoes):
            if arquivo.endswith('.qm'):
                arquivo_qm = os.path.join(diretorio_traducoes, arquivo)

                translator = QTranslator()
                if translator.load(arquivo_qm):
                    print(f"✓ Arquivo {arquivo} carregado com sucesso!")
                    return True

                else:
                    print(f"✗ Falha ao carregar {arquivo}")

        return False

    except ImportError:
        print("PyQt6 não disponível para teste")
        return False

    except Exception as e:
        print(f"Erro durante teste: {e}")
        return False

if __name__ == "__main__":
    print("=== Compilador de Traduções PyQt6 (Python Puro) ===")
    print("Este compilador não depende de ferramentas externas do Qt\n")

    print("Iniciando compilação...")
    compilar_traducoes()

    print("\nTestando arquivos gerados...")
    if testar_traducao():
        print("✓ Teste de tradução bem-sucedido!")

    else:
        print("✗ Teste de tradução falhou, mas os arquivos foram gerados.")

    print("\nProcesso concluído!")
