# Altered TCG Deck Calculator

## Prerequisites
You will need to have <a href="https://www.docker.com/products/docker-desktop/">docker installed</a>.

## How To Run

To run the application locally, once Docker is installed, run this command from the altered folder to deploy with Docker compose.

```
$ docker-compose up -- build
[+] Building 10.0s (14/14) FINISHED
...
Attaching to altered-container, altered-postgres-container
```

After the application starts, navigate to `http://localhost:8000` in your web browser to verify it is running.

If you want to create a superuser for django, you can run this command to create an admin user.

```
$ docker exec -it altered-container python manage.py createsuperuser
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