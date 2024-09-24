from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
from util import *


class Mp3_tag_data(BaseModel):
    url:str
    title: str
    album: str
    artist: str
    genre: str
    year: str


app = FastAPI()

# origins = [
#     "http://localhost:63342",
#     "http://localhost:63342/",
#     "http://localhost",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/quote")
# async def quote():
#     return {"quote": "the sky above the port was the color of television tuned to a dead channel. 22"}



@app.post("/submit-tag-data")
async def submit_tag_data(data: Mp3_tag_data):
    code = generate_code()
    dl_audio(code,data.url)
    tag(code,data.title, data.artist, data.album, data.genre, data.year)
    path = f"audiofiles/mp3s/{code}.mp3"
    if(os.path.exists("audiofiles/temp/rm.webm")):
        os.remove("audiofiles/temp/rm.webm")
    if(os.path.exists("audiofiles/temp/rm.m4a")):
        os.remove("audiofiles/temp/rm.m4a")
    return FileResponse(path, media_type='audio/mpeg', filename='file.mp3')


@app.get("/cleanup")
async def cleanup():
    return {"status": str(cleanup())}
        
@app.get("/quote")
async def quote():
    # pass
    # TODO: make sure this works
    quote = get_quote()
    print(quote[0], "\n", quote[1])
    # return {quote[0], quote[1]}
    return {"quote": quote[0], "author": quote[1]}

