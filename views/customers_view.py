import customtkinter as ctk
from tkinter import ttk, messagebox, simpledialog

from controllers.customer_controller import CustomerController
from brand import CREAM, GOLD, NAVY


class CustomersView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color=CREAM)
        self.customer_id_selected = None
        self.account_id_selected = None

        self.crear_vista()
        self.cargar_clientes()

    def crear_vista(self):
        titulo = ctk.CTkLabel(
            self,
            text="👥 Clientes y crédito",
            text_color=GOLD,
            font=("Arial", 30, "bold")
        )
        titulo.pack(pady=(20, 10))

        contenedor = ctk.CTkFrame(self, fg_color="transparent")
        contenedor.pack(fill="both", expand=True, padx=20, pady=10)

        formulario = ctk.CTkFrame(contenedor)
        formulario.pack(side="left", fill="y", padx=(0, 20))

        ctk.CTkLabel(formulario, text="Nombre").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.nombre_entry = ctk.CTkEntry(formulario, width=260)
        self.nombre_entry.grid(row=0, column=1, padx=10, pady=8)

        ctk.CTkLabel(formulario, text="Teléfono").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.telefono_entry = ctk.CTkEntry(formulario, width=260)
        self.telefono_entry.grid(row=1, column=1, padx=10, pady=8)

        ctk.CTkLabel(formulario, text="Documento").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.documento_entry = ctk.CTkEntry(formulario, width=260)
        self.documento_entry.grid(row=2, column=1, padx=10, pady=8)

        ctk.CTkLabel(formulario, text="Email").grid(row=3, column=0, padx=10, pady=8, sticky="w")
        self.email_entry = ctk.CTkEntry(formulario, width=260)
        self.email_entry.grid(row=3, column=1, padx=10, pady=8)

        ctk.CTkLabel(formulario, text="Dirección").grid(row=4, column=0, padx=10, pady=8, sticky="w")
        self.direccion_entry = ctk.CTkEntry(formulario, width=260)
        self.direccion_entry.grid(row=4, column=1, padx=10, pady=8)

        botones = ctk.CTkFrame(formulario, fg_color="transparent")
        botones.grid(row=5, column=0, columnspan=2, pady=12)

        self.btn_guardar = ctk.CTkButton(botones, text="Guardar cliente", command=self.guardar_cliente)
        self.btn_guardar.pack(side="left", padx=5)

        self.btn_nuevo = ctk.CTkButton(botones, text="Nuevo", command=self.limpiar_cliente)
        self.btn_nuevo.pack(side="left", padx=5)

        self.btn_credito = ctk.CTkButton(botones, text="Agregar crédito", command=self.agregar_credito)
        self.btn_credito.pack(side="left", padx=5)

        self.btn_pago = ctk.CTkButton(botones, text="Registrar pago", command=self.registrar_pago)
        self.btn_pago.pack(side="left", padx=5)

        panel = ctk.CTkFrame(contenedor, fg_color="transparent")
        panel.pack(side="right", fill="both", expand=True)

        self.tabla_clientes = ttk.Treeview(
            panel,
            columns=("id", "nombre", "telefono", "saldo"),
            show="headings",
            height=10
        )
        self.tabla_clientes.heading("id", text="ID")
        self.tabla_clientes.heading("nombre", text="Cliente")
        self.tabla_clientes.heading("telefono", text="Teléfono")
        self.tabla_clientes.heading("saldo", text="Saldo")
        self.tabla_clientes.column("id", width=50, anchor="center")
        self.tabla_clientes.column("nombre", width=200)
        self.tabla_clientes.column("telefono", width=120)
        self.tabla_clientes.column("saldo", width=100, anchor="center")
        self.tabla_clientes.pack(fill="both", expand=True)
        self.tabla_clientes.bind("<<TreeviewSelect>>", self.seleccionar_cliente)

        self.tabla_cuentas = ttk.Treeview(
            self,
            columns=("id", "saldo", "estado", "descripcion"),
            show="headings",
            height=8
        )
        self.tabla_cuentas.heading("id", text="Cuenta")
        self.tabla_cuentas.heading("saldo", text="Saldo")
        self.tabla_cuentas.heading("estado", text="Estado")
        self.tabla_cuentas.heading("descripcion", text="Descripción")
        self.tabla_cuentas.column("id", width=80, anchor="center")
        self.tabla_cuentas.column("saldo", width=100, anchor="center")
        self.tabla_cuentas.column("estado", width=100, anchor="center")
        self.tabla_cuentas.column("descripcion", width=250)
        self.tabla_cuentas.pack(fill="x", padx=20, pady=(10, 20))

    def limpiar_cliente(self):
        self.customer_id_selected = None
        self.account_id_selected = None
        self.nombre_entry.delete(0, "end")
        self.telefono_entry.delete(0, "end")
        self.documento_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.direccion_entry.delete(0, "end")
        self.btn_guardar.configure(text="Guardar cliente")
        self.tabla_clientes.selection_remove(self.tabla_clientes.selection())
        self.cargar_cuentas_cliente(None)

    def guardar_cliente(self):
        nombre = self.nombre_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        documento = self.documento_entry.get().strip()
        email = self.email_entry.get().strip()
        direccion = self.direccion_entry.get().strip()

        if not nombre:
            messagebox.showwarning("Validación", "El nombre del cliente es obligatorio.")
            return

        try:
            if self.customer_id_selected is None:
                CustomerController.crear(nombre, telefono, documento, email, direccion)
                messagebox.showinfo("Cliente", "Cliente creado correctamente.")
            else:
                cliente = CustomerController.obtener_por_id(self.customer_id_selected)
                if cliente is None:
                    raise ValueError("Cliente no encontrado.")
                cliente.nombre = nombre
                cliente.telefono = telefono
                cliente.documento = documento
                cliente.email = email
                cliente.direccion = direccion
                from database.database import SessionLocal
                db = SessionLocal()
                try:
                    db.add(cliente)
                    db.commit()
                finally:
                    db.close()
                messagebox.showinfo("Cliente", "Cliente actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.limpiar_cliente()
        self.cargar_clientes()

    def seleccionar_cliente(self, event):
        seleccionado = self.tabla_clientes.focus()
        if not seleccionado:
            return

        datos = self.tabla_clientes.item(seleccionado)["values"]
        self.customer_id_selected = datos[0]
        self.nombre_entry.delete(0, "end")
        self.nombre_entry.insert(0, self._cliente_por_id(self.customer_id_selected).nombre)
        self.telefono_entry.delete(0, "end")
        self.telefono_entry.insert(0, self._cliente_por_id(self.customer_id_selected).telefono or "")
        self.documento_entry.delete(0, "end")
        self.documento_entry.insert(0, self._cliente_por_id(self.customer_id_selected).documento or "")
        self.email_entry.delete(0, "end")
        self.email_entry.insert(0, self._cliente_por_id(self.customer_id_selected).email or "")
        self.direccion_entry.delete(0, "end")
        self.direccion_entry.insert(0, self._cliente_por_id(self.customer_id_selected).direccion or "")
        self.btn_guardar.configure(text="Actualizar cliente")
        self.cargar_cuentas_cliente(self.customer_id_selected)

    def _cliente_por_id(self, cliente_id):
        return CustomerController.obtener_por_id(cliente_id)

    def cargar_clientes(self):
        for fila in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(fila)

        clientes = CustomerController.listar()
        for cliente in clientes:
            saldo = CustomerController.obtener_saldo_cliente(cliente.id)
            self.tabla_clientes.insert(
                "",
                "end",
                values=(cliente.id, cliente.nombre, cliente.telefono or "-", f"C$ {saldo:.2f}")
            )

    def cargar_cuentas_cliente(self, cliente_id):
        for fila in self.tabla_cuentas.get_children():
            self.tabla_cuentas.delete(fila)

        if cliente_id is None:
            return

        cuentas = CustomerController.listar_cuentas_por_cliente(cliente_id)
        for cuenta in cuentas:
            self.tabla_cuentas.insert(
                "",
                "end",
                values=(cuenta.id, f"C$ {cuenta.saldo:.2f}", cuenta.estado, cuenta.descripcion or "-")
            )

    def agregar_credito(self):
        if self.customer_id_selected is None:
            messagebox.showwarning("Cliente", "Seleccione un cliente primero.")
            return

        monto = simpledialog.askfloat("Crédito", "Ingrese el monto del crédito:", minvalue=0.01)
        if monto is None:
            return

        descripcion = simpledialog.askstring("Descripción", "Descripción del crédito (opcional):") or ""

        try:
            cuenta = CustomerController.agregar_credito(self.customer_id_selected, monto, descripcion)
            messagebox.showinfo("Crédito", f"Crédito registrado correctamente. Saldo actual: C$ {cuenta.saldo:.2f}")
            self.cargar_clientes()
            self.cargar_cuentas_cliente(self.customer_id_selected)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def registrar_pago(self):
        if self.customer_id_selected is None:
            messagebox.showwarning("Cliente", "Seleccione un cliente primero.")
            return

        cuentas = CustomerController.listar_cuentas_por_cliente(self.customer_id_selected)
        if not cuentas:
            messagebox.showwarning("Cuenta", "Este cliente no tiene cuentas de crédito.")
            return

        cuenta_id = self.tabla_cuentas.focus()
        if not cuenta_id:
            cuenta = cuentas[-1]
        else:
            cuenta = next(
                (c for c in cuentas if str(c.id) == self.tabla_cuentas.item(cuenta_id)["values"][0]),
                cuentas[-1]
            )

        monto = simpledialog.askfloat("Pago", "Ingrese el monto del abono:", minvalue=0.01)
        if monto is None:
            return

        descripcion = simpledialog.askstring("Descripción", "Descripción del pago (opcional):") or ""

        try:
            movimiento = CustomerController.registrar_pago(cuenta.id, monto, descripcion)
            messagebox.showinfo("Pago", f"Pago registrado correctamente. Monto: C$ {movimiento.monto:.2f}")
            self.cargar_clientes()
            self.cargar_cuentas_cliente(self.customer_id_selected)
        except Exception as e:
            messagebox.showerror("Error", str(e))
