import os
import time
import threading
import cv2
import numpy as np
import imagehash
import json
import uuid
import subprocess
import torch
import numpy as np
import cv2
from tkinter import Tk, Label, Button, filedialog, messagebox, Canvas, Toplevel, Scale, HORIZONTAL
from PIL import Image, ImageTk, ExifTags, ImageEnhance, ImageOps
from torchvision import transforms, models
from tkinter import Entry, StringVar
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Label, Button, filedialog, messagebox
from tkinter import font
from PIL import Image, ImageTk
from tkinter import Listbox, END
from PIL import ImageDraw, ImageFont
from tkinter import OptionMenu

# Configuración de estilo 3D oscuro
ESTILO_DARK = {
    "bg_main": "#1e1e2f",
    "fg_text": "#ffffff",
    "bg_button": "#2e2e3f",
    "bg_hover": "#44445a",
    "relief": "raised",
    "bd": 2
}

def aplicar_estilo_3d(widget):
        widget.config(
            bg=ESTILO_DARK["bg_button"],
            fg=ESTILO_DARK["fg_text"],
            activebackground=ESTILO_DARK["bg_hover"],
            activeforeground="white",
            relief=ESTILO_DARK["relief"],
            bd=ESTILO_DARK["bd"],
            font=("Segoe UI", 10, "bold")
        )
        
