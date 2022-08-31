from fastapi import FastAPI, Request

from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from camera import VideoCamera


app = FastAPI()
templates = Jinja2Templates(directory="templates")


async def fake_video_streamer():
    for i in range(10):
        yield b"some fake video bytes"
        
def generate(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.get("/")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    # return StreamingResponse(generate())
    return StreamingResponse(generate(VideoCamera()), media_type="multipart/x-mixed-replace;boundary=frame")

@app.get("/camera")
async def read_item(request: Request):
    return templates.TemplateResponse("camera.html", {"request": request})
