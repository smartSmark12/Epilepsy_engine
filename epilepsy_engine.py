import pygame
import random
import csv
from datetime import datetime
import os

pygame.init()

sirka = 1920
vyska = 1080

generate = False

if not os.path.exists("./screenshots"):
    os.mkdir("./screenshots")

if not os.path.exists("./saved"):
    os.mkdir("./saved")

limit_fps = 0
running = True
dt = 0
left_mouse = False
delta = 0
size = 50
vstup = pygame.K_e
color_mode = 1
connect_mode = 1
wait = 1
sleep_time = 0.001
wait_gen_slow = 0
generate_slow_toggle = False
avg_fps = 0
avg_frametime = 0
avg_fps_list = []
avg_frametime_list = []
frame_trigger = 0
render_actual = False
line_thickness = 8
line_color = (0, 0, 0)
show_delta_graph = True
slow_spawn_offset = 0.1
changed = True
make_screenshot = False
save_loc = 0

delta_graph_rect = pygame.Rect(100, 300, 200, 100)
delta_graph_list_current = []
delta_graph_list_new = []

back_color = [0, 0, 0]

mouse_hist = []

class mouse_data:
    def __init__(self, position):
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], size, size)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

okno = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Mouse shis")

def gen_rand():
    for i in range(0, 500):
        mouse = mouse_data((random.randint(0, sirka), random.randint(0, vyska)))
        mouse_hist.append(mouse)

def generate_slow():
    mouse = mouse_data((random.randint(0, sirka), random.randint(0, vyska)))
    mouse_hist.append(mouse)

def save_file():
    if save_loc == 0:
        save_loc_open = "./saved/save1.csv"
    elif save_loc == 1:
        save_loc_open = "./saved/save2.csv"
    elif save_loc == 2:
        save_loc_open = "./saved/save3.csv"
    elif save_loc == 3:
        save_loc_open = "./saved/save4.csv"
    elif save_loc == 4:
        save_loc_open = "./saved/save5.csv"
    try:
        with open(save_loc_open, "w", newline="") as savefile:
            filewriter = csv.writer(savefile, delimiter=" ", quotechar=" ", quoting=csv.QUOTE_MINIMAL)
            for i in range(len(mouse_hist)):
                filewriter.writerow([mouse_hist[i].position[0], mouse_hist[i].position[1]])#, mouse_hist[i].color])
            print(f"saved {len(mouse_hist)} points to loc {save_loc_open}")
    except:
        print(f"couldn't save file {save_loc_open}")

def open_file():
    if save_loc == 0:
        save_loc_open = "./saved/save1.csv"
    elif save_loc == 1:
        save_loc_open = "./saved/save2.csv"
    elif save_loc == 2:
        save_loc_open = "./saved/save3.csv"
    elif save_loc == 3:
        save_loc_open = "./saved/save4.csv"
    elif save_loc == 4:
        save_loc_open = "./saved/save5.csv"
    try:
        with open(save_loc_open, "r", newline="") as savefile:
            filereader = csv.reader(savefile, delimiter=" ", quotechar=" ")
            mouse_hist.clear()
            for row in filereader:
                position = (int(row[0]), int(row[1]))
                mouse = mouse_data(position)
                mouse_hist.append(mouse)
            print(f"loaded {len(mouse_hist)} points from loc {save_loc_open}")
    except:
        print(f"couldn't load file {save_loc_open}")

mouse_pos = (0, 0)
font = pygame.font.SysFont("Arial", 80) 
clock = pygame.time.Clock()

last_connect_mode = connect_mode

