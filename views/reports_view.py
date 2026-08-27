import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.sale_controller import SaleController
from brand import CREAM, GOLD


class ReportsView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color=CREAM)
        self.crear_vista()
        self.cargar_ventas()

    def crear_vista(self):
        ctk.CTkLabel(
            self,
            text="📊 Reportes de ventas",
            text_color=GOLD,
            font=("Arial", 28, "bold")
        ).pack(pady=20)

        resumen = ctk.CTkFrame(self, fg_color="transparent")
        resumen.pack(fill="x", padx=25)
        self.total_label = ctk.CTkLabel(resumen, text="Total histórico: C$ 0.00")
        self.total_label.pack(side="left", padx=10)
        self.cantidad_label = ctk.CTkLabel(resumen, text="Ventas: 0")
        self.cantidad_label.pack(side="left", padx=10)
        ctk.CTkButton(
            resumen,
            text="Actualizar",
            width=110,
            command=self.cargar_ventas
        ).pack(side="right", padx=10)

        self.tabla = ttk.Treeview(
            self,
            columns=("id", "fecha", "total"),
            show="headings"
        )
        self.tabla.heading("id", text="Venta")
        self.tabla.heading("fecha", text="Fecha")
        self.tabla.heading("total", text="Total")
        self.tabla.column("id", width=100, anchor="center")
        self.tabla.column("fecha", width=240)
        self.tabla.column("total", width=180, anchor="e")
        self.tabla.pack(fill="both", expand=True, padx=25, pady=20)

        ctk.CTkButton(
            self,
            text="Ver recibo seleccionado",
            command=self.ver_recibo
        ).pack(pady=(0, 20))

    def cargar_ventas(self):
        ventas = SaleController.listar()
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        total = 0
        for venta in ventas:
            total += venta.total
            self.tabla.insert(
                "", "end", iid=str(venta.id), values=(
                    venta.id,
                    venta.fecha.strftime("%d/%m/%Y %H:%M"),
                    f"C$ {venta.total:.2f}"
                )
            )

        self.total_label.configure(text=f"Total histórico: C$ {total:.2f}")
        self.cantidad_label.configure(text=f"Ventas: {len(ventas)}")

    def ver_recibo(self):
        seleccionado = self.tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Reportes", "Seleccione una venta.")
            return

        from views.recibo_view import ReciboView

        venta = SaleController.obtener_venta(int(seleccionado))
        if venta is not None:
            ReciboView(self, venta)
