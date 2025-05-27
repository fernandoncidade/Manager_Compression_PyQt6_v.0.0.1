import os
import sys
import json
import pickle
from PyQt6.QtCore import QTranslator, QCoreApplication, pyqtSignal, QObject


class GerenciadorTraducao(QObject):
    idioma_alterado = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.tradutor = None
        self.idioma_atual = "pt_BR"
        self.app = QCoreApplication.instance()
        self.idioma_padrao = "pt_BR"

        self.idiomas_disponiveis = {
            "pt_BR": "Português (Brasil)",
            "en_US": "English (United States)"
        }

        self.dir_traducoes = os.path.join(
            getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),
            "Traducao", "translations"
        )

        os.makedirs(self.dir_traducoes, exist_ok=True)
        self.carregar_configuracao_idioma()

    def carregar_configuracao_idioma(self):
        config_path = self.obter_caminho_configuracao()
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    if 'idioma' in config:
                        self.idioma_atual = config['idioma']

        except Exception as e:
            print(f"Erro ao carregar configuração de idioma: {e}")

    def salvar_configuracao_idioma(self):
        config_path = self.obter_caminho_configuracao()
        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            config = {'idioma': self.idioma_atual}
            with open(config_path, 'w') as f:
                json.dump(config, f)

        except Exception as e:
            print(f"Erro ao salvar configuração de idioma: {e}")

    def obter_caminho_configuracao(self):
        config_dir = os.path.join(
            getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),
            "Config_Language"
        )
        return os.path.join(config_dir, 'language.json')

    def aplicar_traducao(self):
        if self.tradutor:
            self.app.removeTranslator(self.tradutor)
            self.tradutor = None

        if self.idioma_atual == self.idioma_padrao:
            return True

        self.tradutor = TranslatorCustom()

        arquivo_traducao = f"manager_compression_{self.idioma_atual}.qm"
        caminho_traducao = os.path.join(self.dir_traducoes, arquivo_traducao)

        if os.path.exists(caminho_traducao):
            if self.tradutor.load(caminho_traducao):
                self.app.installTranslator(self.tradutor)
                return True

            else:
                print(f"Erro ao carregar arquivo de tradução: {caminho_traducao}")

        else:
            print(f"Arquivo de tradução não encontrado: {caminho_traducao}")
            print(f"Arquivos disponíveis em {self.dir_traducoes}:")
            try:
                for arquivo in os.listdir(self.dir_traducoes):
                    print(f"  - {arquivo}")

            except Exception as e:
                print(f"Erro ao listar diretório: {e}")

        return False

    def definir_idioma(self, codigo_idioma):
        if codigo_idioma in self.idiomas_disponiveis:
            self.idioma_atual = codigo_idioma
            self.salvar_configuracao_idioma()
            resultado = self.aplicar_traducao()

            self.idioma_alterado.emit(codigo_idioma)

            return resultado

        return False

    def obter_idioma_atual(self):
        return self.idioma_atual

    def traduzir_botoes_padrao(self, dialogo):
        botoes = {
            dialogo.Ok: "OK",
            dialogo.Cancel: "Cancelar",
            dialogo.Yes: "Sim",
            dialogo.No: "Não",
            dialogo.Abort: "Abortar",
            dialogo.Retry: "Tentar Novamente",
            dialogo.Ignore: "Ignorar",
            dialogo.Close: "Fechar",
            dialogo.Help: "Ajuda",
            dialogo.Apply: "Aplicar",
            dialogo.Reset: "Redefinir",
            dialogo.RestoreDefaults: "Restaurar Padrões",
            dialogo.Save: "Salvar",
            dialogo.SaveAll: "Salvar Tudo",
            dialogo.Open: "Abrir",
        }

        for botao, texto in botoes.items():
            botao_widget = dialogo.button(botao)
            if botao_widget:
                botao_widget.setText(QCoreApplication.translate("Dialog", texto))


class TranslatorCustom(QTranslator):
    def __init__(self):
        super().__init__()
        self.translations = {}

    def load(self, filename):
        try:
            with open(filename, 'rb') as f:
                header = f.read(8)
                if not header.startswith(b'PyQt6QM'):
                    return False

                dados = pickle.load(f)
                self.translations = dados.get('translations', {})
                return True

        except Exception as e:
            print(f"Erro ao carregar tradução: {e}")
            return False

    def translate(self, context, sourceText, disambiguation=None, n=-1):
        key = f"{context}::{sourceText}" if context else sourceText
        return self.translations.get(key, "")