def render(dt):
    global mouse_pos, sirka, vyska, size, back_color, color_mode, delta_graph_rect, avg_fps, avg_frametime, render_actual, line_thickness, line_color, show_delta_graph, changed, make_screenshot

    if changed:
        if connect_mode != 0:
            pygame.mouse.set_cursor(pygame.cursors.broken_x)
        if connect_mode == 0:
            pygame.mouse.set_cursor(pygame.cursors.diamond)
        changed = False

    if color_mode == 0:
        okno.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))#(back_color)

    if color_mode == 1 or color_mode == 2 or color_mode == 3:
        okno.fill((back_color))

    if not make_screenshot:

        if connect_mode != 0:
            pygame.draw.circle(okno, (255, 0, 0), mouse_pos, size)

    if connect_mode != 0:
        if color_mode == 0:
            for i in range(0, len(mouse_hist)):
                pygame.draw.circle(okno, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), mouse_hist[i].position, size) # mouse_hist[i].color
            
        elif color_mode == 1:
            for i in range(0, len(mouse_hist)):
                pygame.draw.circle(okno, mouse_hist[i].color, mouse_hist[i].position, size)
        
        elif color_mode == 2:
            for i in range(0, len(mouse_hist)):
                pygame.draw.circle(okno, "red", mouse_hist[i].position, size)
        
        elif color_mode == 3:
            for i in range(0, len(mouse_hist)):
                pygame.draw.circle(okno, ((mouse_hist[i].color[0]), 0, 0), mouse_hist[i].position, size)

    if connect_mode == 0 or connect_mode == 1:
        for i in range(0, len(mouse_hist)):
            try:
                if color_mode == 0:
                    pygame.draw.line(okno, line_color, mouse_hist[i-1].position, mouse_hist[i].position, line_thickness)
                else:
                    pygame.draw.line(okno, "red", mouse_hist[i-1].position, mouse_hist[i].position, line_thickness)
            except:
                if color_mode == 0:
                    pygame.draw.line(okno, line_color, mouse_pos, mouse_hist[i].position, line_thickness)
                else:
                    pygame.draw.line(okno, "red", mouse_pos, mouse_hist[i].position, line_thickness)

    if connect_mode == 2:
        for i in range(0, len(mouse_hist)):
            try:
                pygame.draw.line(okno, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), mouse_hist[i-1].position, mouse_hist[i].position, line_thickness)
            except:
                pygame.draw.line(okno, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), mouse_pos, mouse_hist[i].position, line_thickness)

    if not make_screenshot:
    
        if render_actual:

            fps_text = font.render(f"{round(clock.get_fps())}fps", False, (120, 120, 120))
            fps_rect = fps_text.get_rect()
            fps_rect.center = (100, 100)
            okno.blit(fps_text, fps_rect)

            dt_text = font.render(f"{round(dt*1000)}ms", False, (255, 255, 255))
            dt_rect = dt_text.get_rect()
            dt_rect.center = (100, 200)
            okno.blit(dt_text, dt_rect)

        if not render_actual:

            fps_text = font.render(f"{avg_fps}fps", False, (120, 120, 120))
            fps_rect = fps_text.get_rect()
            fps_rect.center = (100, 100)
            okno.blit(fps_text, fps_rect)

            dt_text = font.render(f"{avg_frametime}ms", False, (255, 255, 255))
            dt_rect = dt_text.get_rect()
            dt_rect.center = (100, 200)
            okno.blit(dt_text, dt_rect)

            if show_delta_graph:

                for i in range(len(delta_graph_list_current)-1):
                    try:
                        pygame.draw.line(okno, "green", (sirka-10-i*10, delta_graph_list_current[i]), (sirka-10-(i+1)*10, delta_graph_list_current[i+1]), line_thickness)
                    except:
                        pass

        if color_mode == 0:
            count_text = font.render(f"{len(mouse_hist)}", False, "red") #(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        else:
            count_text = font.render(f"{len(mouse_hist)}", False, "white")
        count_rect = count_text.get_rect()
        count_rect.center = (sirka-100, 100)
        okno.blit(count_text, count_rect)

    pygame.display.update()
    if make_screenshot:
        timestamp = datetime.now()
        timestamp_f = timestamp.strftime("%d_%m_%Y-%H_%M_%S")
        pygame.image.save(okno, f"./screenshots/screenshot-{timestamp_f}.png")
        make_screenshot = False

