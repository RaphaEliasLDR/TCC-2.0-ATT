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
import requests

from kivy.uix.screenmanager import Screen, ScreenManager



Window.size = (360, 640)

PRATOS_PATH = "pratos.json"
GERENTE_PATH = "Gerente.json"
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
    return carregar_json(GERENTE_PATH)

def salvar_usuarios(lista):
    salvar_json(GERENTE_PATH, lista)

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
    CadastroGerenteScreen:
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
                on_release: app.mudar_tela('cadastro_gerente')
                pos_hint: {"center_x": 0.5}

<CadastroGerenteScreen>:
    name: 'cadastro_gerente'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(10)

        MDLabel:
            text: "Cadastro de Gerente"
            halign: "center"
            font_style: "H5"

        MDTextField:
            id: nome_gerente
            hint_text: "Nome"

        MDTextField:
            id: email_gerente
            hint_text: "E-mail"

        MDTextField:
            id: senha_gerente
            hint_text: "Senha"
            password: True

        MDRaisedButton:
            text: "Cadastrar"
            on_release: app.cadastrar_gerente()

        MDFlatButton:
            text: "Voltar"
            on_release: app.mudar_tela('login')

<SelecaoCadastroScreen>:
    name: 'selecao_cadastro'
    BoxLayout:
        orientation: 'horizontal'
        padding: dp(20)
        spacing: dp(20)

        FloatLayout:
            size_hint: None, None
            size: dp(150), dp(130)  # Tamanho menor
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            spacing: dp(20)
            canvas.after:    
                Color:
                    rgba: 0, 0, 0, 0.4  
                Rectangle:
                    pos: self.pos
                    size: self.size  

            Image:
                allow_stretch: True
                keep_ratio: False
                size_hint: None, None
                size: dp(150), dp(130)
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                source: 'imagens/img_pratos.jfif'
        
            Label:
                text: "Cadastrar Prato"
                color: 1, 1, 1, 1
                font_size: dp(14)
                bold: True
                pos_hint: {"center_x": 0.5, "center_y": 0.5}

            Button:
                background_color: 0, 0, 0, 0  # invisível
                size_hint: None, None
                size: dp(150), dp(130)
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                on_release: app.mudar_tela('cadastro_prato') 

        FloatLayout:
            size_hint: None, None
            size: dp(150), dp(130)  # Tamanho menor
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            spacing: dp(20)
        
            canvas.after:
                Color:
                    rgba: 0, 0, 0, 0.4  
                Rectangle:
                    pos: self.pos
                    size: self.size
            Image:
                allow_stretch: True
                keep_ratio: False
                size_hint: None, None
                size: dp(150), dp(130)
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                source: 'imagens/img_funcionario.jfif'

            Label:
                text: "Cadastrar Funcionário"
                color: 1, 1, 1, 1
                font_size: dp(14)
                bold: True
                pos_hint: {"center_x": 0.5, "center_y": 0.5}

            Button:
                background_color: 0, 0, 0, 0
                size_hint: None, None
                size: dp(150), dp(130)
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                on_release: app.mudar_tela('cadastro_funcionario')


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
            text: 'Ver Pratos'
            on_release:
                app.exibir_lista_pratos()
                app.mudar_tela('lista_pratos')

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
                text: 'Ver Funcionários'
                on_release:
                    app.exibir_funcionarios()
                    app.mudar_tela('lista_funcionarios')

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
class CadastroGerenteScreen(Screen): pass
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

    def cadastrar_gerente(self):
        tela = self.root.get_screen('cadastro_gerente').ids
        nome = tela.nome_gerente.text.strip()
        email = tela.email_gerente.text.strip()
        senha = tela.senha_gerente.text.strip()

        if not nome or not email or not senha:
            self.exibir_mensagem("Preencha todos os campos.")
            return

        usuarios = carregar_usuarios()
        if any(u["email"] == email for u in usuarios):
            self.exibir_mensagem("Já existe um gerente com este e-mail.")
            return

        usuarios.append({
            "id": str(uuid.uuid4()),
            "nome": nome,
            "email": email,
            "senha": senha
        })
        salvar_usuarios(usuarios)

        tela.nome_gerente.text = ""
        tela.email_gerente.text = ""
        tela.senha_gerente.text = ""

        self.exibir_mensagem("Gerente cadastrado com sucesso!", erro=False)
        self.mudar_tela('login')

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
        
        try:
            with open(imagem_path, 'rb') as img_file:
                files = {'imagem': img_file}
                data = {'nome': nome, 'preco': preco}
                response = requests.post('http://localhost:3000/api/pratos', data=data, files=files)

            if response.status_code == 200:
                self.exibir_mensagem("Prato adicionado com sucesso!", erro=False)
                self.exibir_lista_pratos()
            else:
                self.exibir_mensagem("Erro ao adicionar prato.")

        except Exception as e:
            self.exibir_mensagem(f"Erro: {str(e)}")

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

        pratos = carregar_pratos()  # Aqui estamos carregando os pratos, veja se está trazendo todos corretamente.
        for p in pratos:
            if p['id'] == prato['id']:
                p['nome'] = novo_nome
                p['preco'] = novo_preco

            # Verificar se a imagem foi alterada, caso contrário mantém a original
            if hasattr(self, 'imagem_selecionada') and self.imagem_selecionada:
                p['imagem'] = adaptar_caminho_imagem(self.imagem_selecionada)
            elif hasattr(self, 'prato_editando_imagem') and self.prato_editando_imagem:
                p['imagem'] = adaptar_caminho_imagem(self.prato_editando_imagem['imagem'])

            break

        salvar_pratos(pratos)  # Certifique-se de que a função salvar_pratos está corretamente atualizando o arquivo.
        self.exibir_mensagem("Prato editado com sucesso!", erro=False)
        self.exibir_lista_pratos()


    def remover_prato(self, prato):
        pratos = carregar_pratos()
        pratos = [p for p in pratos if p['id'] != prato['id']]
        salvar_pratos(pratos)
        self.exibir_mensagem("Prato removido com sucesso!", erro=False)
        self.exibir_lista_pratos()

    def confirmar_remocao(self, prato):
        dialog = MDDialog(
            title="Remover Prato",
            text=f"Você tem certeza que deseja remover o prato '{prato['nome']}'?",
            size_hint=(0.8, 0.4),
            buttons=[
                MDRaisedButton(
                    text="SIM",
                    on_release=lambda *args: self.remover_prato(prato, dialog)
                ),
                MDRaisedButton(
                    text="NÃO",
                    on_release=lambda *args: dialog.dismiss()
                ),
            ],
        )
        dialog.open()

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
        # Atualiza o prato com a nova imagem
            self.prato_editando_imagem['imagem'] = caminho_imagem

        # Verifique se self.widget_imagem_para_atualizar está definido corretamente
            if self.widget_imagem_para_atualizar:
                self.widget_imagem_para_atualizar.source = caminho_imagem
            else:
                print("Erro: O widget de imagem não foi encontrado!")

                self.exibir_mensagem("Imagem atualizada. Clique em 'Salvar' para confirmar.", erro=False)
                self.prato_editando_imagem = None
                self.widget_imagem_para_atualizar = None
        else:
        # Novo prato, apenas seleciona a imagem
            self.imagem_selecionada = caminho_imagem
            self.root.get_screen('cadastro_prato').ids.preview_img.source = caminho_imagem

        self.fechar_file_manager()

    # Em algum lugar onde você seleciona um prato para editar, armazene o widget de imagem
    def abrir_edicao_prato(self, prato):    
    # Suponha que 'preview_img' seja o nome do widget de imagem no arquivo .kv
        self.widget_imagem_para_atualizar = self.root.get_screen('cadastro_prato').ids.preview_img
        self.prato_editando_imagem = prato


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



    def enviar_imagem(imagem_path):
        url = 'http://localhost:3000/api/imagem'
    
    # Carregar a imagem (aqui estamos assumindo que é uma string base64 ou um arquivo de imagem)
        with open(imagem_path, 'rb') as img:
            imagem_data = img.read()  # Ou converta para base64, conforme necessário

    # Preparar o payload (dado) que será enviado para a API
        payload = {
            'imagem': imagem_data  # Enviar os dados da imagem
    }

    # Enviar a requisição POST para a API Node.js
        response = requests.post(url, json=payload)
    
        if response.status_code == 200:
            print("Imagem enviada com sucesso!")
        else:
            print("Falha ao enviar a imagem:", response.status_code)



        

GerenteApp().run()
