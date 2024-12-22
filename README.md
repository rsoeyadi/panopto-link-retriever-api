# Panopto Link Retriever

The frontend is accessible at [panopto.vercel.app](https://panopto.vercel.app)

This is a FastAPI backend that parses through Juilliard event links so students/staff can quickly retrieve their performance recordings. On Juilliard's event pages, when a livestream is over, the video seemingly disappears, but I noticed it's hidden in the HTML. This API utilizes Selenium and BeautifulSoup to parse through that HTML and retrieve the links. It exposes a single API endpoint, `/submit-url`, which accepts a POST request with a JSON payload containing the `url` field.

The frontend validates the input, communicates with this API, and displays the retrieved Panopto link if available, along with error handling for invalid URLs or unavailable recordings.
