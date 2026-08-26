import customtkinter as ctk
from tkinter import messagebox

from database.database import SessionLocal
from models.table import Table
from controllers.order_controller import OrderController


class TablesView(ctk.CTkFrame):

    def __init__(self, master, abrir_cuenta_callback=None):
        super().__init__(master)

        self.abrir_cuenta_callback = abrir_cuenta_callback

        self.crear_vista()

        self.cargar_mesas()

    def crear_vista(self):

        titulo = ctk.CTkLabel(
            self,
            text="🪑 Mesas",
            font=("Arial", 30, "bold")
        )
        titulo.pack(pady=20)

        self.contenedor_mesas = ctk.CTkFrame(self)
        self.contenedor_mesas.pack(fill="both", expand=True, padx=30, pady=20)

        self.boton_crear = ctk.CTkButton(
            self,
            text="➕ Crear mesas iniciales",
            command=self.crear_mesas
        )
        self.boton_crear.pack(pady=15)

    def cargar_mesas(self):

        for widget in self.contenedor_mesas.winfo_children():
            widget.destroy()

        db = SessionLocal()

        try:

            mesas = db.query(Table).all()

            fila = 0
            columna = 0

            for mesa in mesas:

                tarjeta = ctk.CTkFrame(
                    self.contenedor_mesas,
                    width=200,
                    height=160,
                    corner_radius=15
                )
                tarjeta.grid(row=fila, column=columna, padx=15, pady=15)
                tarjeta.grid_propagate(False)

                ctk.CTkLabel(
                    tarjeta,
                    text=f"🪑 Mesa {mesa.numero}",
                    font=("Arial", 22, "bold")
                ).pack(pady=15)

                ctk.CTkLabel(
                    tarjeta,
                    text=f"Estado: {mesa.estado}",
                    font=("Arial", 16)
                ).pack()

                texto_boton = "Ver cuenta" if mesa.estado == "Ocupada" else "Abrir mesa"

                boton = ctk.CTkButton(
                    tarjeta,
                    text=texto_boton,
                    command=lambda m=mesa.id: self.abrir_mesa(m)
                )
                boton.pack(pady=10)

                columna += 1

                if columna == 4:
                    columna = 0
                    fila += 1

        finally:

            db.close()

    def abrir_mesa(self, mesa_id):

        try:

            OrderController.abrir_cuenta(mesa_id)

        except Exception as e:

            messagebox.showerror("Error", str(e))
            return

        if self.abrir_cuenta_callback:
            self.abrir_cuenta_callback(mesa_id)

    def crear_mesas(self):

        db = SessionLocal()

        try:

            existe = db.query(Table).count()

            if existe > 0:
                messagebox.showinfo("Mesas", "Las mesas ya fueron creadas.")
                return

            for numero in range(1, 11):
                mesa = Table(numero=numero, estado="Libre")
                db.add(mesa)

            db.commit()

            self.cargar_mesas()

            messagebox.showinfo("Mesas", "Se crearon 10 mesas correctamente.")

        finally:

            db.close()