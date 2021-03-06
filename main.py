import pygame
import random
import math
from WORDS import words
pygame.init()


RADIUS = 20
RAD = 30
POSITIONS = []
LEVEL_POSITIONS =[]
images = []
guessed = []
SOUNDS = []

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


def set_display():
    WIDTH, HEIGHT = 1000, 700
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("HANGMAN...")
    return win


def set_position():
    x, y, A = 200, 500, 65
    for i in range(13):
        POSITIONS.append([x, y, chr(A), 1])
        x += 50
        A += 1

    x, y = 200, 550
    for i in range(13):
        POSITIONS.append([x, y, chr(A), 1])
        x += 50
        A += 1

    x, y, A = 350, 400, 1
    for i in range(5):
        LEVEL_POSITIONS.append([x, y, str(A)])
        x += 70
        A += 1
    
    x, y = 350, 470
    for i in range(5):
        LEVEL_POSITIONS.append([x, y, str(A)])
        x += 70
        A += 1


def load_images():
    for i in range(7):
        image = pygame.image.load("hangman" + str(i) + ".png")
        images.append(image)


def load_sounds():
    sound = pygame.mixer.Sound("Click.mp3")
    SOUNDS.append(sound)
    sound = pygame.mixer.Sound("Correct_guess.wav")
    SOUNDS.append(sound)
    sound = pygame.mixer.Sound("wrong_guess.wav")
    SOUNDS.append(sound)
    sound = pygame.mixer.Sound("game_win.wav")
    SOUNDS.append(sound)
    sound = pygame.mixer.Sound("game_lose.wav")
    SOUNDS.append(sound)


def draw(win, status, word, LEVEL):
    win.fill(WHITE)
    display_text = ""
    for letter in word:
        if letter in guessed:
            display_text += letter + " "
        else:
            display_text += "_ "
    font = pygame.font.SysFont('comicsans', 40)
    text = font.render(display_text, 1, BLACK)
    win.blit(text, (500, 350))

    for pos in POSITIONS:
        x, y, A, vis = pos
        if vis:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(A, 1, BLACK)
            win.blit(text, (x - text.get_width()/2,y - text.get_height()/2))
    
    win.blit(images[status], (200, 200))

    font = pygame.font.SysFont('comicsans', 30)
    text = "Difficulty: " + str(LEVEL)
    textt = font.render(text, 1, RED)
    win.blit(textt, (500, 20))

    pygame.display.update()


def draw_win_lose(win, display_text, word, seconds):
    pygame.time.delay(1000)

    win.fill(WHITE)
    draw_time(win, seconds, "Time Spent: ")
    font = pygame.font.SysFont('comicsans', 100)
    text = font.render(display_text, 1, BLACK)
    win.blit(text,(500 - text.get_width()/2, 350 - text.get_height()/2))

    if display_text == "YOU LOST!":
        win.blit(images[6], (0,0))
        font = pygame.font.SysFont('comicsans', 50)
        text = "The Word Was: " + word
        dis_text = font.render(text, 1, RED)
        win.blit(dis_text, (500 - dis_text.get_width()/2, 480 - dis_text.get_height()/2))

    dis_text = "Press ENTER to play again."
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render(dis_text, 1, BLACK)
    win.blit(text, (500 - text.get_width()/2, 550 - text.get_height()/2))
    pygame.display.update()


def draw_time(win, seconds, dis_tex):
    min = seconds // 60
    sec = seconds % 60
    timer = '{:02d}:{:02d}'.format(min, sec)
    dis_text = dis_tex + timer
    font = pygame.font.SysFont('comicsans', 20)
    text = font.render(dis_text, 1, BLACK)
    win.blit(text, (700, 200))
    pygame.display.update()

def restart():
    guessed.clear()
    POSITIONS.clear()
    main()


def want_to_play_again(win, text, word, seconds):
    pygame.time.delay(1000)
    if text == "YOU WON!":
        SOUNDS[3].play()
    else:
        SOUNDS[4].play()

    FPS = 60
    clock = pygame.time.Clock()
    run = True
    while run:
        draw_win_lose(win, text, word, seconds)
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  
                    restart()
    
    pygame.quit()


def choose_word(LEVEL):
    while True:
        word = random.choice(words).upper()
        if len(word) == LEVEL:
            return word 


def draw_level(win):
    win.fill(WHITE)

    font = pygame.font.SysFont('comicsans', 50)
    text = "Choose Difficulty!"
    textt = font.render(text, 1, BLACK)
    win.blit(textt, (500 - textt.get_width()/2, 200))
    win.blit(images[6], (0,250))

    for pos in LEVEL_POSITIONS:
        x, y, A = pos
        pygame.draw.circle(win, BLACK, (x, y), RAD, 3)
        font = pygame.font.SysFont('comicsans', 30)
        text = font.render(A, 1, BLACK)
        win.blit(text, (x - text.get_width()/2,y - text.get_height()/2))
    
    pygame.display.update()


def select_level(win):
    FPS = 60
    clock = pygame.time.Clock()

    while True:
        draw_level(win)
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for pos in LEVEL_POSITIONS:
                    x, y, A = pos
                    dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                    if dis < RAD:
                        return int(A)



def main():
    FPS = 60
    clock = pygame.time.Clock()
    win = set_display()
    set_position()
    LEVEL = select_level(win)
    word = choose_word(LEVEL)

    run = True
    status = 0
    frames = 0
    seconds = 0
    while run:
        if frames == 60:
            seconds += 1
            frames = 0

        frames += 1
        clock.tick(FPS)

        draw_time(win, seconds, "Time: ")
        draw(win, status, word, LEVEL)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for pos in POSITIONS:
                    x, y, A, vis = pos
                    if vis:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            SOUNDS[0].play()
                            pos[3] = 0
                            guessed.append(A)
                            if A not in word:
                                status += 1
                                SOUNDS[2].play()
                            else:
                                SOUNDS[1].play()

        won = 1    
        for letter in word:
            if letter not in guessed:
                won = 0 
                break
        
        if won:
            draw(win, status, word, LEVEL)
            text = "YOU WON!"
            want_to_play_again(win, text, word, seconds)

        if status == 6:
            draw(win, status, word, LEVEL)
            text = "YOU LOST!"
            want_to_play_again(win, text, word, seconds)
            
    pygame.quit()


if __name__ == "__main__":
    load_images()
    load_sounds()
    main()