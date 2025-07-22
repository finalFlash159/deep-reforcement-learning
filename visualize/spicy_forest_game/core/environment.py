import numpy as np
import config
from collections import deque

class ForestEnv:
    def __init__(self):
        self.width = config.MAP_WIDTH
        self.height = config.MAP_HEIGHT
        self.reset()

    def reset(self):
        while True:
            self.agent_pos = [0, 0]
            self.goal_pos = [self.width - 1, self.height - 1]
            self.trees = self._generate_trees()
            self.rocks = self._generate_rocks()
            self.waters = self._generate_waters()
            self.done = False
            if self._has_path():
                break
        return self._get_obs()

    def _generate_trees(self):
        trees = set()
        while len(trees) < int(self.width * self.height * 0.15):
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            pos = (x, y)
            if pos != tuple(self.agent_pos) and pos != tuple(self.goal_pos):
                trees.add(pos)
        return trees

    def _generate_rocks(self):
        rocks = set()
        while len(rocks) < config.ROCK_COUNT:
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            pos = (x, y)
            if pos != tuple(self.agent_pos) and pos != tuple(self.goal_pos) and pos not in self.trees:
                rocks.add(pos)
        return rocks

    def _generate_waters(self):
        waters = set()
        while len(waters) < config.WATER_COUNT:
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            pos = (x, y)
            if pos != tuple(self.agent_pos) and pos != tuple(self.goal_pos) and pos not in self.trees and pos not in self.rocks:
                waters.add(pos)
        return waters

    def _has_path(self):
        # BFS kiểm tra có đường đi từ agent đến goal không
        queue = deque([tuple(self.agent_pos)])
        visited = set([tuple(self.agent_pos)])
        obstacles = self.trees | self.rocks
        while queue:
            x, y = queue.popleft()
            if (x, y) == tuple(self.goal_pos):
                return True
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in visited and (nx, ny) not in obstacles:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
        return False

    def step(self, action):
        if self.done:
            return self._get_obs(), 0, True, {}
        dx, dy = 0, 0
        if action == 0:
            dy = -1
        elif action == 1:
            dy = 1
        elif action == 2:
            dx = -1
        elif action == 3:
            dx = 1
        new_x = np.clip(self.agent_pos[0] + dx, 0, self.width - 1)
        new_y = np.clip(self.agent_pos[1] + dy, 0, self.height - 1)
        new_pos = (new_x, new_y)
        reward = config.REWARD_GRASS
        # Không cho đi vào đá hoặc cây
        if new_pos in self.rocks or new_pos in self.trees:
            new_pos = tuple(self.agent_pos)  # Không di chuyển
            reward = config.REWARD_GRASS  # Không phạt thêm
        elif new_pos == tuple(self.goal_pos):
            reward = config.REWARD_GOAL
            self.done = True
        elif new_pos in self.waters:
            reward = config.REWARD_WATER
            self.waters.remove(new_pos)
        self.agent_pos = list(new_pos)
        return self._get_obs(), reward, self.done, {}

    def _get_obs(self):
        return {
            'agent': tuple(self.agent_pos),
            'goal': tuple(self.goal_pos),
            'trees': self.trees,
            'rocks': self.rocks,
            'waters': self.waters
        }
