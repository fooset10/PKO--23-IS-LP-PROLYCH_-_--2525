import tkinter as tk
from tkinter import ttk
import math
from PIL import Image, ImageTk
import os
import webbrowser

# Константы, Масштабирование орбит - SCALE, WIDTH - ширина окно программы
SCALE = 150
WIDTH = 1400
HEIGHT = 900
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

# Данные планет: имя, расстояние (а.е.), радиус (в радиусах Земли), цвет, период (дни), нач.угол (градусы)
PLANET_DATA = [
    {"name": "Меркурий", "distance": 0.4, "radius": 11.00, "color": "gray", "period": 88, "angle": 0},
    {"name": "Венера", "distance": 0.7, "radius": 11.00, "color": "khaki", "period": 225, "angle": 120},
    {"name": "Земля", "distance": 1.0, "radius": 11.00, "color": "blue", "period": 365, "angle": 200},
    {"name": "Марс", "distance": 1.5, "radius": 11.00, "color": "red", "period": 687, "angle": 300},
    {"name": "Юпитер", "distance": 5.2, "radius": 11.00, "color": "orange", "period": 4331, "angle": 50},
    {"name": "Сатурн", "distance": 9.5, "radius": 11.00, "color": "goldenrod", "period": 10747, "angle": 140},
    {"name": "Уран", "distance": 19.0, "radius": 11.00, "color": "lightblue", "period": 30589, "angle": 210},
    {"name": "Нептун", "distance": 30.0, "radius": 11.00, "color": "blue", "period": 59800, "angle": 330},
]

MOON_DATA = {"name": "Луна", "distance": 0.1, "radius": 9.00, "color": "white", "period": 27.3, "angle": 0}
SUN_DATA = {"name": "Солнце", "radius": 12, "color": "yellow"}

# Словарь с URL-адресами Википедии для каждого объекта
WIKIPEDIA_URLS = {
    "Солнце": "https://ru.wikipedia.org/wiki/Солнце",
    "Меркурий": "https://ru.wikipedia.org/wiki/Меркурий",
    "Венера": "https://ru.wikipedia.org/wiki/Венера",
    "Земля": "https://ru.wikipedia.org/wiki/Земля",
    "Марс": "https://ru.wikipedia.org/wiki/Марс",
    "Юпитер": "https://ru.wikipedia.org/wiki/Юпитер",
    "Сатурн": "https://ru.wikipedia.org/wiki/Сатурн",
    "Уран": "https://ru.wikipedia.org/wiki/Уран_(планета)",
    "Нептун": "https://ru.wikipedia.org/wiki/Нептун",
    "Луна": "https://ru.wikipedia.org/wiki/Луна"
}

# Краткие описания объектов
OBJECT_DESCRIPTIONS = {
    "Солнце": "Звезда, вокруг которой вращается Земля и другие планеты Солнечной системы. "
              "Содержит 99.86% всей массы Солнечной системы. Температура поверхности: около 5500°C.",

    "Меркурий": "Самая близкая к Солнцу планета. Из-за отсутствия атмосферы перепады температур "
                "на поверхности составляют от -180°C ночью до +430°C днём. Год длится 88 земных дней.",

    "Венера": "Вторая планета от Солнца. Имеет плотную атмосферу из углекислого газа, "
              "создающую сильнейший парниковый эффект. Температура поверхности около 460°C.",

    "Земля": "Третья планета от Солнца. Единственное известное тело во Вселенной, населённое живыми "
             "организмами. 71% поверхности покрыто водой. Имеет один естественный спутник — Луну.",

    "Марс": "Четвёртая планета от Солнца. Из-за содержания оксида железа в грунте имеет красноватый цвет. "
            "Имеет два спутника — Фобос и Деймос. Атмосфера разрежена, состоит в основном из углекислого газа.",

    "Юпитер": "Самая большая планета Солнечной системы. Газовый гигант, не имеет твёрдой поверхности. "
              "Имеет 79 спутников, самые крупные из них — Ио, Европа, Ганимед и Каллисто.",

    "Сатурн": "Шестая планета от Солнца. Известен своей системой колец, состоящих из частичек льда и пыли. "
              "Газовый гигант, имеет 82 спутника. Самый крупный спутник — Титан.",

    "Уран": "Седьмая планета от Солнца. Относится к ледяным гигантам. Имеет систему колец и 27 спутников. "
            "Вращается вокруг Солнца 'лёжа на боку' — ось вращения наклонена на 98 градусов.",

    "Нептун": "Восьмая и самая дальняя планета от Солнца. Ледяной гигант, имеет 14 спутников. "
              "На поверхности бушуют самые сильные ветры в Солнечной системе — до 2100 км/ч.",

    "Луна": "Единственный естественный спутник Земли. Пятый по величине спутник в Солнечной системе. "
            "Всегда повёрнута к Земле одной стороной. Расстояние до Земли: 384 400 км."
}


