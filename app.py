import os
import customtkinter as ctk
from tkinter import filedialog
from ffmpeg import FFmpeg
from CTkMessagebox import CTkMessagebox

class App(ctk.CTk):
	def __init__(self):
		super().__init__()

		# Reference to ffmpeg class
		self.FFmpeg = FFmpeg()

		self.title('Video Converter')

		# Variables for storing inout/output
		self.input_file = ctk.StringVar()
		self.output_dir = ctk.StringVar()
		self.output_file = ctk.StringVar()
		self.operation_var = ctk.StringVar(value='compress')

		self.create_widgets()


	def create_widgets(self):
		# Choose file
		input_label = ctk.CTkLabel(self, text="Input File:")
		input_label.grid(row=0, column=0, padx=10, pady=10)

		input_entry = ctk.CTkEntry(self, textvariable=self.input_file, width=300)
		input_entry.grid(row=0, column=1, padx=10, pady=10)

		input_button = ctk.CTkButton(self, text="Browse", command=self.choose_file)
		input_button.grid(row=0, column=2, padx=10, pady=10)
		
		# Choose output
		output_label = ctk.CTkLabel(self, text="Output File Name:")
		output_label.grid(row=1, column=0, padx=10, pady=10)

		output_entry = ctk.CTkEntry(self, textvariable=self.output_file, width=300)
		output_entry.grid(row=1, column=1, padx=10, pady=10)

		self.output_extension_label = ctk.CTkLabel(self, text=".mp4")
		self.output_extension_label.grid(row=1, column=2, padx=10, pady=10)
		
		# Select Operation
		operation_label = ctk.CTkLabel(self, text="Operation:")
		operation_label.grid(row=2, column=0, padx=10, pady=10)

		operation_options = ["compress", "audio_only", "compress_no_audio"]

		operation_menu = ctk.CTkOptionMenu(self, variable=self.operation_var, values=operation_options, command=self.update_extension)
		operation_menu.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
		
		# Convert button
		start_button = ctk.CTkButton(self, text="Start Conversion", command=self.start_conversion)
		start_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)


	def choose_file(self):
		file_path = filedialog.askopenfilename()

		if file_path:
			self.input_file.set(file_path)
			# Get dir from input file
			self.output_dir.set(os.path.dirname(file_path))
	

	def update_extension(self, *args):
		operation = self.operation_var.get()

		if operation == 'audio_only':
			self.output_extension_label.configure(text=".mp3")
		else:
			self.output_extension_label.configure(text=".mp4")

	def start_conversion(self):
		input_file_path = self.input_file.get()
		output_file_name = self.output_file.get() or os.path.splitext(os.path.basename(input_file_path))[0]
		operation = self.operation_var.get()


		if not input_file_path:
			CTkMessagebox(title="Input Error", message="Please choose a file")
			return
	
		output_extension = ".mp3" if operation == 'audio_only' else ".mp4"
		output_file_path = os.path.join(self.output_dir.get(), f"{output_file_name}{output_extension}")
		self.FFmpeg.run_ffmpeg(input_file_path, output_file_path, operation)
