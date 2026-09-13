import pygame
import sys


class interface:

    def __init__(self, width=1400, height=800):

        pygame.init()

        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption("Quebra-Cabeça da Zebra")

        self.clock = pygame.time.Clock()

        # ====================================================
        # FONTES
        # ====================================================

        self.font = pygame.font.SysFont("Fonte\Roboto-Regular.ttf", 24)
        self.font_bold = pygame.font.SysFont(
            "Fonte\Roboto-Bold.ttf",
            24,
            bold=False
        )

        self.title_font = pygame.font.SysFont(
            "Fonte\Roboto-Regular.ttf",
            28,
            bold=True
        )

        # ====================================================
        # CORES
        # ====================================================

        self.BG = (245, 245, 245)
        self.WHITE = (255, 255, 255)
        self.BLACK = (30, 30, 30)
        self.GRAY = (210, 210, 210)
        self.LIGHT_BLUE = (225, 235, 245)

        # ====================================================
        # TABELA
        # ====================================================

        self.tabela = {}

        # ====================================================
        # MENU
        # ====================================================

        self.menu_aberto = None

    # ========================================================
    # POPULAR CAMPOS
    # ========================================================
    def popular_categorias(self,categorias):
        self.categorias = categorias
        for categoria in categorias:
            self.tabela[categoria] = [""] * 5

    def popular_valores(self, valores):
        self.valores = valores

    def popular_dicas(self,dicas):
        self.dicas = dicas

    # ========================================================
    # QUEBRAR TEXTO
    # ========================================================

    def quebrar_texto(self, texto, fonte, largura):

        palavras = texto.split()
        linhas = []
        linha = ""
        for palavra in palavras:
            teste = (
                linha + " " + palavra
            ).strip()
            if fonte.size(teste)[0] <= largura:
                linha = teste
            else:
                if linha:
                    linhas.append(linha)
                linha = palavra
        if linha:
            linhas.append(linha)
        return linhas

    # ========================================================
    # TEXTO CENTRALIZADO
    # ========================================================
    def texto_centralizado(self, texto, fonte, rect):
        linhas = self.quebrar_texto(
            texto,
            fonte,
            rect.width - 10
        )
        altura_linha = fonte.get_height() + 2
        altura_total = (
            len(linhas) * altura_linha
        )
        y = (
            rect.centery
            - altura_total // 2
        )
        for linha in linhas:
            imagem = fonte.render(
                linha,
                True,
                self.BLACK
            )
            imagem_rect = imagem.get_rect(
                centerx=rect.centerx,
                y=y
            )
            self.screen.blit(
                imagem,
                imagem_rect
            )

            y += altura_linha

    # ========================================================
    # RETORNA RECT DE UMA CÉLULA
    # ========================================================

    def get_cell_rect(self, categoria, posicao):

        tabela_x = 40
        tabela_y = 100

        largura_categoria = 145
        largura_posicao = 115

        altura_header = 45
        altura_linha = 95

        linha = self.categorias.index(
            categoria
        )

        x = (
            tabela_x
            + largura_categoria
            + posicao * largura_posicao
        )

        y = (
            tabela_y
            + altura_header
            + linha * altura_linha
        )

        return pygame.Rect(
            x,
            y,
            largura_posicao,
            altura_linha
        )

    # ========================================================
    # DESENHAR GRADE
    # ========================================================

    def desenhar_grade(self):

        tabela_x = 40
        tabela_y = 100

        largura_categoria = 145
        largura_posicao = 115

        altura_header = 45
        altura_linha = 95

        # ----------------------------------------------------
        # CABEÇALHO
        # ----------------------------------------------------

        for posicao in range(5):

            x = (
                tabela_x
                + largura_categoria
                + posicao * largura_posicao
            )

            rect = pygame.Rect(
                x,
                tabela_y,
                largura_posicao,
                altura_header
            )

            pygame.draw.rect(
                self.screen,
                self.LIGHT_BLUE,
                rect
            )

            pygame.draw.rect(
                self.screen,
                self.BLACK,
                rect,
                1
            )

            imagem = self.font_bold.render(
                f"Posição #{posicao + 1}",
                True,
                self.BLACK
            )

            imagem_rect = imagem.get_rect(
                center=rect.center
            )

            self.screen.blit(
                imagem,
                imagem_rect
            )

        # ----------------------------------------------------
        # CATEGORIAS
        # ----------------------------------------------------

        for linha, categoria in enumerate(
            self.categorias
        ):

            y = (
                tabela_y
                + altura_header
                + linha * altura_linha
            )

            # Nome da categoria

            rect = pygame.Rect(
                tabela_x,
                y,
                largura_categoria,
                altura_linha
            )

            pygame.draw.rect(
                self.screen,
                self.LIGHT_BLUE,
                rect
            )

            pygame.draw.rect(
                self.screen,
                self.BLACK,
                rect,
                1
            )

            imagem = self.font_bold.render(
                categoria,
                True,
                self.BLACK
            )

            imagem_rect = imagem.get_rect(
                center=rect.center
            )

            self.screen.blit(
                imagem,
                imagem_rect
            )

            # ------------------------------------------------
            # CÉLULAS
            # ------------------------------------------------

            for posicao in range(5):

                rect = self.get_cell_rect(
                    categoria,
                    posicao
                )

                # Célula selecionada

                selecionada = (
                    self.menu_aberto is not None
                    and
                    self.menu_aberto["categoria"]
                    == categoria
                    and
                    self.menu_aberto["posicao"]
                    == posicao
                )

                if selecionada:

                    cor = self.LIGHT_BLUE

                else:

                    cor = self.WHITE

                pygame.draw.rect(
                    self.screen,
                    cor,
                    rect
                )

                pygame.draw.rect(
                    self.screen,
                    self.BLACK,
                    rect,
                    1
                )

                valor = self.tabela[
                    categoria
                ][posicao]

                if valor:
                    self.texto_centralizado(
                        valor,
                        self.font,
                        rect
                    )

    # ========================================================
    # ABRIR MENU
    # ========================================================

    def abrir_menu(self, categoria, posicao):

        cell_rect = self.get_cell_rect(
            categoria,
            posicao
        )

        self.menu_aberto = {

            "categoria": categoria,

            "posicao": posicao,

            "cell_rect": cell_rect,

            "menu_rect": None
        }

    # ========================================================
    # DESENHAR MENU
    # ========================================================

    def desenhar_menu(self):

        if self.menu_aberto is None:
            return

        categoria = self.menu_aberto[
            "categoria"
        ]

        opcoes = self.valores[
            categoria
        ]
        opcoes.sort()

        cell_rect = self.menu_aberto[
            "cell_rect"
        ]

        largura = 180
        altura_item = 38

        altura_total = (
            len(opcoes)
            * altura_item
        )

        # ----------------------------------------------------
        # POSIÇÃO
        # ----------------------------------------------------

        x = cell_rect.x

        y = cell_rect.bottom + 3

        # Se não couber embaixo,
        # coloca acima.

        if y + altura_total > self.height:

            y = (
                cell_rect.y
                - altura_total
                - 3
            )

        # Se não couber à direita

        if x + largura > self.width:

            x = (
                self.width
                - largura
                - 10
            )

        menu_rect = pygame.Rect(
            x,
            y,
            largura,
            altura_total
        )

        self.menu_aberto[
            "menu_rect"
        ] = menu_rect

        # ----------------------------------------------------
        # FUNDO
        # ----------------------------------------------------

        pygame.draw.rect(
            self.screen,
            self.WHITE,
            menu_rect
        )

        pygame.draw.rect(
            self.screen,
            self.BLACK,
            menu_rect,
            2
        )

        # ----------------------------------------------------
        # OPÇÕES
        # ----------------------------------------------------

        mouse = pygame.mouse.get_pos()

        for i, opcao in enumerate(opcoes):

            rect = pygame.Rect(
                x,
                y + i * altura_item,
                largura,
                altura_item
            )

            # Hover

            if rect.collidepoint(mouse):

                pygame.draw.rect(
                    self.screen,
                    self.LIGHT_BLUE,
                    rect
                )

            # Divisor

            if i > 0:

                pygame.draw.line(
                    self.screen,
                    self.GRAY,
                    rect.topleft,
                    rect.topright
                )

            imagem = self.font.render(
                opcao,
                True,
                self.BLACK
            )

            imagem_rect = imagem.get_rect(
                center=rect.center
            )

            self.screen.blit(
                imagem,
                imagem_rect
            )

    # ========================================================
    # CLICK NO MENU
    # ========================================================

    def click_menu(self, pos):

        if self.menu_aberto is None:
            return False

        menu_rect = self.menu_aberto[
            "menu_rect"
        ]

        if menu_rect is None:
            return False

        if not menu_rect.collidepoint(pos):

            return False

        categoria = self.menu_aberto[
            "categoria"
        ]

        posicao = self.menu_aberto[
            "posicao"
        ]

        opcoes = self.valores[
            categoria
        ]
        opcoes.sort()
        altura_item = 38

        indice = (
            pos[1]
            - menu_rect.y
        ) // altura_item

        if 0 <= indice < len(opcoes):

            self.tabela[
                categoria
            ][posicao] = opcoes[indice]

        self.menu_aberto = None

        return True

    # ========================================================
    # CLICK NA GRADE
    # ========================================================

    def click_grade(self, pos):

        for categoria in self.categorias:

            for posicao in range(5):

                rect = self.get_cell_rect(
                    categoria,
                    posicao
                )

                if rect.collidepoint(pos):

                    self.abrir_menu(
                        categoria,
                        posicao
                    )

                    return True

        return False

    # ========================================================
    # LIMPAR CÉLULA
    # ========================================================

    def limpar_celula(self, pos):

        for categoria in self.categorias:

            for posicao in range(5):

                rect = self.get_cell_rect(
                    categoria,
                    posicao
                )

                if rect.collidepoint(pos):

                    self.tabela[
                        categoria
                    ][posicao] = ""

                    self.menu_aberto = None

                    return

    def calcular_fonte_dicas(self):

        # Área disponível para o texto
        largura = 550
        altura = self.height - 130

        margem_x = 45
        margem_topo = 65
        margem_bottom = 15

        largura_texto = largura - margem_x - 15
        altura_disponivel = (
            altura
            - margem_topo
            - margem_bottom
        )

        # Começa com a fonte normal
        tamanho = 18

        while tamanho >= 8:

            fonte = pygame.font.SysFont(
                "Fonte\Roboto-Regular.ttf",
                tamanho
            )

            altura_total = 0

            for dica in self.dicas:

                linhas = self.quebrar_texto(
                    dica,
                    fonte,
                    largura_texto
                )

                # Altura das linhas
                altura_total += (
                    len(linhas)
                    * (fonte.get_height() + 4)
                )

                # Espaçamento entre dicas
                altura_total += 15

            if altura_total <= altura_disponivel:
                return fonte

            tamanho -= 1

        # Tamanho mínimo
        return pygame.font.SysFont(
            "Fonte\Roboto-Regular.ttf",
            8
        )

                

    # ========================================================
    # DESENHAR DICAS
    # ========================================================

    def desenhar_dicas(self):

      x = 800
      y = 100

      largura = 550
      altura = self.height - 130

      rect = pygame.Rect(
          x,
          y,
          largura,
          altura
      )

      # Fundo
      pygame.draw.rect(
          self.screen,
          self.WHITE,
          rect
      )

      pygame.draw.rect(
          self.screen,
          self.BLACK,
          rect,
          1
      )

      # ========================================================
      # TÍTULO
      # ========================================================

      imagem = self.title_font.render(
          "Dicas",
          True,
          self.BLACK
      )

      self.screen.blit(
          imagem,
          (
              x + 20,
              y + 15
          )
      )

      # ========================================================
      # FONTE DINÂMICA
      # ========================================================

      fonte = self.calcular_fonte_dicas()

      # ========================================================
      # DICAS
      # ========================================================

      dica_y = y + 65

      largura_texto = largura - 65

      for numero, dica in enumerate(
          self.dicas
      ):

          linhas = self.quebrar_texto(
              dica,
              fonte,
              largura_texto
          )

          # ----------------------------------------------------
          # Número
          # ----------------------------------------------------

          numero_imagem = self.font_bold.render(
              f"{numero + 1}.",
              True,
              self.BLACK
          )

          self.screen.blit(
              numero_imagem,
              (
                  x + 15,
                  dica_y
              )
          )

          # ----------------------------------------------------
          # Texto
          # ----------------------------------------------------

          altura_linha = fonte.get_height() + 4

          for i, linha in enumerate(linhas):

              imagem = fonte.render(
                  linha,
                  True,
                  self.BLACK
              )

              self.screen.blit(
                  imagem,
                  (
                      x + 45,
                      dica_y + i * altura_linha
                  )
              )

          # Próxima dica

          dica_y += (
              len(linhas)
              * altura_linha
              + 15
          )

    # ========================================================
    # EVENTOS
    # ========================================================

    def processar_eventos(self):

        for event in pygame.event.get():

            # Fechar janela

            if event.type == pygame.QUIT:

                return False

            # -----------------------------------------------
            # Mouse
            # -----------------------------------------------

            if event.type == pygame.MOUSEBUTTONDOWN:

                # Botão esquerdo

                if event.button == 1:

                    # Primeiro tenta clicar
                    # em uma opção do menu.

                    if self.click_menu(
                        event.pos
                    ):

                        continue

                    # Depois tenta clicar
                    # em uma célula.

                    if self.click_grade(
                        event.pos
                    ):

                        continue

                    # Clicou fora

                    self.menu_aberto = None

                # -------------------------------------------
                # Botão direito
                # -------------------------------------------

                elif event.button == 3:

                    self.limpar_celula(
                        event.pos
                    )

        return True

    # ========================================================
    # DESENHAR
    # ========================================================

    def desenhar(self):

        self.screen.fill(
            self.BG
        )

        # Título

        titulo = self.title_font.render(
            "Quebra-Cabeça da Zebra",
            True,
            self.BLACK
        )

        self.screen.blit(
            titulo,
            (40, 35)
        )

        # Grade

        self.desenhar_grade()

        # Dicas

        self.desenhar_dicas()

        # Menu por último,
        # para ficar sobre a grade.

        self.desenhar_menu()

        pygame.display.flip()

    # ========================================================
    # EXECUTAR
    # ========================================================

    def executar(self):

        running = True
        while running:

            running = (
                self.processar_eventos()
            )

            self.desenhar()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()