import pygame, random, time, math, sys

pygame.mixer.pre_init(44100,-16,1,512)
pygame.init()

#  _______  __        ______   .______        ___       __         ____    ____  ___      .______          _______.
# /  _____||  |      /  __  \  |   _  \      /   \     |  |        \   \  /   / /   \     |   _  \        /       |
#|  |  __  |  |     |  |  |  | |  |_)  |    /  ^  \    |  |         \   \/   / /  ^  \    |  |_)  |      |   (----`
#|  | |_ | |  |     |  |  |  | |   _  <    /  /_\  \   |  |          \      / /  /_\  \   |      /        \   \    
#|  |__| | |  `----.|  `--'  | |  |_)  |  /  _____  \  |  `----.      \    / /  _____  \  |  |\  \----.----)   |   
# \______| |_______| \______/  |______/  /__/     \__\ |_______|       \__/ /__/     \__\ | _| `._____|_______/    

crash1 = pygame.mixer.Sound('crash1.wav')
crash2 = pygame.mixer.Sound('crash2.wav')
crash3 = pygame.mixer.Sound('crash3.wav')
crash4 = pygame.mixer.Sound('crash4.wav')
crash5 = pygame.mixer.Sound('crash5.wav')
crash6 = pygame.mixer.Sound('crash6.wav')
pew = pygame.mixer.Sound('pew.wav')
thrust_sound = pygame.mixer.Sound('thrust.wav')

WIDTH = 800
HEIGHT = 800
fps = 30
ship_rotation_speed = 2*math.pi/30
projectile_speed = 15
asteroid_speed = 3
starting_asteroid_count = 3
asteroid_count = starting_asteroid_count
star_count = 300
pause = False
rate_of_fire = 8
score = 0
starting_lives = 3
lives = starting_lives
level = 1
level_start = True
spawn_timer = 0
spawn_time = 2
blink_timer = 0
blink_time = 2
game_over = False
level_change = False
level_change_time = 1
level_change_timer = fps*level_change_time
thrust = False

# Colors
white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
light_red = (255,0,0)
green = (0,200,0)
light_green = (0,255,0)
light_yellow = (255, 255, 0)
light_orange = (255, 155, 0)

# Game objects
stars = []
bullets = []
rocks = []
ast_pos = []
junk = []


win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gasteroids")

clock = pygame.time.Clock()


#.___________. __________   ___ .___________.        ___      .__   __.  _______     .______    __    __  .___________.___________.  ______   .__   __.      _______.
#|           ||   ____\  \ /  / |           |       /   \     |  \ |  | |       \    |   _  \  |  |  |  | |           |           | /  __  \  |  \ |  |     /       |
#`---|  |----`|  |__   \  V  /  `---|  |----`      /  ^  \    |   \|  | |  .--.  |   |  |_)  | |  |  |  | `---|  |----`---|  |----`|  |  |  | |   \|  |    |   (----`
#    |  |     |   __|   >   <       |  |          /  /_\  \   |  . `  | |  |  |  |   |   _  <  |  |  |  |     |  |        |  |     |  |  |  | |  . `  |     \   \    
#    |  |     |  |____ /  .  \      |  |         /  _____  \  |  |\   | |  '--'  |   |  |_)  | |  `--'  |     |  |        |  |     |  `--'  | |  |\   | .----)   |   
#    |__|     |_______/__/ \__\     |__|        /__/     \__\ |__| \__| |_______/    |______/   \______/      |__|        |__|      \______/  |__| \__| |_______/   

class button(object):
	def __init__(self, color, x, y, width, height, text_size, text=''):
		self.color = color
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
		self.text_size = text_size

	def draw(self, win, outline=None):
		if outline:
			pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

		if self.text != '':
			font = pygame.font.SysFont('arial', self.text_size)
			text = font.render(self.text, 1, (255,255,255))
			win.blit(text, (self.x + int(round(self.width/2 - text.get_width()/2)), self.y + int(round(self.height/2 - text.get_height()/2))))

	def isOver(self, pos):
		if pos[0] > self.x and pos[0] < self.x + self.width:
			if pos[1] > self.y and pos[1] < self.y + self.height:
				return True

		return False


