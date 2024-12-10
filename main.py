import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
from TTS.utils.synthesizer import Synthesizer
from TTS.utils.io import download_model
from pydub import AudioSegment
from io import BytesIO

# Initialize the synthesizer with a pre-trained model
def initialize_synthesizer():
    model_path, config_path, _ = download_model("tts_models/en/ljspeech/tacotron2-DDC")
    synthesizer = Synthesizer(model_path, config_path, None)
    return synthesizer

# Function to convert text to speech and save it directly as an MP3 file
def text_to_speech():
    text = text_entry.toPlainText().strip()  # Get the text from QTextEdit
    
    if not text:
        # Show error message if no text is entered
        QMessageBox.critical(window, "Input Error", "Please enter some text!")
        return
    
    # Synthesize speech
    synthesizer = initialize_synthesizer()
    wav = synthesizer.tts(text)
    
    # Convert wav to mp3 in-memory
    audio_output_path = "output.mp3"
    
    # Save the wav audio to an in-memory BytesIO object
    wav_file = BytesIO(wav)
    audio = AudioSegment.from_wav(wav_file)
    
    # Export as mp3
    audio.export(audio_output_path, format="mp3")
    
    # Show success message
    QMessageBox.information(window, "Success", f"Speech saved to {audio_output_path}")

# Create the PyQt5 application and window
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Text to Speech")

# Set up layout
layout = QVBoxLayout()

# Create a label for the text entry
text_entry_label = QLabel("Enter Text:")
layout.addWidget(text_entry_label)

# Create a QTextEdit widget for text input
text_entry = QTextEdit()
layout.addWidget(text_entry)

# Create a convert button
convert_button = QPushButton("Convert to Speech")
convert_button.clicked.connect(text_to_speech)  # Connect button click to function
layout.addWidget(convert_button)

# Set the layout on the window
window.setLayout(layout)

# Show the window
window.show()

# Run the application
sys.exit(app.exec_())
