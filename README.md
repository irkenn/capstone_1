# Spotify Comments Web App

Visit the site [here](http://spotify-comments-web-app.herokuapp.com/)

## General description

A site that communicates with [Spotify's API](https://developer.spotify.com/documentation/web-api), and allows users to search from Spotify's catalog and create [threads](#threads) about [Spotify's content](#spotify-content). These threads can also have comments from other users in order to start a discussion about music content.

## Implemented features

1. Authentication process: form validation and data encryption with the use of WTForms and bcrypt.

2. Personal user profile creation page: user info can be edited or deleted, users can check other user's activity in the platform. 

2. Communication with an External API: Information is obtained from Spotify's catalog, the authentication process is done automatically, tokens are renewed if they are required so. Images and relevant information is displayed on the site based on the type of item that is requested.  via API communication, but also from the site's own database.

3. Caching of information: Spotify's information is cached once a thread is done. Nested information is also saved accordingly.For example in the case of a track, the site will cache the artist/s that made track, and the album to which the track belongs in its respective tables.


2. Interconnected database models: Multiple information can be retrieved from a single query. By selecting a user, all the threads and comment that the user has made can be accessed. If a Spotify Item is selected, all the different threads from different users can be accesesed, database schema design can be found in [here](docs/Schema_design_Spotify_Comments.pdf).

## User flow




From there it will extract the necesary data used to show a thumbnail image, the name of each item, it's Spotify ID, and some other extra information.

User's are able to retrieve this information via a form in the /search/API/ route and searching through keywords and item type.

The user can search all the main items from Spotify's API base on the keywords they type, this JSON information is passed directly from an API request and renderd in the page, only until a user starts a thread about the Spotify item. The app will cache the Spotify item, depending if it's a Artist, Album or Track. In the case of Albums or Tracks, this items will need also the caching of more elements in the database. For example if the Artist that made the Album is not found in the database, the app will also cached the Artist. The same will happen if while caching a Track, the Artist or Album asociated with the Track are not found in the database the app will search and cache them as well. Every Spotify item stored in the database will be registered in the table "spotify_content", which will associate the spotify id with the type of item that belongs to (Artist, Album, Track), this is also connected to the tables of each type of item and based on that the query is made.

The app also requires users to register an email and password. Only logged in users are able to search for Spotify content, start threads and make comments. There are functions that can modify the user's info to a certain extent or delete the user.

Once a user logs in, the app will show the latest 5 threads that were created in the app, it will also show the user's own activity, whether it is a new thread or any comment in any thread. When a user clicks in another user, the app will show that user's latest activity, which is very similar to the own user home page except it will not show the latest 5 threads. Following the same way, if a Spotify item is clicked the app will show all the Threads about that specific item.

The process to use the page is to regiter of log in, the user id is stored in the session as SPOTIFY_COMMENTS_USER_KEY and also the user object is stored and pass as the g (global object) in flask. 
Onche the authentication is done, the user is directed to the homepage, in this page the app will show the latest threads that were created in the app, and also the onw user's latest activity. 
From here the user can click in the nav bar to log out, edit/delete the user or search specific threads about the Spotify items or and start a thread about the selected Spotify content. If the user is using a large screen the search field will show instead a search input for the user to go directly from any page to the search threads.

### Spotify Content
Artist, Albums or Tracks taken from Spotify's catalog
It will retrieve information as JSON data related to three main items: Artists, Albums and Tracks.


### Threads
: The app uses flask as the main web framework in which all the routes are stablished. The forms are created using WTForms, the authentication process is handed by individual handlers. The database models and the queries are made using SQL Alchemy, and all the templates used to build the app front end are done using jinja2 to create dynamic elements based upon the type of object or kind of item that is sent. The style of the HTML is done mainly with bootstrap with the help of CSS and also in several occasions the page uses JavaScript and AXIOS to add comment forms, send requests and create comment instances in the threads.

#### API adress: **<https://api.spotify.com/v1>**
#### Site address: **<https://spotify-comments-web-app.herokuapp.com>**