class InfoWindow:
    """Класс для создания информационного окна, привязанного к объекту"""
```def __init__(self, canvas, obj, x, y):
    """
    Конструктор класса InfoWindow.
    Вызывается автоматически при создании нового информационного окна.
    
    Параметры:
    - canvas: холст, на котором будет нарисовано окно
    - obj: объект (планета/солнце/луна), для которого показываем информацию
    - x, y: координаты, где появится окно (рядом с объектом)
    """
    
    # Сохраняем холст, чтобы потом рисовать на нем элементы окна
    self.canvas = canvas
    
    # Сохраняем объект (планету/солнце), чтобы знать:
    # - его имя (для заголовка)
    # - его цвет (для заглушки, если нет картинки)
    # - другую информацию для описания
    self.obj = obj
    
    # Запоминаем координаты окна (x, y)
    # Они будут использоваться при создании и обновлении позиции
    self.x = x
    self.y = y
    
    # Флаг, видимо ли окно в данный момент
    # Нужен, чтобы не пытаться обновлять уже закрытое окно
    self.is_visible = True
    
    # Сюда позже запишется ID главного прямоугольника окна (его фона)
    # ID нужен, чтобы можно было перемещать окно или удалить его
    self.window_id = None
    
    # Сюда запишется ID кнопки закрытия (крестика)
    # Нужен для изменения цвета при наведении и обработки клика
    self.close_button_id = None
    
    # Список для хранения ID всех текстовых элементов внутри окна
    # Пригодится, если понадобится их все сразу удалить
    self.text_items = []
    
    # Переменная для хранения изображения (объект ImageTk.PhotoImage)
    # Храним здесь, чтобы изображение не удалилось сборщиком мусора
    self.image_tk = None
    
    # ID изображения на холсте (чтобы можно было его перемещать)
    self.image_id = None
    
    # ВЫЗЫВАЕМ МЕТОД, КОТОРЫЙ РИСУЕТ ОКНО
    # Здесь мы уже подготовили все данные:
    # - знаем, где рисовать (x, y)
    # - знаем, для какого объекта (obj)
    # - создали переменные для хранения ID элементов
    self.create_window()```
    def __init__(self, canvas, obj, x, y):
        self.canvas = canvas
        self.obj = obj
        self.x = x
        self.y = y
        self.is_visible = True
        self.window_id = None
        self.close_button_id = None
        self.text_items = []
        self.image_tk = None
        self.image_id = None

        self.create_window()

    def create_window(self):
        """Создает окно с информацией"""
        # Координаты окна (справа от планеты)
        window_x = self.x + 50
        window_y = self.y - 120
        window_width = 350
        window_height = 420

        # Создаем фон окна
        self.window_id = self.canvas.create_rectangle(
            window_x, window_y,
            window_x + window_width, window_y + window_height,
            fill="#2b2b2b", outline="yellow", width=2,
            tags="info_window"
        )

        # Создаем заголовок
        self.canvas.create_text(
            window_x + 20, window_y + 25,
            text=f"{self.obj.name}",
            fill="yellow", font=("Arial", 16, "bold"),
            anchor="w", tags="info_window"
        )

        # Пытаемся загрузить изображение
        circle_x = window_x + window_width // 2
        circle_y = window_y + 85
        circle_size = 90

        # Путь к изображению (поддерживаем разные форматы)
        img_path = None
        possible_paths = [
            f"IMAGES/{self.obj.name.upper()}.jpg",
            f"IMAGES/{self.obj.name.upper()}.png",
            f"IMAGES/{self.obj.name.lower()}.jpg",
            f"IMAGES/{self.obj.name.lower()}.png",
            f"images/{self.obj.name.lower()}.jpg",
            f"images/{self.obj.name.lower()}.png"
        ]

        for path in possible_paths:
            if os.path.exists(path):
                img_path = path
                break

        if img_path and os.path.exists(img_path):
            try:
                # Загружаем и уменьшаем изображение
                pil_image = Image.open(img_path)
                pil_image = pil_image.resize((circle_size, circle_size), Image.Resampling.LANCZOS)
                self.image_tk = ImageTk.PhotoImage(pil_image)

                # Создаем изображение на canvas
                self.image_id = self.canvas.create_image(
                    circle_x, circle_y,
                    image=self.image_tk, tags="info_window"
                )

                # Рисуем рамку вокруг изображения
                self.canvas.create_rectangle(
                    circle_x - circle_size // 2 - 2,
                    circle_y - circle_size // 2 - 2,
                    circle_x + circle_size // 2 + 2,
                    circle_y + circle_size // 2 + 2,
                    outline="white", width=2, tags="info_window"
                )
            except Exception as e:
                print(f"Ошибка загрузки изображения {img_path}: {e}")
                # Если ошибка, рисуем круг
                self.draw_fallback_circle(circle_x, circle_y, circle_size)
        else:
            # Если изображение не найдено, рисуем круг
            self.draw_fallback_circle(circle_x, circle_y, circle_size)

        # Добавляем краткое описание
        desc_y = circle_y + circle_size // 2 + 25
        desc = OBJECT_DESCRIPTIONS.get(self.obj.name, "Описание отсутствует")
        if len(desc) > 180:
            desc = desc[:180] + "..."

        self.canvas.create_text(
            window_x + 20, desc_y,
            text=desc,
            fill="white", font=("Arial", 9),
            anchor="nw", width=310, tags="info_window"
        )

        # Добавляем характеристики
        specs_y = desc_y + 80

        # Разделительная линия
        self.canvas.create_line(
            window_x + 20, specs_y - 10,
            window_x + window_width - 20, specs_y - 10,
            fill="gray", width=1, tags="info_window"
        )

        if isinstance(self.obj, Sun):
            specs = [
                f"• Радиус: {SUN_DATA['radius']} земных радиусов",
                f"• Температура: 5500°C",
                f"• Возраст: 4.6 млрд лет"
            ]
        elif isinstance(self.obj, Planet):
            planet_info = next((p for p in PLANET_DATA if p["name"] == self.obj.name), None)
            if planet_info:
                specs = [
                    f"• Расстояние от Солнца: {planet_info['distance']} а.е.",
                    f"• Радиус: {planet_info['radius']} земных",
                    f"• Период обращения: {planet_info['period']} дней"
                ]
        elif isinstance(self.obj, Moon):
            specs = [
                f"• Радиус: {MOON_DATA['radius']} земных",
                f"• Период обращения: {MOON_DATA['period']} дней",
                f"• Расстояние от Земли: 384 400 км"
            ]
        else:
            specs = []

        for i, spec in enumerate(specs):
            self.canvas.create_text(
                window_x + 20, specs_y + i * 22,
                text=spec,
                fill="lightblue", font=("Arial", 9),
                anchor="w", tags="info_window"
            )

        # Создаем кнопку "Подробнее"
        self.canvas.create_rectangle(
            window_x + 20, window_y + window_height - 45,
            window_x + 130, window_y + window_height - 20,
            fill="#4a4a4a", outline="yellow", width=1,
            tags=("info_window", "more_btn")
        )

        self.canvas.create_text(
            window_x + 75, window_y + window_height - 32,
            text="📖 Подробнее",
            fill="white", font=("Arial", 9),
            tags=("info_window", "more_btn")
        )

        # Привязываем события к кнопке
        self.canvas.tag_bind("more_btn", '<Button-1>',
                             lambda e: self.open_wikipedia())
        self.canvas.tag_bind("more_btn", '<Enter>',
                             lambda e: self.on_more_enter())
        self.canvas.tag_bind("more_btn", '<Leave>',
                             lambda e: self.on_more_leave())

        # Создаем кнопку закрытия
        self.canvas.create_text(
            window_x + window_width - 20, window_y + 20,
            text="✕", fill="red", font=("Arial", 16, "bold"),
            tags=("info_window", "close_btn")
        )

        # Привязываем событие закрытия
        self.canvas.tag_bind("close_btn", '<Button-1>',
                             lambda e: self.close())
        self.canvas.tag_bind("close_btn", '<Enter>',
                             lambda e: self.canvas.itemconfig("close_btn", fill="yellow"))
        self.canvas.tag_bind("close_btn", '<Leave>',
                             lambda e: self.canvas.itemconfig("close_btn", fill="red"))

    def draw_fallback_circle(self, x, y, size):
        """Рисует круг-заглушку, если изображение не найдено"""
        # Рисуем круг
        self.canvas.create_oval(
            x - size // 2,
            y - size // 2,
            x + size // 2,
            y + size // 2,
            fill=self.obj.color, outline="white", width=3,
            tags="info_window"
        )

        # Добавляем эмодзи или букву в центр
        if isinstance(self.obj, Sun):
            symbol = "☀️"
        elif isinstance(self.obj, Moon):
            symbol = "🌙"
        elif self.obj.name == "Земля":
            symbol = "🌍"
        elif self.obj.name == "Марс":
            symbol = "🔴"
        elif self.obj.name in ["Юпитер", "Сатурн"]:
            symbol = "🪐"
        else:
            symbol = self.obj.name[0]

        self.canvas.create_text(
            x, y,
            text=symbol,
            fill="white", font=("Arial", 40),
            tags="info_window"
        )

    def on_more_enter(self):
        """Эффект при наведении на кнопку 'Подробнее'"""
        self.canvas.itemconfig("more_btn", fill="yellow")

    def on_more_leave(self):
        """Эффект при убирании мыши с кнопки 'Подробнее'"""
        self.canvas.itemconfig("more_btn", fill="white")

    def open_wikipedia(self):
        """Открывает страницу Википедии"""
        if self.obj.name in WIKIPEDIA_URLS:
            webbrowser.open(WIKIPEDIA_URLS[self.obj.name])

    def close(self):
        """Закрывает информационное окно"""
        self.canvas.delete("info_window")
        self.is_visible = False

    def update_position(self, x, y):
        """Обновляет позицию окна (если планета движется)"""
        if not self.is_visible:
            return

        self.x = x
        self.y = y

        # Получаем текущие координаты всех элементов окна
        if self.window_id:
            coords = self.canvas.coords(self.window_id)
            if coords:
                # Вычисляем смещение
                dx = (x + 50) - coords[0]
                dy = (y - 120) - coords[1]

                # Перемещаем все элементы окна
                for item_id in self.canvas.find_withtag("info_window"):
                    self.canvas.move(item_id, dx, dy)


