from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
import os
import uuid
import json
from kivy.uix.screenmanager import Screen, ScreenManager

Window.size = (360, 640)

PRATOS_PATH = "pratos.json"
USUARIOS_PATH = "usuarios.json"
FUNCIONARIOS_PATH = "funcionarios.json"

def carregar_json(path):
    return json.load(open(path, "r", encoding="utf-8")) if os.path.exists(path) else []

def salvar_json(path, dados):
    json.dump(dados, open(path, "w", encoding="utf-8"), indent=4, ensure_ascii=False)

def carregar_pratos():
    return carregar_json(PRATOS_PATH)

def salvar_pratos(lista):
    salvar_json(PRATOS_PATH, lista)

def carregar_usuarios():
    return carregar_json(USUARIOS_PATH)

def salvar_usuarios(lista):
    salvar_json(USUARIOS_PATH, lista)

def carregar_funcionarios():
    return carregar_json(FUNCIONARIOS_PATH)

def salvar_funcionarios(lista):
    salvar_json(FUNCIONARIOS_PATH, lista)

def validar_preco(preco):
    try:
        return float(preco) > 0
    except ValueError:
        return False

def adaptar_caminho_imagem(caminho):
    return caminho.replace("\\", "/")

KV = '''
ScreenManager:
    LoginScreen:
    SelecaoCadastroScreen:
    CadastroPratoScreen:
    ListaPratosScreen:
    CadastroFuncionarioScreen:
    ListaFuncionariosScreen:

<LoginScreen>:
    name: 'login'
    FloatLayout:
        MDCard:
            orientation: 'vertical'
            size_hint: None, None
            size: dp(300), dp(350)
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            padding: dp(20)
            spacing: dp(15)
            elevation: 8

            MDLabel:
                text: "Login"
                halign: "center"
                font_style: "H5"

            MDTextField:
                id: login_usuario
                hint_text: "E-mail"

            MDTextField:
                id: login_senha
                hint_text: "Senha"
                password: True

            MDRaisedButton:
                text: "Entrar"
                on_release: app.login()
                pos_hint: {"center_x": 0.5}
                size_hint_x: 1

            MDFlatButton:
                text: "Não tem conta?"
                on_release: app.mudar_tela('selecao_cadastro')
                pos_hint: {"center_x": 0.5}

<SelecaoCadastroScreen>:
    name: 'selecao_cadastro'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(10)

        MDRaisedButton:
            text: 'Cadastrar Prato'
            on_release: app.mudar_tela('cadastro_prato')

        MDRaisedButton:
            text: 'Ver Pratos'
            on_release:
                app.exibir_lista_pratos()
                app.mudar_tela('lista_pratos')

        MDRaisedButton:
            text: 'Cadastrar Funcionário'
            on_release: app.mudar_tela('cadastro_funcionario')

        MDRaisedButton:
            text: 'Ver Funcionários'
            on_release:
                app.exibir_funcionarios()
                app.mudar_tela('lista_funcionarios')

<CadastroPratoScreen>:
    name: 'cadastro_prato'
    BoxLayout:
        id: form_layout 
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        size_hint_y: None
        width: dp(350)
        pos_hint: {"center_x": 0.5}
        elevation: 8
        height: form_layout.minimum_height

        MDLabel:
            text: "Cadastro de Pratos"
            halign: "center"
            font_style: "H5"
            size_hint_y: None
            height: dp(30)

        MDTextField:
            id: nome_input
            hint_text: "Nome do Prato"

        MDTextField:
            id: preco_input
            hint_text: "Preço"

        MDRaisedButton:
            text: "Selecionar Imagem"
            on_release: app.abrir_file_manager()

        Image:
            id: preview_img
            size_hint_y: None
            height: 150
            allow_stretch: True

        MDRaisedButton:
            text: "Adicionar Prato"
            on_release: app.adicionar_prato()

        MDRaisedButton:
            text: "Voltar"
            on_release: app.mudar_tela('selecao_cadastro')

<ListaPratosScreen>:
    name: 'lista_pratos'
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(6)

        MDLabel:
            text: "Lista de Pratos"
            halign: "center"
            font_style: "H6"
            size_hint_y: None
            height: dp(50)
            padding: dp(6), 0
            pos_hint: {"top": 1, "center_x": 0.5}

        ScrollView:
            MDList:
                id: pratos_list

        MDRaisedButton:
            text: "Voltar"
            on_release: app.mudar_tela('selecao_cadastro')

<CadastroFuncionarioScreen>:
    name: 'cadastro_funcionario'
    ScrollView:
        do_scroll_x: False

        BoxLayout:
            id: form_layout 
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(20)
            size_hint_y: None
            width: dp(350)
            pos_hint: {"center_x": 0.5}
            elevation: 8
            height: form_layout.minimum_height

            MDLabel:
                text: "Cadastro de Funcionário"
                halign: "center"
                font_style: "H6"
                size_hint_y: None
                height: dp(30)

            MDTextField:
                id: nome_func_input
                hint_text: "Nome do Funcionário"
                size_hint_y: None
                height: dp(60)

            MDTextField:
                id: cpf_func_input
                hint_text: "CPF"
                input_filter: 'int'
                size_hint_y: None
                height: dp(60)

            MDTextField:
                id: cargo_func_input
                hint_text: "Cargo"
                size_hint_y: None
                height: dp(60)

            MDTextField:
                id: telefone_func_input
                hint_text: "Telefone"
                size_hint_y: None
                height: dp(60)

            MDRaisedButton:
                text: "Cadastro de Funcionários"
                on_release: app.adicionar_funcionario()
                size_hint_y: None
                height: dp(50)

            MDRaisedButton:
                text: "Voltar"
                on_release: app.mudar_tela('selecao_cadastro')
                size_hint_y: None
                height: dp(50)


<ListaFuncionariosScreen>:
    name: 'lista_funcionarios'
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(6)

        MDLabel:
            text: "Lista de Funcionários"
            halign: "center"
            font_style: "H6"
            size_hint_y: None
            height: dp(50)
            padding: dp(6), 0
            pos_hint: {"top": 1, "center_x": 0.5}

        ScrollView:
            MDList:
                id: funcionarios_list
                

        MDRaisedButton:
            text: "Voltar"
            on_release: app.mudar_tela('selecao_cadastro')
            size_hint_y: None
            height: dp(50)
            pos_hint: {"center_x": 0.5}
'''

