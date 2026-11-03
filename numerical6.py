# Import libraries for GUI and mathematical plotting
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define the differential equation from Problem 3(d)
# y' = sin(x) + e^(-x)
def f(x, y):
    return np.sin(x) + np.exp(-x)

# Initial conditions for 3(d)
X0 = 0.0
Y0 = 0.0
H = 0.05
X_END = 1.0

# Main evaluation function
def evaluate():
    tree.delete(*tree.get_children())
    
    # Setup initial values
    x_val, y_val = X0, Y0
    rows = [(0, f"{x_val:.2f}", f"{y_val:.4f}")]
    x_v, y_v = [x_val], [y_val]
    
    n = 0
    # Loop for 20 iterations using Euler's method
    while round(x_val, 5) < round(X_END, 5):
        # Euler Formula: y_{i+1} = y_i + h * f(x_i, y_i)
        y_next = y_val + H * f(x_val, y_val)
        
        # Step forward
        x_val += H
        y_val = y_next
        n += 1
        
        # Store results for table and plot
        rows.append((n, f"{x_val:.2f}", f"{y_val:.4f}"))
        x_v.append(x_val)
        y_v.append(y_val)

    # Configure Treeview table (Updated with Unicode Subscripts)
    cols = (("i", "i", 60), ("x", "xᵢ", 120), ("y", "yᵢ", 150))
    tree.config(columns=[c[0] for c in cols], height=7)
    for cid, title, w in cols:
        tree.heading(cid, text=title)
        tree.column(cid, width=w, anchor="center")

    # Insert data into the table
    for i, r in enumerate(rows):
        tree.insert("", "end", values=r, tags=('even' if i % 2 == 0 else 'odd',))

    # Display formulas and final result (Split into two labels for better spacing)
    lbl_formula_1.config(text="Euler Method: yᵢ₊₁ = yᵢ + h f(xᵢ, yᵢ)")
    lbl_formula_2.config(text=f"yᵢ₊₁ = yᵢ + {H}(sin(xᵢ) + e⁻ˣᵢ)")
    lbl_result.config(text=f"Final Approximation at x = {x_val:.2f}: y ≈ {y_val:.4f}")

    # Reveal results containers on first click
    if not table_frame.winfo_ismapped():
        table_frame.pack(pady=8, padx=25, fill="x", before=lbl_formula_1)
        plot_container.pack(fill="both", expand=True, padx=25, pady=(5, 20))
        root.geometry("640x840") 

    # Generate convergence plot
    plt.close('all')
    fig, ax = plt.subplots(figsize=(6, 2.5), dpi=100)
    fig.patch.set_facecolor('#1e1e2e')
    ax.set_facecolor('#313244')
    ax.tick_params(colors='#cdd6f4', labelsize=9)

    ax.plot(x_v, y_v, color='#89b4fa', marker='o', markersize=4, linewidth=2, label='Euler Solution')

    ax.set_title("Numerical Solution (Euler Method)", color='#cdd6f4', fontsize=11, fontweight='bold', pad=10)
    ax.set_xlabel("x", color='#cdd6f4', fontsize=10)
    ax.set_ylabel("y(x)", color='#cdd6f4', fontsize=10)
    ax.legend(facecolor='#1e1e2e', edgecolor='#45475a', labelcolor='#cdd6f4', fontsize=9, loc='upper left')
    ax.grid(color='#45475a', linestyle='--', linewidth=0.5, alpha=0.7)
    
    fig.tight_layout()

    # Draw plot on canvas
    for w in plot_container.winfo_children(): w.destroy()
    canvas = FigureCanvasTkAgg(fig, master=plot_container)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# GUI Setup 
root = tk.Tk()
root.title("ODE Solver - Sheet 6")
root.geometry("640x260")
root.configure(bg="#1e1e2e")

FNT, BG_CARD, FG_TXT = "Segoe UI", "#313244", "#cdd6f4"

tk.Label(root, text="Euler Method Calculator", font=(FNT, 17, "bold"), bg="#1e1e2e", fg=FG_TXT).pack(pady=(15, 2))
tk.Label(root, text="Sheet 6 - Problem 3(d)", font=(FNT, 11, "bold"), bg="#1e1e2e", fg="#89b4fa").pack(pady=(0, 2))
# Updated static label with Unicode Exponent
tk.Label(root, text="y' = sin(x) + e⁻ˣ  |  y(0) = 0  |  h = 0.05", font=("Consolas", 11, "bold"), bg="#1e1e2e", fg="#a6e3a1").pack(pady=(0, 15))

tk.Button(root, text="Generate Table & Plot", font=(FNT, 11, "bold"),
          bg="#89b4fa", fg="#11111b", activebackground="#b4befe",
          relief="flat", cursor="hand2", width=24, pady=6, command=evaluate).pack(pady=10)

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background=BG_CARD, foreground=FG_TXT, fieldbackground=BG_CARD, borderwidth=0, font=(FNT, 10), rowheight=26)
style.configure("Treeview.Heading", background="#181825", foreground=FG_TXT, font=(FNT, 10, "bold"), padding=4)
style.map("Treeview", background=[("selected", "#45475a")])

table_frame = tk.Frame(root, bg="#1e1e2e")
tree = ttk.Treeview(table_frame, show="headings")
tree.tag_configure('even', background="#313244")
tree.tag_configure('odd', background="#292a3a")
tree.pack(fill="x", expand=True)

lbl_formula_1 = tk.Label(root, text="", font=(FNT, 16, "bold"), bg="#1e1e2e", fg="#f38ba8", justify="center")
lbl_formula_1.pack(pady=(10, 3))

lbl_formula_2 = tk.Label(root, text="", font=(FNT, 16, "bold"), bg="#1e1e2e", fg="#f38ba8", justify="center")
lbl_formula_2.pack(pady=(0, 12)) 

lbl_result = tk.Label(root, text="", font=(FNT, 15, "bold"), bg="#1e1e2e", fg="#a6e3a1")
lbl_result.pack(pady=(0, 8))

plot_container = tk.Frame(root, bg="#1e1e2e")

root.mainloop()