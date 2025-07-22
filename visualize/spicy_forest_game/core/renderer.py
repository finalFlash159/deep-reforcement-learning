import pygame
import os
import config

class Renderer:
    def __init__(self, screen, info_width=0):
        self.screen = screen
        self.tile_size = config.TILE_SIZE
        self.info_width = info_width
        self.assets = self._load_assets()
        self.font = pygame.font.SysFont('Arial', 18)
        self.font_small = pygame.font.SysFont('Arial', 14)

    def _load_assets(self):
        base = os.path.dirname(os.path.abspath(__file__))
        assets = {}
        assets['grass'] = pygame.image.load(os.path.join(base, '../assets/tiles/grass.png'))
        assets['tree'] = pygame.image.load(os.path.join(base, '../assets/tiles/tree.png'))
        assets['goal'] = pygame.image.load(os.path.join(base, '../assets/tiles/goal.png'))
        assets['chili_idle'] = pygame.image.load(os.path.join(base, '../assets/sprites/chili_idle.png'))
        assets['chili_walk'] = pygame.image.load(os.path.join(base, '../assets/sprites/chili_walk.png'))
        assets['water'] = pygame.image.load(os.path.join(base, '../assets/tiles/water.png'))
        assets['rock'] = pygame.image.load(os.path.join(base, '../assets/tiles/rock.png'))
        return assets

    def draw(self, env, info=None):
        # Vẽ map
        for y in range(env.height):
            for x in range(env.width):
                pos = (x * self.tile_size, y * self.tile_size)
                self.screen.blit(self.assets['grass'], pos)
                if (x, y) in env.rocks:
                    self.screen.blit(self.assets['rock'], pos)
                if (x, y) in env.trees:
                    self.screen.blit(self.assets['tree'], pos)
                if (x, y) in env.waters:
                    self.screen.blit(self.assets['water'], pos)
                # Vẽ goal sau cùng để không bị che khuất
                if (x, y) == env.goal_pos:
                    self.screen.blit(self.assets['goal'], pos)
        # Highlight đường đi đã qua
        if info and 'history' in info:
            for st in info['history']:
                hx, hy = st
                highlight_rect = pygame.Rect(hx * self.tile_size, hy * self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(self.screen, (255, 255, 0, 60), highlight_rect, 0)
        # Highlight state hiện tại
        if info:
            cx, cy = info['state']
            cur_rect = pygame.Rect(cx * self.tile_size, cy * self.tile_size, self.tile_size, self.tile_size)
            pygame.draw.rect(self.screen, (255, 100, 100, 80), cur_rect, 0)
        # Vẽ agent
        agent_pos = (env.agent_pos[0] * self.tile_size, env.agent_pos[1] * self.tile_size)
        self.screen.blit(self.assets['chili_idle'], agent_pos)
        # Vẽ action vừa chọn (mũi tên)
        if info and 'action' in info:
            self._draw_action_arrow(info['state'], info['action'])
        # Hiển thị Q-value quanh agent
        if info and info['q_value'] is not None:
            self._draw_q_values(info['state'], info['q_value'])
        # Vẽ khung thông tin bên phải
        if self.info_width and info:
            self._draw_info_panel(env, info)
        pygame.display.flip()

    def _draw_action_arrow(self, state, action):
        x, y = state
        cx = x * self.tile_size + self.tile_size // 2
        cy = y * self.tile_size + self.tile_size // 2
        color = (0, 0, 200)
        if action == 0:  # Lên
            pygame.draw.polygon(self.screen, color, [(cx, cy-16), (cx-6, cy-2), (cx+6, cy-2)])
        elif action == 1:  # Xuống
            pygame.draw.polygon(self.screen, color, [(cx, cy+16), (cx-6, cy+2), (cx+6, cy+2)])
        elif action == 2:  # Trái
            pygame.draw.polygon(self.screen, color, [(cx-16, cy), (cx-2, cy-6), (cx-2, cy+6)])
        elif action == 3:  # Phải
            pygame.draw.polygon(self.screen, color, [(cx+16, cy), (cx+2, cy-6), (cx+2, cy+6)])

    def _draw_q_values(self, state, q_values):
        x, y = state
        actions = ['↑', '↓', '←', '→']
        for i, q in enumerate(q_values):
            if i == 0:
                pos = (x * self.tile_size + self.tile_size//2 - 8, y * self.tile_size + 2)
            elif i == 1:
                pos = (x * self.tile_size + self.tile_size//2 - 8, y * self.tile_size + self.tile_size - 18)
            elif i == 2:
                pos = (x * self.tile_size + 2, y * self.tile_size + self.tile_size//2 - 8)
            elif i == 3:
                pos = (x * self.tile_size + self.tile_size - 18, y * self.tile_size + self.tile_size//2 - 8)
            text = self.font_small.render(f"{actions[i]}:{q:.2f}", True, (0, 80, 180))
            self.screen.blit(text, pos)

    def _draw_info_panel(self, env, info):
        panel_x = config.MAP_WIDTH * self.tile_size
        panel_y = 0
        panel_w = self.info_width
        panel_h = config.MAP_HEIGHT * self.tile_size
        # Nền trắng mờ
        pygame.draw.rect(self.screen, (245, 245, 245), (panel_x, panel_y, panel_w, panel_h))
        # Viền
        pygame.draw.rect(self.screen, (80, 80, 80), (panel_x, panel_y, panel_w, panel_h), 2)
        y = 20
        x = panel_x + 16
        # Thuật toán
        text = self.font.render(f"Thuật toán: {info['algorithm']}", True, (30, 30, 120))
        self.screen.blit(text, (x, y))
        y += 32
        # Bước
        text = self.font.render(f"Bước: {info['step']}", True, (0, 0, 0))
        self.screen.blit(text, (x, y))
        y += 28
        # State
        text = self.font.render(f"State: {info['state']}", True, (0, 0, 0))
        self.screen.blit(text, (x, y))
        y += 28
        # Reward
        text = self.font.render(f"Reward: {info['reward']}", True, (0, 0, 0))
        self.screen.blit(text, (x, y))
        y += 28
        # Done
        text = self.font.render(f"Done: {info['done']}", True, (0, 0, 0))
        self.screen.blit(text, (x, y))
        y += 28
        # Q-value
        qv = info['q_value']
        if qv is not None:
            text = self.font_small.render(f"Q-value: {qv}", True, (0, 80, 0))
            self.screen.blit(text, (x, y))
            y += 24
        # Giải thích thuật toán
        y += 10
        lines = info['explain'].split('\n')
        for line in lines:
            text = self.font_small.render(line, True, (80, 80, 80))
            self.screen.blit(text, (x, y))
            y += 20