class LoginScreen(Screen): pass
class SelecaoCadastroScreen(Screen): pass
class CadastroPratoScreen(Screen): pass
class ListaPratosScreen(Screen): pass
class CadastroFuncionarioScreen(Screen): pass
class ListaFuncionariosScreen(Screen): pass

class GerenteApp(MDApp):
    def build(self):
        self.imagem_selecionada = None
        self.mensagem_dialog = None
        self.file_manager = MDFileManager(
            exit_manager=self.fechar_file_manager,
            select_path=self.selecionar_imagem,
            ext=['.jpg', '.jpeg', '.png']
        )
        return Builder.load_string(KV)

    def mudar_tela(self, nome):
        self.root.current = nome

    def login(self):
        email = self.root.get_screen('login').ids.login_usuario.text.strip()
        senha = self.root.get_screen('login').ids.login_senha.text
        for u in carregar_usuarios():
            if u['email'] == email and u['senha'] == senha:
                self.root.current = 'selecao_cadastro'
                return
        self.exibir_mensagem("E-mail ou senha inválidos.")

    def adicionar_prato(self):
        ids = self.root.get_screen('cadastro_prato').ids
        nome = ids.nome_input.text.strip()
        preco = ids.preco_input.text.strip()
        imagem_path = self.imagem_selecionada

        if not nome or not preco or not imagem_path:
            self.exibir_mensagem("Preencha todos os campos.")
            return
        if not validar_preco(preco):
            self.exibir_mensagem("Preço inválido.")
            return

        pratos = carregar_pratos()
        pratos.append({'id': str(uuid.uuid4()), 'nome': nome, 'preco': preco, 'imagem': adaptar_caminho_imagem(imagem_path)})
        salvar_pratos(pratos)

        for field in [ids.nome_input, ids.preco_input]:
            field.text = ""
        ids.preview_img.source = ""
        self.exibir_mensagem("Prato adicionado com sucesso!", erro=False)

    def exibir_lista_pratos(self):
        pratos = carregar_pratos()
        pratos_list = self.root.get_screen('lista_pratos').ids.pratos_list
        pratos_list.clear_widgets()

        for prato in pratos:
            card = MDCard(
                size_hint=(None, None),
                size=(dp(320), dp(200)),
                elevation=4,
                radius=[12],
                orientation="vertical",
                padding=dp(10),
                spacing=dp(10),
                ripple_behavior=True
            )

            top_box = BoxLayout(orientation="horizontal", spacing=dp(10))
            imagem = Image(source=adaptar_caminho_imagem(prato['imagem']), size_hint=(None, None), size=(dp(100), dp(100)), allow_stretch=True)
            info_box = BoxLayout(orientation='vertical', spacing=dp(5))
            nome_input = MDTextField(text=prato['nome'], hint_text="Nome", mode="rectangle")
            preco_input = MDTextField(text=prato['preco'], hint_text="Preço", mode="rectangle")
            info_box.add_widget(nome_input)
            info_box.add_widget(preco_input)

            top_box.add_widget(imagem)
            top_box.add_widget(info_box)

            buttons_box = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(40))
            salvar_btn = MDRaisedButton(text="Salvar", on_release=lambda btn, p=prato, n=nome_input, pr=preco_input: self.salvar_edicao_prato(p, n.text, pr.text))
            remover_btn = MDRaisedButton(text="Remover", md_bg_color=(1, 0.2, 0.2, 1), on_release=lambda btn, p=prato: self.remover_prato(p))
            alterar_img_btn = MDRaisedButton(text="Alterar Imagem", on_release=lambda btn, p=prato, i=imagem: self.abrir_file_manager_para_edicao(p, i))

            buttons_box.add_widget(salvar_btn)
            buttons_box.add_widget(remover_btn)
            buttons_box.add_widget(alterar_img_btn)

            card.add_widget(top_box)
            card.add_widget(buttons_box)

            pratos_list.add_widget(card)

    def salvar_edicao_prato(self, prato, novo_nome, novo_preco):
        if not novo_nome or not novo_preco:
            self.exibir_mensagem("Preencha todos os campos.")
            return
        if not validar_preco(novo_preco):
            self.exibir_mensagem("Preço inválido.")
            return

        pratos = carregar_pratos()
        for p in pratos:
            if p['id'] == prato['id']:
                p['nome'] = novo_nome
                p['preco'] = novo_preco
                if self.imagem_selecionada:
                    p['imagem'] = adaptar_caminho_imagem(self.imagem_selecionada)
                break

        salvar_pratos(pratos)
        self.exibir_mensagem("Prato editado com sucesso!", erro=False)
        self.exibir_lista_pratos()

    def remover_prato(self, prato):
        pratos = carregar_pratos()
        pratos = [p for p in pratos if p['id'] != prato['id']]
        salvar_pratos(pratos)
        self.exibir_mensagem("Prato removido com sucesso!", erro=False)
        self.exibir_lista_pratos()

    def adicionar_funcionario(self):
        tela = self.root.get_screen('cadastro_funcionario').ids
        nome = tela.nome_func_input.text.strip()
        cpf = tela.cpf_func_input.text.strip()
        cargo = tela.cargo_func_input.text.strip()
        telefone = tela.telefone_func_input.text.strip()

        if not nome or not cpf or not cargo or not telefone:
            self.exibir_mensagem("Preencha todos os campos.")
            return

        if not cpf.isdigit() or len(cpf) != 11:
            self.exibir_mensagem("CPF inválido. Deve conter 11 dígitos numéricos.")
            return

        funcionarios = carregar_funcionarios()
        if any(f.get("cpf") == cpf for f in funcionarios):
            self.exibir_mensagem("Já existe um funcionário com este CPF.")
            return

        funcionarios.append({
            'id': str(uuid.uuid4()),
            'nome': nome,
            'cpf': cpf,
            'cargo': cargo,
            'telefone': telefone
        })
        salvar_funcionarios(funcionarios)

        tela.nome_func_input.text = ""
        tela.cpf_func_input.text = ""
        tela.cargo_func_input.text = ""
        tela.telefone_func_input.text = ""
        self.exibir_mensagem("Funcionário cadastrado com sucesso!", erro=False)


    

    def abrir_file_manager(self):
        self.file_manager.show(os.path.expanduser("~"))

    def abrir_file_manager_para_edicao(self, prato, widget_imagem):
        self.prato_editando_imagem = prato
        self.widget_imagem_para_atualizar = widget_imagem
        self.file_manager.show(os.path.expanduser("~"))

    def fechar_file_manager(self, *args):
        self.file_manager.close()

    def selecionar_imagem(self, path):
        caminho_imagem = adaptar_caminho_imagem(path)

        if hasattr(self, 'prato_editando_imagem') and self.prato_editando_imagem:
            self.prato_editando_imagem['imagem'] = caminho_imagem
            self.widget_imagem_para_atualizar.source = caminho_imagem
            salvar_pratos(carregar_pratos())
            self.exibir_mensagem("Imagem atualizada. Clique em 'Salvar' para confirmar.", erro=False)
            self.prato_editando_imagem = None
            self.widget_imagem_para_atualizar = None
        else:
            self.imagem_selecionada = caminho_imagem
            self.root.get_screen('cadastro_prato').ids.preview_img.source = caminho_imagem

        self.fechar_file_manager()

    def exibir_mensagem(self, texto, erro=True):
        if self.mensagem_dialog:
            self.mensagem_dialog.dismiss()

        self.mensagem_dialog = MDDialog(
            title="Erro" if erro else "Sucesso",
            text=texto,
            buttons=[
                MDFlatButton(text="OK", on_release=self.fechar_mensagem)
            ]
        )
        self.mensagem_dialog.open()

    def fechar_mensagem(self, instance):
        if self.mensagem_dialog:
            self.mensagem_dialog.dismiss()
            self.mensagem_dialog = None


    def exibir_funcionarios(self):
        funcionarios = carregar_funcionarios()
        container = self.root.get_screen('lista_funcionarios').ids.funcionarios_list
        container.clear_widgets()

        for f in funcionarios:

            card = MDCard(
            size_hint=(None, None),
            size=(dp(320), dp(280)),
            elevation=4,
            radius=[12],
            orientation="vertical",
            padding=dp(4),
            spacing=dp(4),
            ripple_behavior=True
            )

            inner_layout = BoxLayout(
                orientation="vertical",
                spacing=dp(2),
                size_hint_y=None
            )

            nome_input = MDTextField(
                text=f['nome'], 
                size_hint_y=None,
                height=dp(30),
                font_size="10sp",
                hint_text="Nome")
            
            cpf_input = MDTextField(
                text=f.get('cpf', ''),
                size_hint_y=None,
                height=dp(20), 
                font_size="10sp",
                hint_text="CPF", 
                input_filter='int')
            
            cargo_input = MDTextField(
                text=f['cargo'],
                size_hint_y=None,
                height=dp(20),                    
                font_size="10sp",
                hint_text="Cargo")
            
            telefone_input = MDTextField(
                text=f['telefone'],
                size_hint_y=None,
                height=dp(20),
                font_size="10sp",
                hint_text="Telefone")

            botoes = BoxLayout(
                orientation='horizontal',
                spacing=dp(8), 
                size_hint_y=None, 
                height=dp(30))

            salvar_btn = MDIconButton(
                icon="content-save",
                on_release=lambda btn, func=f, nome=nome_input, cpf=cpf_input, cargo=cargo_input, tel=telefone_input:
                self.salvar_edicao_funcionario(func, nome.text, cpf.text, cargo.text, tel.text) 
            )

            remover_btn = MDIconButton(
                icon="delete",
                on_release=lambda btn, func=f: self.confirmar_remocao_funcionario(func)
            )

            botoes.add_widget(salvar_btn)
            botoes.add_widget(remover_btn)

            # Adiciona os inputs
        for widget in (nome_input, cpf_input, cargo_input, telefone_input):
            inner_layout.add_widget(widget)

        inner_layout.add_widget(botoes)
        card.add_widget(inner_layout)

