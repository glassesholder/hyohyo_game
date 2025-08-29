import pygame
import random
import sys
import math
from datetime import datetime

def christmas_runner():
    """크리스마스 어드벤처 러너 게임"""
    # 초기화
    pygame.init()

    # 화면 크기 및 설정
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 700
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🎄 크리스마스 어드벤처 러너 🎄")

    # 색상 팔레트 (크리스마스 테마)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    DARK_GREEN = (0, 100, 0)
    LIGHT_GREEN = (34, 139, 34)
    RED = (220, 20, 60)
    GOLD = (255, 215, 0)
    SILVER = (192, 192, 192)
    SNOW_WHITE = (250, 250, 250)
    NIGHT_BLUE = (25, 25, 112)
    STAR_YELLOW = (255, 255, 224)
    BROWN = (139, 69, 19)

    # 게임 클래스들
    class Particle:
        def __init__(self, x, y, color, size=3):
            self.x = x
            self.y = y
            self.vx = random.uniform(-2, 2)
            self.vy = random.uniform(-1, 1)
            self.color = color
            self.size = size
            self.life = 60
            
        def update(self):
            self.x += self.vx
            self.y += self.vy
            self.life -= 1
            
        def draw(self, screen):
            if self.life > 0:
                alpha = max(0, self.life / 60 * 255)
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

    class PowerUp:
        def __init__(self, x, y, type_name):
            self.rect = pygame.Rect(x, y, 30, 30)
            self.type = type_name
            self.bounce = 0
            
        def update(self):
            self.rect.x -= obstacle_speed
            self.bounce += 0.2
            
        def draw(self, screen):
            bounce_offset = math.sin(self.bounce) * 5
            if self.type == "double_jump":
                pygame.draw.circle(screen, GOLD, (self.rect.centerx, int(self.rect.centery + bounce_offset)), 15)
                pygame.draw.circle(screen, WHITE, (self.rect.centerx, int(self.rect.centery + bounce_offset)), 10)
            elif self.type == "shield":
                pygame.draw.circle(screen, SILVER, (self.rect.centerx, int(self.rect.centery + bounce_offset)), 15)
                pygame.draw.circle(screen, LIGHT_GREEN, (self.rect.centerx, int(self.rect.centery + bounce_offset)), 10)

    # 플레이어 설정
    player_width, player_height = 40, 60
    player = pygame.Rect(100, SCREEN_HEIGHT - 150, player_width, player_height)
    player_jump = False
    y_velocity = 0
    gravity = 0.8
    jump_charge = 0
    max_jump_charge = 25
    charging = False
    double_jump_available = False
    shield_active = False
    shield_timer = 0

    # 장애물 설정
    obstacles = []
    OBSTACLE_WIDTH = 60
    obstacle_timer = 0
    obstacle_speed = 6
    obstacle_patterns = ["single", "double", "triple", "moving"]

    # 파워업 설정
    powerups = []
    powerup_timer = 0

    # 파티클 시스템
    particles = []
    snowflakes = []
    stars = []

    # 점수 시스템
    score = 0
    high_score = 0
    combo = 0
    max_combo = 0

    # 배경 요소 초기화
    for _ in range(100):
        snowflakes.append({
            'x': random.randint(0, SCREEN_WIDTH),
            'y': random.randint(0, SCREEN_HEIGHT),
            'speed': random.uniform(1, 3),
            'size': random.randint(2, 4)
        })

    for _ in range(50):
        stars.append({
            'x': random.randint(0, SCREEN_WIDTH),
            'y': random.randint(0, SCREEN_HEIGHT // 2),
            'twinkle': random.randint(0, 60)
        })

    # 폰트 설정
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)
    start_time = datetime.now()
    elapsed_time = 0

    # 게임 루프 제어
    clock = pygame.time.Clock()
    running = True
    game_over = False
    difficulty_level = 1

    # 게임 함수들
    def draw_background():
        # 그라데이션 배경 (밤하늘)
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(NIGHT_BLUE[0] * (1 - color_ratio) + BLACK[0] * color_ratio)
            g = int(NIGHT_BLUE[1] * (1 - color_ratio) + BLACK[1] * color_ratio)
            b = int(NIGHT_BLUE[2] * (1 - color_ratio) + BLACK[2] * color_ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # 별 그리기
        for star in stars:
            star['twinkle'] = (star['twinkle'] + 1) % 120
            alpha = abs(math.sin(star['twinkle'] * 0.1)) * 255
            if alpha > 100:
                pygame.draw.circle(screen, STAR_YELLOW, (star['x'], star['y']), 2)
        
        # 눈 내리기
        for flake in snowflakes:
            flake['y'] += flake['speed']
            flake['x'] += math.sin(flake['y'] * 0.01) * 0.5
            if flake['y'] > SCREEN_HEIGHT:
                flake['y'] = -10
                flake['x'] = random.randint(0, SCREEN_WIDTH)
            pygame.draw.circle(screen, SNOW_WHITE, (int(flake['x']), int(flake['y'])), flake['size'])
        
        # 바닥 그리기
        pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        for i in range(0, SCREEN_WIDTH, 20):
            pygame.draw.circle(screen, SNOW_WHITE, (i, SCREEN_HEIGHT - 25), 8)

    def draw_player():
        # 산타 캐릭터 그리기
        # 몸통
        pygame.draw.ellipse(screen, RED, (player.x, player.y + 20, player_width, player_height - 20))
        # 머리
        pygame.draw.circle(screen, (255, 220, 177), (player.centerx, player.y + 15), 15)
        # 모자
        hat_points = [(player.x + 5, player.y + 5), (player.x + 35, player.y + 5), (player.x + 40, player.y - 5)]
        pygame.draw.polygon(screen, RED, hat_points)
        pygame.draw.circle(screen, WHITE, (player.x + 40, player.y - 5), 5)
        # 벨트
        pygame.draw.rect(screen, BLACK, (player.x + 5, player.y + 35, player_width - 10, 8))
        pygame.draw.rect(screen, GOLD, (player.centerx - 3, player.y + 35, 6, 8))
        
        # 쉴드 효과
        if shield_active:
            pygame.draw.circle(screen, SILVER, player.center, 35, 3)
            pygame.draw.circle(screen, LIGHT_GREEN, player.center, 32, 2)

    def create_obstacle_pattern(pattern_type, x):
        if pattern_type == "single":
            height = random.randint(80, 150)
            obstacles.append({
                'rect': pygame.Rect(x, SCREEN_HEIGHT - 50 - height, OBSTACLE_WIDTH, height),
                'type': 'tree',
                'moving': False
            })
        elif pattern_type == "double":
            for i in range(2):
                height = random.randint(60, 120)
                obstacles.append({
                    'rect': pygame.Rect(x + i * 80, SCREEN_HEIGHT - 50 - height, OBSTACLE_WIDTH, height),
                    'type': 'tree',
                    'moving': False
                })
        elif pattern_type == "triple":
            heights = [100, 60, 120]
            for i in range(3):
                obstacles.append({
                    'rect': pygame.Rect(x + i * 60, SCREEN_HEIGHT - 50 - heights[i], OBSTACLE_WIDTH, heights[i]),
                    'type': 'tree',
                    'moving': False
                })
        elif pattern_type == "moving":
            height = random.randint(100, 180)
            obstacles.append({
                'rect': pygame.Rect(x, SCREEN_HEIGHT - 50 - height, OBSTACLE_WIDTH, height),
                'type': 'moving_tree',
                'moving': True,
                'move_direction': 1,
                'original_y': SCREEN_HEIGHT - 50 - height
            })

    def draw_obstacle(obstacle):
        rect = obstacle['rect']
        if obstacle['type'] in ['tree', 'moving_tree']:
            # 크리스마스 트리 그리기
            # 나무 몸통
            trunk_rect = pygame.Rect(rect.centerx - 8, rect.bottom - 20, 16, 20)
            pygame.draw.rect(screen, BROWN, trunk_rect)
            
            # 트리 층들
            layers = 3
            layer_height = (rect.height - 20) // layers
            for i in range(layers):
                layer_y = rect.y + i * layer_height
                layer_width = 50 - i * 8
                points = [
                    (rect.centerx, layer_y),
                    (rect.centerx - layer_width//2, layer_y + layer_height),
                    (rect.centerx + layer_width//2, layer_y + layer_height)
                ]
                pygame.draw.polygon(screen, DARK_GREEN, points)
                # 장식
                if i % 2 == 0:
                    pygame.draw.circle(screen, RED, (rect.centerx - 10, layer_y + layer_height//2), 3)
                    pygame.draw.circle(screen, GOLD, (rect.centerx + 10, layer_y + layer_height//2), 3)

    # 메인 게임 루프
    while True:
        if running:
            draw_background()

            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not player_jump:  # 스페이스바로 점프
                        charging = True
                    elif event.key == pygame.K_SPACE and player_jump and double_jump_available:
                        y_velocity = -15
                        double_jump_available = False
                        # 파티클 효과
                        for _ in range(10):
                            particles.append(Particle(player.centerx, player.centery, GOLD))
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE and charging:
                        charging = False
                        player_jump = True
                        y_velocity = -jump_charge * 0.8
                        double_jump_available = True
                        jump_charge = 0
                        # 점프 파티클
                        for _ in range(5):
                            particles.append(Particle(player.centerx, player.bottom, WHITE))

            # 점프 게이지 충전
            if charging:
                jump_charge += 2
                if jump_charge > max_jump_charge:
                    jump_charge = max_jump_charge

            # 쉴드 타이머 처리
            if shield_active:
                shield_timer -= 1
                if shield_timer <= 0:
                    shield_active = False

            # 플레이어 점프 처리
            if player_jump:
                player.y += y_velocity
                y_velocity += gravity
                if player.y >= SCREEN_HEIGHT - 150:  # 바닥에 닿으면
                    player.y = SCREEN_HEIGHT - 150
                    player_jump = False
                    y_velocity = 0

            # 장애물 생성 및 패턴
            if obstacle_timer > max(60 - difficulty_level * 5, 30):
                pattern = random.choice(obstacle_patterns)
                create_obstacle_pattern(pattern, SCREEN_WIDTH)
                obstacle_timer = 0
            obstacle_timer += 1

            # 파워업 생성
            if powerup_timer > 300:  # 5초마다
                powerup_type = random.choice(["double_jump", "shield"])
                powerups.append(PowerUp(SCREEN_WIDTH, SCREEN_HEIGHT - 200, powerup_type))
                powerup_timer = 0
            powerup_timer += 1

            # 장애물 업데이트
            for obstacle in obstacles[:]:
                obstacle['rect'].x -= obstacle_speed
                
                # 움직이는 장애물 처리
                if obstacle['moving']:
                    obstacle['rect'].y += obstacle['move_direction'] * 2
                    if obstacle['rect'].y <= obstacle['original_y'] - 30:
                        obstacle['move_direction'] = 1
                    elif obstacle['rect'].y >= obstacle['original_y'] + 30:
                        obstacle['move_direction'] = -1
                
                # 충돌 검사
                if obstacle['rect'].colliderect(player) and not shield_active:
                    running = False
                    game_over = True
                    elapsed_time = (datetime.now() - start_time).seconds
                    if score > high_score:
                        high_score = score
                
                # 화면 밖으로 나간 장애물 제거 및 점수 증가
                if obstacle['rect'].x < -OBSTACLE_WIDTH:
                    obstacles.remove(obstacle)
                    score += 10
                    combo += 1
                    if combo > max_combo:
                        max_combo = combo
                    # 콤보 보너스
                    if combo % 5 == 0:
                        score += combo * 2
                        for _ in range(combo):
                            particles.append(Particle(50, 50, GOLD, 5))

            # 파워업 업데이트
            for powerup in powerups[:]:
                powerup.update()
                
                # 파워업 충돌 검사
                if powerup.rect.colliderect(player):
                    if powerup.type == "double_jump":
                        double_jump_available = True
                    elif powerup.type == "shield":
                        shield_active = True
                        shield_timer = 300  # 5초
                    powerups.remove(powerup)
                    score += 50
                    # 파워업 파티클
                    for _ in range(15):
                        particles.append(Particle(powerup.rect.centerx, powerup.rect.centery, GOLD, 4))
                
                # 화면 밖으로 나간 파워업 제거
                if powerup.rect.x < -30:
                    powerups.remove(powerup)

            # 파티클 업데이트
            for particle in particles[:]:
                particle.update()
                if particle.life <= 0:
                    particles.remove(particle)

            # 난이도 증가
            current_time = (datetime.now() - start_time).seconds
            difficulty_level = min(10, current_time // 15 + 1)
            obstacle_speed = 6 + difficulty_level * 0.5

            # 그리기
            draw_player()
            
            # 장애물 그리기
            for obstacle in obstacles:
                draw_obstacle(obstacle)
            
            # 파워업 그리기
            for powerup in powerups:
                powerup.draw(screen)
            
            # 파티클 그리기
            for particle in particles:
                particle.draw(screen)
            
            # UI 그리기
            # 점프 게이지
            if charging:
                gauge_width = int((jump_charge / max_jump_charge) * 200)
                pygame.draw.rect(screen, RED, (50, SCREEN_HEIGHT - 100, gauge_width, 20))
                pygame.draw.rect(screen, WHITE, (50, SCREEN_HEIGHT - 100, 200, 20), 3)
            
            # 점수 및 정보
            score_text = font_medium.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            
            combo_text = font_small.render(f"Combo: {combo}", True, GOLD)
            screen.blit(combo_text, (10, 50))
            
            level_text = font_small.render(f"Level: {difficulty_level}", True, WHITE)
            screen.blit(level_text, (10, 75))
            
            time_text = font_small.render(f"Time: {current_time}s", True, WHITE)
            screen.blit(time_text, (10, 100))
            
            # 파워업 상태 표시
            if shield_active:
                shield_text = font_small.render(f"Shield: {shield_timer//60 + 1}s", True, SILVER)
                screen.blit(shield_text, (SCREEN_WIDTH - 150, 10))
            
            if double_jump_available:
                jump_text = font_small.render("Double Jump Ready!", True, GOLD)
                screen.blit(jump_text, (SCREEN_WIDTH - 200, 35))

            # 화면 업데이트
            pygame.display.flip()
            clock.tick(60)

        elif game_over:  # 게임 오버 화면
            draw_background()
            
            # 반투명 오버레이
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # 게임 오버 텍스트
            game_over_text = font_large.render("* GAME OVER *", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            screen.blit(game_over_text, text_rect)
            
            # 최종 점수
            final_score_text = font_medium.render(f"Final Score: {score}", True, GOLD)
            score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(final_score_text, score_rect)
            
            # 최고 점수
            if score == high_score and score > 0:
                new_record_text = font_medium.render("NEW HIGH SCORE!", True, GOLD)
                record_rect = new_record_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
                screen.blit(new_record_text, record_rect)
            else:
                high_score_text = font_small.render(f"High Score: {high_score}", True, WHITE)
                high_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
                screen.blit(high_score_text, high_rect)
            
            # 통계
            stats_text = font_small.render(f"Max Combo: {max_combo} | Time: {elapsed_time}s | Level: {difficulty_level}", True, WHITE)
            stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
            screen.blit(stats_text, stats_rect)
            
            # 재시작 안내
            restart_text = font_medium.render("Press R to Restart | ESC to Quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            screen.blit(restart_text, restart_rect)

            # 다시하기 버튼 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # 게임 상태 초기화
                        running = True
                        game_over = False
                        player.y = SCREEN_HEIGHT - 150
                        player_jump = False
                        y_velocity = 0
                        obstacles = []
                        powerups = []
                        particles = []
                        obstacle_speed = 6
                        obstacle_timer = 0
                        powerup_timer = 0
                        score = 0
                        combo = 0
                        difficulty_level = 1
                        shield_active = False
                        shield_timer = 0
                        double_jump_available = False
                        charging = False
                        jump_charge = 0
                        start_time = datetime.now()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

            pygame.display.flip()
            clock.tick(60)
