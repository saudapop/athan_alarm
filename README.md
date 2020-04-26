**Requirements:**
Docker
or
python3, nodejs, npm (for manual install)

### Recommended install

#### `./init.sh`

This interactive method will:

- optionally create a python virtual environment
- prompt for the coordinates of your location from https://www.latlong.net/

and then handle building the rest of the application for you. Once it is done. The application should be available at http://localhost:5000

### Manual install

** Get Prayer Times **

- Create and activate your python virtual environment then `pip install -r requirements.txt`
- Fetch your coordinates from https://www.latlong.net/
- run `cd server && python fetch_prayer_times.py --LAT <YOUR_LATITUDE> --LONG <YOUR_LONGITUDE>`

** Build front-end deps **

- `cd .. && cd client && npm i`
- `npm run build`

** Start the app **

- `cd .. && cd server && python app.py`

### Development

To run in development mode simply run `npm start` from the client directory(`cd client && npm start`) in a separate window while the app is running (activate python virtual env and then from the server directory`python app.py`).
**NOTE:** After building it will say the app is running on `localhost:1234`, don't go to that. It will not have the same origin as the python app and requests will not work as expected. Instead go to http://localhost:5000 as provided by the python app.

The front end uses ParcelJS and will watch the files for changes and should reload the browser automatically.
