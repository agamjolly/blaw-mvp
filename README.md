# Berkeley Law MVP

Simple API-based MVP for the seating chart app at UC Berkeley School of Law. The app can be accessed (as of 7/1) [here](http://agamjolly.me). 

## API Scopes

The mock API is deployed on the endpoint http://agamjolly.me/api/v1/. If you make a single `GET` request (or try to access the link from your browser), you will be able to view the entire mock database. For specific data, you can make a `POST` request to the endpoint with a raw JSON body that looks something like the follows:

```json
{
     "key": "YOUR_KEY_HERE"
}
```

You can change `YOUR_KEY_HERE` with three parameters that the API currently supports: 

1. `admins` will show you a list of all admins available in the database.
2. `instructors` will give you a list of all instructors, with all classes they’re teaching this semester and details about every student in each class that an instructor should need.
3. `students` should give you a list of all students. 

The mock API has been designed with a noSQL database in such a way that a call to this endpoint should be enough to structure everything on to the three final pages for instructors, students and admins. 

## Useful Docker Commands

Making a Docker image using the Dockerfile.

`docker build -t blaw-mvp .`

Running the Docker image on port 80. 

`docker run -p 80:80 blaw-mvp`

Stopping all Docker containers.

`docker stop $(docker ps -aq)`

Deleting all Docker containers.

`docker rm $(docker ps -aq)`

Running the Docker image until stopped.

`docker run -d --restart unless-stopped -p 80:80 blaw-mvp`
