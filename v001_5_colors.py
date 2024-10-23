import winreg

def is_dark_mode_enabled():
    try:
        # Abre a chave do registro onde o Windows armazena as configurações de tema
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize')
        # Lê o valor da configuração do tema escuro para aplicativos
        # O valor 0 indica tema claro, e o valor 1 indica tema escuro
        is_dark, _ = winreg.QueryValueEx(key, 'AppsUseLightTheme')
        winreg.CloseKey(key)
        # Retorna True se o tema escuro estiver habilitado, False caso contrário
        return not is_dark
    except FileNotFoundError:
        # Se a chave do registro não for encontrada, assume tema claro
        return False

def apply_neutral_standart_theme(self):
    if is_dark_mode_enabled():
        # Aplica o tema escuro
        self.setStyleSheet("""
        QPushButton {
            min-width: 16em;
            max-width: 16em;
            font-family: Arial;
            font-size: 8pt;
        }
        QPushButton:hover {
            border-style: solid;
            border-width: 1.2px;
            border-radius: 6px;
            border-color: #ff8c00;
        }
        QPushButton:pressed {
            background-color: #3c3c3c;
            border-style: solid;
            border-width: 1.2px;
            border-radius: 6px;
            border-color: #ff8c00;
        }
        QListWidget {
            min-width: 150px;
            min-height: 70px;
        }
        """)
    else:
        # Aplica o tema claro
        self.setStyleSheet("""
        QPushButton {
            min-width: 16em;
            max-width: 16em;
            font-family: Arial;
            font-size: 8pt;
        }
        QPushButton:hover {
            border-style: solid;
            border-width: 1.2px;
            border-radius: 6px;
            border-color: #ff8c00;
        }
        QPushButton:pressed {
            background-color: #d9d9d9;
            border-style: solid;
            border-width: 1.2px;
            border-radius: 6px;
            border-color: #ff8c00;
        }
        QListWidget {
            min-width: 150px;
            min-height: 70px;
        }
        """)


# O método apply_dark_theme(self) é usado para aplicar um tema escuro à interface do usuário de um aplicativo PyQt.
# Ele faz isso definindo uma folha de estilo para o objeto atual (self), ...
# que provavelmente é uma janela ou widget que contém outros widgets.
def apply_dialog_box_theme(self):
    self.setStyleSheet("""
    QPushButton {
        min-width: 7em;
        max-width: 7em;
    }
    QPushButton:hover {
        min-width: 7em;
        max-width: 7em;
    }
    """)
