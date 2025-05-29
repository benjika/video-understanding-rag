from fastapi import FastAPI
from app.api.routes import router
import gradio as gr
from app.front.front_main import create_gradio_interface

app = FastAPI()
app.include_router(router)
gradio_app = create_gradio_interface()
app = gr.mount_gradio_app(app, gradio_app, path="/gradio")