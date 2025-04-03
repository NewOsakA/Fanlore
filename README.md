# FanLore
FanLore is a web-based community platform dedicated to fan-based content where users can share, create, and collaborate on their favorite fandoms.

## 1. Clone the repository
Run this in your terminal
```
https://github.com/KunKid-cmd/FanLore.git
```
## 2. Navigate to the project directory
```commandline
cd Fanlore
```
## 3. Create a virtual environment
```commandline
python -m venv myenv
```
## 4. Activate the Virtual environment
For Mac/Linux
```commandline
source myenv/bin/activate
```
For Windows
```commandline
.\myenv\Scripts\activate
```
## 5. Install requirements
```
pip install -r requirements.txt
```
## 6. Create your own .env file
In the `sample.env` file, we have provided everything necessary to run the file,
So you can duplicate and rename it to `.env`
### To create a .env file in terminal
For Mac/Linux
```commandline
cp sample.env .env
```
For windows
```commandline
copy sample.env .env
```

<br>You'll have to create your own neon.tech Postgre database and Cloudinary to connect with the application<br>
You'll also have to create a API and Service credential in Google Cloud Console to be able to use the OAuth system<br>
Follow these tutorial, you only have to get values for your .env <br>
[neon.tech Postgre database](https://www.youtube.com/watch?v=kvIK2NpuF2I) <br>
[Cloudinary tutorial]() <br><br>
Google OAuth Admin Setting:

* Go to admin page and add this sites
```
http://127.0.0.1:8000
```
* Open your setting file and make sure that ```SITE_ID``` match the Sites ID in the database <br><br>

* Then add Social Application with these value
    * Provider : ```Google```
    * Name : ```Google API```
    * Client id : ```{YOUR_CLIENT_ID}```
    * Secret key: ```{YOUR_CLIENT_SECRET}```
    * Sites: ```http://127.0.0.1:8000```<br>
  
## 7. Migrate
```commandline
python manage.py migrate
```

## 8. Run tests
```commandline
python manage.py test
```

## 9. Run Application
```commandline
python manage.py runserver
```
