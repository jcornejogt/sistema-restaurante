import customtkinter as ctk
from tkinter import messagebox, ttk

from brand import CREAM, DANGER, DANGER_HOVER, GOLD
from controllers.expense_controller import ExpenseController


class ExpensesView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color=CREAM)
        self.crear_vista()
        self.cargar_salidas()

    def crear_vista(self):
        ctk.CTkLabel(
            self, text="Salidas y gastos", text_color=GOLD,
            font=("Arial", 30, "bold")
        ).pack(pady=20)

        formulario = ctk.CTkFrame(self)
        formulario.pack(fill="x", padx=25, pady=5)

        ctk.CTkLabel(formulario, text="Concepto").grid(row=0, column=0, padx=8, pady=8)
        self.concepto_entry = ctk.CTkEntry(formulario, width=220)
        self.concepto_entry.grid(row=0, column=1, padx=8, pady=8)

        ctk.CTkLabel(formulario, text="Categoría").grid(row=0, column=2, padx=8, pady=8)
        self.categoria_entry = ctk.CTkEntry(formulario, width=160)
        self.categoria_entry.insert(0, "General")
        self.categoria_entry.grid(row=0, column=3, padx=8, pady=8)

        ctk.CTkLabel(formulario, text="Monto").grid(row=0, column=4, padx=8, pady=8)
        self.monto_entry = ctk.CTkEntry(formulario, width=120)
        self.monto_entry.grid(row=0, column=5, padx=8, pady=8)

        ctk.CTkLabel(formulario, text="Notas").grid(row=1, column=0, padx=8, pady=8)
        self.notas_entry = ctk.CTkEntry(formulario, width=220)
        self.notas_entry.grid(row=1, column=1, padx=8, pady=8)

        ctk.CTkButton(formulario, text="Registrar salida", command=self.registrar).grid(row=1, column=3, padx=8, pady=8)
        ctk.CTkButton(formulario, text="Limpiar", command=self.limpiar).grid(row=1, column=4, padx=8, pady=8)
        ctk.CTkButton(formulario, text="Eliminar seleccionada", fg_color=DANGER, hover_color=DANGER_HOVER, command=self.eliminar).grid(row=1, column=5, padx=8, pady=8)

        self.total_label = ctk.CTkLabel(self, text="Total registrado: C$ 0.00", font=("Arial", 20, "bold"))
        self.total_label.pack(anchor="w", padx=25, pady=(15, 0))

        self.tabla = ttk.Treeview(
            self, columns=("id", "fecha", "concepto", "categoria", "monto", "notas"), show="headings"
        )
        for columna, texto in (("id", "ID"), ("fecha", "Fecha"), ("concepto", "Concepto"), ("categoria", "Categoría"), ("monto", "Monto"), ("notas", "Notas")):
            self.tabla.heading(columna, text=texto)
        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("fecha", width=140, anchor="center")
        self.tabla.column("concepto", width=220)
        self.tabla.column("categoria", width=140)
        self.tabla.column("monto", width=120, anchor="e")
        self.tabla.column("notas", width=220)
        self.tabla.pack(fill="both", expand=True, padx=25, pady=20)

    def cargar_salidas(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        salidas = ExpenseController.listar()
        for salida in salidas:
            self.tabla.insert("", "end", iid=str(salida.id), values=(
                salida.id, salida.fecha.strftime("%d/%m/%Y %H:%M"), salida.concepto,
                salida.categoria, f"C$ {salida.monto:.2f}", salida.notas or ""
            ))
        self.total_label.configure(text=f"Total registrado: C$ {sum(s.monto for s in salidas):.2f}")

    def registrar(self):
        try:
            ExpenseController.crear(self.concepto_entry.get(), self.monto_entry.get(), self.categoria_entry.get(), notas=self.notas_entry.get())
        except ValueError as error:
            messagebox.showwarning("Salidas", str(error))
            return
        self.limpiar()
        self.cargar_salidas()
        messagebox.showinfo("Salidas", "Salida registrada correctamente.")

    def eliminar(self):
        seleccionado = self.tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Salidas", "Seleccione una salida.")
            return
        if messagebox.askyesno("Salidas", "¿Desea eliminar la salida seleccionada?"):
            ExpenseController.eliminar(int(seleccionado))
            self.cargar_salidas()

    def limpiar(self):
        for entry in (self.concepto_entry, self.monto_entry, self.notas_entry):
            entry.delete(0, "end")
        self.categoria_entry.delete(0, "end")
        self.categoria_entry.insert(0, "General")