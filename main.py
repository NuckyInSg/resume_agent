import os
import json
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.pdf2json import pdf2json
from src.json2tex import json_to_latex
import subprocess

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 定义文件路径
INPUT_DIR = "input"
OUTPUT_DIR = "output"
INPUT_PDF = os.path.join(INPUT_DIR, "original.pdf")
INPUT_JSON = os.path.join(INPUT_DIR, "original.json")
OUTPUT_TEX = os.path.join(OUTPUT_DIR, "output.tex")
OUTPUT_PDF = os.path.join(OUTPUT_DIR, "output.pdf")
HEADER_TEX = "src/header_eng.tex"

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # 确保目录存在
        os.makedirs(INPUT_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # 保存上传的文件
        with open(INPUT_PDF, "wb") as buffer:
            buffer.write(await file.read())

        logger.info(f"Input PDF saved: {INPUT_PDF}")

        # 步骤 1: 转换 PDF 到 JSON
        pdf2json(INPUT_PDF, INPUT_JSON)

        # 读取生成的JSON文件
        with open(INPUT_JSON, 'r') as f:
            json_data = json.load(f)

        return JSONResponse(content=json_data)

    except Exception as e:
        logger.exception("An error occurred during file processing")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
async def generate_pdf(json_data: dict = Body(...)):
    try:
        logger.info("Received request to generate PDF")

        # 保存JSON数据到文件
        with open(INPUT_JSON, 'w') as f:
            json.dump(json_data, f)

        # 转换 JSON 到 LaTeX
        json_to_latex(INPUT_JSON, OUTPUT_TEX, HEADER_TEX)

        # 读取生成的LaTeX文件
        with open(OUTPUT_TEX, 'r', encoding='utf-8') as f:
            latex_content = f.read()

        # 编译 LaTeX 到 PDF
        logger.info("Running pdflatex command")
        result = subprocess.run(
            ["pdflatex", "-output-directory", OUTPUT_DIR, OUTPUT_TEX],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info(f"pdflatex stdout: {result.stdout}")
        logger.info(f"pdflatex stderr: {result.stderr}")

        # 检查输出文件是否存在
        if not os.path.exists(OUTPUT_PDF):
            logger.error(f"Output PDF file not found: {OUTPUT_PDF}")
            logger.error(f"Directory contents: {os.listdir(OUTPUT_DIR)}")
            raise HTTPException(status_code=500, detail="Failed to generate output PDF.")

        logger.info(f"PDF generated successfully: {OUTPUT_PDF}")
        return FileResponse(OUTPUT_PDF, filename="converted_resume.pdf")

    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to compile LaTeX to PDF: {e.stdout}\n{e.stderr}")
        raise HTTPException(status_code=500, detail=f"Failed to compile LaTeX to PDF: {e.stderr}")
    except Exception as e:
        logger.exception("An error occurred during PDF generation")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