def show_text(win, x, y, color, text, text_size):
	# (window, center x and y, text color as (r,g,b), text to show, size of text)
	font = pygame.font.SysFont('arial', text_size)
	text_surf = font.render(text, 1, color)
	text_rect = text_surf.get_rect()
	text_rect.center = (x,y)
	win.blit(text_surf, text_rect)



#  ______   .______          __   _______   ______ .___________.    _______.
# /  __  \  |   _  \        |  | |   ____| /      ||           |   /       |
#|  |  |  | |  |_)  |       |  | |  |__   |  ,----'`---|  |----`  |   (----`
#|  |  |  | |   _  <  .--.  |  | |   __|  |  |         |  |        \   \    
#|  `--'  | |  |_)  | |  `--'  | |  |____ |  `----.    |  |    .----)   |   
# \______/  |______/   \______/  |_______| \______|    |__|    |_______/   

class star(object):
	def __init__(self, x, y, size):
		self.x = x
		self.y = y
		eps = random.randint(0,200)
		self.color = (255-eps,255-eps,255-eps)
		self.size = size

	def draw(self, win):
		pygame.draw.circle(win, self.color, (self.x, self.y), self.size)


class player(object):
	def __init__(self, x, y, color, size):
		self.x = x
		self.y = y
		self.size = size
		self.color = color
		self.thrust_color = (255,155,0)
		self.dx = 0
		self.dy = 0
		self.angle = 0
		self.ship_model = [(0, -5), (-2.5, 2.5), (2.5, 2.5)]
		#self.ship_model = [(0,-5), (1,-3), (2.5,2.5), (1,5), (-1,5), (-2.5,2.5), (-1,-3), (0,-5)]
		self.thrust_model = [(0,5), (-1, 2.5), (1, 2.5)]
		self.dead = False
   
	def draw(self, win):
		transformed = []
		for point in self.ship_model:
			transformed.append(translate_point(rotate_point(scale_point(point, (0, 0), self.size), (0,0), self.angle), (self.x, self.y)))
		pygame.draw.polygon(win, self.color, transformed)
   
	def thrust(self):
		self.dx += 0.2*math.cos(self.angle - math.pi/2)
		self.dy += 0.2*math.sin(self.angle - math.pi/2)

	def draw_thrust(self, win):
		transformed = []
		for point in self.thrust_model:
			transformed.append(translate_point(rotate_point(scale_point(point, (0, 0), self.size), (0,0), self.angle), (self.x, self.y)))
		pygame.draw.polygon(win, self.thrust_color, transformed)

   
	def move(self):
		self.x += self.dx
		self.y += self.dy


class projectile(object):
	def __init__(self, x, y, dx, dy, color, size):
		self.x = x
		self.y = y
		self.color = color
		self.size = size
		self.dx = dx
		self.dy = dy
		self.angle = 0
		self.dead = False

	def draw(self, win):
		pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.size)

	def move(self):
		self.x += self.dx
		self.y += self.dy


class asteroid(object):
	def __init__(self, x, y, color, size):
		self.x = x
		self.y = y
		self.color = color
		self.size = size
		self.angle = 0
		self.dx = random.choice([-1.5,1.5]) * asteroid_speed
		self.dy = random.choice([-1.5,1.5]) * asteroid_speed
		self.nodes = 10
		self.model = []
		for i in range(0, self.nodes):
			r = random.randint(-10,10)/50
			self.model.append(((1+r)*math.cos(i*2*math.pi/self.nodes), (1+r)*math.sin(i*2*math.pi/self.nodes)))

	def draw(self, win):
		transformed = []
		for point in self.model:
			transformed.append(translate_point(rotate_point(scale_point(point, (0, 0), self.size), (0,0), self.angle), (self.x, self.y)))
		pygame.draw.polygon(win, self.color, transformed)

	def move(self):
		self.angle += math.pi/180 * asteroid_speed
		self.x += self.dx
		self.y += self.dy


