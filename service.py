from fastapi import FastAPI
from pydantic import BaseModel
import linkify  # your existing functions live here

app = FastAPI(title="Link Service")

class Req(BaseModel):
    pdf_url: str
    sitemap_url: str
    link_density: int = 500
    anchor_style: str = "exact_or_synonym"

@app.post("/linkify")
async def run(req: Req):
    html = linkify.insert_links(
        linkify.pdf_to_text(req.pdf_url),
        linkify.get_sitemap_links(req.sitemap_url)
    )
    return {"html": html, "link_count": html.count("<a ")}
