# Most recent video titles

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