class VisorFotos:
    def __init__(self, root):
        self.root = root
        self.root.title("Visor de Fotos Avanzado")
        self.root.geometry("900x700")

        # Estructura de frames
        self.frame_top = Frame(root)
        self.frame_top.pack(side="top", fill="x")

        self.frame_top2 = Frame(root)
        self.frame_top2.pack(side="top", fill="x")

        self.frame_bottom = Frame(root)
        self.frame_bottom.pack(side="top", fill="x")

        self.frame_left = Frame(root)
        self.frame_left.pack(side="left", fill="y")

        self.frame_main = Frame(root, bg="black")
        self.frame_main.pack(expand=True, fill="both")

        self.label = Label(self.frame_main, bg="black")
        self.label.pack(expand=True, fill="both")

        self.frame_bottom = Frame(root)
        self.frame_bottom.pack(side="bottom", fill="x")

        self.frame_bottom_extra = Frame(root)
        self.frame_bottom_extra.pack(side="top", fill="x")


        # Botones superiores
        botones_top = [
            ("📁 Cargar Carpeta", self.cargar_carpeta),
            ("🖼 Seleccionar Imágenes", self.seleccionar_imagenes),
            ("⏮ Anterior", self.anterior),
            ("Siguiente ⏭", self.siguiente),
            ("🔍 Zoom +", self.zoom_in),
            ("🔎 Zoom -", self.zoom_out),
            ("💾 Guardar Copia", self.guardar_copia),
            ("🗑 Eliminar", self.eliminar_imagen),
            ("🖥 Pantalla Completa", self.toggle_fullscreen),
            ("🎞 Presentación", self.presentacion),
            ("🖼 Mosaico", self.ver_mosaico),
            ("📄 Ver EXIF", self.ver_exif),
            ("🌀 Desenfoque Selectivo", self.desenfoque_selectivo),
            ("💧 Marca de Agua", self.configurar_marca_agua),
        ]
        for texto, comando in botones_top:
            Button(self.frame_top, text=texto, command=comando).pack(side="left", padx=3, pady=2)

        # Botones laterales (solo ejemplo)
        botones_left = [
            ("🖤 B/N", self.filtro_bn),
            ("🟤 Sepia", self.filtro_sepia),
            ("🔄 Invertir", self.filtro_invertir),
            ("☀️ Brillo/Contraste", self.ajustar_brillo_contraste),
            ("↩️ Deshacer", self.deshacer_cambios),
            ("✏️ Dibujar", self.dibujar_imagen),
            ("🏷️ Texto", self.insertar_texto),
            ("✂️ Recorte", self.recortar_imagen),
            ("🎭 Rostros", self.detectar_rostros),
            ("🌓 Tema", self.cambiar_tema),
            ("↺ 90°", self.rotar_izquierda),
            ("↻ 90°", self.rotar_derecha),
            ("🔄 180°", self.rotar_180),
            ("🎯 Rotar Libre", self.rotar_libre),
            ("📸 Capturar Webcam", self.capturar_desde_webcam),
            ("🎞 Crear GIF", self.crear_gif),
            ("🧩 Comparar", self.comparar_imagenes),
            ("🕵️ Buscar Duplicados", self.buscar_duplicados),
            ("📅 Agrupar por Fecha", self.agrupar_por_fecha),
            ("⭐ Favorito", self.toggle_favorito),
            ("🛠 Reconstruir Imagen", self.reconstruir_imagen),
        ]
        for texto, comando in botones_left:
            Button(self.frame_left, text=texto, command=comando).pack(pady=2)

        # Botones laterales (solo ejemplo)
        botones_right = [
            ("🎨 Estilo Artístico", self.aplicar_estilo_artistico),
            ("🎨 Filtros Instagram", self.filtros_instagram),
            ("🖌️ Clonar", self.abrir_clonador),
            ("🗺 Ver en mapa", self.mostrar_en_mapa),  # Nuevo botón agregado aquí
            ("👁 Ver favoritos", self.toggle_ver_favoritos),  # Se agregó correctamente aquí
            ("📤 Compartir", self.menu_compartir),
            ("🔧 Superresolución (ESRGAN)", self.reconstruccion_esrgan),
            ("😊 Restaurar Rostros (GFPGAN)", self.restaurar_rostros_gfpgan),
            ("🔎 Búsqueda Inversa", self.buscar_inversa_google),
            ("🗺 Mapa GPS", self.mostrar_mapa_con_gps),
        ]
        for texto, comando in botones_right:
            Button(self.frame_bottom_extra, text=texto, command=comando).pack(side="left",padx=5, pady=5)

        # Botones laterales
        botones_top2 = [
            ("🧱 Crear Collage", self.crear_collage),
            ("🤣 Generar Meme", self.generar_meme),
            ("🖼️ Sticker PNG", self.agregar_sticker_png),
            ("✨ Retoque Mágico", self.retoque_magico),
            ("📣 Crear Poster", self.generar_poster),
        ]
        for texto, comando in botones_top2:
            Button(self.frame_top2, text=texto, command=comando).pack(side="left", padx=3, pady=2)

        self.imagenes = []
        self.indice = 0
        self.zoom_factor = 1.0
        self.fullscreen = False
        self.presentando = False
        self.imagen_actual = None
        self.imagen_original = None
        self.historial_ediciones = []
        self.texto_marca = "© Mi Marca"
        self.logo_marca = None  # Para imagen opcional
        self.marca_posicion = "bottom_right"  # Puede ser: top_left, top_right, bottom_left, bottom_right
        self.marca_opacidad = 128  # Entre 0 (transparente) y 255 (opaco)
        self.favoritos = set()        # conjunto de rutas favoritas
        self.ver_favoritos = False    # si está activado el filtro de solo favoritos
        self.imagenes_totales = self.imagenes.copy()
        self.root.configure(bg=ESTILO_DARK["bg_main"])
        self.frame_main.config(bg=ESTILO_DARK["bg_main"])
        self.label.config(bg=ESTILO_DARK["bg_main"])
        self.fuente_general = font.Font(family="Segoe UI", size=10)
        self.label.config(bd=5, relief="groove", highlightbackground="gray", highlightthickness=1)


    def cargar_carpeta(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.imagenes = [os.path.join(carpeta, f) for f in os.listdir(carpeta)
                             if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            self.imagenes.sort()
            self.indice = 0
            self.zoom_factor = 1.0
            self.mostrar_imagen()

    def seleccionar_imagenes(self):
        archivos = filedialog.askopenfilenames(filetypes=[
            ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp")
        ])
        if archivos:
            self.imagenes = list(archivos)
            self.indice = 0
            self.zoom_factor = 1.0
            self.mostrar_imagen()

    def mostrar_imagen(self):
        if self.imagenes:
            ruta = self.imagenes[self.indice]
            if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
                messagebox.showerror("Error", f"La imagen no está disponible:\n{ruta}")
                return
            try:
                imagen = Image.open(ruta)
                self.imagen_original = imagen.copy()
                self.imagen_actual = imagen.copy()
                self.zoom = 1.0  # Reinicia zoom al cambiar de imagen
                self.redibujar_imagen()

                # Obtener dimensiones visibles de la ventana
                self.label.update_idletasks()
                contenedor_ancho = self.label.winfo_width()
                contenedor_alto = self.label.winfo_height()

                # Si el tamaño aún no está disponible, establecer uno por defecto
                if contenedor_ancho < 10 or contenedor_alto < 10:
                    contenedor_ancho = 800
                    contenedor_alto = 300

                # Redimensionar proporcionalmente a la ventana
                escala = min(contenedor_ancho / imagen.width, contenedor_alto / imagen.height, 0.9)
                nuevo_ancho = int(imagen.width * escala)
                nuevo_alto = int(imagen.height * escala)
                imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

                self.actualizar_imagen(imagen_redimensionada)
                self.root.title(f"Visor de Fotos - {os.path.basename(ruta)} ({self.indice + 1}/{len(self.imagenes)})")
            except Exception as e:
                messagebox.showerror("Error", f"No se puede abrir la imagen:\n{ruta}\n\n{e}")

    def actualizar_imagen(self, nueva_imagen):
        if self.imagen_actual:
            self.historial_ediciones.append(self.imagen_actual.copy())
        self.imagen_actual = nueva_imagen
        ancho, alto = nueva_imagen.size
        nuevo_tam = (int(ancho * self.zoom_factor), int(alto * self.zoom_factor))
        redimensionada = nueva_imagen.resize(nuevo_tam, Image.LANCZOS)
        foto = ImageTk.PhotoImage(redimensionada)
        self.label.config(image=foto)
        self.label.image = foto

    def siguiente(self):
        if self.imagenes:
            self.indice = (self.indice + 1) % len(self.imagenes)
            self.mostrar_imagen()

    def anterior(self):
        if self.imagenes:
            self.indice = (self.indice - 1) % len(self.imagenes)
            self.mostrar_imagen()

    def zoom_in(self):
        self.zoom_factor *= 1.2
        self.actualizar_imagen(self.imagen_actual)

    def zoom_out(self):
        self.zoom_factor /= 1.2
        self.actualizar_imagen(self.imagen_actual)

    def guardar_copia(self):
        if self.imagen_actual:
            ruta_guardado = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                         filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
            if ruta_guardado:
                from PIL import ImageFont, ImageDraw

                # Asegurar que variables necesarias existen
                texto = getattr(self, 'texto_marca', "© Mi Marca")
                posicion = getattr(self, 'marca_posicion', "bottom_right")
                opacidad = getattr(self, 'marca_opacidad', 128)
                logo = getattr(self, 'logo_marca', None)

                img = self.imagen_actual.copy().convert("RGBA")

                try:
                    font = ImageFont.truetype("arial.ttf", 20)
                except:
                    font = ImageFont.load_default()

                text_size = font.getsize(texto)

                if posicion == "bottom_right":
                    pos = (img.width - text_size[0] - 10, img.height - text_size[1] - 10)
                elif posicion == "bottom_left":
                    pos = (10, img.height - text_size[1] - 10)
                elif posicion == "top_left":
                    pos = (10, 10)
                else:  # top_right
                    pos = (img.width - text_size[0] - 10, 10)

                marca = Image.new("RGBA", img.size, (255, 255, 255, 0))
                draw_marca = ImageDraw.Draw(marca)
                draw_marca.text(pos, texto, fill=(255, 255, 255, opacidad), font=font)

                img = Image.alpha_composite(img, marca)

                # Agregar logo si existe
                if logo:
                    if logo.mode != "RGBA":
                        logo = logo.convert("RGBA")
                    logo = logo.copy()
                    logo.thumbnail((100, 100))
                    logo_pos = {
                        "top_left": (10, 10),
                        "top_right": (img.width - logo.width - 10, 10),
                        "bottom_left": (10, img.height - logo.height - 10),
                        "bottom_right": (img.width - logo.width - 10, img.height - logo.height - 10)
                    }
                    img.paste(logo, logo_pos[posicion], mask=logo)

                img = img.convert("RGB")
                img.save(ruta_guardado)
                messagebox.showinfo("Guardado", "Imagen guardada con marca de agua.")

    def eliminar_imagen(self):
        if self.imagenes:
            ruta = self.imagenes[self.indice]
            confirmacion = messagebox.askyesno("Eliminar", f"¿Eliminar imagen?\n{ruta}")
            if confirmacion:
                try:
                    os.remove(ruta)
                    del self.imagenes[self.indice]
                    if self.indice >= len(self.imagenes):
                        self.indice = 0
                    self.mostrar_imagen()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar la imagen:\n\n{e}")

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def presentacion(self):
        if self.presentando:
            self.presentando = False
            self.btn_auto.config(text="🎞 Presentación")
        else:
            self.presentando = True
            self.btn_auto.config(text="⏹ Detener")
            threading.Thread(target=self.presentar_loop, daemon=True).start()

    def presentar_loop(self):
        while self.presentando and self.imagenes:
            self.siguiente()
            time.sleep(2)

    def ver_mosaico(self):
        if not self.imagenes:
            return
        mosaic = Toplevel(self.root)
        mosaic.title("Mosaico de Imágenes")
        fila = 0
        columna = 0
        for ruta in self.imagenes:
            try:
                img = Image.open(ruta)
                img.thumbnail((150, 150))
                foto = ImageTk.PhotoImage(img)
                lbl = Label(mosaic, image=foto)
                lbl.image = foto
                lbl.grid(row=fila, column=columna, padx=5, pady=5)
                columna += 1
                if columna > 4:
                    columna = 0
                    fila += 1
            except:
                continue

    def ver_exif(self):
        if not self.imagenes:
            return
        ruta = self.imagenes[self.indice]
        try:
            img = Image.open(ruta)
            exif_data = img._getexif()
            if not exif_data:
                messagebox.showinfo("EXIF", "La imagen no contiene metadatos EXIF.")
                return
            texto = ""
            for tag_id, valor in exif_data.items():
                etiqueta = ExifTags.TAGS.get(tag_id, tag_id)
                texto += f"{etiqueta}: {valor}\n"
            top = Toplevel(self.root)
            top.title("Metadatos EXIF")
            lbl = Label(top, text=texto, justify="left", anchor="nw")
            lbl.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("EXIF", f"No se pudieron leer los metadatos:\n{e}")

    def filtro_bn(self):
        if self.imagen_actual:
            img = self.imagen_actual.convert("L").convert("RGB")
            self.actualizar_imagen(img)

    def filtro_sepia(self):
        if self.imagen_actual:
            img = self.imagen_actual.convert("RGB")
            sepia = []
            for r, g, b in img.getdata():
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                sepia.append((min(tr, 255), min(tg, 255), min(tb, 255)))
            img.putdata(sepia)
            self.actualizar_imagen(img)

    def filtro_invertir(self):
        if self.imagen_actual:
            invertida = ImageOps.invert(self.imagen_actual.convert("RGB"))
            self.actualizar_imagen(invertida)

    def ajustar_brillo_contraste(self):
        if not self.imagen_actual:
            return
        top = Toplevel(self.root)
        top.title("Brillo y Contraste")

        def aplicar(val=None):
            brillo = brillo_slider.get() / 100
            contraste = contraste_slider.get() / 100
            img = ImageEnhance.Brightness(self.imagen_actual).enhance(brillo)
            img = ImageEnhance.Contrast(img).enhance(contraste)
            self.actualizar_imagen(img)

        Label(top, text="Brillo").pack()
        brillo_slider = Scale(top, from_=50, to=150, orient=HORIZONTAL, command=aplicar)
        brillo_slider.set(100)
        brillo_slider.pack()

        Label(top, text="Contraste").pack()
        contraste_slider = Scale(top, from_=50, to=150, orient=HORIZONTAL, command=aplicar)
        contraste_slider.set(100)
        contraste_slider.pack()

        Button(top, text="Cerrar", command=top.destroy).pack(pady=10)

    def deshacer_cambios(self):
        if self.historial_ediciones:
            ultima = self.historial_ediciones.pop()
            self.actualizar_imagen(ultima)
    
    def dibujar_imagen(self):
        if not self.imagen_actual:
            return

        top = Toplevel(self.root)
        top.title("Dibujo Libre")
        canvas = Canvas(top, width=self.imagen_actual.width, height=self.imagen_actual.height, bg="white")
        canvas.pack()

        # Convertir imagen a formato compatible con canvas
        self.img_dibujo = self.imagen_actual.copy()
        self.tk_img_dibujo = ImageTk.PhotoImage(self.img_dibujo)
        canvas.create_image(0, 0, anchor="nw", image=self.tk_img_dibujo)

        self.color_dibujo = "red"
        self.grosor = 3
        self.ult_x, self.ult_y = None, None

        def dibujar(event):
            if self.ult_x and self.ult_y:
                canvas.create_line(self.ult_x, self.ult_y, event.x, event.y, fill=self.color_dibujo, width=self.grosor)
                draw.line((self.ult_x, self.ult_y, event.x, event.y), fill=self.color_dibujo, width=self.grosor)
            self.ult_x, self.ult_y = event.x, event.y

        def reset(event):
            self.ult_x, self.ult_y = None, None

        from PIL import ImageDraw
        draw = ImageDraw.Draw(self.img_dibujo)

        canvas.bind("<B1-Motion>", dibujar)
        canvas.bind("<ButtonRelease-1>", reset)

        def guardar():
            self.actualizar_imagen(self.img_dibujo)
            top.destroy()

        Button(top, text="✅ Guardar Cambios", command=guardar).pack(side="left", padx=10)
        Button(top, text="❌ Cancelar", command=top.destroy).pack(side="right", padx=10)

    def insertar_texto(self):
        if not self.imagen_actual:
            return

        top = Toplevel(self.root)
        top.title("Insertar Texto")

        canvas = Canvas(top, width=self.imagen_actual.width, height=self.imagen_actual.height)
        canvas.pack()

        img_temp = self.imagen_actual.copy()
        self.tk_img_texto = ImageTk.PhotoImage(img_temp)
        canvas.create_image(0, 0, anchor="nw", image=self.tk_img_texto)

        from tkinter import Entry, StringVar, colorchooser

        texto_var = StringVar()
        entrada = Entry(top, textvariable=texto_var, width=30)
        entrada.pack()

        color = ["black"]  # Color como lista mutable
        tamano = [20]

        def elegir_color():
            c = colorchooser.askcolor(title="Seleccionar color")[1]
            if c:
                color[0] = c

        def aumentar_tamano():
            tamano[0] += 2

        def reducir_tamano():
            if tamano[0] > 4:
                tamano[0] -= 2

        def click_posicion(event):
            texto = texto_var.get()
            if texto.strip() == "":
                return
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img_temp)

            try:
                font = ImageFont.truetype("arial.ttf", tamano[0])
            except:
                font = ImageFont.load_default()

            draw.text((event.x, event.y), texto, font=font, fill=color[0])
            self.tk_img_texto = ImageTk.PhotoImage(img_temp)
            canvas.create_image(0, 0, anchor="nw", image=self.tk_img_texto)

        canvas.bind("<Button-1>", click_posicion)

        Button(top, text="🎨 Color", command=elegir_color).pack(side="left")
        Button(top, text="🔺 +", command=aumentar_tamano).pack(side="left")
        Button(top, text="🔻 -", command=reducir_tamano).pack(side="left")

        def guardar():
            self.actualizar_imagen(img_temp)
            top.destroy()

        Button(top, text="✅ Guardar Texto", command=guardar).pack(side="left", padx=10)
        Button(top, text="❌ Cancelar", command=top.destroy).pack(side="right", padx=10)

    def recortar_imagen(self):
        if not self.imagen_actual:
            return

        top = Toplevel(self.root)
        top.title("Herramienta de Recorte")

        canvas = Canvas(top, width=self.imagen_actual.width, height=self.imagen_actual.height, cursor="cross")
        canvas.pack()

        img_temp = self.imagen_actual.copy()
        self.tk_img_crop = ImageTk.PhotoImage(img_temp)
        canvas.create_image(0, 0, anchor="nw", image=self.tk_img_crop)

        self.recorte_coords = [None, None, None, None]  # x1, y1, x2, y2
        rect_id = [None]

        def comenzar(event):
            self.recorte_coords[0] = event.x
            self.recorte_coords[1] = event.y
            if rect_id[0]:
                canvas.delete(rect_id[0])
            rect_id[0] = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="red", width=2)

        def arrastrar(event):
            self.recorte_coords[2] = event.x
            self.recorte_coords[3] = event.y
            canvas.coords(rect_id[0], self.recorte_coords[0], self.recorte_coords[1], event.x, event.y)

        canvas.bind("<Button-1>", comenzar)
        canvas.bind("<B1-Motion>", arrastrar)

        def aplicar_recorte():
            x1, y1, x2, y2 = self.recorte_coords
            if None in [x1, y1, x2, y2]:
                return
            box = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
            recortada = img_temp.crop(box)
            self.actualizar_imagen(recortada)
            top.destroy()

        Button(top, text="✅ Aplicar Recorte", command=aplicar_recorte).pack(side="left", padx=10)
        Button(top, text="❌ Cancelar", command=top.destroy).pack(side="right", padx=10)

    def detectar_rostros(self):
        if not self.imagen_actual:
            return

        # Convertir imagen PIL a OpenCV
        img_cv = cv2.cvtColor(np.array(self.imagen_actual), cv2.COLOR_RGB2BGR)
        gris = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # Cargar clasificador de rostros
        cascada = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        rostros = cascada.detectMultiScale(gris, scaleFactor=1.1, minNeighbors=5)

        # Dibujar rectángulos sobre los rostros
        for (x, y, w, h) in rostros:
            cv2.rectangle(img_cv, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Convertir de nuevo a PIL
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        img_detectada = Image.fromarray(img_rgb)

        # Mostrar y guardar
        self.actualizar_imagen(img_detectada)

        messagebox.showinfo("Rostros Detectados", f"Se encontraron {len(rostros)} rostro(s).")

    def cambiar_tema(self):
        self.tema_oscuro = not self.tema_oscuro

        color_fondo = "#1e1e1e" if self.tema_oscuro else "#f0f0f0"
        color_texto = "#ffffff" if self.tema_oscuro else "#000000"
        btn_bg = "#333333" if self.tema_oscuro else "#e0e0e0"

        # Fondo principal
        self.root.configure(bg=color_fondo)
        self.label.configure(bg=color_fondo)

        # Botones (recorre todos los hijos del root)
        for widget in self.root.winfo_children():
            if isinstance(widget, Button):
                widget.configure(bg=btn_bg, fg=color_texto, activebackground=color_fondo, activeforeground=color_texto)
    
    def rotar_izquierda(self):
        if self.imagen_actual:
            rotada = self.imagen_actual.rotate(90, expand=True)
            self.actualizar_imagen(rotada)

    def rotar_derecha(self):
        if self.imagen_actual:
            rotada = self.imagen_actual.rotate(-90, expand=True)
            self.actualizar_imagen(rotada)

    def rotar_180(self):
        if self.imagen_actual:
            rotada = self.imagen_actual.rotate(180, expand=True)
            self.actualizar_imagen(rotada)

    def rotar_libre(self):
        if self.imagen_actual:
            from tkinter.simpledialog import askfloat
            angulo = askfloat("Rotar libre", "Ingresa el ángulo de rotación (°):", minvalue=-360, maxvalue=360)
            if angulo is not None:
                rotada = self.imagen_actual.rotate(-angulo, expand=True)
                self.actualizar_imagen(rotada)
    
    def actualizar_imagen(self, imagen):
        self.imagen_actual = imagen
        foto = ImageTk.PhotoImage(imagen)
        self.label.config(image=foto)
        self.label.image = foto
    
    def capturar_desde_webcam(self):
        import cv2

        cap = cv2.VideoCapture(0)
        cv2.namedWindow("Webcam - Presiona ESPACIO para capturar / ESC para cancelar")

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Webcam - Presiona ESPACIO para capturar / ESC para cancelar", frame)
            key = cv2.waitKey(1)

            if key == 27:  # ESC
                break
            elif key == 32:  # Barra espaciadora
                # Captura y cierra
                cap.release()
                cv2.destroyAllWindows()

                from PIL import Image
                # Convertir imagen de BGR (OpenCV) a RGB (PIL)
                img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(img_rgb)

                self.actualizar_imagen(img_pil)
                return

        cap.release()
        cv2.destroyAllWindows()

    def actualizar_imagen(self, imagen):
        self.imagen_actual = imagen
        foto = ImageTk.PhotoImage(imagen)
        self.label.config(image=foto)
        self.label.image = foto

    def abrir_goma(self):
        if not self.imagen_actual:
            return

        top = Toplevel(self.root)
        top.title("🧹 Herramienta de Borrado")

        canvas = Canvas(top, width=self.imagen_actual.width, height=self.imagen_actual.height, cursor="dot")
        canvas.pack()

        imagen_editable = self.imagen_actual.convert("RGBA").copy()
        self.tk_img_borrar = ImageTk.PhotoImage(imagen_editable)
        canvas.create_image(0, 0, anchor="nw", image=self.tk_img_borrar)

        from PIL import ImageDraw
        draw = ImageDraw.Draw(imagen_editable)

        # Goma: tamaño dinámico
        tamano_goma = [20]
        ultima_pos = [None]

        def borrar(event):
            x, y = event.x, event.y
            r = tamano_goma[0] // 2
            draw.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, 0))  # Borrar con transparencia
            self.tk_img_borrar = ImageTk.PhotoImage(imagen_editable)
            canvas.create_image(0, 0, anchor="nw", image=self.tk_img_borrar)

        def reset(event):
            ultima_pos[0] = None

        def aumentar_goma():
            tamano_goma[0] += 5

        def reducir_goma():
            if tamano_goma[0] > 5:
                tamano_goma[0] -= 5

        canvas.bind("<B1-Motion>", borrar)
        canvas.bind("<ButtonRelease-1>", reset)

        Button(top, text="🔺 Tamaño +", command=aumentar_goma).pack(side="left", padx=5)
        Button(top, text="🔻 Tamaño -", command=reducir_goma).pack(side="left", padx=5)

        def guardar():
            self.actualizar_imagen(imagen_editable.convert("RGB"))  # Convierte de vuelta para ver en visor
            top.destroy()

        Button(top, text="✅ Guardar Cambios", command=guardar).pack(side="left", padx=10)
        Button(top, text="❌ Cancelar", command=top.destroy).pack(side="right", padx=10)

    def comparar_imagenes(self):
        from tkinter import filedialog

        rutas = filedialog.askopenfilenames(title="Selecciona dos imágenes para comparar",
                                            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp *.gif")])

        if len(rutas) != 2:
            messagebox.showwarning("Comparación", "Debes seleccionar exactamente dos imágenes.")
            return

        try:
            img1 = Image.open(rutas[0])
            img2 = Image.open(rutas[1])

            # Ajustar tamaño (máx 400 px de alto)
            max_alto = 400
            factor1 = max_alto / img1.height if img1.height > max_alto else 1
            factor2 = max_alto / img2.height if img2.height > max_alto else 1

            img1 = img1.resize((int(img1.width * factor1), int(img1.height * factor1)), Image.LANCZOS)
            img2 = img2.resize((int(img2.width * factor2), int(img2.height * factor2)), Image.LANCZOS)

            ventana = Toplevel(self.root)
            ventana.title("🧩 Comparación de Imágenes")

            tk_img1 = ImageTk.PhotoImage(img1)
            tk_img2 = ImageTk.PhotoImage(img2)

            lbl1 = Label(ventana, image=tk_img1)
            lbl1.image = tk_img1
            lbl1.pack(side="left", padx=10, pady=10)

            lbl2 = Label(ventana, image=tk_img2)
            lbl2.image = tk_img2
            lbl2.pack(side="left", padx=10, pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron abrir las imágenes.\n\n{e}")
    
    def buscar_duplicados(self):
        if len(self.imagenes) < 2:
            messagebox.showinfo("Duplicados", "Carga al menos dos imágenes para comparar.")
            return

        hashes = {}
        duplicados = []

        for ruta in self.imagenes:
            try:
                with Image.open(ruta) as img:
                    h = imagehash.phash(img)
                    if h in hashes:
                        duplicados.append((ruta, hashes[h]))
                    else:
                        hashes[h] = ruta
            except Exception as e:
                print(f"Error al procesar {ruta}: {e}")

        if not duplicados:
            messagebox.showinfo("Duplicados", "No se encontraron imágenes duplicadas.")
            return

        # Mostrar resultados
        ventana = Toplevel(self.root)
        ventana.title("🕵️ Imágenes Duplicadas Encontradas")

        for idx, (img1, img2) in enumerate(duplicados):
            try:
                im1 = Image.open(img1).resize((150, 150))
                im2 = Image.open(img2).resize((150, 150))
                tk1 = ImageTk.PhotoImage(im1)
                tk2 = ImageTk.PhotoImage(im2)

                lbl1 = Label(ventana, image=tk1)
                lbl1.image = tk1
                lbl1.grid(row=idx, column=0, padx=5, pady=5)

                lbl2 = Label(ventana, image=tk2)
                lbl2.image = tk2
                lbl2.grid(row=idx, column=1, padx=5, pady=5)

                Label(ventana, text="⇄").grid(row=idx, column=2)
            except:
                continue

    def agrupar_por_fecha(self):
        if not self.imagenes:
            messagebox.showinfo("Agrupar por fecha", "No hay imágenes cargadas.")
            return

        from collections import defaultdict
        import datetime

        grupos = defaultdict(list)

        for ruta in self.imagenes:
            try:
                img = Image.open(ruta)
                exif_data = img._getexif()

                fecha_str = "Sin fecha"

                if exif_data:
                    fecha = exif_data.get(36867) or exif_data.get(306)  # DateTimeOriginal o DateTime
                    if fecha:
                        try:
                            fecha_obj = datetime.datetime.strptime(fecha, "%Y:%m:%d %H:%M:%S")
                            fecha_str = fecha_obj.strftime("%Y-%m-%d")
                        except:
                            fecha_str = fecha

                grupos[fecha_str].append(ruta)

            except Exception as e:
                print(f"Error con {ruta}: {e}")
                grupos["Error"].append(ruta)

        # Mostrar agrupados
        ventana = Toplevel(self.root)
        ventana.title("📅 Imágenes agrupadas por fecha")

        fila = 0
        for fecha, rutas in sorted(grupos.items()):
            Label(ventana, text=f"📅 {fecha} ({len(rutas)} imagen/es)", font=("Arial", 12, "bold")).grid(row=fila, column=0, sticky="w", padx=10, pady=5)
            fila += 1

            col = 0
            for ruta in rutas:
                try:
                    img = Image.open(ruta)
                    img.thumbnail((100, 100))
                    tk_img = ImageTk.PhotoImage(img)

                    lbl = Label(ventana, image=tk_img)
                    lbl.image = tk_img
                    lbl.grid(row=fila, column=col, padx=5, pady=5)

                    col += 1
                    if col > 6:
                        col = 0
                        fila += 1
                except:
                    continue
            fila += 1
    
    def crear_gif(self):
        if len(self.imagenes) < 2:
            messagebox.showinfo("GIF", "Debes tener al menos 2 imágenes cargadas para crear un GIF.")
            return

        from tkinter.simpledialog import askinteger
        duracion = askinteger("Duración", "Tiempo entre imágenes (ms):", minvalue=100, maxvalue=5000)
        if not duracion:
            return

        imagenes_gif = []
        for ruta in self.imagenes:
            try:
                img = Image.open(ruta).convert("RGB")
                img = img.resize((500, 500), Image.LANCZOS)  # Tamaño fijo para todas
                imagenes_gif.append(img)
            except Exception as e:
                print(f"Error al procesar {ruta}: {e}")

        if not imagenes_gif:
            messagebox.showerror("GIF", "No se pudieron procesar imágenes para el GIF.")
            return

        archivo = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF", "*.gif")])
        if archivo:
            imagenes_gif[0].save(
                archivo,
                save_all=True,
                append_images=imagenes_gif[1:],
                duration=duracion,
                loop=0
            )
            messagebox.showinfo("GIF", f"GIF guardado correctamente:\n{archivo}")
            
    def desenfoque_selectivo(self):
        if not self.imagen_actual:
            return

        top = Toplevel(self.root)
        top.title("🌀 Desenfoque Selectivo")

        canvas = Canvas(top, width=self.imagen_actual.width, height=self.imagen_actual.height, cursor="cross")
        canvas.pack()

        img_original = self.imagen_actual.copy().convert("RGB")
        tk_img = ImageTk.PhotoImage(img_original)
        canvas.create_image(0, 0, anchor="nw", image=tk_img)

        coords = [None, None, None, None]
        rect_id = [None]

        def comenzar(event):
            coords[0], coords[1] = event.x, event.y
            if rect_id[0]:
                canvas.delete(rect_id[0])
            rect_id[0] = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="red", width=2)

        def arrastrar(event):
            coords[2], coords[3] = event.x, event.y
            canvas.coords(rect_id[0], coords[0], coords[1], coords[2], coords[3])

        canvas.bind("<Button-1>", comenzar)
        canvas.bind("<B1-Motion>", arrastrar)

        def aplicar():
            if None in coords:
                return

            from PIL import ImageFilter

            x1, y1, x2, y2 = map(int, coords)
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)

            desenfocada = img_original.filter(ImageFilter.GaussianBlur(radius=10))
            enfocada = img_original.crop((x1, y1, x2, y2))

            desenfocada.paste(enfocada, (x1, y1))
            self.actualizar_imagen(desenfocada)
            top.destroy()

        Button(top, text="✅ Aplicar Desenfoque", command=aplicar).pack(side="left", padx=10)
        Button(top, text="❌ Cancelar", command=top.destroy).pack(side="right", padx=10)

    def configurar_marca_agua(self):
        top = Toplevel(self.root)
        top.title("💧 Configurar Marca de Agua")

        from tkinter import Entry, StringVar, OptionMenu, filedialog

        Label(top, text="Texto de la marca:").pack()
        texto_var = StringVar(value=self.texto_marca)
        Entry(top, textvariable=texto_var).pack()

        Label(top, text="Posición:").pack()
        opciones = ["top_left", "top_right", "bottom_left", "bottom_right"]
        pos_var = StringVar(value=self.marca_posicion)
        OptionMenu(top, pos_var, *opciones).pack()

        def cargar_logo():
            ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")])
            if ruta:
                self.logo_marca = Image.open(ruta).convert("RGBA")

        Button(top, text="📷 Cargar Logo (opcional)", command=cargar_logo).pack(pady=5)

        def guardar_config():
            self.texto_marca = texto_var.get()
            self.marca_posicion = pos_var.get()
            top.destroy()

        Button(top, text="✅ Aplicar", command=guardar_config).pack(side="left", padx=10)
        Button(top, text="❌ Cancelar", command=top.destroy).pack(side="right", padx=10)
    def toggle_favorito(self):
        if not self.imagen_actual_path:
            return
        if self.imagen_actual_path in self.favoritos:
            self.favoritos.remove(self.imagen_actual_path)
            messagebox.showinfo("Favoritos", "Imagen removida de favoritos.")
        else:
            self.favoritos.add(self.imagen_actual_path)
            messagebox.showinfo("Favoritos", "Imagen añadida a favoritos.")

    def toggle_ver_favoritos(self):
        self.ver_favoritos = not self.ver_favoritos
        self.filtrar_imagenes()

    def filtrar_imagenes(self):
        if self.ver_favoritos:
            self.imagenes = [img for img in self.imagenes_totales if img in self.favoritos]
        else:
            self.imagenes = self.imagenes_totales.copy()
        self.indice_imagen = 0
        if self.imagenes:
            self.mostrar_imagen()
        else:
            messagebox.showinfo("Favoritos", "No hay imágenes favoritas.")
    def guardar_favoritos(self):
        with open("favoritos.json", "w") as f:
            json.dump(list(self.favoritos), f)

    def cargar_favoritos(self):
        if os.path.exists("favoritos.json"):
            with open("favoritos.json", "r") as f:
                self.favoritos = set(json.load(f))
    
    def obtener_coordenadas_gps(self, img_path):
        try:
            from PIL import ExifTags
            img = Image.open(img_path)
            exif = img._getexif()

            if not exif:
                return None

            gps_info = {}
            for tag, value in exif.items():
                key = ExifTags.TAGS.get(tag)
                if key == "GPSInfo":
                    for t in value:
                        sub_tag = ExifTags.GPSTAGS.get(t)
                        gps_info[sub_tag] = value[t]

            if not ("GPSLatitude" in gps_info and "GPSLongitude" in gps_info):
                return None

            def convertir_grados(coord, ref):
                grados = coord[0][0] / coord[0][1]
                minutos = coord[1][0] / coord[1][1]
                segundos = coord[2][0] / coord[2][1]
                decimal = grados + minutos / 60 + segundos / 3600
                if ref in ['S', 'W']:
                    decimal = -decimal
                return decimal

            lat = convertir_grados(gps_info["GPSLatitude"], gps_info["GPSLatitudeRef"])
            lon = convertir_grados(gps_info["GPSLongitude"], gps_info["GPSLongitudeRef"])
            return (lat, lon)
        except Exception as e:
            print("Error al obtener coordenadas:", e)
            return None
        
    def mostrar_en_mapa(self):
        if not self.imagen_actual_path:
            return

        coords = self.obtener_coordenadas_gps(self.imagen_actual_path)
        if coords:
            lat, lon = coords
            import webbrowser
            url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            webbrowser.open(url)
        else:
            messagebox.showinfo("Sin GPS", "La imagen no contiene información GPS.")
    
    def reconstruir_imagen(self):
        if not self.imagen_actual:
            return

        top = Toplevel(self.root)
        top.title("🛠 Reconstrucción de Imagen Dañada")

        canvas = Canvas(top, width=self.imagen_actual.width, height=self.imagen_actual.height, cursor="spraycan")
        canvas.pack()

        original_img = self.imagen_actual.convert("RGB")
        img_cv = cv2.cvtColor(np.array(original_img), cv2.COLOR_RGB2BGR)
        mask = np.zeros(img_cv.shape[:2], dtype=np.uint8)

        tk_img = ImageTk.PhotoImage(original_img)
        canvas.create_image(0, 0, anchor="nw", image=tk_img)

        # Dibujar sobre la máscara
        def pintar(event):
            x, y = event.x, event.y
            r = 10
            cv2.circle(mask, (x, y), r, 255, -1)
            canvas.create_oval(x - r, y - r, x + r, y + r, fill="red", outline="")

        canvas.bind("<B1-Motion>", pintar)

        def aplicar_inpainting():
            restaurada = cv2.inpaint(img_cv, mask, 3, cv2.INPAINT_TELEA)
            restaurada_img = Image.fromarray(cv2.cvtColor(restaurada, cv2.COLOR_BGR2RGB))
            self.actualizar_imagen(restaurada_img)
            top.destroy()

        Button(top, text="✅ Reconstruir", command=aplicar_inpainting).pack(side="left", padx=10)
        Button(top, text="❌ Cancelar", command=top.destroy).pack(side="right", padx=10)
    
    def filtros_instagram(self):
        if not self.imagen_actual:
            return

        from PIL import ImageEnhance, ImageFilter

        top = Toplevel(self.root)
        top.title("🎨 Filtros Estilo Instagram")

        canvas = Canvas(top, width=self.imagen_actual.width, height=self.imagen_actual.height)
        canvas.pack()

        original = self.imagen_actual.copy()
        img = original.copy()
        tk_img = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor="nw", image=tk_img)

        def aplicar_filtro(nombre):
            nonlocal img, tk_img
            img = original.copy()

            if nombre == "Clarendon":
                img = ImageEnhance.Color(img).enhance(1.5)
                img = ImageEnhance.Brightness(img).enhance(1.1)
                img = ImageEnhance.Contrast(img).enhance(1.2)

            elif nombre == "Gingham":
                img = ImageEnhance.Color(img).enhance(0.75)
                img = ImageEnhance.Brightness(img).enhance(1.1)
                img = img.filter(ImageFilter.GaussianBlur(radius=1))

            elif nombre == "Moon":
                img = img.convert("L").convert("RGB")
                img = ImageEnhance.Contrast(img).enhance(1.2)

            elif nombre == "Lark":
                img = ImageEnhance.Color(img).enhance(1.3)
                img = ImageEnhance.Brightness(img).enhance(1.2)

            elif nombre == "Reyes":
                img = ImageEnhance.Color(img).enhance(0.6)
                img = ImageEnhance.Brightness(img).enhance(1.1)

            elif nombre == "Juno":
                img = ImageEnhance.Color(img).enhance(1.4)
                img = ImageEnhance.Contrast(img).enhance(1.2)
            
            elif nombre == "Valencia":
                img = ImageEnhance.Color(img).enhance(1.2)
                img = ImageEnhance.Brightness(img).enhance(1.1)
                img = ImageEnhance.Contrast(img).enhance(0.9)
            elif nombre == "X-Pro II":
                img = ImageEnhance.Contrast(img).enhance(1.5)
                img = ImageEnhance.Color(img).enhance(1.3)
                img = img.filter(ImageFilter.GaussianBlur(radius=1))
            elif nombre == "Sierra":
                img = ImageEnhance.Color(img).enhance(1.1)
                img = ImageEnhance.Brightness(img).enhance(1.05)
                img = img.filter(ImageFilter.SMOOTH)
            elif nombre == "Lo-fi":
                img = ImageEnhance.Color(img).enhance(1.6)
                img = ImageEnhance.Contrast(img).enhance(1.3)
                img = ImageEnhance.Brightness(img).enhance(0.9)
            elif nombre == "Nashville":
                overlay = Image.new("RGB", img.size, (247, 176, 153))
                img = Image.blend(img, overlay, 0.2)
                img = ImageEnhance.Contrast(img).enhance(1.1)
            elif nombre == "Earlybird":
                img = ImageEnhance.Color(img).enhance(0.8)
                img = ImageEnhance.Brightness(img).enhance(1.1)
                overlay = Image.new("RGB", img.size, (255, 165, 102))
                img = Image.blend(img, overlay, 0.1)
            elif nombre == "Toaster":
                overlay = Image.new("RGB", img.size, (255, 145, 0))
                img = Image.blend(img, overlay, 0.2)
                img = ImageEnhance.Contrast(img).enhance(1.4)
            elif nombre == "1977":
                overlay = Image.new("RGB", img.size, (243, 106, 188))
                img = Image.blend(img, overlay, 0.2)
                img = ImageEnhance.Brightness(img).enhance(1.1)
            elif nombre == "Hudson":
                img = ImageEnhance.Color(img).enhance(1.1)
                img = ImageEnhance.Contrast(img).enhance(1.2)
                overlay = Image.new("RGB", img.size, (100, 150, 255))
                img = Image.blend(img, overlay, 0.1)
            elif nombre == "Hefe":
                img = ImageEnhance.Contrast(img).enhance(1.3)
                img = ImageEnhance.Color(img).enhance(1.3)
                img = ImageEnhance.Brightness(img).enhance(0.95)
            elif nombre == "Brannan":
                img = img.convert("L").convert("RGB")
                img = ImageEnhance.Contrast(img).enhance(1.4)
            elif nombre == "Kelvin":
                overlay = Image.new("RGB", img.size, (255, 240, 120))
                img = Image.blend(img, overlay, 0.3)
            elif nombre == "Inkwell":
                img = img.convert("L").convert("RGB")
            elif nombre == "Walden":
                overlay = Image.new("RGB", img.size, (255, 255, 204))
                img = Image.blend(img, overlay, 0.2)
            elif nombre == "Bleach":
                img = ImageEnhance.Color(img).enhance(0.3)
                img = ImageEnhance.Contrast(img).enhance(1.5)

            elif nombre == "Sepia":
                sepia = Image.new("RGB", img.size)
                pixels = img.load()
                for y in range(img.height):
                    for x in range(img.width):
                        r, g, b = pixels[x, y]
                        tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                        tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                        tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                        sepia.putpixel((x, y), (min(tr, 255), min(tg, 255), min(tb, 255)))
                img = sepia

            elif nombre == "Drama":
                img = img.filter(ImageFilter.DETAIL)
                img = ImageEnhance.Contrast(img).enhance(1.8)

            elif nombre == "Cool":
                overlay = Image.new("RGB", img.size, (180, 220, 255))
                img = Image.blend(img, overlay, 0.15)

            elif nombre == "Warm":
                overlay = Image.new("RGB", img.size, (255, 220, 180))
                img = Image.blend(img, overlay, 0.15)

            elif nombre == "Glow":
                blur = img.filter(ImageFilter.GaussianBlur(2))
                img = Image.blend(img, blur, 0.4)

            elif nombre == "Matte":
                img = ImageEnhance.Contrast(img).enhance(0.8)
                img = ImageEnhance.Brightness(img).enhance(1.1)

            elif nombre == "Vintage Blue":
                overlay = Image.new("RGB", img.size, (180, 210, 255))
                img = Image.blend(img, overlay, 0.2)
                img = ImageEnhance.Color(img).enhance(0.7)

            elif nombre == "Cinema":
                blue_overlay = Image.new("RGB", img.size, (100, 140, 255))
                img = Image.blend(img, blue_overlay, 0.2)
                img = ImageEnhance.Contrast(img).enhance(1.2)

            elif nombre == "Duotone":
                img = img.convert("L")
                img = ImageOps.colorize(img, "#5f2c82", "#49a09d")

            tk_img = ImageTk.PhotoImage(img)
            canvas.create_image(0, 0, anchor="nw", image=tk_img)

        # Botones de filtro
        filtros = [
                    "Clarendon", "Gingham", "Moon", "Lark", "Reyes", "Juno",
                    "Valencia", "X-Pro II", "Sierra", "Lo-fi", "Nashville",
                    "Earlybird", "Toaster", "1977", "Hudson", "Hefe", "Brannan",
                    "Kelvin", "Inkwell", "Walden", "Bleach", "Sepia", "Drama",
                    "Cool", "Warm", "Glow", "Matte", "Vintage Blue", "Cinema", "Duotone"
                ]
        for nombre in filtros:
            Button(top, text=nombre, command=lambda n=nombre: aplicar_filtro(n)).pack(side="left", padx=2)

        def aplicar():
            self.actualizar_imagen(img)
            top.destroy()

        Button(top, text="✅ Aplicar", command=aplicar).pack(side="left", padx=10)
        Button(top, text="❌ Cancelar", command=top.destroy).pack(side="right", padx=10)

    def abrir_clonador(self):
        if not self.imagen_actual:
            return

        top = Toplevel(self.root)
        top.title("🖌️ Herramienta de Clonación")

        canvas = Canvas(top, width=self.imagen_actual.width, height=self.imagen_actual.height, cursor="tcross")
        canvas.pack()

        imagen_editable = self.imagen_actual.convert("RGBA").copy()
        self.tk_img_clon = ImageTk.PhotoImage(imagen_editable)
        canvas.create_image(0, 0, anchor="nw", image=self.tk_img_clon)

        from PIL import ImageDraw
        draw = ImageDraw.Draw(imagen_editable)

        punto_origen = [None]
        tamano_pincel = [20]

        def definir_origen(event):
            punto_origen[0] = (event.x, event.y)
            canvas.create_oval(event.x - 4, event.y - 4, event.x + 4, event.y + 4, outline="green", width=2)

        def clonar(event):
            if punto_origen[0] is None:
                return

            ox, oy = punto_origen[0]
            dx, dy = event.x, event.y
            offset_x = dx - ox
            offset_y = dy - oy

            # Define la zona de origen y destino
            r = tamano_pincel[0] // 2
            src_box = (ox - r, oy - r, ox + r, oy + r)
            dst_pos = (dx - r, dy - r)

            try:
                zona = imagen_editable.crop(src_box)
                imagen_editable.paste(zona, dst_pos)
                self.tk_img_clon = ImageTk.PhotoImage(imagen_editable)
                canvas.create_image(0, 0, anchor="nw", image=self.tk_img_clon)
            except:
                pass

        def aumentar():
            tamano_pincel[0] += 5

        def reducir():
            if tamano_pincel[0] > 5:
                tamano_pincel[0] -= 5

        canvas.bind("<Button-1>", definir_origen)
        canvas.bind("<B1-Motion>", clonar)

        Button(top, text="🔺 Tamaño +", command=aumentar).pack(side="left", padx=5)
        Button(top, text="🔻 Tamaño -", command=reducir).pack(side="left", padx=5)

        def guardar():
            self.actualizar_imagen(imagen_editable.convert("RGB"))
            top.destroy()

        Button(top, text="✅ Guardar", command=guardar).pack(side="left", padx=10)
        Button(top, text="❌ Cancelar", command=top.destroy).pack(side="right", padx=10)
    
    def aplicar_estilo_artistico(self):
        if not self.imagen_actual:
            return

        import torch
        from torchvision import transforms, models
        from PIL import Image
        from tkinter import filedialog, messagebox

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        def cargar_img(path, max_size=400):
            image = Image.open(path).convert("RGB")
            if max(image.size) > max_size:
                size = max_size
            else:
                size = max(image.size)
            in_transform = transforms.Compose([
                transforms.Resize(size),
                transforms.ToTensor(),
                transforms.Lambda(lambda x: x[:3, :, :]),  # por si tiene canal alpha
                transforms.Normalize((0.485, 0.456, 0.406),
                                    (0.229, 0.224, 0.225))])
            image = in_transform(image)[:3, :, :].unsqueeze(0)
            return image.to(device)

        def imagen_tens_a_pil(tensor):
            image = tensor.to("cpu").clone().detach()
            image = image.squeeze(0)
            image = image * torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
            image = image + torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
            image = image.clamp(0, 1)
            image = transforms.ToPILImage()(image)
            return image

        # Elegir imagen de estilo
        path_estilo = filedialog.askopenfilename(title="Selecciona imagen de estilo (cuadro artístico)",
                                             filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if not path_estilo:
            return 

        content = self.imagen_actual
        content.save("_temp_content.jpg")
        content_tensor = cargar_img("_temp_content.jpg")
        style_tensor = cargar_img(path_estilo)

        # Modelo preentrenado
        vgg = models.vgg19(pretrained=True).features.to(device).eval()

        # Usamos solo estas capas
        capas = {'0': 'conv1_1',
                '5': 'conv2_1',
                '10': 'conv3_1',
                '19': 'conv4_1',
                '21': 'conv4_2',  # contenido
                '28': 'conv5_1'}

        def obtener_caracteristicas(imagen, modelo):
            features = {}
            x = imagen
            for name, layer in modelo._modules.items():
                x = layer(x)
                if name in capas:
                    features[capas[name]] = x
            return features

        def gram_matrix(tensor):
            b, c, h, w = tensor.size()
            tensor = tensor.view(c, h * w)
            G = torch.mm(tensor, tensor.t())
            return G / (c * h * w)

        content_features = obtener_caracteristicas(content_tensor, vgg)
        style_features = obtener_caracteristicas(style_tensor, vgg)
        style_grams = {layer: gram_matrix(style_features[layer]) for layer in style_features}

        target = content_tensor.clone().requires_grad_(True).to(device)

        optim = torch.optim.Adam([target], lr=0.003)
        pasos = 300

        for i in range(pasos):
            target_features = obtener_caracteristicas(target, vgg)

            content_loss = torch.mean((target_features['conv4_2'] - content_features['conv4_2']) ** 2)

            style_loss = 0
            for layer in style_grams:
                target_feature = target_features[layer]
                target_gram = gram_matrix(target_feature)
                style_gram = style_grams[layer]
                layer_loss = torch.mean((target_gram - style_gram) ** 2)
                style_loss += layer_loss

            total_loss = content_loss + style_loss * 1e5
            optim.zero_grad()
            total_loss.backward()
            optim.step()

            salida = imagen_tens_a_pil(target)
            self.actualizar_imagen(salida)
            messagebox.showinfo("Estilo aplicado", "🎨 Estilo artístico aplicado correctamente.")

    def buscar_imagenes(self):
        query = self.buscador_var.get().lower().strip()
        if not query:
            messagebox.showinfo("Búsqueda", "Ingresa un texto para buscar.")
            return

        resultado = []
        for ruta in self.imagenes_totales:
            nombre = os.path.basename(ruta).lower()
            if query in nombre:
                resultado.append(ruta)
                continue

            try:
                img = Image.open(ruta)
                exif = img._getexif()

                if exif:
                    fecha = exif.get(36867) or exif.get(306)
                    if fecha and query in fecha.lower():
                        resultado.append(ruta)
                        continue

                    gps = exif.get(34853)
                    if gps and query in str(gps):
                            resultado.append(ruta)
            except:
                    continue

        if resultado:
            self.imagenes = resultado
            self.indice = 0
            self.mostrar_imagen()
            messagebox.showinfo("Resultado", f"Se encontraron {len(resultado)} coincidencia(s).")
        else:
            messagebox.showinfo("Sin resultados", "No se encontraron imágenes que coincidan.")

    def restaurar_todas(self):
        self.imagenes = self.imagenes_totales.copy()
        self.indice = 0
        self.mostrar_imagen()

    def comparar_con_slider(self):
        if not self.imagen_actual or not self.imagen_original:
            messagebox.showinfo("Comparación", "No hay edición activa para comparar.")
            return

        from PIL import ImageTk
        comp_win = Toplevel(self.root)
        comp_win.title("🕶️ Comparación Antes / Después")
    
        ancho, alto = self.imagen_actual.size
        canvas = Canvas(comp_win, width=ancho, height=alto)
        canvas.pack()

        # Convertir imágenes a PhotoImage
        original = self.imagen_original.copy()
        editada = self.imagen_actual.copy()
        self.tk_original = ImageTk.PhotoImage(original)
        self.tk_editada = ImageTk.PhotoImage(editada)

        # Fondo: editada completa
        canvas.create_image(0, 0, anchor="nw", image=self.tk_editada)

        # Superposición: parte visible de la original
        recorte = original.crop((0, 0, ancho // 2, alto))
        self.tk_corte = ImageTk.PhotoImage(recorte)
        self.overlay_id = canvas.create_image(0, 0, anchor="nw", image=self.tk_corte)

        # Slider para ajustar
        def mover(val):
            x = int(val)
            recorte = original.crop((0, 0, x, alto))
            self.tk_corte = ImageTk.PhotoImage(recorte)
            canvas.itemconfig(self.overlay_id, image=self.tk_corte)

        slider = Scale(comp_win, from_=0, to=ancho, orient="horizontal", length=ancho, command=mover)
        slider.set(ancho // 2)
        slider.pack()

    def subir_a_drive(self):
        if not self.imagen_actual_path:
            messagebox.showinfo("Google Drive", "No hay imagen cargada.")
            return

        try:
            from pydrive.auth import GoogleAuth
            from pydrive.drive import GoogleDrive

            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()  # Abre navegador para autenticar una vez

            drive = GoogleDrive(gauth)

            nombre_archivo = os.path.basename(self.imagen_actual_path)
            archivo = drive.CreateFile({'title': nombre_archivo})
            archivo.SetContentFile(self.imagen_actual_path)
            archivo.Upload()

            link = archivo['alternateLink']
            messagebox.showinfo("Subida Exitosa", f"Imagen subida a Google Drive:\n{link}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo subir la imagen:\n{e}")
    
    def mostrar_filtros_20(self):
        if not self.imagen_actual:
            return

        from PIL import ImageEnhance, ImageFilter, ImageOps

        top = Toplevel(self.root)
        top.title("🧪 Filtros Estéticos (20)")
        canvas = Canvas(top, width=self.imagen_actual.width, height=self.imagen_actual.height)
        canvas.pack()

        original = self.imagen_actual.copy()
        img = original.copy()
        tk_img = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor="nw", image=tk_img)

        def aplicar_filtro(nombre):
            nonlocal img, tk_img
            img = original.copy()

            try:
                if nombre == "BN":  # Blanco y negro
                    img = img.convert("L").convert("RGB")
                elif nombre == "Sepia":
                    sepia = [(int(0.393*r + 0.769*g + 0.189*b),
                                int(0.349*r + 0.686*g + 0.168*b),
                                int(0.272*r + 0.534*g + 0.131*b)) for (r, g, b) in img.getdata()]
                    img.putdata([tuple(map(lambda x: min(255, x), p)) for p in sepia])
                elif nombre == "Invertir":
                    img = ImageOps.invert(img.convert("RGB"))
                elif nombre == "Clarendon":
                    img = ImageEnhance.Color(img).enhance(1.5)
                elif nombre == "Moon":
                    img = img.convert("L").convert("RGB")
                    img = ImageEnhance.Contrast(img).enhance(1.2)
                elif nombre == "Desenfoque":
                    img = img.filter(ImageFilter.GaussianBlur(radius=2))
                elif nombre == "Pastel":
                    overlay = Image.new("RGB", img.size, (255, 228, 225))
                    img = Image.blend(img, overlay, 0.2)
                elif nombre == "Térmico":
                    img = ImageOps.colorize(img.convert("L"), black="blue", white="red")
                elif nombre == "Brillante":
                    img = ImageEnhance.Brightness(img).enhance(1.3)
                elif nombre == "Oscuro":
                    img = ImageEnhance.Brightness(img).enhance(0.7)
                elif nombre == "Contraste+":
                    img = ImageEnhance.Contrast(img).enhance(1.5)
                elif nombre == "Contraste-":
                    img = ImageEnhance.Contrast(img).enhance(0.7)
                elif nombre == "Color+":
                    img = ImageEnhance.Color(img).enhance(1.5)
                elif nombre == "Color-":
                    img = ImageEnhance.Color(img).enhance(0.5)
                elif nombre == "Espejo":
                    img = ImageOps.mirror(img)
                elif nombre == "Solarizar":
                    img = ImageOps.solarize(img, threshold=128)
                elif nombre == "Emboss":
                    img = img.filter(ImageFilter.EMBOSS)
                elif nombre == "Dibujo":
                    img = img.convert("L").filter(ImageFilter.CONTOUR)
                elif nombre == "Borde":
                    img = img.filter(ImageFilter.FIND_EDGES)
                elif nombre == "Pixelado":
                    small = img.resize((img.width//10, img.height//10), resample=Image.NEAREST)
                    img = small.resize(img.size, Image.NEAREST)

                tk_img = ImageTk.PhotoImage(img)
                canvas.create_image(0, 0, anchor="nw", image=tk_img)

            except Exception as e:
                messagebox.showerror("Filtro", f"Error aplicando {nombre}:\n{e}")

        filtros = [
            "BN", "Sepia", "Invertir", "Clarendon", "Moon",
            "Desenfoque", "Pastel", "Térmico", "Brillante", "Oscuro",
            "Contraste+", "Contraste-", "Color+", "Color-",
            "Espejo", "Solarizar", "Emboss", "Dibujo", "Borde", "Pixelado"
        ]

        marco = Canvas(top)
        marco.pack()
        for f in filtros:
            Button(marco, text=f, width=10, command=lambda n=f: aplicar_filtro(n)).pack(side="left", padx=2)

        def aplicar():
            self.actualizar_imagen(img)
            top.destroy()

        Button(top, text="✅ Aplicar", command=aplicar).pack(side="left", padx=10)
        Button(top, text="❌ Cancelar", command=top.destroy).pack(side="right", padx=10)


    def redibujar_imagen(self):
        if not self.imagen_original:
            return

        self.label.update_idletasks()
        contenedor_ancho = self.label.winfo_width()
        contenedor_alto = self.label.winfo_height()

        if contenedor_ancho < 50 or contenedor_alto < 50:
            contenedor_ancho, contenedor_alto = 800, 600

        img = self.imagen_original.copy()
        nuevo_ancho = int(img.width * self.zoom)
        nuevo_alto = int(img.height * self.zoom)

        if nuevo_ancho > contenedor_ancho or nuevo_alto > contenedor_alto:
            escala = min(contenedor_ancho / nuevo_ancho, contenedor_alto / nuevo_alto, 1.0)
            nuevo_ancho = int(nuevo_ancho * escala)
            nuevo_alto = int(nuevo_alto * escala)

        img = img.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
        foto = ImageTk.PhotoImage(img)
        self.label.config(image=foto)
        self.label.image = foto

    def menu_compartir(self):
        if not self.imagen_actual:
            messagebox.showinfo("Compartir", "No hay imagen cargada.")
            return

        top = Toplevel(self.root)
        top.title("📤 Compartir Imagen")
        top.geometry("300x200")

        Button(top, text="📧 Por Correo", command=self.compartir_por_correo).pack(fill="x", pady=5, padx=20)
        Button(top, text="💬 WhatsApp Web", command=self.compartir_por_whatsapp).pack(fill="x", pady=5, padx=20)
        Button(top, text="🌐 Facebook", command=self.compartir_en_facebook).pack(fill="x", pady=5, padx=20)
        Button(top, text="🐦 Twitter / X", command=self.compartir_en_twitter).pack(fill="x", pady=5, padx=20)

    def compartir_por_correo(self):
        import webbrowser
        if not hasattr(self, 'imagen_actual_path') or not self.imagen_actual_path:
            messagebox.showinfo("Correo", "No hay imagen seleccionada.")
            return

        asunto = "Mira esta imagen"
        cuerpo = "Te comparto esta imagen desde mi visor de fotos."
        webbrowser.open(f"mailto:?subject={asunto}&body={cuerpo}")

    def compartir_por_whatsapp(self):
        import webbrowser
        mensaje = "Mira esta imagen que edité con el visor de fotos."
        mensaje_url = mensaje.replace(" ", "%20")
        webbrowser.open(f"https://web.whatsapp.com/send?text={mensaje_url}")
    
    def compartir_en_facebook(self):
        import webbrowser
        mensaje = "Mira esta imagen editada en mi visor de fotos."
        mensaje_url = mensaje.replace(" ", "%20")
        webbrowser.open(f"https://www.facebook.com/sharer/sharer.php?u=&quote={mensaje_url}")

    def compartir_en_twitter(self):
        import webbrowser
        mensaje = "Edité esta imagen con mi visor de fotos avanzado. #Python"
        mensaje_url = mensaje.replace(" ", "%20")
        webbrowser.open(f"https://twitter.com/intent/tweet?text={mensaje_url}")

    def reconstruccion_esrgan(self):
        import os, uuid, subprocess
        from PIL import Image

        if not self.imagen_actual:
            messagebox.showinfo("ESRGAN", "No hay imagen cargada.")
            return

        temp_id = uuid.uuid4().hex[:8]
        input_path = f"temp_esrgan_{temp_id}.jpg"
        output_dir = "salida_esrgan"
        os.makedirs(output_dir, exist_ok=True)
        self.imagen_actual.save(input_path)

        # Ejecuta Real-ESRGAN desde carpeta local
        comando = [
            "python", "Real-ESRGAN/inference_realesrgan.py",
            "-n", "RealESRGAN_x4plus",
            "-i", input_path,
            "-o", output_dir,
            "--model_path", "weights/RealESRGAN_x4plus.pth"
        ]

        try:
            subprocess.run(comando, check=True)

            nombre_out = os.path.splitext(os.path.basename(input_path))[0] + "_out.jpg"
            output_path = os.path.join(output_dir, nombre_out)

            if os.path.exists(output_path):
                imagen = Image.open(output_path)
                self.actualizar_imagen(imagen)
                messagebox.showinfo("Real-ESRGAN", "✅ Imagen mejorada con éxito.")
            else:
                messagebox.showerror("Real-ESRGAN", "No se generó la imagen de salida.")
            os.remove(input_path)
        except Exception as e:
            messagebox.showerror("Real-ESRGAN", f"Error al ejecutar Real-ESRGAN:\n{e}")
    
    def restaurar_rostros_gfpgan(self):
        import subprocess, os, uuid
        from PIL import Image

        if not self.imagen_actual:
            messagebox.showinfo("GFPGAN", "No hay imagen cargada.")
            return

        temp_id = uuid.uuid4().hex[:8]
        input_path = f"temp_in_{temp_id}.jpg"
        output_dir = "salida_gfpgan"
        os.makedirs(output_dir, exist_ok=True)
        self.imagen_actual.save(input_path)

        # Ajuste personalizado para cargar modelo desde carpeta weights
        comando = [
            "python", "GFPGAN/inference_gfpgan.py",
            "-i", input_path,
            "-o", output_dir,
            "-v", "1.3",
            "--model_path", "weights/GFPGANv1.3.pth"  # Aquí le dices dónde está
        ]

        try:
            subprocess.run(comando, check=True)

            output_img = os.path.join(output_dir, os.path.basename(input_path).replace(".jpg", ".png"))
            if os.path.exists(output_img):
                imagen_resultado = Image.open(output_img)
                self.actualizar_imagen(imagen_resultado)
                messagebox.showinfo("GFPGAN", "✅ Rostros restaurados con éxito.")
            else:
                messagebox.showerror("GFPGAN", "No se generó la imagen de salida.")

            os.remove(input_path)
        except Exception as e:
            messagebox.showerror("GFPGAN", f"Error ejecutando GFPGAN:\n{e}")
    
    def buscar_inversa_google(self):
        if not self.imagen_actual:
            messagebox.showinfo("Búsqueda inversa", "No hay imagen cargada.")
            return

        import webbrowser
        webbrowser.open("https://images.google.com")
        messagebox.showinfo("Búsqueda inversa", "📂 Arrastra la imagen a la barra de búsqueda de Google Images.")

    def mostrar_mapa_con_gps(self):
        if not self.imagenes:
            messagebox.showinfo("Mapa GPS", "No hay imágenes cargadas.")
            return

        import folium
        from PIL import ExifTags
        import webbrowser
        import base64
        from io import BytesIO

        puntos = []

        for ruta in self.imagenes:
            try:
                img = Image.open(ruta)
                exif = img._getexif()
                if not exif:
                    continue
                gps_data = {}
                for tag, value in exif.items():
                    key = ExifTags.TAGS.get(tag)
                    if key == "GPSInfo":
                        for t in value:
                            sub_tag = ExifTags.GPSTAGS.get(t)
                            gps_data[sub_tag] = value[t]

                if "GPSLatitude" in gps_data and "GPSLongitude" in gps_data:
                    def convertir_grados(coord, ref):
                        grados = coord[0][0] / coord[0][1]
                        minutos = coord[1][0] / coord[1][1]
                        segundos = coord[2][0] / coord[2][1]
                        decimal = grados + minutos / 60 + segundos / 3600
                        if ref in ['S', 'W']:
                            decimal = -decimal
                        return decimal

                    lat = convertir_grados(gps_data["GPSLatitude"], gps_data["GPSLatitudeRef"])
                    lon = convertir_grados(gps_data["GPSLongitude"], gps_data["GPSLongitudeRef"])

                    # Convertir imagen a base64 (miniatura)
                    mini = img.copy()
                    mini.thumbnail((100, 100))
                    buffer = BytesIO()
                    mini.save(buffer, format="JPEG")
                    img_b64 = base64.b64encode(buffer.getvalue()).decode()
                    html = f'<img src="data:image/jpeg;base64,{img_b64}"><br><b>{os.path.basename(ruta)}</b>'

                    puntos.append((lat, lon, html))
            except:
                continue

        if not puntos:
            messagebox.showinfo("GPS", "No se encontraron imágenes con coordenadas GPS.")
            return

        # Crear mapa centrado en el primer punto
        mapa = folium.Map(location=[puntos[0][0], puntos[0][1]], zoom_start=5)

        for lat, lon, popup in puntos:
            folium.Marker(location=[lat, lon], popup=folium.Popup(popup, max_width=200)).add_to(mapa)

        mapa_path = "mapa_gps.html"
        mapa.save(mapa_path)
        webbrowser.open(mapa_path)
    
    def generar_meme(self):
        if not self.imagen_actual:
            messagebox.showinfo("Generador de Memes", "No hay imagen cargada.")
            return

        from PIL import ImageDraw, ImageFont

        top = Toplevel(self.root)
        top.title("🤣 Generador de Memes")

        Label(top, text="Texto superior:").pack()
        entrada_arriba = Entry(top, width=50)
        entrada_arriba.pack()

        Label(top, text="Texto inferior:").pack()
        entrada_abajo = Entry(top, width=50)
        entrada_abajo.pack()

        canvas = Canvas(top, width=self.imagen_actual.width, height=self.imagen_actual.height)
        canvas.pack()

        meme_img = self.imagen_actual.copy()
        tk_meme = ImageTk.PhotoImage(meme_img)
        canvas_img_id = canvas.create_image(0, 0, anchor="nw", image=tk_meme)

        def aplicar_texto():
            nonlocal meme_img, tk_meme
            meme_img = self.imagen_actual.copy()
            draw = ImageDraw.Draw(meme_img)

            try:
                font = ImageFont.truetype("impact.ttf", size=int(meme_img.height * 0.07))
            except:
                font = ImageFont.truetype("arialbd.ttf", size=int(meme_img.height * 0.07))

            texto_arriba = entrada_arriba.get().upper()
            texto_abajo = entrada_abajo.get().upper()

            def dibujar_texto(texto, y_pos):
                w, h = draw.textsize(texto, font=font)
                x = (meme_img.width - w) / 2
                draw.text((x - 2, y_pos - 2), texto, font=font, fill="black")
                draw.text((x + 2, y_pos - 2), texto, font=font, fill="black")
                draw.text((x - 2, y_pos + 2), texto, font=font, fill="black")
                draw.text((x + 2, y_pos + 2), texto, font=font, fill="black")
                draw.text((x, y_pos), texto, font=font, fill="white")

            if texto_arriba:
                dibujar_texto(texto_arriba, 10)
            if texto_abajo:
                dibujar_texto(texto_abajo, meme_img.height - int(meme_img.height * 0.1))

            tk_meme = ImageTk.PhotoImage(meme_img)
            canvas.itemconfig(canvas_img_id, image=tk_meme)
            canvas.image = tk_meme

        def guardar_meme():
            ruta = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
            if ruta:
                meme_img.save(ruta)
                messagebox.showinfo("Guardado", f"Meme guardado en:\n{ruta}")

        Button(top, text="🔤 Aplicar Texto", command=aplicar_texto).pack(pady=5)
        Button(top, text="💾 Guardar Meme", command=guardar_meme).pack()
        Button(top, text="❌ Cerrar", command=top.destroy).pack(pady=5)

    def crear_collage(self):
        ventana = Toplevel()
        ventana.title("Selecciona el tipo de collage")
        ventana.geometry("250x300")
        ventana.resizable(False, False)

        Label(ventana, text="Selecciona un formato:", font=("Arial", 12, "bold")).pack(pady=10)

        formatos = [
            ("2 x 2", 2, 2),
            ("2 x 3", 2, 3),
            ("2 x 4", 2, 4),
            ("3 x 3", 3, 3),
            ("4 x 4", 4, 4),
            ("4 x 5", 4, 5),
        ]

        for texto, cols, rows in formatos:
            Button(
                ventana, 
                text=f"🧱 Collage {texto}",
                width=20,
                command=lambda c=cols, r=rows, win=ventana: [win.destroy(), self.abrir_interfaz_collage(c, r)]
            ).pack(pady=5)

    def abrir_interfaz_collage(self, columnas, filas):
        from PIL import ImageTk

        self.cuadros_collage = []
        self.imagenes_collage = [[None for _ in range(columnas)] for _ in range(filas)]

        win = Toplevel()
        win.title(f"Collage {columnas}x{filas}")
        win.geometry(f"{columnas*160}x{filas*160 + 60}")
        win.resizable(False, False)

        frame = Frame(win)
        frame.pack()

        def seleccionar_imagen(f, c, boton):
            ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif")])
            if ruta:
                self.imagenes_collage[f][c] = ruta
            try:
                img = Image.open(ruta)
                img.thumbnail((100, 100))  # Tamaño de miniatura más grande
                foto = ImageTk.PhotoImage(img)
                boton.config(image=foto, text="", compound="center")
                boton.image = foto  # Guardar referencia para evitar que se borre

                # Mostrar vista previa en ventana emergente
                def ver_grande():
                    vista = Toplevel()
                    vista.title("Vista previa")
                    img_grande = Image.open(ruta)
                    img_grande.thumbnail((600, 600))
                    img_tk = ImageTk.PhotoImage(img_grande)
                    Label(vista, image=img_tk).pack()
                    vista.img = img_tk  # mantener referencia

                # También abrir vista previa al seleccionar
                ver_grande()

            except Exception as e:
                print(f"Error al cargar imagen: {e}")

        # Crear los cuadros de selección
        for f in range(filas):
            fila_botones = []
            for c in range(columnas):
                btn = Button(frame, text="🆕", width=12, height=6)
                btn.grid(row=f, column=c, padx=5, pady=5)
                btn.config(command=lambda fila=f, col=c, b=btn: seleccionar_imagen(fila, col, b))
                fila_botones.append(btn)
            self.cuadros_collage.append(fila_botones)

        # Botón para generar el collage
        def generar():
            rutas = [ruta for fila in self.imagenes_collage for ruta in fila if ruta]
            total = columnas * filas
            if len(rutas) != total:
                messagebox.showwarning("Faltan imágenes", f"Debes seleccionar {total} imágenes.")
                return
            win.destroy()
            self.generar_collage_visual(columnas, filas, self.imagenes_collage)

        Button(win, text="🎨 Generar Collage", command=generar).pack(pady=10)
    
    def agregar_sticker_png(self):
        from tkinter import Toplevel, Canvas, Button, OptionMenu, StringVar, messagebox
        import os
        from PIL import Image, ImageTk

        if not self.imagen_actual:
            return

        top = Toplevel(self.root)
        top.title("🖼️ Añadir Sticker PNG")

        canvas = Canvas(top, width=self.imagen_actual.width, height=self.imagen_actual.height, cursor="hand2")
        canvas.pack()

        base = self.imagen_actual.copy().convert("RGBA")
        self.tk_img_base = ImageTk.PhotoImage(base)
        canvas.create_image(0, 0, anchor="nw", image=self.tk_img_base)

        sticker_dir = "stickers"
        if not os.path.exists(sticker_dir):
            messagebox.showerror("Error", "No se encontró la carpeta 'stickers/'.")
            return

        archivos = [f for f in os.listdir(sticker_dir) if f.endswith(".png")]
        if not archivos:
            messagebox.showerror("Error", "No hay stickers PNG en la carpeta 'stickers/'.")
            return

        sticker_var = StringVar(value=archivos[0])
        OptionMenu(top, sticker_var, *archivos).pack()

        size = [100]
        pos = [100, 100]
        sticker_img = [None]
        sticker_tk = [None]
        sticker_id = [None]

        def cargar_y_mostrar():
            ruta = os.path.join(sticker_dir, sticker_var.get())
            img = Image.open(ruta).convert("RGBA").resize((size[0], size[0]), Image.LANCZOS)
            sticker_img[0] = img
            sticker_tk[0] = ImageTk.PhotoImage(img)
            if sticker_id[0]:
                canvas.delete(sticker_id[0])
            sticker_id[0] = canvas.create_image(pos[0], pos[1], image=sticker_tk[0], anchor="nw")
            canvas.image = sticker_tk[0]

        cargar_y_mostrar()

        def mover(event):
            pos[0], pos[1] = event.x, event.y
            cargar_y_mostrar()

        canvas.bind("<B1-Motion>", mover)

        Button(top, text="🔺 Tamaño +", command=lambda: (size.__setitem__(0, size[0]+10), cargar_y_mostrar())).pack(side="left")
        Button(top, text="🔻 Tamaño -", command=lambda: (size.__setitem__(0, max(20, size[0]-10)), cargar_y_mostrar())).pack(side="left")

        def aplicar():
            final = base.copy()
            final.paste(sticker_img[0], tuple(pos), sticker_img[0])
            self.actualizar_imagen(final.convert("RGB"))
            top.destroy()

        Button(top, text="✅ Aplicar", command=aplicar).pack(side="left", padx=10)
        Button(top, text="❌ Cancelar", command=top.destroy).pack(side="right", padx=10)

    def retoque_magico(self):
        if not self.imagen_actual:
            return

        top = Toplevel(self.root)
        top.title("✨ Retoque Mágico")

        # Convertimos la imagen PIL a OpenCV
        original_pil = self.imagen_actual.convert("RGB")
        img_cv = cv2.cvtColor(np.array(original_pil), cv2.COLOR_RGB2BGR)

        # Creamos una máscara negra del mismo tamaño
        mask = np.zeros(img_cv.shape[:2], dtype=np.uint8)

        # Mostramos imagen en el canvas
        canvas = Canvas(top, width=original_pil.width, height=original_pil.height, cursor="spraycan")
        canvas.pack()

        self.tk_img_retoque = ImageTk.PhotoImage(original_pil)  # Guardamos referencia en self
        canvas.create_image(0, 0, anchor="nw", image=self.tk_img_retoque)

        # Dibujar sobre la máscara
        def pintar(event):
            x, y = event.x, event.y
            r = 8
            cv2.circle(mask, (x, y), r, 255, -1)
            canvas.create_oval(x - r, y - r, x + r, y + r, fill="red", outline="")

        canvas.bind("<B1-Motion>", pintar)

        def aplicar_inpainting():
            restaurada = cv2.inpaint(img_cv, mask, 3, cv2.INPAINT_TELEA)
            restaurada_pil = Image.fromarray(cv2.cvtColor(restaurada, cv2.COLOR_BGR2RGB))
            self.actualizar_imagen(restaurada_pil)
            top.destroy()

        Button(top, text="✅ Aplicar Retoque", command=aplicar_inpainting).pack(side="left", padx=10)
        Button(top, text="❌ Cancelar", command=top.destroy).pack(side="right", padx=10)

    def generar_poster(self):
        if not self.imagen_actual:
            return

        top = Toplevel(self.root)
        top.title("🎨 Generador de Poster Avanzado")
        top.geometry("450x380")

        # Inputs
        Label(top, text="Título Principal:").pack()
        titulo_var = StringVar(value="¡IMPACTANTE!")
        Entry(top, textvariable=titulo_var).pack(fill="x", padx=10)

        Label(top, text="Subtítulo:").pack()
        subtitulo_var = StringVar(value="¡No creerás lo que pasó!")
        Entry(top, textvariable=subtitulo_var).pack(fill="x", padx=10)

        Label(top, text="Estilo Visual:").pack()
        estilo_var = StringVar(value="Cómic")
        opciones = ["Cómic", "Vintage", "Noir", "Pop Art", "Retro Futurista"]
        OptionMenu(top, estilo_var, *opciones).pack(pady=5)

        def aplicar_estilo(estilo, poster, draw, ancho_total, alto_total, fuente_titulo, fuente_sub):
            # Rectángulos y textos según el estilo
            titulo = titulo_var.get()
            subtitulo = subtitulo_var.get()

            if estilo == "Cómic":
                draw.rectangle([10, 10, ancho_total - 10, 50], fill="#ffcc00")
                draw.rectangle([10, alto_total - 50, ancho_total - 10, alto_total - 10], fill="#222")
                draw.text((ancho_total // 2, 15), titulo, font=fuente_titulo, fill="black", anchor="mm")
                draw.text((ancho_total // 2, alto_total - 40), subtitulo, font=fuente_sub, fill="white", anchor="mm")

            elif estilo == "Vintage":
                draw.rectangle([10, 10, ancho_total - 10, 50], fill="#d8c292")
                draw.rectangle([10, alto_total - 50, ancho_total - 10, alto_total - 10], fill="#4b3225")
                draw.text((ancho_total // 2, 15), titulo, font=fuente_titulo, fill="#4b3225", anchor="mm")
                draw.text((ancho_total // 2, alto_total - 40), subtitulo, font=fuente_sub, fill="#f2e2c4", anchor="mm")

            elif estilo == "Noir":
                poster.paste(Image.new("RGB", poster.size, "black"))
                draw.text((ancho_total // 2, 15), titulo, font=fuente_titulo, fill="white", anchor="mm")
                draw.text((ancho_total // 2, alto_total - 40), subtitulo, font=fuente_sub, fill="gray", anchor="mm")

            elif estilo == "Pop Art":
                draw.rectangle([10, 10, ancho_total - 10, 50], fill="#ff00ff")
                draw.rectangle([10, alto_total - 50, ancho_total - 10, alto_total - 10], fill="#00ffff")
                draw.text((ancho_total // 2, 15), titulo.upper(), font=fuente_titulo, fill="white", anchor="mm")
                draw.text((ancho_total // 2, alto_total - 40), subtitulo.upper(), font=fuente_sub, fill="black", anchor="mm")

            elif estilo == "Retro Futurista":
                fondo = Image.new("RGB", poster.size, "#0f0f3d")
                poster.paste(fondo)
                draw = ImageDraw.Draw(poster)
                draw.text((ancho_total // 2, 15), titulo, font=fuente_titulo, fill="#00ffff", anchor="mm")
                draw.text((ancho_total // 2, alto_total - 40), subtitulo, font=fuente_sub, fill="#ff00ff", anchor="mm")

            return poster

        def crear_poster():
            img = self.imagen_actual.copy().convert("RGB")
            ancho, alto = img.size
            poster = Image.new("RGB", (ancho + 40, alto + 120), "white")
            poster.paste(img, (20, 60))

            draw = ImageDraw.Draw(poster)
            try:
                fuente_titulo = ImageFont.truetype("arialbd.ttf", 36)
                fuente_sub = ImageFont.truetype("arial.ttf", 24)
            except:
                fuente_titulo = ImageFont.load_default()
                fuente_sub = ImageFont.load_default()

            estilo = estilo_var.get()
            poster = aplicar_estilo(estilo, poster, draw, poster.width, poster.height, fuente_titulo, fuente_sub)

            self.actualizar_imagen(poster)
            top.destroy()
            messagebox.showinfo("Poster creado", "🎉 Poster aplicado, ahora puedes guardarlo con 💾 Guardar Copia")

        Button(top, text="🎬 Generar Poster", command=crear_poster).pack(pady=10)
        Button(top, text="❌ Cancelar", command=top.destroy).pack()

        
if __name__ == "__main__":
    root = Tk()
    app = VisorFotos(root)
    root.mainloop()

