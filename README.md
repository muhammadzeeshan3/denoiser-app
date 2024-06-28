# Audio Enhancer Django Project

This Django project allows users to upload audio files, process them for enhancement, and display the original and enhanced audio along with their respective graphs.

## Features

- **Upload Audio**: Users can upload audio files (in various formats) through the web interface.
- **Enhance Audio**: Once uploaded, users can enhance the uploaded audio file.
- **Visual Representation**: Both the original and enhanced audio files are displayed with graphical representations.

## Technologies Used

- **Django**: Python web framework used for backend development.
- **HTML/CSS**: Frontend for user interface design.
- **JavaScript**: Client-side scripting for dynamic interactions.
- **REST API**: Used for communication between frontend and backend.
- **Bootstrap**: Used minimally for styling components.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/muhammadzeeshan3/denoiser-app.git
   cd denoiser
   ```

2. **Setup virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   Open your web browser and go to `http://127.0.0.1:8000/` to view the application.

## Usage

1. **Upload Audio**:
   - Click on the "Upload Audio" button to select an audio file from your local system.
   - Once selected, click on "Enhance Audio" to process the audio file.
   
2. **Enhance Audio**:
   - After uploading, the original audio and its graph will be displayed.
   - Upon enhancement, the enhanced audio and its graph will replace the original ones.