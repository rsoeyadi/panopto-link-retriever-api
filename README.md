# Panopto Link Retriever

The frontend is accessible at [panopto.vercel.app](https://panopto.vercel.app)

This is a FastAPI backend to parse through Juilliard event links so students/staff can quickly retrieve their performance recordings. On Juilliard's event pages, when a livestream is over, the video seemingly disappears, but I noticed it's hidden in the HTML. This API utilizes Selenium and BeautifulSoup to parse through that HTML and retrieve the links. It exposes a single API endpoint, `/submit-url`, which accepts a POST request with a JSON payload containing the `url` field.

This is an application that consists of a FastAPI backend and a React frontend built with Vite. It is designed to retrieve Panopto video links from Juilliard event pages. The backend is powered by FastAPI and utilizes Selenium and BeautifulSoup to scrape Panopto links from Juilliard event pages. It exposes a single API endpoint, `/submit-url`, which accepts a POST request with a JSON payload containing the `url` field. The frontend validates the input, communicates with this API, and displays the retrieved Panopto link if available, along with error handling for invalid URLs or unavailable recordings.
