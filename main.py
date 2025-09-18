# main.py
import tkinter as tk
from tkinter import scrolledtext, filedialog
from PIL import Image, ImageTk
from core import neural
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

def analyze_query(query_widget, output_area, plot_frame):
    query = query_widget.get("1.0", tk.END).strip()
    if not query:
        output_area.config(state='normal')
        output_area.insert(tk.END, "(ANNA: Please enter a scientific query)\n")
        output_area.config(state='disabled')
        return

    output_area.config(state='normal')
    output_area.insert(tk.END, f"\nQuery: {query}\nANNA Response:\n")
    output_area.config(state='disabled')

    response, analysis_data = neural.reason(query)

    # Print text response
    output_area.config(state='normal')
    output_area.insert(tk.END, f"{response}\n")
    output_area.see(tk.END)
    output_area.config(state='disabled')

    # Show heatmap if DataFrame is returned
    if isinstance(analysis_data, pd.DataFrame):
        show_heatmap(analysis_data, plot_frame, output_area)

def upload_file(query_widget):
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if file_path:
        query_widget.delete("1.0", tk.END)
        query_widget.insert(tk.END, f"analyze file {file_path}")

def show_heatmap(df, plot_frame, output_area):
    # Clear previous plot
    for widget in plot_frame.winfo_children():
        widget.destroy()

    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) < 2:
        return

    corr = df[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
    cax = ax.matshow(corr, cmap="coolwarm")
    fig.colorbar(cax)

    ticks = np.arange(len(corr.columns))
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(corr.columns, rotation=90)
    ax.set_yticklabels(corr.columns)

    # Clickable cells
    def on_click(event):
        if event.inaxes == ax:
            i = int(round(event.ydata))
            j = int(round(event.xdata))
            if 0 <= i < len(corr.columns) and 0 <= j < len(corr.columns):
                col1, col2 = corr.columns[i], corr.columns[j]
                value = corr.iloc[i, j]
                output_area.config(state='normal')
                output_area.insert(tk.END, f"\n(Insight) {col1} ↔ {col2} correlation = {value:.2f}\n")
                output_area.see(tk.END)
                output_area.config(state='disabled')

                # Show plot depending on column types
                show_data_plot(df, col1, col2)

    fig.canvas.mpl_connect("button_press_event", on_click)

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def show_data_plot(df, col1, col2):
    plot_window = tk.Toplevel()
    plot_window.title(f"Data Plot: {col1} vs {col2}")
    plot_window.geometry("600x500")

    fig, ax = plt.subplots(figsize=(6,5), dpi=100)

    col1_is_numeric = pd.api.types.is_numeric_dtype(df[col1])
    col2_is_numeric = pd.api.types.is_numeric_dtype(df[col2])

    if col1_is_numeric and col2_is_numeric:
        # Scatter plot for numeric-numeric
        ax.scatter(df[col1], df[col2], color='darkblue', alpha=0.7)
        ax.set_xlabel(col1)
        ax.set_ylabel(col2)
        ax.set_title(f"{col1} vs {col2} Scatter Plot")
    else:
        # Bar plot for categorical (or mixed)
        # Use counts of value combinations
        counts = df.groupby([col1, col2]).size().unstack(fill_value=0)
        counts.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')
        ax.set_xlabel(col1)
        ax.set_ylabel("Count")
        ax.set_title(f"{col1} vs {col2} Occurrences")
        ax.legend(title=col2, bbox_to_anchor=(1.05, 1), loc='upper left')

    ax.grid(True)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def main():
    root = tk.Tk()
    root.title("ANNA: Autonomous Scientific Advisor")
    root.geometry("1200x800")

    # Background image
    try:
        bg_image = Image.open(os.path.join("C:/ANNA/assets", "background.png")).resize((1200, 800))
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(root, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Background load failed: {e}")

    # Layout frames
    main_frame = tk.Frame(root, bg="white", bd=2, relief="sunken")
    main_frame.place(x=20, y=20, width=560, height=740)

    plot_frame = tk.Frame(root, bg="white", bd=2, relief="sunken")
    plot_frame.place(x=600, y=20, width=580, height=740)

    # Query input
    tk.Label(main_frame, text="Enter your scientific query:", bg="white", fg="black",
             font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 0))

    query_input = scrolledtext.ScrolledText(main_frame, height=4, bg="white", fg="black",
                                            font=("Arial", 12), bd=1, relief="solid")
    query_input.pack(fill="x", padx=10, pady=5)

    # Buttons
    button_frame = tk.Frame(main_frame, bg="white")
    button_frame.pack(pady=5)

    tk.Button(button_frame, text="Analyze Query", bg="#0b1f5b", fg="white",
              font=("Arial", 12, "bold"),
              command=lambda: analyze_query(query_input, output_area, plot_frame)).pack(side="left", padx=5)

    tk.Button(button_frame, text="Upload CSV", bg="#0b1f5b", fg="white",
              font=("Arial", 12, "bold"),
              command=lambda: upload_file(query_input)).pack(side="left", padx=5)

    # Output area
    output_area = scrolledtext.ScrolledText(main_frame, height=30, state='disabled',
                                            bg="white", fg="black", font=("Arial", 12),
                                            bd=1, relief="solid")
    output_area.pack(fill="both", padx=10, pady=5, expand=True)

    query_input.bind("<Return>", lambda e: (analyze_query(query_input, output_area, plot_frame), "break"))

    root.mainloop()

if __name__ == "__main__":
    main()
