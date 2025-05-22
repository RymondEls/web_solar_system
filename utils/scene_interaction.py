import pygame
from operations.atmosphere_study import study_atmosphere
from operations.surface_study import study_surface
from operations.data_collection import collect_data
from entities.spacecraft import Spacecraft

class SceneInteraction:
    def __init__(self, scale, offset, tracked_body, dragging, last_mouse_pos, pause, time_scale):
        self.scale = scale
        self.offset = offset
        self.tracked_body = tracked_body
        self.dragging = dragging
        self.last_mouse_pos = last_mouse_pos
        self.pause = pause
        self.time_scale = time_scale

    def handle_mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.dragging = True
                self.tracked_body = None
                self.last_mouse_pos = pygame.mouse.get_pos()
            elif event.button == 4: 
                self.scale *= 1.5
            elif event.button == 5:
                self.scale /= 1.5

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: 
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging and self.last_mouse_pos:
                current_mouse_pos = pygame.mouse.get_pos()
                dx = current_mouse_pos[0] - self.last_mouse_pos[0]
                dy = current_mouse_pos[1] - self.last_mouse_pos[1]
                self.offset[0] += dx
                self.offset[1] += dy
                self.last_mouse_pos = current_mouse_pos

    def handle_keyboard_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: 
                self.pause = not self.pause
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS: 
                self.time_scale *= 2
                print(f"Масштаб времени: {self.time_scale}x")
            elif event.key == pygame.K_MINUS: 
                self.time_scale /= 2
                print(f"Масштаб времени: {self.time_scale}x")

    def menu(self, bodies, screen):
        print('''Выберите операцию:
        1. Изучение атмосферы планеты
        2. Изучение поверхности планеты
        3. Сбор данных
        4. Запуск космического аппарата
        5. Слежение за телом''')
        action = input()

        if action == "1":
            self.study_atmosphere(bodies)
        elif action == "2":
            self.study_surface(bodies)
        elif action == "3":
            self.collect_data(bodies)
        elif action == "4":
            self.launch_spacecraft(bodies)
        elif action == "5":
            self.track_body(bodies, screen)
        else:
            print("Ошибка: введите число от 1 до 5.")

    def study_atmosphere(self, bodies):
        print("Выберите планету для изучения атмосферы:")
        planets = [body for body in bodies if body.type == "planet"]
        for i, planet in enumerate(planets):
            print(f"{i + 1}. {planet.name}")

        try:
            study_planet = int(input()) - 1
            if 0 <= study_planet < len(planets):
                study_atmosphere(planets[study_planet])
            else:
                print("Вы ввели число не из списка")
        except ValueError:
            print("Ошибка: введите число.")

    def study_surface(self, bodies):
        print("Выберите планету для изучения поверхности:")
        planets = [body for body in bodies if body.type == "planet"]
        for i, planet in enumerate(planets):
            print(f"{i + 1}. {planet.name}")

        try:
            study_planet = int(input()) - 1
            if 0 <= study_planet < len(planets):
                study_surface(planets[study_planet])
            else:
                print("Вы ввели число не из списка")
        except ValueError:
            print("Ошибка: введите число.")

    def collect_data(self, bodies):
        print("Выберите тело для сбора данных:")
        for i, body in enumerate(bodies):
            print(f"{i + 1}. {body.name}")

        try:
            data_body = int(input()) - 1
            if 0 <= data_body < len(bodies):
                collect_data(bodies[data_body])
            else:
                print("Вы ввели число не из списка")
        except ValueError:
            print("Ошибка: введите число.")

    def launch_spacecraft(self, bodies):
        print("Запуск космического аппарата. Введите начальные параметры:")
        name = input("Введите название аппарата: ")
        type = "spacecraft"
        mass = float(input("Введите массу объекта (в кг): "))
        
        names = [body.name for body in bodies]
        try:
            earth_index = names.index("Earth")
        except ValueError:
            print("Земля не найдена, в качестве тела отправления используется Солнце.")
            earth_index = 0

        position = [
            bodies[earth_index].position[0],
            bodies[earth_index].position[1] + bodies[earth_index].radius + 10000
        ]
        velocity = [
            float(input("Введите скорость по x (в м/с): ")),
            float(input("Введите скорость по y (в м/с): "))
        ]
        color = (255, 255, 255)
        radius = float(input("Введите радиус (в метрах): "))
        mission = input("Опишите миссию космического аппарата: ")

        spacecraft = Spacecraft(name, type, mass, position, velocity, color, radius, mission)
        bodies.append(spacecraft)
        print(f"Космический аппарат {name} запущен с миссией: {mission}")

    def track_body(self, bodies, screen):
        print("Выберите тело слежения:")
        for i, body in enumerate(bodies):
            print(f"{i + 1}. {body.name}")

        try:
            input_body = int(input()) - 1
            if 0 <= input_body < len(bodies):
                self.tracked_body = bodies[input_body]
                self.offset[0] = screen.get_width() // 2 - self.tracked_body.position[0] * self.scale
                self.offset[1] = screen.get_height() // 2 - self.tracked_body.position[1] * self.scale
            else:
                print("Вы ввели число не из списка")
        except ValueError:
            print("Ошибка: введите число.")