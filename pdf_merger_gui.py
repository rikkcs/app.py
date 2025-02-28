import tkinter as tk
from tkinter import filedialog, ttk
from pdf_merger import merge_pdfs, process_folder
import os
from tkinter import messagebox

class PDFMergerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Unione PDF")
        self.root.geometry("800x400")
        self.test_suffix = tk.StringVar(value="_test")
        self.notest_suffix = tk.StringVar(value="_notest")
        self.insert_blank = tk.BooleanVar(value=True)
        self.file_pairs = []  # Initialize file_pairs list
        self.setup_gui()

    def setup_gui(self):
        # Create menubar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Create Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Configuration", command=self.show_settings)

        # Main content frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Center buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(expand=True, fill='both')

        # Create inner frame for buttons to center them
        inner_buttons_frame = ttk.Frame(buttons_frame)
        inner_buttons_frame.place(relx=0.5, rely=0.05, anchor='n')  # Reduced from 0.1 to 0.05

        # Add folder selection buttons centered
        btn_select = ttk.Button(inner_buttons_frame, text="Seleziona Cartella", command=self.select_folder)
        btn_select.pack(side='left', padx=5)

        btn_add_folder = ttk.Button(inner_buttons_frame, text="Aggiungi Altra Cartella", command=self.add_folder)
        btn_add_folder.pack(side='left', padx=5)

        # Create treeview to display file pairs
        self.tree = ttk.Treeview(main_frame, columns=('Test File', 'No Test File', 'Output File'), show='headings')
        self.tree.heading('Test File', text='Test File')
        self.tree.heading('No Test File', text='No Test File')
        self.tree.heading('Output File', text='Output File')
        self.tree.pack(pady=(20,10), fill='both', expand=True)  # Reduced top padding from 50 to 20

        # Add scrollbar to treeview
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Add merge button
        self.merge_button = ttk.Button(main_frame, text="Unisci PDF", command=self.merge_selected_files)
        self.merge_button.pack(pady=10)
        self.merge_button.config(state='disabled')

    def show_settings(self):
        # Create settings dialog
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Configurazione")
        settings_window.geometry("400x200")
        settings_window.transient(self.root)
        settings_window.grab_set()

        # Center the window relative to the main window
        settings_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - settings_window.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - settings_window.winfo_height()) // 2
        settings_window.geometry(f"+{x}+{y}")
        # Settings frame
        settings_frame = ttk.LabelFrame(settings_window, text="Configurazione Suffissi", padding="10")
        settings_frame.pack(pady=10, padx=10, fill='x')

        # Test suffix configuration
        ttk.Label(settings_frame, text="Suffisso Testalino:", anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(settings_frame, textvariable=self.test_suffix).grid(row=0, column=1, padx=5, pady=5)

        # No-test suffix configuration
        ttk.Label(settings_frame, text="Suffisso No Testalino:", anchor="w").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(settings_frame, textvariable=self.notest_suffix).grid(row=1, column=1, padx=5, pady=5)

        # Blank page checkbox
        ttk.Checkbutton(settings_frame, text="Inserisci pagina bianca", variable=self.insert_blank).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Close button
        ttk.Button(settings_window, text="Chiudi", command=settings_window.destroy).pack(pady=10)

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            # Clear existing items before showing new selection
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.file_pairs = []  # Reset file pairs
            self.show_file_pairs(folder_selected)

    def add_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.show_file_pairs(folder_selected)

    def show_file_pairs(self, directory):
        test_suffix = self.test_suffix.get()
        notest_suffix = self.notest_suffix.get()
        
        for root, _, files in os.walk(directory):
            test_files = [f for f in files if f.endswith(f'{test_suffix}.pdf')]
            notest_files = [f for f in files if f.endswith(f'{notest_suffix}.pdf')]

            for test_file in test_files:
                base_name = test_file.replace(f'{test_suffix}.pdf', '')
                notest_file = f'{base_name}{notest_suffix}.pdf'
                
                if notest_file in notest_files:
                    test_path = os.path.join(root, test_file)
                    notest_path = os.path.join(root, notest_file)
                    output_path = os.path.join(root, f'{base_name}.pdf')
                    
                    self.file_pairs.append((test_path, notest_path, output_path))
                    self.tree.insert('', 'end', values=(test_file, notest_file, f'{base_name}.pdf'))

        if self.file_pairs:
            self.merge_button.config(state='normal')
        else:
            self.merge_button.config(state='disabled')

    def merge_selected_files(self):
        for test_path, notest_path, output_path in self.file_pairs:
            merge_pdfs(test_path, notest_path, output_path, self.insert_blank.get())
            print(f'Creato: {output_path}')
        
        # Show completion message
        tk.messagebox.showinfo("Completato", "Tutti i PDF sono stati uniti con successo!")

    def run(self):
        self.root.mainloop()