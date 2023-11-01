import uvicorn

from app.root.app import create_app

app = create_app()


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
