from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from movies import movies, get_rating

templates = Jinja2Templates(directory="templates", auto_reload=True)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.get("/")
def index():
    return RedirectResponse(app.url_path_for("dashboard_page"))


@app.get("/home")
def dashboard_page(request: Request):
    featured = [movie for movie in movies if movie.featured]
    featured.sort(key=get_rating, reverse=True)
    return templates.TemplateResponse("dashboard.html", {"request": request, "featured_movies": featured})


@app.get("/movies")
def movies_page(request: Request):
    return templates.TemplateResponse("movies.html", {"request": request, "movies": movies})


@app.get("/movies/{slug}")
def movie_page(request: Request, slug: str):
    movie = [movie for movie in movies if movie.slug == slug][0]
    return templates.TemplateResponse("movie.html", {"request": request, "movie": movie})