def main():

    global mouse_pos
    global left_mouse
    global running
    global delta, vstup, mouse_hist, back_color, color_mode, wait, generate, wait_gen_slow, generate_slow_toggle, delta_graph_rect, delta_graph_list_current, make_screenshot, delta_graph_list_new, avg_fps, avg_frametime_list, avg_frametime, avg_frametime_list, frame_trigger, line_color, connect_mode, show_delta_graph, slow_spawn_offset, changed, last_connect_mode, save_loc

    while running:
        dt = clock.tick(limit_fps)/1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                left_mouse = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                left_mouse = True
        if pygame.mouse.get_pressed()[0]:
            left_mouse = True

        vstup = pygame.key.get_pressed()
        
        if vstup[pygame.K_SPACE]:
            mouse_hist.clear()
        
        mouse_pos = pygame.mouse.get_pos()

        if left_mouse:

            mouse = mouse_data(mouse_pos)

            mouse_hist.append(mouse)

        if vstup[pygame.K_LSHIFT] and wait > 0.2:
            color_mode += 1
            if color_mode > 3:
                color_mode = 0
            wait = 0

        if vstup[pygame.K_LCTRL] and wait > 0.2:
            connect_mode += 1
            if connect_mode > 3:
                connect_mode = 0
            wait = 0

        if vstup[pygame.K_UP] and wait > 0.2:
            if slow_spawn_offset - 0.05 >= 0:
                slow_spawn_offset -= 0.05
            if slow_spawn_offset < 0:
                slow_spawn_offset = 0.1
            wait = 0

        if vstup[pygame.K_DOWN] and wait > 0.2:
            slow_spawn_offset += 0.05
            wait = 0

        wait += 1*dt

        if vstup[pygame.K_g] and wait > 0.5:
            generate = True
            wait = 0

        if vstup[pygame.K_f] and wait > 0.2:
            if generate_slow_toggle:
                generate_slow_toggle = False
            elif not generate_slow_toggle:
                generate_slow_toggle = True
            wait = 0

        if vstup[pygame.K_s] and wait > 0.5:
            make_screenshot = True
            wait = 0

        # ukládání
        if vstup[pygame.K_1] and wait > 0.5:
            save_loc = 0
            save_file()
            wait = 0

        if vstup[pygame.K_2] and wait > 0.5:
            save_loc = 1
            save_file()
            wait = 0

        if vstup[pygame.K_3] and wait > 0.5:
            save_loc = 2
            save_file()
            wait = 0

        if vstup[pygame.K_4] and wait > 0.5:
            save_loc = 3
            save_file()
            wait = 0

        if vstup[pygame.K_5] and wait > 0.5:
            save_loc = 4
            save_file()
            wait = 0

        # načítání
        if vstup[pygame.K_6] and wait > 0.5:
            save_loc = 0
            open_file()
            wait = 0

        if vstup[pygame.K_7] and wait > 0.5:
            save_loc = 1
            open_file()
            wait = 0

        if vstup[pygame.K_8] and wait > 0.5:
            save_loc = 2
            open_file()
            wait = 0

        if vstup[pygame.K_9] and wait > 0.5:
            save_loc = 3
            open_file()
            wait = 0
        
        if vstup[pygame.K_0] and wait > 0.5:
            save_loc = 4
            open_file()
            wait = 0

        if generate:
            gen_rand()
            generate = False

        if generate_slow_toggle and wait_gen_slow > slow_spawn_offset:
            generate_slow()
            wait_gen_slow = 0
        wait_gen_slow += 1*dt

        avg_fps_list.append(round(clock.get_fps()))
        avg_frametime_list.append(dt)
        if frame_trigger > 1:
            avg_fps = round(sum(avg_fps_list) / len(avg_fps_list))
            avg_frametime = round(sum(avg_frametime_list) / len(avg_frametime_list)*1000)
            avg_fps_list.clear()
            avg_frametime_list.clear()

            # změna v grafu
            if show_delta_graph:
                delta_graph_list_current.append(avg_frametime)
                if len(delta_graph_list_current) > 20:
                    delta_graph_list_current.remove(delta_graph_list_current[0])
                for i in range(len(delta_graph_list_new)):
                    try:
                        delta_graph_list_new[i] = delta_graph_list_current[i+1]
                    except:
                        pass
                delta_graph_list_current = delta_graph_list_new

            frame_trigger = 0

        if color_mode == 0:
            line_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        if last_connect_mode != connect_mode:
            changed = True

        last_connect_mode = connect_mode

        frame_trigger += 1*dt

        render(dt)

        left_mouse = False

if __name__ == "__main__":
	main()