class SolarObject:
    def __init__(self, canvas, x, y, name, radius_earth, color, img_path=None):
        self.canvas = canvas
        self.name = name
        self.color = color
        self.base_radius = max(3, radius_earth * 3)
        self.radius_px = self.base_radius
        self.x = x
        self.y = y
        self.info_window = None

        self.image_tk = None
        self.image_id = None

        # Пытаемся загрузить изображение для отображения на орбите
        if img_path and os.path.exists(img_path):
            try:
                pil_image = Image.open(img_path)
                img_size = int(self.radius_px * 2)
                pil_image = pil_image.resize((img_size, img_size), Image.Resampling.LANCZOS)
                self.image_tk = ImageTk.PhotoImage(pil_image)
                self.image_id = self.canvas.create_image(x, y, image=self.image_tk, anchor='center', tags=self.name)
            except Exception as e:
                print(f"Ошибка загрузки {img_path}: {e}. Рисуем круг.")
                self.image_id = self.canvas.create_oval(x - self.radius_px, y - self.radius_px,
                                                        x + self.radius_px, y + self.radius_px,
                                                        fill=self.color, outline="white", tags=self.name)
        else:
            # Если изображение не найдено, рисуем круг
            self.image_id = self.canvas.create_oval(x - self.radius_px, y - self.radius_px,
                                                    x + self.radius_px, y + self.radius_px,
                                                    fill=self.color, outline="white", tags=self.name)

    def set_zoom(self, zoom):
        self.radius_px = max(2, self.base_radius * zoom)
        if not self.image_tk:
            x1 = self.x - self.radius_px
            y1 = self.y - self.radius_px
            x2 = self.x + self.radius_px
            y2 = self.y + self.radius_px
            self.canvas.coords(self.image_id, x1, y1, x2, y2)

    def move_to(self, x, y):
        self.x = x
        self.y = y
        if self.image_tk:
            self.canvas.coords(self.image_id, x, y)
        else:
            self.canvas.coords(self.image_id, x - self.radius_px, y - self.radius_px,
                               x + self.radius_px, y + self.radius_px)

        if self.info_window and self.info_window.is_visible:
            self.info_window.update_position(x, y)

    def show_info(self):
        """Показывает информационное окно рядом с объектом"""
        # Закрываем предыдущее окно, если было открыто
        if self.info_window:
            self.info_window.close()

        # Создаем новое окно
        self.info_window = InfoWindow(self.canvas, self, self.x, self.y)


