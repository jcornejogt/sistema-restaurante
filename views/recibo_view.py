import os
import sys
import customtkinter as ctk
from tkinter import messagebox


def get_recibos_dir():

    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(base_dir)

    carpeta = os.path.join(base_dir, "recibos")

    os.makedirs(carpeta, exist_ok=True)

    return carpeta


class ReciboView(ctk.CTkToplevel):

    def __init__(self, master, venta):
        super().__init__(master)

        self.venta = venta
        self.ruta_archivo = None

        self.title(f"Recibo #{venta['id']}")
        self.geometry("380x520")
        self.resizable(False, False)

        self.grab_set()

        self.crear_vista()

    def crear_vista(self):

        ctk.CTkLabel(
            self,
            text="🍽️ Sistema Restaurante",
            font=("Arial", 20, "bold")
        ).pack(pady=(15, 0))

        ctk.CTkLabel(
            self,
            text=f"Recibo #{self.venta['id']}",
            font=("Arial", 16)
        ).pack()

        ctk.CTkLabel(
            self,
            text=self.venta["fecha"].strftime("%d/%m/%Y %H:%M"),
            font=("Arial", 14)
        ).pack(pady=(0, 10))

        caja = ctk.CTkTextbox(
            self,
            width=340,
            height=310
        )

        caja.pack(padx=15, pady=5)

        texto = self.generar_texto()

        caja.insert("0.0", texto)
        caja.configure(state="disabled")

        botones = ctk.CTkFrame(self, fg_color="transparent")
        botones.pack(pady=10)

        ctk.CTkButton(
            botones,
            text="💾 Guardar",
            width=110,
            command=self.guardar
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            botones,
            text="🖨️ Imprimir",
            width=110,
            command=self.imprimir
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            botones,
            text="Cerrar",
            width=110,
            fg_color="gray",
            command=self.destroy
        ).pack(side="left", padx=5)

    def generar_texto(self):

        lineas = []

        lineas.append("=" * 34)
        lineas.append("     SISTEMA RESTAURANTE")
        lineas.append("=" * 34)
        lineas.append(f"Recibo #: {self.venta['id']}")
        lineas.append(f"Fecha: {self.venta['fecha'].strftime('%d/%m/%Y %H:%M')}")
        lineas.append("-" * 34)
        lineas.append(f"{'Producto':<16}{'Cant':>4}{'Subt.':>10}")
        lineas.append("-" * 34)

        for item in self.venta["items"]:

            nombre = item["producto_nombre"][:16]

            lineas.append(
                f"{nombre:<16}{item['cantidad']:>4}"
                f"{item['subtotal']:>10.2f}"
            )

        lineas.append("-" * 34)
        lineas.append(f"{'TOTAL:':<20}C$ {self.venta['total']:>9.2f}")
        lineas.append("=" * 34)
        lineas.append("     ¡Gracias por su visita!")

        return "\n".join(lineas)

    def guardar_archivo(self):
        """Guarda el .txt en disco (si no se ha guardado ya) y devuelve la ruta."""

        if self.ruta_archivo and os.path.exists(self.ruta_archivo):
            return self.ruta_archivo

        carpeta = get_recibos_dir()

        nombre_archivo = f"recibo_{self.venta['id']}.txt"

        ruta = os.path.join(carpeta, nombre_archivo)

        with open(ruta, "w", encoding="utf-8") as f:
            f.write(self.generar_texto())

        self.ruta_archivo = ruta

        return ruta

    def guardar(self):

        ruta = self.guardar_archivo()

        messagebox.showinfo(
            "Recibo guardado",
            f"Se guardó en:\n{ruta}"
        )

    def imprimir(self):

        ruta = self.guardar_archivo()

        try:

            os.startfile(ruta, "print")

        except Exception as e:

            messagebox.showerror(
                "Error al imprimir",
                f"No se pudo enviar a imprimir automáticamente.\n\n"
                f"Puedes abrir el archivo manualmente aquí:\n{ruta}\n\n"
                f"Detalle: {e}"
            )