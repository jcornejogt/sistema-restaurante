import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.product_controller import ProductController
from controllers.customer_controller import CustomerController
from database.sales_model import SalesModel
from brand import CREAM, GOLD, GOLD_HOVER, SUCCESS, SUCCESS_HOVER


class SalesView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.carrito = []
        self.configure(fg_color=CREAM)

        titulo = ctk.CTkLabel(
            self,
            text="🛒 Ventas",
            text_color=GOLD,
            font=("Arial", 30, "bold")
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
            font=("Arial", 20, "bold")
        ).pack(pady=(10, 5))

        self.busqueda_frame = ctk.CTkFrame(izquierda, fg_color="transparent")
        self.busqueda_frame.pack(fill="x", padx=10, pady=(0, 8))

        self.busqueda_entry = ctk.CTkEntry(
            self.busqueda_frame,
            placeholder_text="Buscar producto por nombre",
            width=150
        )
        self.busqueda_entry.pack(side="left", fill="x", expand=True)
        self.busqueda_entry.bind("<Return>", lambda event: self.cargar_productos())

        ctk.CTkButton(
            self.busqueda_frame,
            text="🔎",
            width=40,
            command=self.cargar_productos
        ).pack(side="left", padx=(8, 0))

        ctk.CTkLabel(
            izquierda,
            text="Lo más vendido",
            font=("Arial", 16, "bold"),
            text_color=GOLD
        ).pack(anchor="w", padx=10, pady=(0, 6))

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

        cantidad_frame = ctk.CTkFrame(izquierda, fg_color="transparent")
        cantidad_frame.pack(pady=(0, 10))
        ctk.CTkLabel(cantidad_frame, text="Cantidad:").pack(side="left", padx=5)
        self.cantidad_entry = ctk.CTkEntry(cantidad_frame, width=70)
        self.cantidad_entry.insert(0, "1")
        self.cantidad_entry.pack(side="left")
        self.cantidad_entry.bind("<Return>", lambda event: self.agregar_producto())

        derecha = ctk.CTkFrame(contenedor)
        derecha.pack(
            side="right",
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            derecha,
            text="Detalle de venta",
            font=("Arial", 20, "bold")
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
            font=("Arial", 24, "bold")
        )

        self.total_label.pack(pady=15)

        metodo_frame = ctk.CTkFrame(derecha, fg_color="transparent")
        metodo_frame.pack(fill="x", padx=10, pady=(0, 8))

        ctk.CTkLabel(metodo_frame, text="Método de pago:").pack(anchor="w")
        self.metodo_pago_var = ctk.StringVar(value="Efectivo")
        self.metodo_pago = ctk.CTkOptionMenu(
            metodo_frame,
            variable=self.metodo_pago_var,
            values=["Efectivo", "Tarjeta", "Transferencia", "Credito"],
            command=self.actualizar_metodo_pago
        )
        self.metodo_pago.pack(fill="x", pady=(4, 0))

        self.cliente_frame = ctk.CTkFrame(derecha, fg_color="transparent")
        self.cliente_frame.pack(fill="x", padx=10, pady=(0, 8))

        ctk.CTkLabel(self.cliente_frame, text="Cliente (crédito):").pack(anchor="w")
        self.clientes_map = {}
        self.cliente_seleccionado = None
        self.cliente_combo = ctk.CTkOptionMenu(
            self.cliente_frame,
            values=["Seleccione un cliente"],
            state="disabled"
        )
        self.cliente_combo.pack(fill="x", pady=(4, 0))
        self.cliente_combo.bind("<<ComboboxSelected>>", lambda event: self._actualizar_cliente_seleccionado())

        ctk.CTkButton(
            derecha,
            text="Quitar producto seleccionado",
            fg_color="red",
            hover_color="#990000",
            command=self.quitar_producto
        ).pack(pady=(0, 10))

        ctk.CTkButton(
            derecha,
            text="Finalizar Venta",
            fg_color=SUCCESS,
            hover_color=SUCCESS_HOVER,
            command=self.finalizar
        ).pack(pady=10)

        self.cargar_productos()
        self.cargar_clientes()
        self.actualizar_metodo_pago(self.metodo_pago_var.get())


    def cargar_productos(self):

        for fila in self.productos.get_children():
            self.productos.delete(fila)

        texto_busqueda = self.busqueda_entry.get().strip()
        productos = ProductController.listar_disponibles(filtro=texto_busqueda)

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

        if texto_busqueda:
            self.productos.heading("nombre", text=f"Resultados para: {texto_busqueda}")
        else:
            self.productos.heading("nombre", text="Nombre")

    def cargar_clientes(self):
        clientes = CustomerController.listar()
        opciones = ["Seleccione un cliente"]
        self.clientes_map = {}

        for cliente in clientes:
            opciones.append(cliente.nombre)
            self.clientes_map[cliente.nombre] = cliente.id

        self.cliente_combo.configure(values=opciones)
        self.cliente_combo.set(opciones[0])
        self.cliente_seleccionado = None

    def _actualizar_cliente_seleccionado(self):
        cliente_nombre = self.cliente_combo.get()
        self.cliente_seleccionado = self.clientes_map.get(cliente_nombre)

    def actualizar_metodo_pago(self, metodo):
        if metodo == "Credito":
            self.cliente_combo.configure(state="normal")
            if not self.clientes_map:
                messagebox.showwarning("Venta", "No hay clientes registrados para ventas a crédito.")
        else:
            self.cliente_combo.configure(state="disabled")
            self.cliente_combo.set("Seleccione un cliente")
            self.cliente_seleccionado = None


    def agregar_producto(self):

        seleccionado = self.productos.focus()

        if not seleccionado:
            messagebox.showwarning(
                "Venta",
                "Seleccione un producto."
            )
            return

        datos = self.productos.item(seleccionado)["values"]


        try:
            cantidad = int(self.cantidad_entry.get())
        except ValueError:
            messagebox.showerror("Venta", "La cantidad debe ser un número entero.")
            return

        if cantidad <= 0:
            messagebox.showwarning("Venta", "La cantidad debe ser mayor que cero.")
            return

        precio = float(datos[2])

        producto_existente = next(
            (item for item in self.carrito if item["id"] == datos[0]),
            None
        )

        producto_actual = ProductController.obtener_por_id(int(datos[0]))
        cantidad_carrito = producto_existente["cantidad"] if producto_existente else 0
        if producto_actual is None or cantidad_carrito + cantidad > producto_actual.stock:
            disponible = producto_actual.stock if producto_actual else 0
            messagebox.showwarning(
                "Venta",
                f"Stock insuficiente. Disponible: {disponible}."
            )
            return

        if producto_existente:
            producto_existente["cantidad"] += cantidad
            producto_existente["subtotal"] = (
                producto_existente["precio"] * producto_existente["cantidad"]
            )
            self.actualizar_carrito()
            return


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



    @staticmethod
    def quitar_producto_del_carrito(carrito, producto_id):
        return [item for item in carrito if item["id"] != producto_id]

    def quitar_producto(self):
        seleccionado = self.detalle.focus()

        if not seleccionado:
            messagebox.showwarning("Venta", "Seleccione un producto del detalle para quitarlo.")
            return

        producto_id = int(seleccionado)
        self.carrito = self.quitar_producto_del_carrito(self.carrito, producto_id)
        self.actualizar_carrito()

    def actualizar_carrito(self):

        for fila in self.detalle.get_children():
            self.detalle.delete(fila)

        total = 0

        for item in self.carrito:
            subtotal = item["precio"] * item["cantidad"]
            item["subtotal"] = subtotal
            total += subtotal

            self.detalle.insert(
                "",
                str(item["id"]),
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

        metodo_pago = self.metodo_pago_var.get()
        customer_id = None

        if metodo_pago == "Credito":
            customer_id = self.cliente_seleccionado
            if customer_id is None:
                messagebox.showwarning(
                    "Venta",
                    "Seleccione un cliente para registrar la venta a crédito."
                )
                return

        try:
            venta_id = SalesModel.guardar(
                total,
                self.carrito,
                metodo_pago=metodo_pago,
                customer_id=customer_id
            )
        except Exception as e:
            messagebox.showerror("No se pudo registrar la venta", str(e))
            return

        from controllers.sale_controller import SaleController
        from views.recibo_view import ReciboView

        venta = SaleController.obtener_venta(venta_id)

        if venta:
            ReciboView(self.winfo_toplevel(), venta)

        messagebox.showinfo(
            "Venta",
            f"Venta registrada correctamente con pago {metodo_pago}."
        )

        self.carrito.clear()
        self.actualizar_carrito()
        self.cargar_productos()
        self.cargar_clientes()
        self.actualizar_metodo_pago(self.metodo_pago_var.get())