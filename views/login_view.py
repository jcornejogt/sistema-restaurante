import customtkinter as ctk
from tkinter import messagebox

from controllers.user_controller import UserController


class LoginView(ctk.CTkFrame):

    def __init__(self, master, on_success):
        super().__init__(master)

        self.on_success = on_success

        self.pack(fill="both", expand=True)

        self.crear_vista()

    def crear_vista(self):

        contenedor = ctk.CTkFrame(
            self,
            width=350,
            height=400,
            corner_radius=15
        )

        contenedor.place(relx=0.5, rely=0.5, anchor="center")

        contenedor.pack_propagate(False)

        ctk.CTkLabel(
            contenedor,
            text="🍽️",
            font=("Arial", 40)
        ).pack(pady=(30, 0))

        ctk.CTkLabel(
            contenedor,
            text="Sistema Restaurante",
            font=("Arial", 22, "bold")
        ).pack(pady=(0, 25))

        ctk.CTkLabel(
            contenedor,
            text="Usuario"
        ).pack(anchor="w", padx=45)

        self.usuario_entry = ctk.CTkEntry(
            contenedor,
            width=260
        )
        self.usuario_entry.pack(pady=(0, 15), padx=45)

        ctk.CTkLabel(
            contenedor,
            text="Contraseña"
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
            command=self.iniciar_sesion
        ).pack(pady=5)

        self.usuario_entry.focus()

    def iniciar_sesion(self):

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