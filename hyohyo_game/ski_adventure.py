import pygame
import random
import math
import sys
from datetime import datetime

def ski_adventure():
    """눈덩이 대피하기 - 스키 어드벤처 게임"""
    # 초기화
    pygame.init()

    # 화면 설정
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("❄️ 눈덩이 대피하기 - 스키 어드벤처 ❄️")

    # 색상 팔레트
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (135, 206, 235)  # 하늘색
    DARK_BLUE = (70, 130, 180)
    SNOW_WHITE = (250, 250, 250)
    ICE_BLUE = (173, 216, 230)
    RED = (220, 20, 60)
    ORANGE = (255, 165, 0)
    YELLOW = (255, 255, 0)
    GREEN = (34, 139, 34)
    PURPLE = (138, 43, 226)
    GOLD = (255, 215, 0)
    SILVER = (192, 192, 192)

    # 게임 클래스들
    class Snowball:
        def __init__(self, x, y, size, speed, ball_type="normal"):
            self.x = x
            self.y = y
            self.size = size
            self.speed = speed
            self.type = ball_type
            self.rect = pygame.Rect(x - size, y - size, size * 2, size * 2)
            self.rotation = 0
            self.bounce_offset = 0
            self.trail = []  # 궤적 효과
            
        def update(self):
            self.y += self.speed
            self.rect.y = self.y - self.size
            self.rotation += 5
            self.bounce_offset += 0.1
            
            # 궤적 효과 업데이트
            self.trail.append((self.x, self.y))
            if len(self.trail) > 8:
                self.trail.pop(0)
            
            # 특수 타입별 움직임
            if self.type == "zigzag":
                self.x += math.sin(self.y * 0.02) * 3
                self.rect.x = self.x - self.size
            elif self.type == "bouncing":
                bounce = math.sin(self.bounce_offset) * 2
                self.x += bounce
                self.rect.x = self.x - self.size
        
        def draw(self, screen):
            # 궤적 그리기
            for i, (trail_x, trail_y) in enumerate(self.trail):
                alpha = (i + 1) / len(self.trail)
                trail_size = int(self.size * alpha * 0.5)
                if trail_size > 0:
                    pygame.draw.circle(screen, (200, 200, 255), (int(trail_x), int(trail_y)), trail_size)
            
            # 눈덩이 타입별 그리기
            if self.type == "normal":
                pygame.draw.circle(screen, SNOW_WHITE, (int(self.x), int(self.y)), self.size)
                pygame.draw.circle(screen, ICE_BLUE, (int(self.x), int(self.y)), self.size, 2)
            elif self.type == "ice":
                pygame.draw.circle(screen, ICE_BLUE, (int(self.x), int(self.y)), self.size)
                pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size - 3)
                # 얼음 반짝임 효과
                for i in range(3):
                    angle = self.rotation + i * 120
                    spark_x = self.x + math.cos(math.radians(angle)) * (self.size - 5)
                    spark_y = self.y + math.sin(math.radians(angle)) * (self.size - 5)
                    pygame.draw.circle(screen, WHITE, (int(spark_x), int(spark_y)), 2)
            elif self.type == "giant":
                # 거대 눈덩이 - 그라데이션 효과
                for i in range(self.size, 0, -3):
                    color_intensity = 255 - (self.size - i) * 2
                    color = (color_intensity, color_intensity, 255)
                    pygame.draw.circle(screen, color, (int(self.x), int(self.y)), i)
            elif self.type == "zigzag":
                pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.size)
                pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.size - 3)
            elif self.type == "bouncing":
                pygame.draw.circle(screen, PURPLE, (int(self.x), int(self.y)), self.size)
                pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size - 3)

    class PowerUp:
        def __init__(self, x, y, power_type):
            self.x = x
            self.y = y
            self.type = power_type
            self.rect = pygame.Rect(x - 15, y - 15, 30, 30)
            self.bounce = 0
            self.rotation = 0
            
        def update(self):
            self.y += 3
            self.rect.y = self.y - 15
            self.bounce += 0.2
            self.rotation += 8
            
        def draw(self, screen):
            bounce_offset = math.sin(self.bounce) * 5
            draw_y = int(self.y + bounce_offset)
            
            if self.type == "shield":
                pygame.draw.circle(screen, SILVER, (int(self.x), draw_y), 15)
                pygame.draw.circle(screen, BLUE, (int(self.x), draw_y), 10)
            elif self.type == "slow":
                pygame.draw.circle(screen, GOLD, (int(self.x), draw_y), 15)
                pygame.draw.circle(screen, YELLOW, (int(self.x), draw_y), 10)
            elif self.type == "score":
                pygame.draw.circle(screen, GREEN, (int(self.x), draw_y), 15)
                pygame.draw.circle(screen, WHITE, (int(self.x), draw_y), 10)

    class Particle:
        def __init__(self, x, y, color, velocity_x=0, velocity_y=0, life=60):
            self.x = x
            self.y = y
            self.vx = velocity_x + random.uniform(-2, 2)
            self.vy = velocity_y + random.uniform(-2, 2)
            self.color = color
            self.life = life
            self.max_life = life
            self.size = random.randint(2, 5)
            
        def update(self):
            self.x += self.vx
            self.y += self.vy
            self.life -= 1
            self.vy += 0.1  # 중력
            
        def draw(self, screen):
            if self.life > 0:
                alpha = self.life / self.max_life
                size = int(self.size * alpha)
                if size > 0:
                    pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

    # 플레이어 설정
    player_width, player_height = 50, 70
    player = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, player_width, player_height)
    player_speed = 8

    # 게임 상태 변수
    snowballs = []
    powerups = []
    particles = []
    background_snow = []

    # 게임 시스템
    score = 0
    high_score = 0
    survival_time = 0
    start_time = datetime.now()
    difficulty_level = 1
    snowball_spawn_timer = 0
    powerup_spawn_timer = 0

    # 파워업 상태
    shield_active = False
    shield_timer = 0
    slow_motion_active = False
    slow_motion_timer = 0
    score_multiplier = 1
    multiplier_timer = 0

    # 배경 눈송이 초기화
    for _ in range(150):
        background_snow.append({
            'x': random.randint(0, SCREEN_WIDTH),
            'y': random.randint(0, SCREEN_HEIGHT),
            'speed': random.uniform(1, 4),
            'size': random.randint(1, 3),
            'sway': random.uniform(0, 2 * math.pi)
        })

    # 폰트 설정
    font_large = pygame.font.Font(None, 56)
    font_medium = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)

    # 게임 루프 제어
    clock = pygame.time.Clock()
    running = True
    game_over = False

    def draw_background():
        # 하늘 그라데이션
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(BLUE[0] * (1 - ratio) + DARK_BLUE[0] * ratio)
            g = int(BLUE[1] * (1 - ratio) + DARK_BLUE[1] * ratio)
            b = int(BLUE[2] * (1 - ratio) + DARK_BLUE[2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # 배경 눈송이
        for flake in background_snow:
            flake['y'] += flake['speed']
            flake['sway'] += 0.02
            flake['x'] += math.sin(flake['sway']) * 0.5
            
            if flake['y'] > SCREEN_HEIGHT:
                flake['y'] = -10
                flake['x'] = random.randint(0, SCREEN_WIDTH)
            
            if 0 <= flake['x'] <= SCREEN_WIDTH:
                pygame.draw.circle(screen, SNOW_WHITE, (int(flake['x']), int(flake['y'])), flake['size'])

    def draw_player():
        # 스키어 캐릭터
        # 몸통 (스키복)
        pygame.draw.ellipse(screen, RED, (player.x + 5, player.y + 25, player_width - 10, player_height - 35))
        
        # 머리
        pygame.draw.circle(screen, (255, 220, 177), (player.centerx, player.y + 15), 12)
        
        # 스키 헬멧
        pygame.draw.circle(screen, BLUE, (player.centerx, player.y + 15), 15, 3)
        
        # 스키 폴대
        pygame.draw.line(screen, BLACK, (player.x + 5, player.y + 30), (player.x - 5, player.y + 50), 3)
        pygame.draw.line(screen, BLACK, (player.x + player_width - 5, player.y + 30), (player.x + player_width + 5, player.y + 50), 3)
        
        # 스키
        pygame.draw.rect(screen, YELLOW, (player.x + 5, player.bottom - 5, player_width - 10, 8))
        
        # 쉴드 효과
        if shield_active:
            shield_radius = 40 + math.sin(pygame.time.get_ticks() * 0.01) * 5
            pygame.draw.circle(screen, SILVER, player.center, int(shield_radius), 3)
            pygame.draw.circle(screen, ICE_BLUE, player.center, int(shield_radius - 3), 2)

    def spawn_snowball():
        x = random.randint(50, SCREEN_WIDTH - 50)
        
        # 난이도에 따른 눈덩이 타입 결정
        if difficulty_level <= 2:
            ball_type = "normal"
            size = random.randint(15, 25)
            speed = random.uniform(3, 5)
        elif difficulty_level <= 4:
            ball_type = random.choice(["normal", "normal", "ice"])
            size = random.randint(15, 30)
            speed = random.uniform(4, 7)
        elif difficulty_level <= 6:
            ball_type = random.choice(["normal", "ice", "zigzag"])
            size = random.randint(15, 35)
            speed = random.uniform(5, 8)
        elif difficulty_level <= 8:
            ball_type = random.choice(["normal", "ice", "zigzag", "bouncing", "giant"])
            size = random.randint(20, 40) if ball_type != "giant" else random.randint(35, 50)
            speed = random.uniform(6, 10)
        else:
            ball_type = random.choice(["normal", "ice", "zigzag", "bouncing", "giant", "giant"])
            size = random.randint(25, 45) if ball_type != "giant" else random.randint(40, 60)
            speed = random.uniform(7, 12)
        
        snowballs.append(Snowball(x, -size, size, speed, ball_type))

    def spawn_powerup():
        x = random.randint(50, SCREEN_WIDTH - 50)
        power_type = random.choice(["shield", "slow", "score"])
        powerups.append(PowerUp(x, -30, power_type))

    def create_explosion_particles(x, y, color, count=15):
        for _ in range(count):
            particles.append(Particle(x, y, color, 
                                    random.uniform(-5, 5), 
                                    random.uniform(-8, -2), 
                                    random.randint(30, 60)))

    # 메인 게임 루프
    while True:
        dt = clock.tick(60) / 1000.0  # 델타 타임
        
        if running:
            draw_background()
            
            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
            # 플레이어 이동
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x > 0:
                player.x -= player_speed
            if keys[pygame.K_RIGHT] and player.x < SCREEN_WIDTH - player_width:
                player.x += player_speed
            if keys[pygame.K_UP] and player.y > 0:
                player.y -= player_speed
            if keys[pygame.K_DOWN] and player.y < SCREEN_HEIGHT - player_height:
                player.y += player_speed
            
            # 시간 및 난이도 업데이트
            current_time = datetime.now()
            survival_time = (current_time - start_time).total_seconds()
            difficulty_level = min(10, int(survival_time // 10) + 1)
            
            # 파워업 타이머 업데이트
            if shield_active:
                shield_timer -= dt
                if shield_timer <= 0:
                    shield_active = False
            
            if slow_motion_active:
                slow_motion_timer -= dt
                if slow_motion_timer <= 0:
                    slow_motion_active = False
            
            if score_multiplier > 1:
                multiplier_timer -= dt
                if multiplier_timer <= 0:
                    score_multiplier = 1
            
            # 눈덩이 생성
            spawn_rate = max(20 - difficulty_level * 2, 8)
            if slow_motion_active:
                spawn_rate *= 2
                
            if snowball_spawn_timer <= 0:
                spawn_snowball()
                if difficulty_level >= 5 and random.random() < 0.3:  # 높은 난이도에서 연속 생성
                    spawn_snowball()
                snowball_spawn_timer = spawn_rate
            snowball_spawn_timer -= 1
            
            # 파워업 생성
            if powerup_spawn_timer <= 0:
                if random.random() < 0.3:  # 30% 확률
                    spawn_powerup()
                powerup_spawn_timer = random.randint(180, 300)  # 3-5초
            powerup_spawn_timer -= 1
            
            # 눈덩이 업데이트
            for snowball in snowballs[:]:
                if slow_motion_active:
                    snowball.speed *= 0.5
                snowball.update()
                if slow_motion_active:
                    snowball.speed *= 2
                
                # 충돌 검사
                if snowball.rect.colliderect(player) and not shield_active:
                    running = False
                    game_over = True
                    if score > high_score:
                        high_score = score
                    # 충돌 파티클
                    create_explosion_particles(player.centerx, player.centery, RED, 20)
                
                # 화면 밖으로 나간 눈덩이 제거 및 점수 증가
                if snowball.y > SCREEN_HEIGHT + 50:
                    snowballs.remove(snowball)
                    points = 10
                    if snowball.type == "ice":
                        points = 15
                    elif snowball.type == "giant":
                        points = 25
                    elif snowball.type in ["zigzag", "bouncing"]:
                        points = 20
                    
                    score += points * score_multiplier
                    create_explosion_particles(50, 50, GOLD, 5)
            
            # 파워업 업데이트
            for powerup in powerups[:]:
                powerup.update()
                
                # 파워업 충돌 검사
                if powerup.rect.colliderect(player):
                    if powerup.type == "shield":
                        shield_active = True
                        shield_timer = 5.0
                    elif powerup.type == "slow":
                        slow_motion_active = True
                        slow_motion_timer = 3.0
                    elif powerup.type == "score":
                        score_multiplier = 2
                        multiplier_timer = 8.0
                    
                    powerups.remove(powerup)
                    score += 50 * score_multiplier
                    create_explosion_particles(powerup.x, powerup.y, GOLD, 10)
                
                # 화면 밖으로 나간 파워업 제거
                if powerup.y > SCREEN_HEIGHT + 30:
                    powerups.remove(powerup)
            
            # 파티클 업데이트
            for particle in particles[:]:
                particle.update()
                if particle.life <= 0:
                    particles.remove(particle)
            
            # 그리기
            draw_player()
            
            for snowball in snowballs:
                snowball.draw(screen)
            
            for powerup in powerups:
                powerup.draw(screen)
            
            for particle in particles:
                particle.draw(screen)
            
            # UI 그리기
            score_text = font_medium.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            
            time_text = font_small.render(f"Time: {survival_time:.1f}s", True, WHITE)
            screen.blit(time_text, (10, 50))
            
            level_text = font_small.render(f"Level: {difficulty_level}", True, WHITE)
            screen.blit(level_text, (10, 75))
            
            # 파워업 상태 표시
            y_offset = 10
            if shield_active:
                shield_text = font_small.render(f"🛡️ Shield: {shield_timer:.1f}s", True, SILVER)
                screen.blit(shield_text, (SCREEN_WIDTH - 200, y_offset))
                y_offset += 25
            
            if slow_motion_active:
                slow_text = font_small.render(f"⏰ Slow Motion: {slow_motion_timer:.1f}s", True, GOLD)
                screen.blit(slow_text, (SCREEN_WIDTH - 200, y_offset))
                y_offset += 25
            
            if score_multiplier > 1:
                mult_text = font_small.render(f"✨ Score x{score_multiplier}: {multiplier_timer:.1f}s", True, GREEN)
                screen.blit(mult_text, (SCREEN_WIDTH - 200, y_offset))
            
            # 슬로우 모션 효과
            if slow_motion_active:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(30)
                overlay.fill(YELLOW)
                screen.blit(overlay, (0, 0))
            
            pygame.display.flip()
        
        elif game_over:
            draw_background()
            
            # 반투명 오버레이
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # 게임 오버 텍스트
            game_over_text = font_large.render("* GAME OVER *", True, ICE_BLUE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
            screen.blit(game_over_text, text_rect)
            
            # 최종 점수
            final_score_text = font_medium.render(f"Final Score: {score}", True, GOLD)
            score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 70))
            screen.blit(final_score_text, score_rect)
            
            # 생존 시간
            survival_text = font_medium.render(f"Survival Time: {survival_time:.1f}s", True, WHITE)
            survival_rect = survival_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            screen.blit(survival_text, survival_rect)
            
            # 최고 점수
            if score == high_score and score > 0:
                new_record_text = font_medium.render("* NEW HIGH SCORE! *", True, GOLD)
                record_rect = new_record_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))
                screen.blit(new_record_text, record_rect)
            else:
                high_score_text = font_small.render(f"High Score: {high_score}", True, WHITE)
                high_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))
                screen.blit(high_score_text, high_rect)
            
            # 달성 레벨
            level_achieved_text = font_small.render(f"Level Reached: {difficulty_level}", True, WHITE)
            level_rect = level_achieved_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            screen.blit(level_achieved_text, level_rect)
            
            # 재시작 안내
            restart_text = font_medium.render("Press R to Restart | ESC to Quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            screen.blit(restart_text, restart_rect)
            
            # 조작법 안내
            controls_text = font_small.render("Controls: Arrow Keys to Move", True, WHITE)
            controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            screen.blit(controls_text, controls_rect)
            
            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # 게임 재시작
                        running = True
                        game_over = False
                        player.x = SCREEN_WIDTH // 2
                        player.y = SCREEN_HEIGHT - 100
                        snowballs.clear()
                        powerups.clear()
                        particles.clear()
                        score = 0
                        survival_time = 0
                        difficulty_level = 1
                        snowball_spawn_timer = 0
                        powerup_spawn_timer = 0
                        shield_active = False
                        shield_timer = 0
                        slow_motion_active = False
                        slow_motion_timer = 0
                        score_multiplier = 1
                        multiplier_timer = 0
                        start_time = datetime.now()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
            
            pygame.display.flip()
