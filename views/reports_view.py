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
        self.total_neto_label = ctk.CTkLabel(resumen, text="Total neto: C$ 0.00")
        self.total_neto_label.pack(side="left", padx=10)
        ctk.CTkButton(
            resumen,
            text="Actualizar",
            width=110,
            command=self.cargar_ventas
        ).pack(side="right", padx=10)

        filtro_frame = ctk.CTkFrame(self, fg_color="transparent")
        filtro_frame.pack(fill="x", padx=25, pady=(10, 0))

        self.filtro_var = ctk.StringVar(value="Últimos 7 días")

        ctk.CTkLabel(filtro_frame, text="Rango:").pack(side="left", padx=(0, 8))

        self.filtro_combo = ctk.CTkOptionMenu(
            filtro_frame,
            values=["Últimos 7 días", "Mes actual", "Personalizado"],
            variable=self.filtro_var,
            command=self.cambiar_filtro
        )
        self.filtro_combo.pack(side="left", padx=(0, 12))

        self.fecha_inicio_entry = ctk.CTkEntry(filtro_frame, placeholder_text="YYYY-MM-DD")
        self.fecha_inicio_entry.pack(side="left", padx=4)

        ctk.CTkLabel(filtro_frame, text="a").pack(side="left", padx=6)

        self.fecha_fin_entry = ctk.CTkEntry(filtro_frame, placeholder_text="YYYY-MM-DD")
        self.fecha_fin_entry.pack(side="left", padx=4)

        ctk.CTkButton(
            filtro_frame,
            text="Aplicar",
            command=self.aplicar_filtro
        ).pack(side="left", padx=(8, 0))

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

        ctk.CTkLabel(
            self,
            text="📅 Reporte diario",
            text_color=GOLD,
            font=("Arial", 20, "bold")
        ).pack(pady=(10, 5))

        self.tabla_diaria = ttk.Treeview(
            self,
            columns=("fecha", "ventas", "total_dia"),
            show="headings"
        )
        self.tabla_diaria.heading("fecha", text="Fecha")
        self.tabla_diaria.heading("ventas", text="Ventas")
        self.tabla_diaria.heading("total_dia", text="Total del día")
        self.tabla_diaria.column("fecha", width=170, anchor="center")
        self.tabla_diaria.column("ventas", width=120, anchor="center")
        self.tabla_diaria.column("total_dia", width=180, anchor="e")
        self.tabla_diaria.pack(fill="x", expand=False, padx=25, pady=(0, 20))

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

        self.aplicar_filtro()

    def cambiar_filtro(self, valor):
        if valor == "Últimos 7 días":
            self.fecha_inicio_entry.delete(0, "end")
            self.fecha_fin_entry.delete(0, "end")
            self.aplicar_filtro()
            return

        if valor == "Mes actual":
            self.fecha_inicio_entry.delete(0, "end")
            self.fecha_fin_entry.delete(0, "end")
            self.aplicar_filtro()
            return

        self.fecha_inicio_entry.focus_set()

    def aplicar_filtro(self):
        seleccion = self.filtro_var.get()

        if seleccion == "Últimos 7 días":
            reporte = SaleController.reporte_ultimos_dias(7)
        elif seleccion == "Mes actual":
            reporte = SaleController.reporte_mes_actual()
        else:
            inicio = self.fecha_inicio_entry.get().strip()
            fin = self.fecha_fin_entry.get().strip()

            if not inicio or not fin:
                reporte = SaleController.reporte_diario()
            else:
                try:
                    from datetime import datetime
                    inicio_date = datetime.strptime(inicio, "%Y-%m-%d").date()
                    fin_date = datetime.strptime(fin, "%Y-%m-%d").date()
                except ValueError:
                    messagebox.showwarning("Reportes", "Las fechas deben tener el formato YYYY-MM-DD.")
                    return

                if fin_date < inicio_date:
                    messagebox.showwarning("Reportes", "La fecha final no puede ser menor a la inicial.")
                    return

                reporte = SaleController.reporte_por_rango(inicio_date, fin_date)

        self._render_reporte_diario(reporte)

    def _render_reporte_diario(self, reporte):
        for fila in self.tabla_diaria.get_children():
            self.tabla_diaria.delete(fila)

        total_neto = 0.0
        for item in reporte:
            total_neto += item["total_dia"]
            self.tabla_diaria.insert(
                "", "end", values=(
                    item["fecha"],
                    item["cantidad_ventas"],
                    f"C$ {item['total_dia']:.2f}"
                )
            )

        self.total_neto_label.configure(text=f"Total neto: C$ {total_neto:.2f}")

    def ver_recibo(self):
        seleccionado = self.tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Reportes", "Seleccione una venta.")
            return

        from views.recibo_view import ReciboView

        venta = SaleController.obtener_venta(int(seleccionado))
        if venta is not None:
            ReciboView(self, venta)
