import tkinter as tk
from tkinter import ttk
import math
from PIL import Image, ImageTk
import os

# Константы
SCALE = 150
WIDTH = 1400
HEIGHT = 900
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

# Данные планет: имя, расстояние (а.е.), радиус (в радиусах Земли), цвет, период (дни), нач.угол (градусы)
PLANET_DATA = [
    {"name": "Меркурий", "distance": 0.4, "radius": 0.38, "color": "gray", "period": 88,   "angle": 0},
    {"name": "Венера",   "distance": 0.7, "radius": 0.95, "color": "khaki", "period": 225,  "angle": 120},
    {"name": "Земля",    "distance": 1.0, "radius": 1.0,  "color": "blue",  "period": 365,  "angle": 200},
    {"name": "Марс",     "distance": 1.5, "radius": 0.53, "color": "red",   "period": 687,  "angle": 300},
    {"name": "Юпитер",   "distance": 5.2, "radius": 11.2, "color": "orange","period": 4331, "angle": 50},
    {"name": "Сатурн",   "distance": 9.5, "radius": 9.5,  "color": "goldenrod","period": 10747,"angle": 140},
    {"name": "Уран",     "distance": 19.0,"radius": 4.0,  "color": "lightblue","period": 30589,"angle": 210},
    {"name": "Нептун",   "distance": 30.0,"radius": 3.9,  "color": "blue",  "period": 59800,"angle": 330},
    {"name": "Плутон",   "distance": 39.5,"radius": 0.2,  "color": "brown", "period": 90560,"angle": 80},
]

MOON_DATA = {"name": "Луна", "distance": 0.0025, "radius": 0.27, "color": "white", "period": 27.3, "angle": 0}
SUN_DATA = {"name": "Солнце", "radius": 12, "color": "yellow"}

class SolarObject:
    def __init__(self, canvas, x, y, name, radius_earth, color, img_path=None):
        self.canvas = canvas
        self.name = name
        self.color = color
        self.base_radius = max(3, radius_earth * 3)
        self.radius_px = self.base_radius
        self.x = x
        self.y = y

        self.image_tk = None
        self.image_id = None
        if img_path and os.path.exists(img_path):
            try:
                pil_image = Image.open(img_path)
                img_size = int(self.radius_px * 2)
                pil_image = pil_image.resize((img_size, img_size), Image.Resampling.LANCZOS)
                self.image_tk = ImageTk.PhotoImage(pil_image)
                self.image_id = self.canvas.create_image(x, y, image=self.image_tk, anchor='center', tags=self.name)
            except Exception as e:
                print(f"Ошибка загрузки {img_path}: {e}. Рисуем круг.")
                self.image_id = self.canvas.create_oval(x-self.radius_px, y-self.radius_px,
                                                         x+self.radius_px, y+self.radius_px,
                                                         fill=self.color, outline="white", tags=self.name)
        else:
            self.image_id = self.canvas.create_oval(x-self.radius_px, y-self.radius_px,
                                                     x+self.radius_px, y+self.radius_px,
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
            self.canvas.coords(self.image_id, x-self.radius_px, y-self.radius_px,
                               x+self.radius_px, y+self.radius_px)

class Planet(SolarObject):
    def __init__(self, canvas, distance_au, data, img_path=None):
        self.distance_au = distance_au
        self.period = data["period"]
        self.angle = math.radians(data["angle"])
        self.orbit_radius_base = distance_au * SCALE
        super().__init__(canvas, CENTER_X, CENTER_Y, data["name"],
                         data["radius"], data["color"], img_path)
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

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(root)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        ttk.Button(control_frame, text="▶", command=self.play).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="⏸", command=self.pause).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="↺", command=self.reset_angles).pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text="Скорость:").pack(side=tk.LEFT, padx=5)
        self.time_scale = tk.Scale(control_frame, from_=0, to_=200, orient=tk.HORIZONTAL,
                                   length=200, command=self.set_time_mult)
        self.time_scale.set(20)
        self.time_scale.pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text="Масштаб:").pack(side=tk.LEFT, padx=20)
        self.zoom_scale = tk.Scale(control_frame, from_=0.2, to_=3.0, resolution=0.1,
                                   orient=tk.HORIZONTAL, length=200, command=self.set_zoom)
        self.zoom_scale.set(1.0)
        self.zoom_scale.pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, text="Сброс вида", command=self.reset_view).pack(side=tk.LEFT, padx=20)

        self.create_objects()
        self.draw_orbits()
        self.bind_clicks()  # <-- добавлено: привязка кликов
        self.animate()

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
        self.moon.angle = math.radians(MOON_DATA["angle"])

    def create_objects(self):
        self.sun = Sun(self.canvas, "images/sun.png")
        self.planets = []
        self.earth = None
        for data in PLANET_DATA:
            img_path = f"images/{data['name'].lower()}.png"
            planet = Planet(self.canvas, data["distance"], data, img_path)
            planet.initial_angle = data["angle"]
            self.planets.append(planet)
            if data["name"] == "Земля":
                self.earth = planet
        if self.earth:
            self.moon = Moon(self.canvas, self.earth, MOON_DATA["distance"],
                             MOON_DATA, "images/moon.png")
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

    # --- Новый метод: привязка событий клика ---
    def bind_clicks(self):
        # Для каждой планеты
        for planet in self.planets:
            self.canvas.tag_bind(planet.name, '<Button-1>', lambda e, p=planet: self.show_info(p))
        # Для Луны
        if self.moon:
            self.canvas.tag_bind(self.moon.name, '<Button-1>', lambda e, m=self.moon: self.show_info(m))
        # Для Солнца
        self.canvas.tag_bind(self.sun.name, '<Button-1>', lambda e, s=self.sun: self.show_info(s))

    # --- Новый метод: отображение информации об объекте ---
    def show_info(self, obj):
        # Создаём всплывающее окно
        info_win = tk.Toplevel(self.root)
        info_win.title(f"Информация: {obj.name}")
        info_win.geometry("300x200")
        info_win.resizable(False, False)

        # Формируем текст в зависимости от типа объекта
        if isinstance(obj, Sun):
            text = f"Солнце\nРадиус: {SUN_DATA['radius']} земных радиусов\nЦвет: {obj.color}"
        elif isinstance(obj, Planet):
            text = (f"Планета: {obj.name}\n"
                    f"Расстояние от Солнца: {obj.distance_au} а.е.\n"
                    f"Радиус: {obj.base_radius/3:.2f} земных радиусов\n"
                    f"Период обращения: {obj.period} дней\n"
                    f"Цвет: {obj.color}")
        elif isinstance(obj, Moon):
            text = (f"Спутник: {obj.name}\n"
                    f"Радиус: {obj.base_radius/3:.2f} земных радиусов\n"
                    f"Период обращения вокруг Земли: {obj.period} дней\n"
                    f"Цвет: {obj.color}")
        else:
            text = "Неизвестный объект"

        label = tk.Label(info_win, text=text, font=("Arial", 10), justify=tk.LEFT, padx=10, pady=10)
        label.pack(expand=True, fill=tk.BOTH)

        # Кнопка закрытия
        tk.Button(info_win, text="Закрыть", command=info_win.destroy).pack(pady=5)

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
