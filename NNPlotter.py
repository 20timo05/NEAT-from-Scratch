import pygame

class Plotter():
    def __init__(self, genome, calculateHandler = None):
        self.nodes = genome.nodes
        self.connections = genome.connections

        self.SHOW_WEIGHTS = True
        self.SCREEN_WIDTH = 700
        self.SCREEN_HEIGHT = 600
        self.CONTROLS_HEADER_HEIGHT = 100

        self.buttons = {
            "random weight": lambda: genome.mutate(0),
            "weight shift": lambda: genome.mutate(1),
            "Link mutate": lambda: genome.mutate(2),
            "Node mutate": lambda: genome.mutate(3),
            "on/ off": lambda: genome.mutate(4),
            "Mutate": lambda: genome.mutate(),
            "Calculate": lambda: calculateHandler()
        }

    def __getcoords(self, pos):
        return (pos.x * self.SCREEN_WIDTH, self.CONTROLS_HEADER_HEIGHT + pos.y * (self.SCREEN_HEIGHT - self.CONTROLS_HEADER_HEIGHT))

    def drawFrame(self, screen, my_font, font_name):
        screen.fill((0, 0, 0))

        self.drawHeader(screen, font_name)
        self.drawNN(screen, my_font)

        pygame.display.update()

    def draw(self):
        pygame.init()
        screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 20)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                
                if event.type == pygame.MOUSEBUTTONUP:
                    posX, posY = pygame.mouse.get_pos()
                    if posY < self.CONTROLS_HEADER_HEIGHT:
                        button_clicked_idx = int(posX / (self.SCREEN_WIDTH / len(self.buttons)))
                        self.buttons[list(self.buttons.keys())[button_clicked_idx]]()

            self.drawFrame(screen, my_font, 'Comic Sans MS')

        pygame.quit()
    
    def drawNN(self, screen, my_font):
        # draw circle for each node
        for node in self.nodes:
            pygame.draw.circle(
                screen, (255, 255, 255), self.__getcoords(node), 10)

        # draw line for each connection
        for con in self.connections:
            color = (255, 255, 255) if con.enabled else (255, 0, 0)
            startPos = self.__getcoords(con.origin)
            endPos = self.__getcoords(con.target)
            pygame.draw.line(screen, color, startPos, endPos)

            # draw weight
            if self.SHOW_WEIGHTS and con.weight != None and con.enabled:
                text_surface = my_font.render(
                    f"{round(con.weight, 3)}", False, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(startPos[0] + (
                    endPos[0] - startPos[0]) * con.percentOfLine, startPos[1] + (endPos[1] - startPos[1]) * con.percentOfLine))
                screen.blit(text_surface, text_rect)
    
    def drawHeader(self, screen, font_name):
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, self.CONTROLS_HEADER_HEIGHT - 5, self.SCREEN_WIDTH, 5))

        button_width = self.SCREEN_WIDTH / len(self.buttons)

        longest_text = max(self.buttons.keys(), key=len)
        max_font_size = self.__get_maximum_font_size(longest_text, button_width - 10, self.SCREEN_HEIGHT, font_name)
        my_font = pygame.font.SysFont(font_name, max_font_size)

        for idx, buttonText in enumerate(self.buttons.keys()):
            text_surface = my_font.render(
                    buttonText, False, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(button_width * (idx + 0.5), self.CONTROLS_HEADER_HEIGHT / 2))
            screen.blit(text_surface, text_rect)
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(button_width * idx, 0, 5, self.CONTROLS_HEADER_HEIGHT))
    
    
    def __get_maximum_font_size(self, text, box_width, box_height, font_name, upper_bound=72, lower_bound=1):
        pygame.init()
        font = pygame.font.SysFont(font_name, upper_bound)
        text_width, text_height = font.size(text)

        # Binary search to find the maximum font size that fits the box
        while upper_bound - lower_bound > 1:
            middle_font_size = (upper_bound + lower_bound) // 2
            font = pygame.font.SysFont(font_name, middle_font_size)
            text_width, text_height = font.size(text)

            if text_width <= box_width and text_height <= box_height:
                lower_bound = middle_font_size
            else:
                upper_bound = middle_font_size

        return lower_bound