class debris(object):
	def __init__(self, x, y, speed, color, max_life):
		self.x = x
		self.y = y
		self.color = color
		self.radius = 2
		self.speed = speed + random.randint(-3,3)
		self.angle = random.randint(1,200) *  math.pi / 100
		self.life = random.randint(1,2) * fps
		self.alive = True
		self.life_count = 0
		self.max_life = max_life

	def draw(self, win):
		pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)

	def move(self):
		self.x += int(self.speed * math.cos(self.angle))
		self.y += int(self.speed * math.sin(self.angle))
		self.life_count += 1
		if self.life_count > self.max_life:
			self.alive = False


def explode(obj, thing):
	num = random.randint(1,6)
	if num == 1:
		pygame.mixer.Sound.play(crash1)
	if num == 2:
		pygame.mixer.Sound.play(crash2)
	if num == 3:
		pygame.mixer.Sound.play(crash3)
	if num == 4:
		pygame.mixer.Sound.play(crash4)
	if num == 5:
		pygame.mixer.Sound.play(crash5)
	if num == 6:
		pygame.mixer.Sound.play(crash6)
	for i in range(100):
		# debris(x, y, speed, color, max_life)
		thing.append(debris(obj.x, obj.y, 3, obj.color, 5 + 0.5*obj.size))



#     _______..______      ___       ______  __       ___       __          _______  __    __  .__   __.   ______ .___________. __    ______   .__   __.      _______.
#    /       ||   _  \    /   \     /      ||  |     /   \     |  |        |   ____||  |  |  | |  \ |  |  /      ||           ||  |  /  __  \  |  \ |  |     /       |
#   |   (----`|  |_)  |  /  ^  \   |  ,----'|  |    /  ^  \    |  |        |  |__   |  |  |  | |   \|  | |  ,----'`---|  |----`|  | |  |  |  | |   \|  |    |   (----`
#    \   \    |   ___/  /  /_\  \  |  |     |  |   /  /_\  \   |  |        |   __|  |  |  |  | |  . `  | |  |         |  |     |  | |  |  |  | |  . `  |     \   \    
#.----)   |   |  |     /  _____  \ |  `----.|  |  /  _____  \  |  `----.   |  |     |  `--'  | |  |\   | |  `----.    |  |     |  | |  `--'  | |  |\   | .----)   |   
#|_______/    | _|    /__/     \__\ \______||__| /__/     \__\ |_______|   |__|      \______/  |__| \__|  \______|    |__|     |__|  \______/  |__| \__| |_______/    
                                                                                                                                                                   

def rotate_point(point, center, angle):
	a = 0
	b = 0
	a = math.cos(angle)*(point[0] - center[0]) - math.sin(angle)*(point[1] - center[1]) + center[0]
	b = math.sin(angle)*(point[0] - center[0]) + math.cos(angle)*(point[1] - center[1]) + center[1]
	return a, b

def scale_point(point, center, amt):
	a = 0
	b = 0
	a = amt * (point[0] - center[0]) + center[0]
	b = amt * (point[1] - center[0]) + center[1]
	return a, b
 
def translate_point(point, change):
	a = 0
	b = 0
	a = point[0] + change[0]
	b = point[1] + change[1]
	return int(a), int(b)

def wrap_coordinates(thing):
	if thing.y + thing.size < 0:
		thing.y = HEIGHT + thing.size
		thing.x = WIDTH - thing.x

	if thing.y - thing.size > HEIGHT:
		thing.y = 0 - thing.size
		thing.x = WIDTH - thing.x

	if thing.x + thing.size < 0:
		thing.x = WIDTH + thing.size

	if thing.x - thing.size > WIDTH:
		thing.x = 0 - thing.size