class Planet(SolarObject):
    def __init__(self, canvas, distance_au, data, img_path=None):
        self.distance_au = distance_au
        self.period = data["period"]
        self.angle = math.radians(data["angle"])
        self.orbit_radius_base = distance_au * SCALE
        super().__init__(canvas, CENTER_X, CENTER_Y, data["name"],
                         data["radius"], data["color"], img_path)
        self.initial_angle = data["angle"]
        self.label_id = self.canvas.create_text(0, 0, text=data["name"],
                                                fill="white", font=("Arial", 8),
                                                tags=f"label_{data['name']}")

    def update_position(self, time_mult, zoom, dt=0.05):
        delta_angle = (2 * math.pi / self.period) * dt * time_mult
        self.angle += delta_angle
        orbit_r = self.orbit_radius_base * zoom
        x = CENTER_X + orbit_r * math.cos(self.angle)
        y = CENTER_Y + orbit_r * math.sin(self.angle)
        self.move_to(x, y)
        self.canvas.coords(self.label_id, x - 15, y - self.radius_px - 5)

    def set_zoom(self, zoom):
        super().set_zoom(zoom)


class Moon(SolarObject):
    def __init__(self, canvas, parent_planet, distance_au, data, img_path=None):
        self.parent = parent_planet
        self.distance_au = distance_au
        self.period = data["period"]
        self.angle = math.radians(data["angle"])
        self.base_orbit_radius = distance_au * SCALE
        super().__init__(canvas, parent_planet.x, parent_planet.y, data["name"],
                         data["radius"], data["color"], img_path)
        self.label_id = self.canvas.create_text(0, 0, text=data["name"],
                                                fill="white", font=("Arial", 7),
                                                tags=f"label_{data['name']}")

    def update_position(self, time_mult, zoom, dt=0.05):
        delta_angle = (2 * math.pi / self.period) * dt * time_mult
        self.angle += delta_angle
        orbit_r = self.base_orbit_radius * zoom
        rel_x = orbit_r * math.cos(self.angle)
        rel_y = orbit_r * math.sin(self.angle)
        abs_x = self.parent.x + rel_x
        abs_y = self.parent.y + rel_y
        self.move_to(abs_x, abs_y)
        self.canvas.coords(self.label_id, abs_x - 10, abs_y - self.radius_px - 3)


