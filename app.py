import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from markitdown import MarkItDown

app = FastAPI(title="Document to Markdown Parser Service")
md = MarkItDown()

@app.get("/")
def read_root():
    return {"status": "Parser service is running online"}

@app.post("/convert")
async def convert_file(file: UploadFile = File(...)):
    allowed_extensions = {'.pdf', '.docx', '.txt', '.pptx', '.xlsx', '.csv', '.html'}
    _, ext = os.path.splitext(file.filename.lower())
    
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type {ext}")

    # Create a unique temporary file path on disk
    temp_path = f"temp_{file.filename}"

    try:
        # 1. Stream the incoming upload directly to a temporary file
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 2. Convert using convert_local (which natively parses files from paths perfectly)
        result = md.convert_local(temp_path)
        
        return {"markdown": result.text_content}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
        
    finally:
        # 3. Always clean up the temporary file from your disk
        if os.path.exists(temp_path):
            os.remove(temp_path)