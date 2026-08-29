import customtkinter as ctk
from tkinter import messagebox

from database.database import SessionLocal
from models.table import Table
from controllers.order_controller import OrderController
from brand import CREAM, GOLD


class TablesView(ctk.CTkFrame):

    @staticmethod
    def _next_table_number(mesas):
        if not mesas:
            return 1
        return max(mesas) + 1

    def __init__(self, master, abrir_cuenta_callback=None):
        super().__init__(master)

        self.abrir_cuenta_callback = abrir_cuenta_callback
        self.configure(fg_color=CREAM)

        self.crear_vista()

        self.cargar_mesas()

    def crear_vista(self):

        titulo = ctk.CTkLabel(
            self,
            text="🪑 Mesas",
            text_color=GOLD,
            font=("Arial", 30, "bold")
        )
        titulo.pack(pady=20)

        self.contenedor_mesas = ctk.CTkFrame(self)
        self.contenedor_mesas.pack(fill="both", expand=True, padx=30, pady=20)

        self.botones_accion = ctk.CTkFrame(self)
        self.botones_accion.pack(pady=10)

        self.boton_crear = ctk.CTkButton(
            self.botones_accion,
            text="➕ Agregar mesa",
            command=self.agregar_mesa
        )
        self.boton_crear.pack(side="left", padx=10)

        self.boton_crear_iniciales = ctk.CTkButton(
            self.botones_accion,
            text="🏁 Crear 10 mesas iniciales",
            command=self.crear_mesas_iniciales
        )
        self.boton_crear_iniciales.pack(side="left", padx=10)

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
                boton.pack(pady=6)

                boton_eliminar = ctk.CTkButton(
                    tarjeta,
                    text="🗑 Eliminar",
                    fg_color="#b22222",
                    hover_color="#8b1e1e",
                    command=lambda m=mesa.id: self.eliminar_mesa(m)
                )
                boton_eliminar.pack(pady=(0, 10))

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

    def agregar_mesa(self):

        db = SessionLocal()

        try:
            numeros = [mesa.numero for mesa in db.query(Table.numero).all()]
            numero = self._next_table_number(numeros)
            mesa = Table(numero=numero, estado="Libre")
            db.add(mesa)
            db.commit()

            self.cargar_mesas()
            messagebox.showinfo("Mesas", f"Se creó la mesa {numero} correctamente.")

        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", f"No se pudo crear la mesa: {str(e)}")

        finally:
            db.close()

    def crear_mesas_iniciales(self):

        db = SessionLocal()

        try:
            existe = db.query(Table).count()

            if existe > 0:
                messagebox.showinfo("Mesas", "Ya existen mesas registradas. Usa 'Agregar mesa' para crear más.")
                return

            for numero in range(1, 11):
                mesa = Table(numero=numero, estado="Libre")
                db.add(mesa)

            db.commit()

            self.cargar_mesas()
            messagebox.showinfo("Mesas", "Se crearon 10 mesas correctamente.")

        finally:
            db.close()

    def eliminar_mesa(self, mesa_id):

        db = SessionLocal()

        try:
            mesa = db.query(Table).filter(Table.id == mesa_id).first()

            if mesa is None:
                messagebox.showwarning("Mesas", "La mesa que intentas eliminar no existe.")
                return

            if mesa.estado == "Ocupada":
                messagebox.showwarning("Mesas", "No puedes eliminar una mesa ocupada. Cierra la cuenta primero.")
                return

            from models.order import Order
            from models.order_detail import OrderDetail

            ordenes = db.query(Order.id).filter(Order.mesa_id == mesa_id).all()
            ids_ordenes = [orden.id for orden in ordenes]

            if ids_ordenes:
                db.query(OrderDetail).filter(OrderDetail.order_id.in_(ids_ordenes)).delete(synchronize_session=False)
                db.query(Order).filter(Order.mesa_id == mesa_id).delete(synchronize_session=False)

            db.delete(mesa)
            db.commit()

            self.cargar_mesas()
            messagebox.showinfo("Mesas", f"Se eliminó la mesa {mesa.numero} correctamente.")

        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", f"No se pudo eliminar la mesa: {str(e)}")

        finally:
            db.close()