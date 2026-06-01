from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import schemas, crud
from .database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FSTR Mountain Passes API",
    description="API для регистрации и модерации горных перевалов",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.post("/submitData", response_model=schemas.SubmitResponse, status_code=200)
async def submit_data(pass_data: schemas.PassCreate, db: Session = Depends(get_db)):
    if not pass_data.title or not pass_data.coords.latitude or not pass_data.coords.longitude:
        return schemas.SubmitResponse(status=400, message="Bad Request: missing required fields", id=None)
    if not pass_data.user.email:
        return schemas.SubmitResponse(status=400, message="Bad Request: user.email is required", id=None)
    try:
        success, message, pass_id = crud.DatabaseManager.submit_pass(db, pass_data)
        if success:
            return schemas.SubmitResponse(status=200, message=None, id=pass_id)
        return schemas.SubmitResponse(status=500, message=message, id=None)
    except Exception as e:
        return schemas.SubmitResponse(status=500, message=f"Ошибка подключения к базе данных: {str(e)}", id=None)

@app.get("/submitData/{pass_id}", response_model=schemas.PassRead)
def get_pass(pass_id: int, db: Session = Depends(get_db)):
    pass_obj = crud.DatabaseManager.get_pass_by_id(db, pass_id)
    if not pass_obj:
        raise HTTPException(status_code=404, detail="Перевал не найден")
    return pass_obj

@app.patch("/submitData/{pass_id}", response_model=schemas.UpdateResponse)
def update_pass(pass_id: int, pass_data: schemas.PassCreate, db: Session = Depends(get_db)):
    state, message = crud.DatabaseManager.update_pass(db, pass_id, pass_data)
    return {"state": state, "message": message}

@app.get("/submitData/", response_model=list[schemas.PassRead])
def get_passes_by_email(user__email: str = Query(..., description="Email пользователя"), db: Session = Depends(get_db)):
    return crud.DatabaseManager.get_passes_by_user_email(db, user__email)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)