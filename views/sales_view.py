import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.product_controller import ProductController
from database.sales_model import SalesModel


class SalesView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.carrito = []

        titulo = ctk.CTkLabel(
            self,
            text="🛒 Ventas",
            font=("Arial", 28, "bold")
        )
        titulo.pack(pady=20)

        contenedor = ctk.CTkFrame(self)
        contenedor.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        izquierda = ctk.CTkFrame(contenedor)
        izquierda.pack(
            side="left",
            fill="y",
            padx=10
        )

        ctk.CTkLabel(
            izquierda,
            text="Productos",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        self.productos = ttk.Treeview(
            izquierda,
            columns=("id", "nombre", "precio"),
            show="headings",
            height=15
        )

        self.productos.heading("id", text="ID")
        self.productos.heading("nombre", text="Nombre")
        self.productos.heading("precio", text="Precio")

        self.productos.column("id", width=50)
        self.productos.column("nombre", width=180)
        self.productos.column("precio", width=80)

        self.productos.pack(
            padx=10,
            pady=10
        )

        ctk.CTkButton(
            izquierda,
            text="Agregar ➕",
            command=self.agregar_producto
        ).pack(pady=10)

        derecha = ctk.CTkFrame(contenedor)
        derecha.pack(
            side="right",
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            derecha,
            text="Detalle de venta",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        self.detalle = ttk.Treeview(
            derecha,
            columns=("nombre", "precio", "cantidad", "subtotal"),
            show="headings"
        )

        self.detalle.heading("nombre", text="Nombre")
        self.detalle.heading("precio", text="Precio")
        self.detalle.heading("cantidad", text="Cantidad")
        self.detalle.heading("subtotal", text="Subtotal")

        self.detalle.pack(
            fill="both",
            expand=True,
            padx=10
        )

        self.total_label = ctk.CTkLabel(
            derecha,
            text="Total: C$ 0.00",
            font=("Arial", 22, "bold")
        )

        self.total_label.pack(pady=15)

        ctk.CTkButton(
            derecha,
            text="Finalizar Venta",
            fg_color="green",
            command=self.finalizar
        ).pack(pady=10)

        self.cargar_productos()


    def cargar_productos(self):

        for fila in self.productos.get_children():
            self.productos.delete(fila)

        productos = ProductController.listar()

        for producto in productos:
            self.productos.insert(
                "",
                "end",
                values=(
                    producto.id,
                    producto.nombre,
                    producto.precio
                )
            )


    def agregar_producto(self):

        seleccionado = self.productos.focus()

        if not seleccionado:
            messagebox.showwarning(
                "Venta",
                "Seleccione un producto."
            )
            return

        datos = self.productos.item(seleccionado)["values"]


        precio = float(datos[2])
        cantidad = 1


        producto = {

            "id": datos[0],

            "nombre": datos[1],

            "precio": precio,

            "cantidad": cantidad,

            # NUEVO CAMPO NECESARIO PARA GUARDAR EN BD
            "subtotal": precio * cantidad
        }


        self.carrito.append(producto)

        self.actualizar_carrito()



    def actualizar_carrito(self):

        for fila in self.detalle.get_children():
            self.detalle.delete(fila)

        total = 0


        for item in self.carrito:

            subtotal = item["precio"] * item["cantidad"]

            # Mantener actualizado el subtotal
            item["subtotal"] = subtotal

            total += subtotal


            self.detalle.insert(
                "",
                "end",
                values=(
                    item["nombre"],
                    f"{item['precio']:.2f}",
                    item["cantidad"],
                    f"{subtotal:.2f}"
                )
            )


        self.total_label.configure(
            text=f"Total: C$ {total:.2f}"
        )



    def finalizar(self):

        if len(self.carrito) == 0:
            messagebox.showwarning(
                "Venta",
                "No hay productos en el carrito."
            )
            return


        total = sum(
            item["subtotal"]
            for item in self.carrito
        )


        SalesModel.guardar(
            total,
            self.carrito
        )


        messagebox.showinfo(
            "Venta",
            "Venta registrada correctamente."
        )


        self.carrito.clear()

        self.actualizar_carrito()

        self.cargar_productos()