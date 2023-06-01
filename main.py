from typing import Optional
from tkinter import filedialog, messagebox
from pathlib import Path
from tkinter import ttk

import tkinter as tk



class Notepad(tk.Tk):
	def __init__(self)->None:
		super().__init__()
		
		self.title("untitled - Notepad Plus")
		self.geometry("800x500")
		
		
		# Crear la barra de menus
		
		self.menubar = tk.Menu()
		self.filemenu = tk.Menu(tearoff=False)
		self.filemenu.add_command(label="Nuevo", command=self.new_file)
		self.filemenu.add_command(label="Abrir", command=self.open)
		self.filemenu.add_command(label="Guardar", command=self.save)
		self.filemenu.add_command(label="Guardar como...", command=self.save_as)
		
		self.menubar.add_cascade(menu=self.filemenu, label="Archivo")
		self.config(menu=self.menubar)
		
		self.text = tk.Text()
		
		# Configuramos para que se expanda el TextInput
		self.text.pack(expand=True, fill=tk.BOTH)
		
		
		# El atributo `current_file` contiene la ruta del archivo
        # que se está editando actualmente o `None` si aún no se
        # ha guardado el archivo.
	
		self.current_file: Optional[Path] = None
		
		self.filetypes: tuple[tuple[str, str], ...] = (
			("Archivo de texto", "*.txt"),
			("Todos los archivos", "*.*")
		)
		
		# Remplazar el mecanismo de cierre
		
		self.protocol("WM_DELETE_WINDOW", self.close)
		
	def close(self)->None:
		if not self.can_continue():
			return
		
		# Si no se cumple lo anterior se cierra el programa
		self.destroy()


	def set_current_file(self, current_file: Path)->None:
		self.current_file = current_file
		
		self.title(self.current_file.name+" - Notepad Plus")
		
	def can_continue(self)->bool:
		if self.text.edit_modified():
			result = messagebox.askyesnocancel(
				title="Existen cambios sin guardar",
				message="¿Desea guardar el archivo actual antes de continuar?"
			)
			
			cancel = result is None
			save_before  = result is True
			
			if cancel:
				return False
			
			elif save_before:
				self.save()
			
			return True
		
		return True

	
	def new_file(self)->None:
		if not self.can_continue:
			return
			
		self.text.delete("1.0", tk.END)
		self.current_file = None
		self.title(f"untitled - Notepad Plus")
		
	
	def open(self)->None:
		filename = filedialog.askopenfilename(filetypes=self.filetypes)
		if not filename or not self.can_continue:
			return
		
		# Aqui eliminamos el texto anterior e insertamos el del nuevo
		
		self.text.delete("1.0", tk.END)
		file = Path(filename)
		self.text.insert("1.0", file.read_text("utf-8"))
		
		# Reiniciamos el estado del texto al insertar uno nuevo
		
		self.text.edit_modified(False)
		self.set_current_file(file)
		
	def save_current_file(self)->None:
		if self.current_file is None:
			return
	
		self.current_file.write_text(self.text.get("1.0", tk.END), "utf-8")
		
	def save(self):
		if self.current_file is None:
			self.save_as()
			return
		self.save_current_file()
		
	def save_as(self):
		filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=self.filetypes)
		
		if not filename:
			return
		
		self.set_current_file(Path(filename))
		self.save_current_file()
			


notepad = Notepad()
notepad.mainloop()		
		
			
			