# CORRETO: usar o container obtido no início da função
        container.add_widget(card)

    def salvar_edicao_funcionario(self, funcionario_original, nome, cpf, cargo, telefone):
    # Verifica se todos os campos foram preenchidos
        if not nome or not cpf or not cargo or not telefone:
            self.exibir_mensagem("Preencha todos os campos.")
            return

    # Valida o CPF
        if not cpf.isdigit() or len(cpf) != 11:
            self.exibir_mensagem("CPF inválido. Deve ter 11 dígitos.")
            return

    # Carrega a lista de funcionários
        funcionarios = carregar_funcionarios()

    # Verifica se já existe um funcionário com o mesmo CPF
        for f in funcionarios:
            if f.get('cpf') == cpf and f['id'] != funcionario_original['id']:
                self.exibir_mensagem("Já existe um funcionário com este CPF.")
                return

    # Atualiza os dados do funcionário original
        for f in funcionarios:
            if f['id'] == funcionario_original['id']:
                f['nome'] = nome
                f['cpf'] = cpf
                f['cargo'] = cargo
                f['telefone'] = telefone
                break

    # Salva os dados atualizados
        salvar_funcionarios(funcionarios)

    # Exibe uma mensagem de sucesso
        self.exibir_mensagem("Funcionário editado com sucesso!", erro=False)

    # Atualiza a lista de funcionários na interface
        self.exibir_funcionarios()

        def confirmar_remocao_funcionario(self, funcionario):
            dialog = MDDialog(
                title="Confirmar Remoção",
                text=f"Tem certeza que deseja remover o funcionário {funcionario['nome']}?",
                buttons=[
                    MDFlatButton(text="Cancelar", on_release=lambda x: dialog.dismiss()),
                    MDFlatButton(
                        text="Remover",
                        text_color=(1, 0, 0, 1),
                        on_release=lambda x: self.remover_funcionario(funcionario, dialog)
                )
            ]
        )
            dialog.open()

    def remover_funcionario(self, funcionario, dialog):
        funcionarios = carregar_funcionarios()
        funcionarios = [f for f in funcionarios if f['id'] != funcionario['id']]
        salvar_funcionarios(funcionarios)
        dialog.dismiss()
        self.exibir_mensagem("Funcionário removido com sucesso!", erro=False)
        self.exibir_funcionarios()

        

GerenteApp().run()
