import pygame
from core.environment import ForestEnv
from core.agent import ChiliAgent
from core.renderer import Renderer
import config

INFO_WIDTH = 260  # Độ rộng khung thông tin bên phải


def main():
    pygame.init()
    screen = pygame.display.set_mode((config.MAP_WIDTH * config.TILE_SIZE + INFO_WIDTH, config.MAP_HEIGHT * config.TILE_SIZE))
    pygame.display.set_caption('Spicy Forest Game')
    clock = pygame.time.Clock()

    env = ForestEnv()
    agent = ChiliAgent(method='td')  # hoặc 'td'
    renderer = Renderer(screen, info_width=INFO_WIDTH)

    running = True
    state = env.reset()
    step_count = 0
    state_history = []
    last_action = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Agent chọn hành động
        action = agent.get_action(state)
        next_state, reward, done, _ = env.step(action)
        agent.remember(state, action, reward)
        step_count += 1
        state_history.append(tuple(int(x) for x in state['agent']))
        # Thông tin hiển thị
        info = {
            'algorithm': agent.method.upper(),
            'step': step_count,
            'state': tuple(int(x) for x in state['agent']),
            'reward': reward,
            'done': done,
            'q_value': agent.Q.get(agent._state_to_key(state), None),
            'action': action,
            'explain': '',
            'history': state_history[-30:]  # chỉ lấy 30 bước gần nhất
        }
        # Giải thích từng bước
        action_map = ['Lên', 'Xuống', 'Trái', 'Phải']
        if agent.method == 'mc':
            info['explain'] = f"Agent chọn action: {action_map[action]} tại state {info['state']}, nhận reward {reward}.\nQ sẽ được cập nhật sau khi kết thúc episode."
        else:
            info['explain'] = f"Agent chọn action: {action_map[action]} tại state {info['state']}, nhận reward {reward}.\nQ được cập nhật ngay sau bước này."
        state = next_state

        renderer.draw(env, info)
        clock.tick(5)

        if done:
            agent.update(done)
            state = env.reset()
            step_count = 0
            state_history = []
            last_action = None

    pygame.quit()

if __name__ == '__main__':
    main()
