import pygame, random

#COLOURS DEFINITION
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#CLASS Brick
class Brick(pygame.sprite.Sprite):
	def __init__(self, color, width, height):
		pygame.sprite.Sprite.__init__(self)
		
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		
		self.rect = self.image.get_rect()

#GAME INITIALIZATION
pygame.init()
screen_width = 700
screen_height = 500
margin = 5
brick_width = 30
brick_height = 15
screen = pygame.display.set_mode([screen_width,screen_height])

#DEFINING LISTS
brick_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
only_player = pygame.sprite.Group()

#CREATING BRICKS LAYOUT
layout = [	[0,0,1,1,0,1,1,0,0,0,0,0,0,1,1,0,1,1,0,0],
		[0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,0],
		[1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1],
		[0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,0],
		[0,0,1,1,1,1,1,0,2,2,2,2,0,1,1,1,1,1,0,0],
		[0,0,0,1,1,1,0,0,2,0,0,0,0,0,1,1,1,0,0,0],
		[0,0,0,0,1,0,0,0,2,2,2,2,0,0,0,1,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0]
	 ]

#CREATING BRICKS
for r in range(len(layout)):
	for c in range(len(layout[r])):
		if layout[r][c] == 1:		
			brick = Brick(RED, brick_width, brick_height)
			brick.rect.x = (c * (brick_width + margin))
			brick.rect.y = 20 + (r * (brick_height + margin))
		
			brick_list.add(brick)
			all_sprites_list.add(brick)
		if layout[r][c] == 2:		
			brick = Brick(BLUE, brick_width, brick_height)
			brick.rect.x = (c * (brick_width + margin))
			brick.rect.y = 20 + (r * (brick_height + margin))
		
			brick_list.add(brick)
			all_sprites_list.add(brick)

"""for r in range(8):
	for c in range(screen_width/(brick_width+margin)):
		brick = Brick(BLUE, brick_width, brick_height)
		brick.rect.x = (c * (brick_width + margin))
		brick.rect.y = 20 + (r * (brick_height + margin))
		
		brick_list.add(brick)
		all_sprites_list.add(brick)"""

#PLAYER
player_width = 100
player_height = 20
player = Brick(RED, player_width, player_height)
player.rect.x = (screen_width/2 - player_width/2)
player.rect.y = (screen_height - player_height)
all_sprites_list.add(player)
only_player.add(player)

#BULLET
bullet_width = 10
bullet_height = 10
bullet = Brick(GREEN, bullet_width, bullet_height)
bullet.rect.x = (screen_width/2 - bullet_width/2)
bullet.rect.y = (screen_height - player_height - bullet_height)
all_sprites_list.add(bullet)

#VARIABLES DECLARATION
done = False
clock = pygame.time.Clock()
score = 0
game_over = 0
player_speed_x = 0
bullet_speed_x = 5
bullet_speed_y = -5
font = pygame.font.SysFont("comicsansms", 42)
ins_page = 1
display_ins = True
bg_image = pygame.image.load("bg1.jpg").convert()
bg_pos = [-40, 10]

#CREATING BACKGROUND SNOW
snow_list = []
for i in range(50):
	x = random.randrange(0,700)
	y = random.randrange(0,500)
	snow_list.append([x,y])

#INSTRUCTIONS LOOP
while done == False and display_ins == True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			ins_page += 1
			if ins_page == 2:
				display_ins = False

	screen.blit(bg_image, bg_pos)
	
	if ins_page == 1:
		text = font.render("Click here to begin", True, BLACK)
		screen.blit(text, [screen_width/2 - text.get_width() // 2, 180 + (screen_height/2) - text.get_width() // 2])
		credits = font.render("By Sahil", True, GREEN)
		screen.blit(credits, (screen_width/2 - credits.get_width() // 2, screen_height - 60))

	clock.tick(20)
	pygame.display.flip()


#MAIN LOOP
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				player_speed_x = -15
			if event.key == pygame.K_RIGHT:
				player_speed_x = 15
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				player_speed_x = 0
			if event.key == pygame.K_RIGHT:
				player_speed_x = 0
		elif event.type == pygame.MOUSEBUTTONDOWN and game_over == 1:
			done = True

	pygame.mouse.set_visible(0)
	#PLAYER MOVEMENT
	player.rect.x += player_speed_x
	if player.rect.x > (screen_width - player_width):
		player.rect.x = (screen_width - player_width)
	if player.rect.x < 0:
		player.rect.x = 0
	
	#BULLET MOVEMENT
	bullet.rect.x += bullet_speed_x
	bullet.rect.y += bullet_speed_y
	if bullet.rect.x > (screen_width - bullet_width) or bullet.rect.x < 0:
		bullet_speed_x *= -1
	if bullet.rect.y < 0:
		bullet_speed_y *= -1
	if bullet.rect.y > (screen_height - bullet_height):
		game_over = 1 #GAME OVER FLAG
	
	#FILLING SCREEN
	screen.fill(BLACK)
	for i in range(len(snow_list)):
		pygame.draw.circle(screen, WHITE, snow_list[i],2)
		snow_list[i][1] += 1
		if snow_list[i][1] > 500:
			y = random.randrange(-50, -10)
			snow_list[i][1] = y
			x = random.randrange(0, 700)
			snow_list[i][0] = x
	
	#BULLET HITS PLAYER
	player_hit = pygame.sprite.spritecollide(bullet, only_player, False)
	if player_hit:
		bullet_speed_y *= -1
		if (player.rect.x + player_width/2) >= bullet.rect.x:
			if bullet_speed_x > 0:
				bullet_speed_x *= -1
		
		if (player.rect.x + player_width/2) <= bullet.rect.x:
			if bullet_speed_x < 0:
				bullet_speed_x *= -1
	
	#BULLET HITS BRICKS
	bricks_hit_list = pygame.sprite.spritecollide(bullet, brick_list, True)
	for brick in bricks_hit_list:
		score += 1
		#print(score)
	if bricks_hit_list:
		bullet_speed_y *= -1
		if bullet_speed_x > 0:
			if score%5 == 0:
				bullet_speed_x += 1
		if bullet_speed_x < 0:
			if score%5 == 0:
				bullet_speed_x -= 1
		if bullet_speed_y > 0:
			if score%5 == 0:
				bullet_speed_y += 1
		if bullet_speed_y > 0:
			if score%5 == 0:
				bullet_speed_y -= 1
		#print(bullet_speed_x)
	
	
	#DRAW ALL THE SPRITES
	all_sprites_list.draw(screen)
	
	#GAME OVER
	if game_over == 1:
		pygame.mouse.set_visible(1)
		screen.fill(BLACK)
		screen.blit(bg_image, bg_pos)
		
		pygame.draw.rect(screen, WHITE, [(screen_width/2 - 110) , (screen_height/2 - 40) , 230, 70])
		
		text_string = "Score: {0}".format(score)
		over_text = font.render(text_string, True, (0, 0, 255))
		screen.blit(over_text, (screen_width/2 - over_text.get_width() // 2, screen_height/2 - over_text.get_height() // 2))
		exit_text = font.render("Click here to EXIT!", True, (255, 0, 0))
		screen.blit(exit_text, (screen_width/2 - exit_text.get_width() // 2, 60 + screen_height/2 - exit_text.get_height() // 2))
		credits = font.render("By Sahil", True, GREEN)
		screen.blit(credits, (screen_width/2 - credits.get_width() // 2, screen_height - 60))

	clock.tick(60)
	pygame.display.flip()
pygame.quit()
