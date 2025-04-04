# FanLore

**FanLore** is a web-based community platform for fandom lovers to create,
share, and collaborate on fan-based content.  
Users can create events, post creative works, earn achievements, and explore
fandoms together.

---

## Getting Started

Follow these steps to set up the project locally.

---

### 1. Clone the Repository

```bash
git clone https://github.com/KunKid-cmd/FanLore.git
```

### 2. Navigate to the project directory

```bash
cd Fanlore
```

### 3. Create a virtual environment

```bash
python -m venv myenv
```

### 4. Activate the Virtual environment

For Mac/Linux

```bash
source myenv/bin/activate
```

For Windows

```bash
.\myenv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Environment Setup

We provide a `sample.env` file with all necessary environment variables.
Create your own .env file by copying it:

### To create a .env file in terminal

For Mac/Linux

```bash
cp sample.env .env
```

For windows

```bash
copy sample.env .env
```

### 7. Setup Required Services

You'll need the following services to run the app properly:

* A PostgreSQL database
  via [neon.tech Postgre database](https://www.youtube.com/watch?v=kvIK2NpuF2I)
* A Cloudinary account for media
  uploads [Cloudinary tutorial](https://cloudinary.com/documentation/python_quickstart)
* A Google Cloud Console project to enable OAuth login

---

[Google OAuth Setup](https://dev.to/odhiambo/integrate-google-oauth2-social-authentication-into-your-django-web-app-1bk5)

1) Go to your Google Cloud Console and set the authorized domain to:

```cpp
http://127.0.0.1:8000
```

2) In your Django Admin panel:

* Set ```SITE_ID``` in your ```settings.py``` to match the `Site ID` shown in
  the Sites model in the database.

* Add a new Social Application with the following values:
    * Provider : ```Google```
    * Name : ```Google API```
    * Client id : ```{YOUR_CLIENT_ID}```
    * Secret key: ```{YOUR_CLIENT_SECRET}```
    * Sites: ```http://127.0.0.1:8000```

### 8. Database Setup (first time only)

Run the following commands to set up your database for the first time:

```bash
python manage.py makemigrations
```

and then

```bash
python manage.py migrate
```

### 9. Run tests

```commandline
python manage.py test
```

### 10. Start the Development Server

```commandline
python manage.py runserver
```

Then open your browser and go to:
[http://127.0.0.1:8000](http://127.0.0.1:8000)
