import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class FinanzasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Ingresos y Gastos")
        self.root.geometry("800x550")
        self.root.configure(bg="#FFF3E0")

        self.total_ingresos = 0
        self.total_gastos = 0

        # ====== 🔲 CASILLA 1: REGISTRO ======
        frame_registro = tk.LabelFrame(root, text="Registro de Transacción",
                                       bg="#FFE0B2", font=("Arial", 11, "bold"))
        frame_registro.pack(fill="x", padx=15, pady=10)

        tk.Label(frame_registro, text="Descripción:", bg="#FFE0B2").grid(row=0, column=0, padx=5, pady=5)
        self.descripcion = tk.Entry(frame_registro, width=20)
        self.descripcion.grid(row=0, column=1, padx=5)

        tk.Label(frame_registro, text="Monto:", bg="#FFE0B2").grid(row=0, column=2, padx=5)
        self.monto = tk.Entry(frame_registro, width=10)
        self.monto.grid(row=0, column=3, padx=5)

        tk.Label(frame_registro, text="Tipo:", bg="#FFE0B2").grid(row=0, column=4, padx=5)
        self.tipo = ttk.Combobox(frame_registro,
                                 values=["Ingreso", "Gasto"],
                                 state="readonly",
                                 width=10)
        self.tipo.grid(row=0, column=5, padx=5)
        self.tipo.current(0)

        tk.Button(frame_registro,
                  text="Agregar",
                  bg="#FFB74D",
                  fg="white",
                  command=self.agregar).grid(row=0, column=6, padx=10)

        # ====== 🔲 CASILLA 2: LISTA ======
        frame_lista = tk.LabelFrame(root, text="Lista de Movimientos",
                                    bg="#FFE0B2", font=("Arial", 11, "bold"))
        frame_lista.pack(fill="both", expand=True, padx=15, pady=10)

        self.tabla = ttk.Treeview(frame_lista,
                                  columns=("Descripción", "Monto", "Tipo", "Fecha y Hora"),
                                  show="headings")
        self.tabla.pack(fill="both", expand=True, pady=5)

        self.tabla.heading("Descripción", text="Descripción")
        self.tabla.heading("Monto", text="Monto")
        self.tabla.heading("Tipo", text="Tipo")
        self.tabla.heading("Fecha y Hora", text="Fecha y Hora")

        tk.Button(frame_lista,
                  text="Eliminar Seleccionado",
                  bg="#E57373",
                  fg="white",
                  command=self.eliminar).pack(pady=5)

        # ====== 🔲 CASILLA 3: RESUMEN ======
        frame_resumen = tk.LabelFrame(root, text="Resumen Financiero",
                                      bg="#FFE0B2", font=("Arial", 11, "bold"))
        frame_resumen.pack(fill="x", padx=15, pady=10)

        self.label_ingresos = tk.Label(frame_resumen,
                                       text="Total Ingresos: $0",
                                       font=("Arial", 12, "bold"),
                                       bg="#FFE0B2")
        self.label_ingresos.pack()

        self.label_gastos = tk.Label(frame_resumen,
                                     text="Total Gastos: $0",
                                     font=("Arial", 12, "bold"),
                                     bg="#FFE0B2")
        self.label_gastos.pack()

        self.label_balance = tk.Label(frame_resumen,
                                      text="Balance: $0",
                                      font=("Arial", 14, "bold"),
                                      fg="#E65100",
                                      bg="#FFE0B2")
        self.label_balance.pack(pady=5)

    # ===== FUNCIONES =====

    def agregar(self):
        descripcion = self.descripcion.get()
        monto_texto = self.monto.get()
        tipo = self.tipo.get()

        if not descripcion or not monto_texto:
            messagebox.showerror("Error", "Complete todos los campos")
            return

        try:
            monto = float(monto_texto)
        except ValueError:
            messagebox.showerror("Error", "Monto inválido")
            return

        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if tipo == "Ingreso":
            self.total_ingresos += monto
        else:
            self.total_gastos += monto

        self.tabla.insert("", "end",
                          values=(descripcion, f"{monto:.2f}", tipo, fecha_hora))

        self.actualizar_totales()

        self.descripcion.delete(0, tk.END)
        self.monto.delete(0, tk.END)

    def eliminar(self):
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione una fila")
            return

        for item in seleccion:
            valores = self.tabla.item(item, "values")
            monto = float(valores[1])
            tipo = valores[2]

            if tipo == "Ingreso":
                self.total_ingresos -= monto
            else:
                self.total_gastos -= monto

            self.tabla.delete(item)

        self.actualizar_totales()

    def actualizar_totales(self):
        balance = self.total_ingresos - self.total_gastos

        self.label_ingresos.config(text=f"Total Ingresos: ${self.total_ingresos:.2f}")
        self.label_gastos.config(text=f"Total Gastos: ${self.total_gastos:.2f}")
        self.label_balance.config(text=f"Balance: ${balance:.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanzasApp(root)
    root.mainloop()
