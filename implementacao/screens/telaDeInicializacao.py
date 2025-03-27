from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

KV = '''
Screen:
    canvas.before:
        Color:
            rgb: 0, 0, 0
        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(20)

        Image:
            source: "assets/logoSAP.png"  
            size_hint: None, None
            size: dp(800), dp(400)
            pos_hint: {"center_x": 0.5}

        BotaoImagem:
            source: "assets/botoes/botaoPedidos.png"
            on_release: app.root.current = "pedidos"

        BotaoImagem:
            source: "assets/botoes/botaoCozinha.png"
            on_release: app.root.current = "telaCozinha"

        BotaoImagem:
            source: "assets/botoes/botaoGestao.png"
            on_release: app.root.current = "telaGestao"
'''

class BotaoImagem(ButtonBehavior, Image):
    pass

class TelaDeInicializacao(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Builder.load_string(KV))
