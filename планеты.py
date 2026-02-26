import tkinter as tk
from tkinter import ttk
import math
from PIL import Image, ImageTk
import os



SCALE = 150

WIDTH = 1400
HEIGHT = 900
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2



PLANET_DATA = [
    {"name": "Меркурий", "distance": 0.4, "radius": 0.38, "color": "gray", "period_days": 88},
    {"name": "Венера", "distance": 0.7, "radius": 0.95, "color": "khaki", "period_days": 225},
    {"name": "Земля", "distance": 1.0, "radius": 1.0, "color": "blue", "period_days": 365},
    {"name": "Марс", "distance": 1.5, "radius": 0.53, "color": "red", "period_days": 687},
    {"name": "Юпитер", "distance": 5.2, "radius": 11.2, "color": "orange", "period_days": 4331},
    {"name": "Сатурн", "distance": 9.5, "radius": 9.5, "color": "goldenrod", "period_days": 10747},
    {"name": "Уран", "distance": 19.0, "radius": 4.0, "color": "lightblue", "period_days": 30589},
    {"name": "Нептун", "distance": 30.0, "radius": 3.9, "color": "blue", "period_days": 59800},
    {"name": "Плутон", "distance": 39.5, "radius": 0.2, "color": "brown", "period_days": 90560}, # Для красоты
    {"name": "Луна", "distance": 1.0, "radius": 0.27, "color": "white", "period_days": 27.3}, # Вокруг Земли, позже
]


SUN_DATA = {"name": "Солнце", "radius": 109, "color": "yellow"}


class Planet:
    def __init__(self, canvas, x, y, name, distance_au, radius_earth, color, period_days, img_path=None):
        self.canvas = canvas
        self.name = name
        self.distance_au = distance_au

        self.radius_px = max(3, radius_earth * 3)
        self.color = color
        self.period_days = period_days
        self.angle = math.radians((hash(name) % 360))
        self.orbit_radius_px = distance_au * SCALE


        self.image = None
        self.image_tk = None
        if img_path and os.path.exists(img_path):
            try:
                pil_image = Image.open(img_path)

                img_size = self.radius_px * 2
                if img_size < 5: img_size = 10
                pil_image = pil_image.resize((img_size, img_size), Image.Resampling.LANCZOS)
                self.image_tk = ImageTk.PhotoImage(pil_image)
                self.image = self.canvas.create_image(x, y, image=self.image_tk, anchor='center', tags=(f"planet_{name}", "planet"))
            except Exception as e:
                print(f"Ошибка загрузки {img_path}: {e}. Будет использован круг.")
                self.image = self.canvas.create_oval(x-self.radius_px, y-self.radius_px, x+self.radius_px, y+self.radius_px, fill=self.color, outline="white", tags=(f"planet_{name}", "planet"))
        else:

            self.image = self.canvas.create_oval(x-self.radius_px, y-self.radius_px, x+self.radius_px, y+self.radius_px, fill=self.color, outline="white", tags=(f"planet_{name}", "planet"))

    def update_position(self, time_multiplier, zoom):

        delta_angle = (2 * math.pi / (self.period_days)) * 0.01 * time_multiplier
        self.angle += delta_angle


        display_orbit_radius = self.orbit_radius_px * zoom
        x = CENTER_X + display_orbit_radius * math.cos(self.angle)
        y = CENTER_Y + display_orbit_radius * math.sin(self.angle)


        if isinstance(self.image, int):
            self.canvas.coords(self.image, x-self.radius_px, y-self.radius_px, x+self.radius_px, y+self.radius_px)
        else:
            self.canvas.coords(self.image, x, y)


class Sun:
    def __init__(self, canvas, x, y, radius_earth, img_path=None):
        self.canvas = canvas
        self.radius_px = max(10, radius_earth * 0.5)
        self.x = x
        self.y = y
        self.image = None
        if img_path and os.path.exists(img_path):
            try:
                pil_image = Image.open(img_path)
                img_size = self.radius_px * 2
                pil_image = pil_image.resize((img_size, img_size), Image.Resampling.LANCZOS)
                self.image_tk = ImageTk.PhotoImage(pil_image)
                self.image = self.canvas.create_image(x, y, image=self.image_tk, anchor='center', tags="sun")
            except Exception as e:
                print(f"Ошибка загрузки Солнца: {e}")
                self.image = self.canvas.create_oval(x-self.radius_px, y-self.radius_px, x+self.radius_px, y+self.radius_px, fill="yellow", tags="sun")
        else:
            self.image = self.canvas.create_oval(x-self.radius_px, y-self.radius_px, x+self.radius_px, y+self.radius_px, fill="yellow", tags="sun")

    def update_zoom(self, zoom):

        pass



class SolarSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Симуляция Солнечной системы")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")


        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)


        control_frame = ttk.Frame(root)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)


        ttk.Label(control_frame, text="Ускорение времени:").pack(side=tk.LEFT, padx=5)
        self.time_scale = tk.Scale(control_frame, from_=1, to_=100, orient=tk.HORIZONTAL, length=200)
        self.time_scale.set(1)
        self.time_scale.pack(side=tk.LEFT, padx=5)


        ttk.Label(control_frame, text="Масштаб:").pack(side=tk.LEFT, padx=20)
        self.zoom_scale = tk.Scale(control_frame, from_=0.2, to_=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=200)
        self.zoom_scale.set(1.0)
        self.zoom_scale.pack(side=tk.LEFT, padx=5)


        ttk.Button(control_frame, text="Сброс вида", command=self.reset_view).pack(side=tk.LEFT, padx=20)


        self.planets = []
        self.create_objects()


        self.animate()

    def create_objects(self):
        # Солнце
        self.sun = Sun(self.canvas, CENTER_X, CENTER_Y, SUN_DATA["radius"], "images/sun.png")


        for data in PLANET_DATA:
            img_path = f"images/{data['name'].lower()}.png"
            planet = Planet(
                self.canvas, CENTER_X, CENTER_Y, data['name'],
                data['distance'], data['radius'], data['color'], data['period_days'],
                img_path
            )
            self.planets.append(planet)

    def reset_view(self):
        self.zoom_scale.set(1.0)
        self.time_scale.set(1)


    def animate(self):

        time_mult = self.time_scale.get()
        zoom = self.zoom_scale.get()


        for planet in self.planets:
            planet.update_position(time_mult, zoom)


        self.root.after(50, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = SolarSystemApp(root)
    root.mainloop()