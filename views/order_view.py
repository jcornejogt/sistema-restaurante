import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.order_controller import OrderController
from controllers.product_controller import ProductController
from brand import CREAM, GOLD
from controllers.sale_controller import SaleController
from views.recibo_view import ReciboView


class OrderView(ctk.CTkFrame):

    def __init__(self, master, mesa_id, volver_callback=None):
        super().__init__(master)

        self.mesa_id = mesa_id
        self.configure(fg_color=CREAM)
        self.volver_callback = volver_callback
        self.cuenta = None

        self.crear_vista()

        self.cargar_cuenta()

    def crear_vista(self):

        titulo = ctk.CTkLabel(
            self,
            text="🧾 Cuenta de Mesa",
            font=("Arial", 28, "bold")
        )
        titulo.pack(pady=(15, 5))

        self.info_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 16)
        )
        self.info_label.pack(pady=5)

        contenedor = ctk.CTkFrame(self)
        contenedor.pack(fill="both", expand=True, padx=20, pady=10)

        izquierda = ctk.CTkFrame(contenedor)
        izquierda.pack(side="left", fill="y", padx=10)

        ctk.CTkLabel(
            izquierda,
            text="Productos disponibles",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.productos = ttk.Treeview(
            izquierda,
            columns=("id", "nombre", "precio", "stock"),
            show="headings",
            height=15
        )

        self.productos.heading("id", text="ID")
        self.productos.heading("nombre", text="Nombre")
        self.productos.heading("precio", text="Precio")
        self.productos.heading("stock", text="Stock")

        self.productos.column("id", width=40)
        self.productos.column("nombre", width=160)
        self.productos.column("precio", width=70)
        self.productos.column("stock", width=60)

        self.productos.pack(padx=10, pady=5)

        cant_frame = ctk.CTkFrame(izquierda, fg_color="transparent")
        cant_frame.pack(pady=5)

        ctk.CTkLabel(cant_frame, text="Cantidad:").pack(side="left", padx=5)

        self.cantidad_entry = ctk.CTkEntry(cant_frame, width=60)
        self.cantidad_entry.insert(0, "1")
        self.cantidad_entry.pack(side="left")

        ctk.CTkButton(
            izquierda,
            text="Agregar ➕",
            command=self.agregar_producto
        ).pack(pady=10)

        derecha = ctk.CTkFrame(contenedor)
        derecha.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(
            derecha,
            text="Detalle de la cuenta",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.detalle = ttk.Treeview(
            derecha,
            columns=("producto", "cantidad", "precio", "subtotal"),
            show="headings"
        )

        self.detalle.heading("producto", text="Producto")
        self.detalle.heading("cantidad", text="Cantidad")
        self.detalle.heading("precio", text="Precio")
        self.detalle.heading("subtotal", text="Subtotal")

        self.detalle.pack(fill="both", expand=True, padx=10)

        ctk.CTkButton(
            derecha,
            text="Quitar producto seleccionado",
            fg_color="red",
            hover_color="#990000",
            command=self.eliminar_producto
        ).pack(pady=10)

        self.total_label = ctk.CTkLabel(
            derecha,
            text="Total: C$ 0.00",
            font=("Arial", 22, "bold")
        )
        self.total_label.pack(pady=10)

        botones_inferior = ctk.CTkFrame(self, fg_color="transparent")
        botones_inferior.pack(pady=15)

        ctk.CTkButton(
            botones_inferior,
            text="⬅ Volver a Mesas",
            command=self.volver
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            botones_inferior,
            text="Cerrar cuenta y cobrar",
            fg_color="green",
            command=self.cerrar_cuenta
        ).pack(side="left", padx=10)

        self.cargar_productos_disponibles()

    def cargar_productos_disponibles(self):

        for fila in self.productos.get_children():
            self.productos.delete(fila)

        for producto in ProductController.listar_disponibles():

            self.productos.insert(
                "",
                "end",
                values=(
                    producto.id,
                    producto.nombre,
                    f"{producto.precio:.2f}",
                    producto.stock
                )
            )

    def cargar_cuenta(self):

        self.cuenta = OrderController.obtener_cuenta_abierta(self.mesa_id)

        if self.cuenta is None:

            self.info_label.configure(
                text="No existe una cuenta abierta para esta mesa."
            )
            return

        self.info_label.configure(
            text=f"Cuenta #{self.cuenta.id} - Mesa {self.mesa_id}"
        )

        self.actualizar_detalle()

    def actualizar_detalle(self):

        for fila in self.detalle.get_children():
            self.detalle.delete(fila)

        detalles = OrderController.obtener_detalle(self.cuenta.id)

        total = 0

        for item in detalles:

            total += item["subtotal"]

            self.detalle.insert(
                "",
                "end",
                iid=item["id"],
                values=(
                    item["producto_nombre"],
                    item["cantidad"],
                    f"{item['precio']:.2f}",
                    f"{item['subtotal']:.2f}"
                )
            )

        self.total_label.configure(
            text=f"Total: C$ {total:.2f}"
        )

    def agregar_producto(self):

        if self.cuenta is None:
            return

        seleccionado = self.productos.focus()

        if not seleccionado:
            messagebox.showwarning(
                "Cuenta",
                "Seleccione un producto."
            )
            return

        try:
            cantidad = int(self.cantidad_entry.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "La cantidad debe ser un número entero."
            )
            return

        if cantidad <= 0:
            messagebox.showwarning(
                "Cuenta",
                "La cantidad debe ser mayor que cero."
            )
            return

        datos = self.productos.item(seleccionado)["values"]
        producto_id = datos[0]

        OrderController.agregar_producto(
            self.cuenta.id,
            producto_id,
            cantidad
        )

        self.actualizar_detalle()

    def eliminar_producto(self):

        seleccionado = self.detalle.focus()

        if not seleccionado:
            messagebox.showwarning(
                "Cuenta",
                "Seleccione un producto del detalle."
            )
            return

        OrderController.eliminar_producto(int(seleccionado))

        self.actualizar_detalle()

    def cerrar_cuenta(self):

        if self.cuenta is None:
            return

        respuesta = messagebox.askyesno(
            "Cerrar cuenta",
            "¿Desea cerrar esta cuenta, registrar la venta y liberar la mesa?"
        )

        if not respuesta:
            return

        try:

            venta_id = OrderController.cerrar_cuenta(self.cuenta.id)

        except Exception as e:

            messagebox.showerror(
                "No se pudo cerrar la cuenta",
                str(e)
            )
            return

        if venta_id is not None:
            venta = SaleController.obtener_venta(venta_id)

            if venta:
                ReciboView(self.winfo_toplevel(), venta)

        self.volver()

    def volver(self):

        if self.volver_callback:
            self.volver_callback()