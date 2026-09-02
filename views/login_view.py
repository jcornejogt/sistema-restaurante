import customtkinter as ctk
from tkinter import messagebox

from controllers.user_controller import UserController
from brand import CREAM, GOLD, GOLD_HOVER, MUTED, NAVY, logo_image
from subscription import expiration_text, is_active


class LoginView(ctk.CTkFrame):

    def __init__(self, master, on_success):
        super().__init__(master)

        self.on_success = on_success

        self.pack(fill="both", expand=True)

        self.crear_vista()

    def crear_vista(self):

        self.configure(fg_color=CREAM)

        contenedor = ctk.CTkFrame(
            self,
            width=350,
            height=440,
            corner_radius=15,
            fg_color=NAVY
        )

        contenedor.place(relx=0.5, rely=0.5, anchor="center")

        contenedor.pack_propagate(False)

        imagen_logo = logo_image(115, 115)
        if imagen_logo:
            ctk.CTkLabel(contenedor, text="", image=imagen_logo).pack(pady=(18, 0))
        else:
            ctk.CTkLabel(contenedor, text="LA BAJONA", text_color=GOLD,
                         font=("Arial", 27, "bold")).pack(pady=(30, 0))

        ctk.CTkLabel(
            contenedor,
            text="La Bajona",
            text_color=GOLD,
            font=("Arial", 24, "bold")
        ).pack(pady=(0, 25))

        ctk.CTkLabel(
            contenedor,
            text=f"Su suscripción actual vence el {expiration_text()}",
            text_color=MUTED,
            font=("Arial", 14)
        ).pack(pady=(0, 18))

        ctk.CTkLabel(
            contenedor,
            text="Usuario",
            text_color=MUTED
        ).pack(anchor="w", padx=45)

        self.usuario_entry = ctk.CTkEntry(
            contenedor,
            width=260
        )
        self.usuario_entry.pack(pady=(0, 15), padx=45)

        ctk.CTkLabel(
            contenedor,
            text="Contraseña",
            text_color=MUTED
        ).pack(anchor="w", padx=45)

        self.password_entry = ctk.CTkEntry(
            contenedor,
            width=260,
            show="*"
        )
        self.password_entry.pack(pady=(0, 25), padx=45)

        self.password_entry.bind(
            "<Return>",
            lambda e: self.iniciar_sesion()
        )

        ctk.CTkButton(
            contenedor,
            text="Iniciar sesión",
            width=260,
            fg_color=GOLD,
            hover_color=GOLD_HOVER,
            text_color=NAVY,
            command=self.iniciar_sesion
        ).pack(pady=5)

        self.usuario_entry.focus()

    def iniciar_sesion(self):

        if not is_active():
            messagebox.showerror(
                "Suscripción vencida",
                f"Su suscripción venció el {expiration_text()}."
            )
            return

        usuario = self.usuario_entry.get().strip()
        password = self.password_entry.get()

        if usuario == "" or password == "":
            messagebox.showwarning(
                "Login",
                "Ingrese usuario y contraseña."
            )
            return

        user = UserController.autenticar(usuario, password)

        if user is None:
            messagebox.showerror(
                "Login",
                "Usuario o contraseña incorrectos."
            )
            return

        self.on_success(user)