class Sun(SolarObject):
    def __init__(self, canvas, img_path=None):
        super().__init__(canvas, CENTER_X, CENTER_Y, "Солнце",
                         SUN_DATA["radius"], SUN_DATA["color"], img_path)

    def set_zoom(self, zoom):
        super().set_zoom(zoom)
        self.move_to(CENTER_X, CENTER_Y)


class SolarSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Симуляция Солнечной системы")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")

        self.playing = True
        self.time_mult = 1.0
        self.zoom = 1.0
        self.dt = 0.05

        # Создаем главный контейнер
        main_container = ttk.Frame(root)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Создаем Canvas для отображения планет
        self.canvas = tk.Canvas(main_container, width=WIDTH, height=HEIGHT - 180, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Создаем фрейм для панели с иконками
        icon_frame = ttk.Frame(main_container)
        icon_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 5))

        # Создаем холст для иконок
        self.icon_canvas = tk.Canvas(icon_frame, height=85, bg='#1a1a1a', highlightthickness=0)
        self.icon_canvas.pack(fill=tk.X, padx=10)

        self.create_planet_icons()

        # Создаем фрейм для панели управления
        control_frame = ttk.Frame(main_container)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        # Кнопки управления
        ttk.Button(control_frame, text="▶", command=self.play, width=3).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="⏸", command=self.pause, width=3).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="↺", command=self.reset_angles, width=3).pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text="Скорость:").pack(side=tk.LEFT, padx=(20, 5))
        self.time_scale = tk.Scale(control_frame, from_=0, to_=200, orient=tk.HORIZONTAL,
                                   length=150, command=self.set_time_mult)
        self.time_scale.set(20)
        self.time_scale.pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text="Масштаб:").pack(side=tk.LEFT, padx=(20, 5))
        self.zoom_scale = tk.Scale(control_frame, from_=0.2, to_=3.0, resolution=0.1,
                                   orient=tk.HORIZONTAL, length=150, command=self.set_zoom)
        self.zoom_scale.set(1.0)
        self.zoom_scale.pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, text="Сброс вида", command=self.reset_view).pack(side=tk.LEFT, padx=20)

        self.create_objects()
        self.draw_orbits()
        self.bind_clicks()
        self.animate()

    def create_planet_icons(self):
        """Создает панель с иконками планет"""
        self.planet_icons = []
        icon_size = 40
        spacing = 90

        # Добавляем текст "СОЛНЦЕ" слева
        self.icon_canvas.create_text(40, 30, text="СОЛНЦЕ:",
                                     fill="yellow", font=("Arial", 10, "bold"), anchor="w")

        # Добавляем Солнце
        sun_x = 120
        self.create_single_icon(sun_x, 42, "Солнце", "yellow", icon_size + 5)

        # Добавляем текст "ПЛАНЕТЫ:" с отступом
        planet_text_x = sun_x + 80
        self.icon_canvas.create_text(planet_text_x, 30, text="ПЛАНЕТЫ:",
                                     fill="lightblue", font=("Arial", 10, "bold"), anchor="w")

        # Добавляем планеты
        planet_start_x = planet_text_x + 80
        for i, planet in enumerate(PLANET_DATA):
            x = planet_start_x + i * spacing
            color = planet["color"]
            self.create_single_icon(x, 42, planet["name"], color, icon_size)

        # Добавляем текст "ЛУНА:" с отступом
        moon_text_x = planet_start_x + len(PLANET_DATA) * spacing + 30
        self.icon_canvas.create_text(moon_text_x, 30, text="ЛУНА:",
                                     fill="white", font=("Arial", 10, "bold"), anchor="w")

        # Добавляем Луну
        moon_x = moon_text_x + 60
        self.create_single_icon(moon_x, 42, "Луна", "white", icon_size - 5)

        # Рисуем рамку вокруг иконок
        self.icon_canvas.create_rectangle(10, 10, WIDTH - 20, 75, outline='#444444', width=2)

    def create_single_icon(self, x, y, name, color, size):
        """Создает одну иконку планеты"""
        # Рисуем круг
        icon_id = self.icon_canvas.create_oval(
            x - size // 2, y - size // 2,
            x + size // 2, y + size // 2,
            fill=color, outline="white", width=2,
            tags=f"icon_{name}"
        )

        # Добавляем название под иконкой
        text_id = self.icon_canvas.create_text(
            x, y + size // 2 + 12,
            text=name,
            fill="white", font=("Arial", 8, "bold"),
            tags=f"icon_text_{name}"
        )

        # Добавляем эффект при наведении
        self.icon_canvas.tag_bind(f"icon_{name}", '<Enter>',
                                  lambda e, n=name: self.on_icon_enter(n))
        self.icon_canvas.tag_bind(f"icon_{name}", '<Leave>',
                                  lambda e, n=name: self.on_icon_leave(n))
        self.icon_canvas.tag_bind(f"icon_{name}", '<Button-1>',
                                  lambda e, n=name: self.on_icon_click(n))

        self.icon_canvas.tag_bind(f"icon_text_{name}", '<Enter>',
                                  lambda e, n=name: self.on_icon_enter(n))
        self.icon_canvas.tag_bind(f"icon_text_{name}", '<Leave>',
                                  lambda e, n=name: self.on_icon_leave(n))
        self.icon_canvas.tag_bind(f"icon_text_{name}", '<Button-1>',
                                  lambda e, n=name: self.on_icon_click(n))

        self.planet_icons.append({"name": name, "icon_id": icon_id, "text_id": text_id})

    def on_icon_enter(self, name):
        """Эффект при наведении на иконку"""
        for icon in self.planet_icons:
            if icon["name"] == name:
                self.icon_canvas.itemconfig(icon["icon_id"], width=4, outline="yellow")
                self.icon_canvas.itemconfig(icon["text_id"], fill="yellow")

    def on_icon_leave(self, name):
        """Эффект при убирании мыши с иконки"""
        for icon in self.planet_icons:
            if icon["name"] == name:
                self.icon_canvas.itemconfig(icon["icon_id"], width=2, outline="white")
                self.icon_canvas.itemconfig(icon["text_id"], fill="white")

    def on_icon_click(self, name):
        """Обработка клика по иконке"""
        if name == "Солнце":
            self.sun.show_info()
        elif name == "Луна":
            if self.moon:
                self.moon.show_info()
        else:
            for planet in self.planets:
                if planet.name == name:
                    planet.show_info()
                    break

    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False

    def set_time_mult(self, val):
        self.time_mult = float(val) * 0.1

    def set_zoom(self, val):
        self.zoom = float(val)
        self.sun.set_zoom(self.zoom)
        for p in self.planets:
            p.set_zoom(self.zoom)
        if self.moon:
            self.moon.set_zoom(self.zoom)
        self.canvas.delete("orbit")
        self.draw_orbits()

    def reset_view(self):
        self.zoom_scale.set(1.0)
        self.time_scale.set(20)
        self.set_zoom(1.0)
        self.set_time_mult(20)

    def reset_angles(self):
        for p in self.planets:
            p.angle = math.radians(p.initial_angle)
        if self.moon:
            self.moon.angle = math.radians(MOON_DATA["angle"])

    def create_objects(self):
        """Создает объекты Солнечной системы с изображениями"""
        # Солнце
        self.sun = Sun(self.canvas, "IMAGES/СОЛНЦЕ 2.jpg")

        # Планеты
        self.planets = []
        self.earth = None

        # Словарь соответствия имен планет и файлов изображений
        planet_images = {
            "Меркурий": "IMAGES/МЕРКУРИЙ.jpg",
            "Венера": "IMAGES/ВЕНЕРА.jpg",
            "Земля": "IMAGES/ЗЕМЛЯ.jpg",
            "Марс": "IMAGES/МАРС.jpg",
            "Юпитер": "IMAGES/ЮПИТЕР.jpg",
            "Сатурн": "IMAGES/САТУРН.jpg",
            "Уран": "IMAGES/УРАН.jpg",
            "Нептун": "IMAGES/НЕПТУН.jpg"
        }

        for data in PLANET_DATA:
            img_path = planet_images.get(data["name"])
            planet = Planet(self.canvas, data["distance"], data, img_path)
            planet.initial_angle = data["angle"]
            self.planets.append(planet)
            if data["name"] == "Земля":
                self.earth = planet

        # Луна
        if self.earth:
            self.moon = Moon(self.canvas, self.earth, MOON_DATA["distance"],
                             MOON_DATA, "IMAGES/ЛУНА.jpg")
        else:
            self.moon = None

    def draw_orbits(self):
        for p in self.planets:
            r = p.orbit_radius_base * self.zoom
            x0 = CENTER_X - r
            y0 = CENTER_Y - r
            x1 = CENTER_X + r
            y1 = CENTER_Y + r
            self.canvas.create_oval(x0, y0, x1, y1, outline='gray30', dash=(2, 4), tags="orbit")

    def bind_clicks(self):
        for planet in self.planets:
            self.canvas.tag_bind(planet.name, '<Button-1>', lambda e, p=planet: p.show_info())
        if self.moon:
            self.canvas.tag_bind(self.moon.name, '<Button-1>', lambda e, m=self.moon: m.show_info())
        self.canvas.tag_bind(self.sun.name, '<Button-1>', lambda e, s=self.sun: s.show_info())

    def animate(self):
        if self.playing:
            for planet in self.planets:
                planet.update_position(self.time_mult, self.zoom, self.dt)
            if self.moon:
                self.moon.update_position(self.time_mult, self.zoom, self.dt)
        self.root.after(50, self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    app = SolarSystemApp(root)
    root.mainloop()

