import tkinter as tk
from tkinter import scrolledtext, filedialog
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
from core import navigator, neural

# --- Analysis and Calculation ---
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

    response = navigator.execute_action(
        action_callable=neural.reason,
        action_description=f"Analyze scientific query: '{query}'",
        query=query
    )

    output_area.config(state='normal')
    output_area.insert(tk.END, f"{response}\n")
    output_area.see(tk.END)
    output_area.config(state='disabled')

# --- CSV Upload & Plot ---
def upload_file(output_area, plot_frame):
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    try:
        df = pd.read_csv(file_path)
        summary, correlations, insights = neural.analyze_dataframe(df)

        output_area.config(state='normal')
        output_area.insert(tk.END, "\nData summary:\n")
        output_area.insert(tk.END, f"{summary}\n")
        output_area.insert(tk.END, "\nInsights:\n")
        for insight in insights:
            output_area.insert(tk.END, f"{insight}\n")
        output_area.config(state='disabled')

        # Plot numeric columns
        for widget in plot_frame.winfo_children():
            widget.destroy()

        numeric_cols = df.select_dtypes(include="number").columns
        if numeric_cols.any():
            fig, ax = plt.subplots(figsize=(5,4))
            df[numeric_cols].hist(ax=ax)
            plt.tight_layout()
            plt.savefig("plot.png")
            plt.close(fig)

        output_area.config(state='normal')
        output_area.insert(tk.END, f"Plot saved as 'plot.png'\n")
        output_area.config(state='disabled')

    except Exception as e:
        output_area.config(state='normal')
        output_area.insert(tk.END, f"ANNA Error reading file: {e}\n")
        output_area.config(state='disabled')

# --- Main GUI ---
def main():
    root = tk.Tk()
    root.title("ANNA: Autonomous Scientific Advisor")
    root.geometry("800x700")

    # Background image
    try:
        bg_image = Image.open("background.png")
        bg_photo = ImageTk.PhotoImage(bg_image.resize((800,700)))
        bg_label = tk.Label(root, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except:
        pass

    # Main frame
    main_frame = tk.Frame(root, bg="#f0f0f0")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(main_frame, text="Enter your scientific query:", bg="#f0f0f0",
             fg="black", font=("Consolas", 12)).pack(anchor="w")
    query_input = scrolledtext.ScrolledText(main_frame, height=4)
    query_input.pack(fill="x", pady=5)

    analyze_button = tk.Button(main_frame, text="Analyze Query",
                               command=lambda: analyze_query(query_input, output_area, plot_frame))
    analyze_button.pack(pady=5)

    upload_button = tk.Button(main_frame, text="Upload CSV for Analysis",
                              command=lambda: upload_file(output_area, plot_frame))
    upload_button.pack(pady=5)

    output_area = scrolledtext.ScrolledText(main_frame, height=20, state='disabled')
    output_area.pack(fill="both", pady=5, expand=True)

    plot_frame = tk.Frame(main_frame, bg="#f0f0f0")
    plot_frame.pack(fill="both", pady=5, expand=True)

    # Submit on Enter
    def submit_on_enter(event):
        analyze_query(query_input, output_area, plot_frame)
        return "break"
    query_input.bind("<Return>", submit_on_enter)

    root.mainloop()

if __name__ == "__main__":
    main()
