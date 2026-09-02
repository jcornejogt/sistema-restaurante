import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.user_controller import UserController
from brand import CREAM, GOLD


ROLES = ["Admin", "Mesero"]


class UsersView(ctk.CTkFrame):

    def __init__(self, master, usuario_actual):
        super().__init__(master)

        self.usuario_actual = usuario_actual
        self.configure(fg_color=CREAM)
        self.user_id_seleccionado = None

        titulo = ctk.CTkLabel(
            self,
            text="👤 Usuarios",
            text_color=GOLD,
            font=("Arial", 30, "bold")
        )
        titulo.pack(pady=20)

        formulario = ctk.CTkFrame(self)
        formulario.pack(fill="x", padx=20)

        ctk.CTkLabel(
            formulario,
            text="Nombre completo"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.nombre_entry = ctk.CTkEntry(
            formulario,
            width=250
        )
        self.nombre_entry.grid(row=0, column=1)

        ctk.CTkLabel(
            formulario,
            text="Usuario"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.usuario_entry = ctk.CTkEntry(
            formulario,
            width=250
        )
        self.usuario_entry.grid(row=1, column=1)

        ctk.CTkLabel(
            formulario,
            text="Contraseña"
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.password_entry = ctk.CTkEntry(
            formulario,
            width=250,
            show="*"
        )
        self.password_entry.grid(row=2, column=1)

        self.password_hint = ctk.CTkLabel(
            formulario,
            text="",
            font=("Arial", 13),
            text_color="gray"
        )
        self.password_hint.grid(row=3, column=1, sticky="w")

        ctk.CTkLabel(
            formulario,
            text="Rol"
        ).grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.rol_combo = ctk.CTkComboBox(
            formulario,
            width=250,
            values=ROLES
        )
        self.rol_combo.set(ROLES[1])
        self.rol_combo.grid(row=4, column=1)

        botones = ctk.CTkFrame(
            formulario,
            fg_color="transparent"
        )
        botones.grid(row=5, column=0, columnspan=2, pady=20)

        self.btn_guardar = ctk.CTkButton(
            botones,
            text="Guardar",
            command=self.guardar_usuario
        )
        self.btn_guardar.pack(side="left", padx=5)

        self.btn_eliminar = ctk.CTkButton(
            botones,
            text="Eliminar",
            fg_color="red",
            hover_color="#990000",
            command=self.eliminar_usuario
        )
        self.btn_eliminar.pack(side="left", padx=5)

        self.btn_nuevo = ctk.CTkButton(
            botones,
            text="Nuevo",
            command=self.limpiar
        )
        self.btn_nuevo.pack(side="left", padx=5)

        self.tabla = ttk.Treeview(
            self,
            columns=("id", "nombre", "usuario", "rol"),
            show="headings",
            height=12
        )

        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("usuario", text="Usuario")
        self.tabla.heading("rol", text="Rol")

        self.tabla.column("id", width=50, anchor="center")
        self.tabla.column("nombre", width=250)
        self.tabla.column("usuario", width=150)
        self.tabla.column("rol", width=100, anchor="center")

        self.tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_usuario
        )

        self.cargar_usuarios()

    def guardar_usuario(self):

        nombre = self.nombre_entry.get().strip()
        usuario = self.usuario_entry.get().strip()
        password = self.password_entry.get()
        rol = self.rol_combo.get()

        if nombre == "" or usuario == "":
            messagebox.showwarning(
                "Validación",
                "Ingrese nombre y usuario."
            )
            return

        if self.user_id_seleccionado is None:

            if password == "":
                messagebox.showwarning(
                    "Validación",
                    "La contraseña es obligatoria para un usuario nuevo."
                )
                return

            try:

                UserController.crear(nombre, usuario, password, rol)

            except Exception as e:

                messagebox.showerror("Error", str(e))
                return

            messagebox.showinfo(
                "Usuario",
                "Usuario creado correctamente."
            )

        else:

            try:

                UserController.actualizar(
                    self.user_id_seleccionado,
                    nombre,
                    usuario,
                    rol,
                    password if password else None
                )

            except Exception as e:

                messagebox.showerror("Error", str(e))
                return

            messagebox.showinfo(
                "Usuario",
                "Usuario actualizado correctamente."
            )

        self.limpiar()
        self.cargar_usuarios()

    def seleccionar_usuario(self, event):

        seleccionado = self.tabla.focus()

        if not seleccionado:
            return

        datos = self.tabla.item(seleccionado)["values"]

        self.user_id_seleccionado = datos[0]

        self.nombre_entry.delete(0, "end")
        self.nombre_entry.insert(0, datos[1])

        self.usuario_entry.delete(0, "end")
        self.usuario_entry.insert(0, datos[2])

        self.password_entry.delete(0, "end")

        self.password_hint.configure(
            text="Dejar en blanco para no cambiar la contraseña"
        )

        self.rol_combo.set(datos[3])

        self.btn_guardar.configure(text="Actualizar")

    def eliminar_usuario(self):

        if self.user_id_seleccionado is None:

            messagebox.showwarning(
                "Usuario",
                "Seleccione un usuario."
            )
            return

        respuesta = messagebox.askyesno(
            "Eliminar",
            "¿Desea eliminar este usuario?"
        )

        if not respuesta:
            return

        try:

            UserController.eliminar(
                self.user_id_seleccionado,
                self.usuario_actual["id"]
            )

        except Exception as e:

            messagebox.showerror("Error", str(e))
            return

        messagebox.showinfo(
            "Usuario",
            "Usuario eliminado."
        )

        self.limpiar()
        self.cargar_usuarios()

    def limpiar(self):

        self.user_id_seleccionado = None

        self.nombre_entry.delete(0, "end")
        self.usuario_entry.delete(0, "end")
        self.password_entry.delete(0, "end")

        self.password_hint.configure(text="")

        self.rol_combo.set(ROLES[1])

        self.btn_guardar.configure(text="Guardar")

        self.tabla.selection_remove(
            self.tabla.selection()
        )

    def cargar_usuarios(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        usuarios = UserController.listar()

        for user in usuarios:

            self.tabla.insert(
                "",
                "end",
                values=(
                    user.id,
                    user.nombre,
                    user.usuario,
                    user.rol
                )
            )