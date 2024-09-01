# Most recent video titles

## Prerequisites
You will need to have <a href="https://www.docker.com/products/docker-desktop/">docker installed</a>.

## How To Run

To run the application locally, once Docker is installed, run this command from the backend_video folder to deploy with Docker compose.

```
$ docker-compose up -- build
[+] Building 10.0s (14/14) FINISHED
...
Attaching to spotter-container, spotter-postgres-container
```

After the application starts, navigate to `http://localhost:8000` in your web browser to verify it is running.

If you want to create a superuser for django, you can run this command to create an admin user.

```
$ docker exec -it spotter-container python manage.py createsuperuser
```
You can also run this command in the django container exec to add an admin user instead.

```
python manage.py createsuperuser
```
This superuser will allow you to open the admin panel to add and manage videos: `http://localhost:8000/admin`

You can also directly access the API directly: `http://localhost:8000/api/docs`

Once you are done, you can stop and remove the containers using this command.
```
$ docker compose down
```

## Description

Spotter is starting a new service that offers YouTubers personalized video title suggestions
leveraging Large Language Models (LLM). To achieve this, we need access to the 5 most
recently uploaded videos from a YouTuber upon their registration for the service. Registration
grants us their channel ID, which enables us to retrieve their latest video uploads via the
YouTube Data API.

Additionally, we maintain a database table that archives millions of channels and their respective
videos.

### Endpoint implementations:

Implement the get_most_recent_videos endpoint
This endpoint is designed to return the 5 most recent videos for a given channel. If the channel
is already in the database table, we will retrieve the latest videos from there. Otherwise, we'll
fetch them using the YouTube Data API. Additionally, any videos obtained from the YouTube
Data API will be stored in the database table for future reference.
Optimizing performance is important for this endpoint; we aim to ensure the quickest possible
response time.
Feel free to select any programming language, framework, and database that best suits your
preferences. Design the database schema according to the requirements and load some
sample data for testing purposes. Upon completion, please dump the database into a sql script
and include it along with your code.
Use the attached json file to simulate fetching data from YouTube Data API.
Input parameters: channel_id
Return: a list of most recent 5 videos' title

