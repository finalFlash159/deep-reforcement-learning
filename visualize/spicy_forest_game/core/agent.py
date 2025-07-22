import numpy as np

class ChiliAgent:
    def __init__(self, action_space=4, method='mc', epsilon=0.1, alpha=0.1, gamma=0.99):
        self.action_space = action_space
        self.method = method  # 'mc' hoặc 'td'
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.Q = {}  # Q-table: {(state): [q0, q1, q2, q3]}
        self.episode = []  # Lưu lịch sử episode (state, action, reward)

    def get_action(self, state):
        state_key = self._state_to_key(state)
        if np.random.rand() < self.epsilon or state_key not in self.Q:
            return np.random.randint(self.action_space)
        return np.argmax(self.Q[state_key])

    def update(self, done):
        if self.method == 'mc':
            self._mc_update()
        elif self.method == 'td':
            self._td_update()
        self.episode = []

    def _mc_update(self):
        G = 0
        visited = set()
        for state, action, reward in reversed(self.episode):
            G = self.gamma * G + reward
            key = self._state_to_key(state)
            if (key, action) not in visited:
                visited.add((key, action))
                if key not in self.Q:
                    self.Q[key] = np.zeros(self.action_space)
                self.Q[key][action] += self.alpha * (G - self.Q[key][action])

    def _td_update(self):
        for i, (state, action, reward) in enumerate(self.episode):
            key = self._state_to_key(state)
            if key not in self.Q:
                self.Q[key] = np.zeros(self.action_space)
            if i < len(self.episode) - 1:
                next_state = self._state_to_key(self.episode[i+1][0])
                next_q = np.max(self.Q.get(next_state, np.zeros(self.action_space)))
            else:
                next_q = 0
            self.Q[key][action] += self.alpha * (reward + self.gamma * next_q - self.Q[key][action])

    def remember(self, state, action, reward):
        self.episode.append((state, action, reward))

    def _state_to_key(self, state):
        # Chuyển state dict sang tuple để làm key
        return (state['agent'], state['goal'], tuple(sorted(state['trees'])))
