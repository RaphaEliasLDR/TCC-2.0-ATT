from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.clock import Clock

KV = '''
<TelaPedidos>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)

        Label:
            text: "Número da Mesa:"
            size_hint_y: None
            height: dp(30)

        TextInput:
            id: mesa_input
            hint_text: "Digite o número da mesa"
            size_hint_y: None
            height: dp(40)

        Label:
            text: "Observação:"
            size_hint_y: None
            height: dp(30)

        TextInput:
            id: observacao_input
            hint_text: "Exemplo: sem cebola"
            size_hint_y: None
            height: dp(40)

        ScrollView:
            GridLayout:
                id: categorias_layout
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(15)
                padding: dp(10)

        Label:
            text: "Itens Selecionados:"
            size_hint_y: None
            height: dp(30)

        ScrollView:
            BoxLayout:
                id: lista_pedidos
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(5)
                padding: dp(5)

        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)

            BotaoImagem:
                source: "assets/botoes/botaoCancelar.png"
                on_release: root.cancelar_pedido()

            BotaoImagem:
                source: "assets/botoes/botaoEditar.png"
                on_release: root.editar_pedido()

            BotaoImagem:
                source: "assets/botoes/botaoConfirmar.png"
                on_release: root.confirmar_pedido()
'''

class BotaoImagem(ButtonBehavior, Image):
    pass

class TelaPedidos(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.itens_selecionados = []
        self.load_kv()
        Clock.schedule_once(self.mostrar_todas_categorias, 0.1)

    def load_kv(self):
        Builder.load_string(KV)

    def mostrar_todas_categorias(self, dt):
        categorias_layout = self.ids.categorias_layout
        categorias_layout.clear_widgets()

        categorias = {
            "Prato Principal": [
                {"nome": "Strogonoff", "preco": "R$ 25,00", "imagem": "assets/pratos/strogonoff.png"},
                {"nome": "Macarronada", "preco": "R$ 20,00", "imagem": "assets/pratos/macarronada.png"},
                {"nome": "Feijoada", "preco": "R$ 30,00", "imagem": "assets/pratos/feijoada.png"}
            ],
            "Sobremesas": [
                {"nome": "Pudim", "preco": "R$ 10,00", "imagem": "assets/pratos/pudim.png"},
                {"nome": "Brigadeiro", "preco": "R$ 5,00", "imagem": "assets/pratos/brigadeiro.png"},
                {"nome": "Torta de Maçã", "preco": "R$ 20,00", "imagem": "assets/pratos/tortaDeMaca.png" }
            ],
            "Bebidas": [
                {"nome": "Refrigerante Coca-Cola", "preco": "R$ 10,00", "imagem": "assets/pratos/pudim.png"},
                {"nome": "Refrigerante Pepsi", "preco": "R$ 5,00", "imagem": "assets/pratos/pudim.png"},
                {"nome": "Suco Natural", "preco": "R$ 8,00", "imagem": "assets/pratos/pudim.png"}
            ],
            "Lanches": [
                {"nome": "X-Burger", "preco": "R$ 15,00", "imagem": "assets/pratos/pudim.png"},
                {"nome": "X-Salada", "preco": "R$ 18,00", "imagem": "assets/pratos/pudim.png"},
                {"nome": "Coxinha", "preco": "R$ 6,00", "imagem": "assets/pratos/pudim.png"}
            ]
        }

        for titulo, itens in categorias.items():
            categorias_layout.add_widget(Label(text=f"[b]{titulo}[/b]", markup=True, size_hint_y=None, height=dp(50), font_size=dp(30)))
            for item in itens:
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80))
                box.add_widget(Image(source=item['imagem'], size_hint_x=None, width=dp(80)))
                box.add_widget(Label(text=f"{item['nome']}\n{item['preco']}", size_hint_x=0.7))
                
                # Botão de imagem para adicionar o item
                btn_adicionar = BotaoImagem(source="assets/botoes/botaoAdicionar.png", size_hint_x=0.3)
                btn_adicionar.bind(on_release=lambda btn, nome=item['nome']: self.adicionar_item(nome))
                box.add_widget(btn_adicionar)
                
                categorias_layout.add_widget(box)

    def adicionar_item(self, item):
        self.itens_selecionados.append(item)
        self.atualizar_lista_pedidos()

    def atualizar_lista_pedidos(self):
        lista_pedidos = self.ids.lista_pedidos
        lista_pedidos.clear_widgets()
        for item in self.itens_selecionados:
            lista_pedidos.add_widget(Label(text=item, size_hint_y=None, height=dp(30)))

    def cancelar_pedido(self):
        self.itens_selecionados.clear()
        self.ids.mesa_input.text = ""
        self.ids.observacao_input.text = ""
        self.atualizar_lista_pedidos()

    def editar_pedido(self):
        if self.itens_selecionados:
            self.itens_selecionados.pop()
        self.atualizar_lista_pedidos()

    def confirmar_pedido(self):
        mesa = self.ids.mesa_input.text.strip()
        if not mesa or not self.itens_selecionados:
            self.mostrar_popup("Erro", "Mesa e itens são obrigatórios!")
            return
        self.mostrar_popup("Sucesso", "Pedido adicionado!")
        self.cancelar_pedido()

    def mostrar_popup(self, titulo, mensagem):
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        layout.add_widget(Label(text=mensagem))
        
        # Botão de imagem para fechar o popup
        botao_fechar = BotaoImagem(source="assets/botoes/botaoFechar.png", size_hint_y=None, height=dp(40))
        botao_fechar.bind(on_release=lambda instance: popup.dismiss())
        
        popup = Popup(title=titulo, content=layout, size_hint=(None, None), size=(dp(300), dp(200)))
        layout.add_widget(botao_fechar)
        popup.open()