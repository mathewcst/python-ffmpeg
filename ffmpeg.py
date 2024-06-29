import subprocess
from CTkMessagebox import CTkMessagebox

class FFmpeg():
	def __init__(self):
		pass

	def run_ffmpeg(self, input_file, output_file, operation, callback) -> None:
		try:
			
			# Base FFmpeg commands
			command = ['ffmpeg', '-i', input_file]

			match(operation):
				case 'compress':
					command.extend(['-vcodec', 'h264'])
				case 'audio_only':
					command.extend(['-vn', '-acodec', 'libmp3lame', '-ab', '192k'])
				case 'compress_no_audio':
					command.extend(['-vcodec', 'h264', '-an'])
			
			# Add the output file to the command
			command.append(output_file)

			# Run the command
			result = subprocess.run(command, capture_output=True, text=True)

			callback(result)

		except Exception as e:
			CTkMessagebox(title='Error', message=f"An error occurred: {e}", icon="cancel", option_1="Ok")
