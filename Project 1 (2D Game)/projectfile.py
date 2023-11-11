import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		PLAYER_RFRAMES_1 = pygame.image.load("Graphics/Characters/runner/runf1.png").convert_alpha()
		PLAYER_RFRAMES_2 = pygame.image.load("Graphics/Characters/runner/runf2.png").convert_alpha()
		PLAYER_RFRAMES_3 = pygame.image.load("Graphics/Characters/runner/runf3.png").convert_alpha()
		PLAYER_RFRAMES_4 = pygame.image.load("Graphics/Characters/runner/runf4.png").convert_alpha()
		self.PLAYER_RFRAMES = [PLAYER_RFRAMES_1, PLAYER_RFRAMES_2, PLAYER_RFRAMES_3, PLAYER_RFRAMES_4]
		self.PLAYER_INDEX = 0
		self.PLAYER_JUMP = pygame.image.load("Graphics/Characters/runner/jumpu.png").convert_alpha()

		self.image = self.PLAYER_RFRAMES[self.PLAYER_INDEX]
		self.rect = self.image.get_rect(midbottom = (130, 380))
		self.GRAVITY = 0

	def player_input(self):
		KEYS = pygame.key.get_pressed()
		if KEYS[pygame.K_SPACE] and self.rect.bottom >= 380:
			self.GRAVITY = -23 
			
	def apply_gravity(self):
		self.GRAVITY += 0.75
		self.rect.y += self.GRAVITY
		if self.rect.bottom >= 410: self.rect.bottom = 380

	def animation_state(self):
		if self.rect.bottom < 380: 
			self.image = self.PLAYER_JUMP
		else:
			self.PLAYER_INDEX += 0.1
			if self.PLAYER_INDEX >= len(self.PLAYER_RFRAMES):self.PLAYER_INDEX = 0
			self.image = self.PLAYER_RFRAMES[int(self.PLAYER_INDEX)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'SOLDIER':
			SOLDIER_1 = pygame.image.load("Graphics/Characters/soldier/soldierw1.png").convert_alpha()
			SOLDIER_2 = pygame.image.load("Graphics/Characters/soldier/soldierw2.png").convert_alpha()
			SOLDIER_3 = pygame.image.load("Graphics/Characters/soldier/soldierw3.png").convert_alpha()
			self.frames = [SOLDIER_1, SOLDIER_2, SOLDIER_3]
			y_pos = 380

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(1000, 1500), y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 5
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()

def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = FONT.render(f'Score: {current_time}', False, "Black")
	score_rect = score_surf.get_rect(center = (635, 50))
	screen.blit(score_surf,score_rect)
	return current_time

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
		obstacle_group.empty()
		return False
	else: return True


pygame.init()
screen = pygame.display.set_mode((750,500))
pygame.display.set_caption("GAME")
clock = pygame.time.Clock()
FONT = pygame.font.Font("Font/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

background = pygame.image.load("Graphics/background2.jpg")

player_stand = pygame.image.load("Graphics/Characters/runner/runf2.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1)
player_stand_rect = player_stand.get_rect(center = (375, 250))

game_name = FONT.render('2D Runner', False, "White")
game_name_rect = game_name.get_rect(center = (375, 125))

game_message = FONT.render('CLICK SPACE TO START', False,"White")
game_message_rect = game_message.get_rect(center = (375, 375))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(["SOLDIER"])))
		
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)


	if game_active:
		screen.blit(background, (0, 0))
		score = display_score()
		
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()
		
	else:
		screen.fill("Black")
		screen.blit(player_stand,player_stand_rect)

		score_message = FONT.render(f"Your score: {score}", False, "White")
		score_message_rect = score_message.get_rect(center = (375,375))
		screen.blit(game_name,game_name_rect)

		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)