def distance(point1, point2):
  return math.sqrt( (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)



# __  .__   __.  __  .___________.     ______   .______          __   _______   ______ .___________.    _______.
#|  | |  \ |  | |  | |           |    /  __  \  |   _  \        |  | |   ____| /      ||           |   /       |
#|  | |   \|  | |  | `---|  |----`   |  |  |  | |  |_)  |       |  | |  |__   |  ,----'`---|  |----`  |   (----`
#|  | |  . `  | |  |     |  |        |  |  |  | |   _  <  .--.  |  | |   __|  |  |         |  |        \   \    
#|  | |  |\   | |  |     |  |        |  `--'  | |  |_)  | |  `--'  | |  |____ |  `----.    |  |    .----)   |   
#|__| |__| \__| |__|     |__|         \______/  |______/   \______/  |_______| \______|    |__|    |_______/    

for i in range(star_count):
	stars.append(star(random.randrange(0,WIDTH),random.randrange(1,HEIGHT), random.randrange(1,3)))

ship = player(WIDTH//2, HEIGHT//2, light_green, 5)




# __  .__   __. .___________..______        ______       __        ______     ______   .______   
#|  | |  \ |  | |           ||   _  \      /  __  \     |  |      /  __  \   /  __  \  |   _  \  
#|  | |   \|  | `---|  |----`|  |_)  |    |  |  |  |    |  |     |  |  |  | |  |  |  | |  |_)  | 
#|  | |  . `  |     |  |     |      /     |  |  |  |    |  |     |  |  |  | |  |  |  | |   ___/  
#|  | |  |\   |     |  |     |  |\  \----.|  `--'  |    |  `----.|  `--'  | |  `--'  | |  |      
#|__| |__| \__|     |__|     | _| `._____| \______/     |_______| \______/   \______/  | _|      
                                                                                                
def intro_loop():
	global stars
	global black, white, green, light_green, red, light_red, light_yellow

	intro_running = True

	clicked = False
 
	start_button = button(green, WIDTH//4 + 50, 5*HEIGHT//8 - 50, 100, 40, 20, 'Start')
	quit_button = button(red, 2*WIDTH//4 + 50, 5*HEIGHT//8 - 50, 100, 40, 20, 'Quit')

	while intro_running:
		clock.tick(fps)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				intro_running = False
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					intro_running = False
					game_loop()

		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		# Button Handling
		if start_button.isOver(mouse):
			start_button.color = light_green
			if click[0] == True and clicked == False:
				clicked = True
				start_button.color = (255,255,0)
				intro_running = False
				game_loop()
				break
			if click[0] == False:
				clicked = False
		else:
			start_button.color = green

		if quit_button.isOver(mouse):
			quit_button.color = light_red
			if click[0] == True and clicked == False:
				clicked = True
				quit_button.color = (255,255,0)
				intro_running = False
				pygame.quit()
				break
			if click[0] == False:
				clicked = False
		else:
			quit_button.color = red
 
       # Draw the screen
		win.fill(black)
		for star in stars:
			star.draw(win)

		show_text(win, WIDTH//2, HEIGHT//2 - 50, white, 'Gasteroids', 80)
		start_button.draw(win,white)
		quit_button.draw(win,white)

		# Add some directions on screen.

		pygame.display.update()



#  _______      ___      .___  ___.  _______     __        ______     ______   .______   
# /  _____|    /   \     |   \/   | |   ____|   |  |      /  __  \   /  __  \  |   _  \  
#|  |  __     /  ^  \    |  \  /  | |  |__      |  |     |  |  |  | |  |  |  | |  |_)  | 
#|  | |_ |   /  /_\  \   |  |\/|  | |   __|     |  |     |  |  |  | |  |  |  | |   ___/  
#|  |__| |  /  _____  \  |  |  |  | |  |____    |  `----.|  `--'  | |  `--'  | |  |      
# \______| /__/     \__\ |__|  |__| |_______|   |_______| \______/   \______/  | _|     

def game_loop():
	global stars, rocks, ship, bullets, ast_pos, junk
	global asteroid_count, rate_of_fire, ship_rotation_speed, score, lives, level, level_start, spawn_timer, blink_timer, game_over, level_change_timer, level_change_time, level_change, thrust
	global red, green, black, white, light_red, light_green, light_yellow

	shoot_loop = 0
	upWasPressed = False

	# Create asteroids, asteroid(x, y, color, size):
	if level_start == True:
		level_start = False
		for i in range(asteroid_count):
			ast_pos.append(( int(WIDTH/1.8*math.cos(i*2*math.pi/asteroid_count+.5)+WIDTH/2), int(HEIGHT/2.5*math.sin(i*2*math.pi/asteroid_count+.5)+HEIGHT/2)))

		for i in range(asteroid_count):
			rocks.append(asteroid(ast_pos[i][0], ast_pos[i][1],(90 + random.randint(0,30),77 + random.randint(0,30),55),50 + random.randint(0,30)))

	game_running = True

	while game_running:
		clock.tick(fps)

		if shoot_loop > 0:
			shoot_loop += 1
		if shoot_loop > rate_of_fire:
			shoot_loop = 0

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_running = False
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					game_running = False
					pause_loop()

		keys = pygame.key.get_pressed()
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		if keys[pygame.K_LEFT]:
			ship.angle -= ship_rotation_speed

		if keys[pygame.K_RIGHT]:
			ship.angle += ship_rotation_speed

		if keys[pygame.K_UP]:
			if not upWasPressed and spawn_timer == 0:
				pygame.mixer.Sound.play(thrust_sound, loops=100)
				upWasPressed = True
			ship.thrust()
			thrust = True
		else:
			thrust = False
			upWasPressed = False
			pygame.mixer.Sound.stop(thrust_sound)

		if keys[pygame.K_SPACE] and shoot_loop == 0:
			if spawn_timer == 0:
				pygame.mixer.Sound.play(pew)
				bullets.append(projectile(ship.x, ship.y, projectile_speed*math.sin(ship.angle), -projectile_speed*math.cos(ship.angle), light_yellow, 3))
				shoot_loop = 1

		# Collision and 'off screen' handling
		# spawn_timer controls a wait time between death and respawn
		# blink_timer controls a time of blinking and invicibility after respawn
		if ship.dead == False:
			wrap_coordinates(ship)
		else:     # At this point, ship.dead = True
			if lives >= 0 and spawn_timer > 0:
				spawn_timer -= 1
				if spawn_timer == 0:
					if lives == 0:
						game_running = False
						game_over = True
						pause_loop()
					ship.x = WIDTH//2
					ship.y = HEIGHT//2
					ship.dx = 0
					ship.dy = 0
					ship.angle = 0
					blink_timer = fps*blink_time
			if lives > 0 and blink_timer > 0:
				blink_timer -= 1
				if math.ceil(blink_timer/6) % 2 == 0:
					ship.color = light_green
					ship.thrust_color = light_orange
				else:
					ship.color = black
					ship.thrust_color = black
				if blink_timer == 0:
					ship.dead = False
					ship.color = light_green
					ship.thrust_color = light_orange

		for rock in rocks:
			wrap_coordinates(rock) 

		for bullet in bullets:
			for rock in rocks:
				if distance((rock.x, rock.y), (bullet.x, bullet.y)) < rock.size:
					bullet.y = -150
					explode(rock, junk)
					score += 1
					if rock.size > 20:
						rocks.append(asteroid(rock.x, rock.y, rock.color, rock.size//2))
						rocks.append(asteroid(rock.x, rock.y, rock.color, rock.size//2))
					rocks.pop(rocks.index(rock))
					if len(rocks) == 0:
						# Next level... add some kind of message and delay
						# maybe another function for a transition displaying score, lives, and level.
						level_change = True
						level += 1
						#ast_pos.clear()
						#asteroid_count += 1
						#level_start = True
						#game_running = False
						#game_loop()

			if bullet.x > WIDTH + 100 or bullet.x < 0 - 100 or bullet.y < 0 - 100 or bullet.y > HEIGHT + 100:
				bullets.pop(bullets.index(bullet))

		for rock in rocks:
			if distance((ship.x, ship.y), (rock.x, rock.y)) < rock.size + ship.size:
				if blink_timer == 0:
					explode(ship, junk)
					ship.dead = True
					ship.y = -150
					ship.dy = 0
					spawn_timer = fps*spawn_time
					if lives > 0:
						lives -= 1

		for j in junk:
			if j.alive == False:
				junk.pop(junk.index(j))

		# Draw the screen and Update positions of moving objects
		win.fill(black)
		for star in stars:
			star.draw(win)
		for bullet in bullets:
			bullet.move()
			bullet.draw(win)
		ship.move()
		ship.draw(win)
		if thrust == True:
			ship.draw_thrust(win)
		for rock in rocks:
			rock.move()
			rock.draw(win)
		if len(junk) > 0:
			for j in junk:
				j.move()
				j.draw(win)

		# Lives
		if lives > 0:
			for i in range(lives):
				pygame.draw.circle(win, light_green, (700 + i*30, 45), 10)

		# Show text on screen
		show_text(win, 60, 20, light_yellow, 'Score:', 30)
		show_text(win, 60, 50, light_yellow, str(score), 30)
		show_text(win, 740, 20, light_yellow, 'Lives: ', 30)
		show_text(win, WIDTH//2, 20, light_yellow, 'Level ' + str(level), 30)
		show_text(win, WIDTH//2, HEIGHT-20, light_yellow, str(len(rocks)) + ' asteroids left', 30)

		if ship.dead == True:
			show_text(win,WIDTH//2, HEIGHT//2+80, white, 'You died!', 80)

		# Handles a short transition after the last asteroid is killed and before the next set are spawned.
		if level_change == True:
			if level_change_timer > 0:
				show_text(win,WIDTH//2, HEIGHT//2, white, 'Level: ' + str(level), 100)
				level_change_timer -= 1
			else:
				level_change_timer = fps*level_change_time
				asteroid_count += 1
				ast_pos.clear()
				level_start = True
				level_change = False
				game_loop()		


		pygame.display.update()




#.______      ___      __    __       _______. _______     __        ______     ______   .______   
#|   _  \    /   \    |  |  |  |     /       ||   ____|   |  |      /  __  \   /  __  \  |   _  \  
#|  |_)  |  /  ^  \   |  |  |  |    |   (----`|  |__      |  |     |  |  |  | |  |  |  | |  |_)  | 
#|   ___/  /  /_\  \  |  |  |  |     \   \    |   __|     |  |     |  |  |  | |  |  |  | |   ___/  
#|  |     /  _____  \ |  `--'  | .----)   |   |  |____    |  `----.|  `--'  | |  `--'  | |  |      
#| _|    /__/     \__\ \______/  |_______/    |_______|   |_______| \______/   \______/  | _|      

def pause_loop():
	global stars, rocks, ship, bullets, ast_pos, junk
	global asteroid_count, rate_of_fire, ship_rotation_speed, score, lives, level, level_start, WIDTH, HEIGHT, game_over, thrust
	global red, green, black, white, light_red, light_green, light_yellow

	paused = True

	#pygame.init()

	clicked = False
 
	resume_button = button(green, WIDTH//4 + 50, 5*HEIGHT//8 - 50, 100, 40, 20, 'Resume')
	quit_button = button(red, 2*WIDTH//4 + 50, 5*HEIGHT//8 - 50, 100, 40, 20, 'Quit')
	restart_button = button(green, 2*WIDTH//4 - 50, 3*HEIGHT//8 - 100, 100, 40, 20, 'Restart')

	# Create translucent surface to draw over game screen for dimmed effect
	surface = pygame.Surface((WIDTH, HEIGHT))
	surface.set_alpha(128)
	surface.fill(black)

	while paused:
		clock.tick(fps)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				paused = False
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					pause = False
					game_loop()

		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()


		# Button Handling
		if not game_over:
			if resume_button.isOver(mouse):
				resume_button.color = light_green
				if click[0] == True and clicked == False:
					clicked = True
					resume_button.color = (255,255,0)
					pause = False
					game_loop()
					break
				if click[0] == False:
					clicked = False
			else:
				resume_button.color = green

		if quit_button.isOver(mouse):
			quit_button.color = light_red
			if click[0] == True and clicked == False:
				clicked = True
				quit_button.color = (255,255,0)
				paused = False
				pygame.quit()
				sys.exit()
				break
			if click[0] == False:
				clicked = False
		else:
			quit_button.color = red

		if restart_button.isOver(mouse):
			restart_button.color = light_green
			if click[0] == True and clicked == False:
				clicked = True
				restart_button.color = (255,255,0)
				paused = False
				rocks.clear()
				bullets.clear()
				junk.clear()
				lives = starting_lives
				asteroid_count = starting_asteroid_count
				score = 0
				ship.x = WIDTH//2
				ship.y = HEIGHT//2
				ship.dx = 0
				ship.dy = 0
				ship.angle = 0
				level_start = True
				ship.dead = False
				spawn_timer = 0
				blink_timer = 0
				game_over = False
				level = 1
				intro_loop()
				break
			if click[0] == False:
				clicked = False
		else:
			restart_button.color = green
      
       # Draw the screen
		win.fill(black)
		for star in stars:
			star.draw(win)
		for bullet in bullets:
			bullet.draw(win)
		ship.draw(win)
		if thrust == True:
			ship.draw_thrust(win)
		for rock in rocks:
			rock.draw(win)
		if len(junk) > 0:
			for j in junk:
				j.draw(win)

		# Lives
		if lives > 0:
			for i in range(lives):
				pygame.draw.circle(win, light_green, (700 + i*30, 45), 10)

		# Show text on screen
		show_text(win, 60, 20, light_yellow, 'Score:', 30)
		show_text(win, 60, 50, light_yellow, str(score), 30)
		show_text(win, 740, 20, light_yellow, 'Lives: ', 30)
		show_text(win, WIDTH//2, 20, light_yellow, str(len(rocks)) + ' asteroids left', 30)
		
		# Draw transulcent box over entire window to 'block' out game objects
		win.blit(surface,(0,0))

		if not game_over:
			show_text(win, WIDTH//2, HEIGHT//2 - 50, white, 'Paused', 80)
			resume_button.draw(win,white)
		else:
			show_text(win, WIDTH//2, HEIGHT//2 - 50, white, 'Game Over', 80)
			resume_button.draw(win)

		quit_button.draw(win,white)
		restart_button.draw(win,white)

		# Add some directions to screen

		pygame.display.update()



#.___  ___.      ___       __  .__   __.      ______   ______    _______   _______ 
#|   \/   |     /   \     |  | |  \ |  |     /      | /  __  \  |       \ |   ____|
#|  \  /  |    /  ^  \    |  | |   \|  |    |  ,----'|  |  |  | |  .--.  ||  |__   
#|  |\/|  |   /  /_\  \   |  | |  . `  |    |  |     |  |  |  | |  |  |  ||   __|  
#|  |  |  |  /  _____  \  |  | |  |\   |    |  `----.|  `--'  | |  '--'  ||  |____ 
#|__|  |__| /__/     \__\ |__| |__| \__|     \______| \______/  |_______/ |_______|

intro_loop()
pygame.quit()
quit()