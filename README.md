# 🚀 Resume Agent
This project provides a FastAPI-based web service that converts PDF resumes to JSON, then to LaTeX format, and finally generates a new PDF.

## 🌟 Features

- 📤 Upload PDF files
- 🔄 Convert PDF to JSON
- ✏️ Edit JSON data
- 📝 Generate LaTeX from JSON
- 📄 Compile LaTeX to PDF

## Prerequisites

- Python 3.7+
- FastAPI
- pdflatex

## 🛠️ Installation and Usage

### Using Docker

1. Clone the repository:
   ```
   git clone https://github.com/NuckyInSg/resume_agent
   cd resume_agent
   ```

2. Set environment variables:
   ```
   export ANTHROPIC_API_KEY="your_actual_api_key"
   export ANTHROPIC_API_URL="your_actual_api_url"
   ```

3. Build and run the Docker container:
   ```
   chmod +x build.sh && ./build.sh
   ```

4. Access the web interface at `http://localhost:8000`

### Manual Installation

1. Clone the repository:
   ```
   git clone https://github.com/NuckyInSg/resume_agent
   cd resume_agent
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install pdflatex on your system.
   ```
   # macOS
   brew install --cask basictex
   # Linux
   sudo apt-get install texlive-full
   
   export PATH="/Library/TeX/texbin:$PATH"
   ```

4. Start the server:
   ```
   python main.py
   ```

5. Access the web interface at `http://localhost:8000`

## Usage

1. Upload a PDF file
2. Edit the JSON data if needed
3. Generate the new PDF

## 🔗 API Endpoints

- `POST /upload`: Upload a PDF file
- `POST /generate`: Generate PDF from JSON data
- `GET /`: Serve the main HTML page

## 📁 Project Structure

- `input/`: Directory for input files
- `output/`: Directory for output files
- `src/`: Source code directory
  - `pdf2json.py`: PDF to JSON conversion
  - `json2tex.py`: JSON to LaTeX conversion
  - `header_eng.tex`: LaTeX header template
- `static/`: Static files for the web interface
- `main.py`: Main FastAPI application

