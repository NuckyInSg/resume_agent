# 🚀 PDF to JSON to LaTeX Converter

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

## 🛠️ Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <project-directory>
   ```

2. Install dependencies:
   ```
   pip install fastapi uvicorn python-multipart
   ```

3. Ensure pdflatex is installed on your system.

## Usage

1. Start the server:
   ```
   python main.py
   ```

2. Access the web interface at `http://localhost:8000`

3. Upload a PDF file, edit the JSON data if needed, and generate the new PDF.

![Web Interface Screenshot](path/to/screenshot.jpg)

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

