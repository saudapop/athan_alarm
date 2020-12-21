**Requirements:**
python3, pip, nodejs, npm

optional: docker

### install

NOTE: Use python 3.6.8. I tried newer versions like python3.8 and 3.9 and they cause annoying issues that aren't worth spending time on.

-   Create and activate your python virtual environment then `pip install -r requirements.txt`

** Build front-end deps **

-   `cd client && npm ci`
-   `npm run build`

** Start the app **

-   `cd .. && cd server && python app.py`

### Development

#### Docker:

Just run `make dev` and go to http://localhost
When you're done ,`CTRL + C` and then run `make teardown`

#### Manually:

To run in development mode simply run `npm start` from the client directory(`cd client && npm start`) in a separate window while the app is running (activate python virtual env and then from the server directory`python app.py`) and go to http://localhost:5000.

The front end uses ParcelJS to pakcakge the front end and will watch the files for changes and should reload the browser automatically.
