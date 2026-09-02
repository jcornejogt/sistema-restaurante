import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.product_controller import ProductController
from brand import CREAM, GOLD


class InventoryView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.producto_id = None
        self.configure(fg_color=CREAM)
        self.crear_vista()
        self.cargar_productos()

    def crear_vista(self):
        ctk.CTkLabel(
            self,
            text="📦 Inventario",
            text_color=GOLD,
            font=("Arial", 30, "bold")
        ).pack(pady=20)

        formulario = ctk.CTkFrame(self)
        formulario.pack(fill="x", padx=25, pady=5)

        ctk.CTkLabel(formulario, text="Stock nuevo:").pack(side="left", padx=10)
        self.stock_entry = ctk.CTkEntry(formulario, width=120)
        self.stock_entry.pack(side="left", padx=10)

        ctk.CTkButton(
            formulario,
            text="Actualizar stock",
            command=self.actualizar_stock
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            formulario,
            text="Limpiar",                             
            fg_color="gray",
            command=self.limpiar
        ).pack(side="left", padx=10)

        self.tabla = ttk.Treeview(
            self,
            columns=("id", "nombre", "precio", "stock", "estado"),
            show="headings"
        )

        for columna, texto in (
            ("id", "ID"),
            ("nombre", "Producto"),
            ("precio", "Precio"),
            ("stock", "Stock"),
            ("estado", "Estado")
        ):
            self.tabla.heading(columna, text=texto)

        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("nombre", width=300)
        self.tabla.column("precio", width=120, anchor="center")
        self.tabla.column("stock", width=100, anchor="center")
        self.tabla.column("estado", width=140, anchor="center")
        self.tabla.pack(fill="both", expand=True, padx=25, pady=20)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

    def cargar_productos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for producto in ProductController.listar():
            estado = "Bajo" if producto.stock <= 5 else "Disponible"
            self.tabla.insert(
                "", "end", values=(
                    producto.id,
                    producto.nombre,
                    f"C$ {producto.precio:.2f}",
                    producto.stock,
                    estado
                )
            )

    def seleccionar(self, event):
        seleccionado = self.tabla.focus()
        if not seleccionado:
            return
        datos = self.tabla.item(seleccionado)["values"]
        self.producto_id = int(datos[0])
        self.stock_entry.delete(0, "end")
        self.stock_entry.insert(0, str(datos[3]))

    def actualizar_stock(self):
        if self.producto_id is None:
            messagebox.showwarning("Inventario", "Seleccione un producto.")
            return

        try:
            stock = int(self.stock_entry.get())
        except ValueError:
            messagebox.showerror("Inventario", "El stock debe ser un número entero.")
            return

        if stock < 0:
            messagebox.showwarning("Inventario", "El stock no puede ser negativo.")
            return

        ProductController.actualizar_stock(self.producto_id, stock)
        self.cargar_productos()
        self.limpiar()
        messagebox.showinfo("Inventario", "Stock actualizado correctamente.")

    def limpiar(self):
        self.producto_id = None
        self.stock_entry.delete(0, "end")
        for seleccionado in self.tabla.selection():
            self.tabla.selection_remove(seleccionado)
