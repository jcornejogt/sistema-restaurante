import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.product_controller import ProductController
from brand import CREAM, DANGER, DANGER_HOVER, GOLD, GOLD_HOVER


class ProductsView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.producto_id = None
        self.configure(fg_color=CREAM)

        titulo = ctk.CTkLabel(
            self,
            text="🍔 Productos",
            text_color=GOLD,
            font=("Arial", 30, "bold")
        )
        titulo.pack(pady=20)

        formulario = ctk.CTkFrame(self)
        formulario.pack(fill="x", padx=20)

        ctk.CTkLabel(
            formulario,
            text="Nombre"
        ).grid(row=0, column=0, padx=10, pady=10)

        self.nombre = ctk.CTkEntry(
            formulario,
            width=250
        )
        self.nombre.grid(row=0, column=1)

        ctk.CTkLabel(
            formulario,
            text="Precio"
        ).grid(row=1, column=0, padx=10, pady=10)

        self.precio = ctk.CTkEntry(
            formulario,
            width=250
        )
        self.precio.grid(row=1, column=1)

        ctk.CTkLabel(
            formulario,
            text="Stock"
        ).grid(row=2, column=0, padx=10, pady=10)

        self.stock = ctk.CTkEntry(
            formulario,
            width=250
        )
        self.stock.grid(row=2, column=1)

        botones = ctk.CTkFrame(
            formulario,
            fg_color="transparent"
        )

        botones.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=20
        )

        self.btn_guardar = ctk.CTkButton(
            botones,
            text="Guardar",
            command=self.guardar_producto
        )

        self.btn_guardar.pack(
            side="left",
            padx=5
        )

        self.btn_eliminar = ctk.CTkButton(
            botones,
            text="Eliminar",
            fg_color=DANGER,
            hover_color=DANGER_HOVER,
            command=self.eliminar_producto
        )

        self.btn_eliminar.pack(
            side="left",
            padx=5
        )

        self.btn_nuevo = ctk.CTkButton(
            botones,
            text="Nuevo",
            command=self.limpiar
        )

        self.btn_nuevo.pack(
            side="left",
            padx=5
        )

        self.tabla = ttk.Treeview(
            self,
            columns=(
                "id",
                "nombre",
                "precio",
                "stock"
            ),
            show="headings",
            height=12
        )

        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("stock", text="Stock")

        self.tabla.column(
            "id",
            width=60,
            anchor="center"
        )

        self.tabla.column(
            "nombre",
            width=300
        )

        self.tabla.column(
            "precio",
            width=120,
            anchor="center"
        )

        self.tabla.column(
            "stock",
            width=120,
            anchor="center"
        )

        self.tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_producto
        )

        self.cargar_productos()

    def guardar_producto(self):

        nombre = self.nombre.get().strip()

        if nombre == "":
            messagebox.showwarning(
                "Validación",
                "Ingrese el nombre del producto."
            )
            return

        try:

            precio = float(self.precio.get())
            stock = int(self.stock.get())

        except ValueError:

            messagebox.showerror(
                "Error",
                "Precio y Stock deben ser numéricos."
            )
            return

        if precio <= 0:

            messagebox.showwarning(
                "Validación",
                "El precio debe ser mayor que cero."
            )
            return

        if stock < 0:

            messagebox.showwarning(
                "Validación",
                "El stock no puede ser negativo."
            )
            return

        if self.producto_id is None:

            ProductController.guardar(
                nombre,
                precio,
                stock
            )

            messagebox.showinfo(
                "Producto",
                "Producto creado correctamente."
            )

        else:

            ProductController.actualizar(
                self.producto_id,
                nombre,
                precio,
                stock
            )

            messagebox.showinfo(
                "Producto",
                "Producto actualizado correctamente."
            )

        self.limpiar()

        self.cargar_productos()

    def seleccionar_producto(self, event):

        seleccionado = self.tabla.focus()

        if not seleccionado:
            return

        datos = self.tabla.item(seleccionado)["values"]

        self.producto_id = datos[0]

        self.nombre.delete(0, "end")
        self.nombre.insert(0, datos[1])

        self.precio.delete(0, "end")
        self.precio.insert(0, datos[2])

        self.stock.delete(0, "end")
        self.stock.insert(0, datos[3])

        self.btn_guardar.configure(
            text="Actualizar"
        )

    def eliminar_producto(self):

        if self.producto_id is None:

            messagebox.showwarning(
                "Producto",
                "Seleccione un producto."
            )
            return

        respuesta = messagebox.askyesno(
            "Eliminar",
            "¿Desea eliminar este producto?"
        )

        if not respuesta:
            return

        ProductController.eliminar(
            self.producto_id
        )

        messagebox.showinfo(
            "Producto",
            "Producto eliminado."
        )

        self.limpiar()

        self.cargar_productos()

    def limpiar(self):

        self.producto_id = None

        self.nombre.delete(0, "end")
        self.precio.delete(0, "end")
        self.stock.delete(0, "end")

        self.btn_guardar.configure(
            text="Guardar"
        )

        self.tabla.selection_remove(
            self.tabla.selection()
        )

    def cargar_productos(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        productos = ProductController.listar()

        for producto in productos:

            self.tabla.insert(
                "",
                "end",
                values=(
                    producto.id,
                    producto.nombre,
                    f"{producto.precio:.2f}",
                    producto.stock
                )
            )