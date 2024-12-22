import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

load_dotenv()
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# FastAPI setup from the docs
app = FastAPI()
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def retrieve_panopto_link(link):
    try:
        # Set up Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        user_agent = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36')
        options.add_argument(f'user-agent={user_agent}')

        driver = webdriver.Chrome(options=options)
        driver.get(link)
        time.sleep(2.5)  # Wait for JavaScript to load content

        # Get the page source and parse it
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        driver.quit()

        # Look for the iframe inside the parent div
        parent_div = soup.find(id="panopto-video-player")
        if not parent_div:
            raise ValueError("Could not find 'panopto-video-player' div on the page.")

        # Check for iframe in the div
        if len(parent_div.contents) > 0:
            iframe = parent_div.contents[0]
            link = iframe.get('src')
            if not link:
                raise ValueError("Iframe 'src' attribute is missing.")
            return link
        else:
            raise ValueError("No iframe found in 'panopto-video-player' div.")
    except WebDriverException as e:
        logger.error(f"WebDriver error: {str(e)}")
        raise ValueError(f"WebDriver error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise ValueError(f"Unexpected error: {str(e)}")

class URLData(BaseModel):
    url: str

@app.post("/submit-url")
async def submit_url(data: URLData):
    url = data.url
    try:
        panopto_link = retrieve_panopto_link(url)
        return {"Panopto Link": panopto_link}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
