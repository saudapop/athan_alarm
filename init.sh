cd server;
printf "\n\nAssalamualaikum wa rahmatullahi wa barakatuhu \nالسَّلاَمُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ\n\n\n"

printf "Would you like the python virtual environment to be created for you?\nIf not, make sure you are in a virtual environment and have the requirements installed\n\n(Enter y or n)\n"
read SHOULD_CREATE_PYTHON_ENV
printf "\n"

if [ $SHOULD_CREATE_PYTHON_ENV = "y" ]
then
  	printf "Please enter the desired path (e.g '~/.envs'). Press enter to default to this folder. \n"
	read PATH_TO_ENVS
	printf "\n"
	printf "Creating python virtual environment\n\n"
	pip install virtualenv;
	virtualenv $PATH_TO_ENVS athan-app-venv;
	touch ./athan-app-venv/pip.conf && printf "[install]\ntrusted-host = pypi.org\nindex-url = https://pypi.org/simple" > athan-app-venv/pip.conf
	source ./athan-app-venv/bin/activate;
	pip install -r requirements.txt;
fi

######################################################################
######################################################################
######################################################################

printf "\n\n\n"
printf "Lets fetch prayer times for the year and create JSON files in a folder called 'prayer_times'\n\nWe'll use this for scheduling each daily prayer but before we do that we need the latitude and longitude coordinates\n\n";
printf "Please visit https://www.latlong.net/ to find your coordinates\n\n\n"

printf "What is your latitude?\n\n"
read VAR_LAT
printf "\n"

printf "what is your longitude?\n\n"
read VAR_LONG
printf "\n"

python3 fetch_prayer_times.py --LAT $VAR_LAT --LONG $VAR_LONG;

printf "\n\n Installing client side dependencies and building the front end."
cd ../client;
npm i;
npm run build;
cd ../server;
python3 app.py;
