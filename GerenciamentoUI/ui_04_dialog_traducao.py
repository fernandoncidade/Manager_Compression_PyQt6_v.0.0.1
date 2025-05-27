from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PyQt6.QtCore import QCoreApplication


class DialogoTraduzivel(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.textos_traduzir = {}

    def adicionar_texto_traduzir(self, widget, chave, contexto="Dialog"):
        self.textos_traduzir[widget] = (chave, contexto)

    def traduzir_interface(self):
        for widget, (chave, contexto) in self.textos_traduzir.items():
            if hasattr(widget, "setText"):
                widget.setText(QCoreApplication.translate(contexto, chave))

            elif hasattr(widget, "setTitle"):
                widget.setTitle(QCoreApplication.translate(contexto, chave))

            elif hasattr(widget, "setWindowTitle"):
                widget.setWindowTitle(QCoreApplication.translate(contexto, chave))


class FileDialogTraduzivel(QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.botoes_traduzidos = False

    def traduzir_botoes(self):
        if not self.botoes_traduzidos:
            self.setLabelText(QFileDialog.DialogLabel.LookIn, 
                             QCoreApplication.translate("FileDialog", "Procurar em"))

            self.setLabelText(QFileDialog.DialogLabel.FileName, 
                             QCoreApplication.translate("FileDialog", "Nome do arquivo"))

            self.setLabelText(QFileDialog.DialogLabel.FileType, 
                             QCoreApplication.translate("FileDialog", "Tipo de arquivo"))

            self.setLabelText(QFileDialog.DialogLabel.Accept, 
                             QCoreApplication.translate("FileDialog", "Abrir"))

            self.setLabelText(QFileDialog.DialogLabel.Reject, 
                             QCoreApplication.translate("FileDialog", "Cancelar"))

            self.botoes_traduzidos = True


class MessageBoxTraduzivel(QMessageBox):
    def __init__(self, icon, title, text, buttons=QMessageBox.StandardButton.Ok, parent=None):
        super().__init__(icon, title, text, buttons, parent)
        self.titulo_chave = title
        self.mensagem_chave = text
        self.traduzir_botoes()

    def traduzir_botoes(self):
        botoes = {
            QMessageBox.StandardButton.Ok: "OK",
            QMessageBox.StandardButton.Cancel: "Cancelar",
            QMessageBox.StandardButton.Yes: "Sim",
            QMessageBox.StandardButton.No: "Não",
            QMessageBox.StandardButton.Abort: "Abortar",
            QMessageBox.StandardButton.Retry: "Tentar Novamente",
            QMessageBox.StandardButton.Ignore: "Ignorar",
            QMessageBox.StandardButton.Close: "Fechar",
            QMessageBox.StandardButton.Help: "Ajuda",
            QMessageBox.StandardButton.Apply: "Aplicar",
            QMessageBox.StandardButton.Reset: "Redefinir",
            QMessageBox.StandardButton.RestoreDefaults: "Restaurar Padrões",
            QMessageBox.StandardButton.Save: "Salvar",
            QMessageBox.StandardButton.SaveAll: "Salvar Tudo",
            QMessageBox.StandardButton.Open: "Abrir",
        }

        for botao, texto in botoes.items():
            botao_widget = self.button(botao)
            if botao_widget:
                botao_widget.setText(QCoreApplication.translate("Dialog", texto))

    def atualizar_traducao(self):
        self.setWindowTitle(QCoreApplication.translate("InterfaceGrafica", self.titulo_chave))
        self.setText(QCoreApplication.translate("InterfaceGrafica", self.mensagem_chave))
        self.traduzir_botoes()
