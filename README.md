
Relay2App is a project in development that aims at pattern recognition in a semi-structured datasets.

The app is currently available in production using the following endpoints :
https://varunnsite.pythonanywhere.com
https://varunnsite.pythonanywhere.com/Console

The services are also available using REST APIs.
The app itself is made up of 2 parts - Relay2App as well as MangaDataProcessing System.
The ultimate Objective of the project is to identify patterns in semi-structured data supplied in the form of a raw text file. The patterns can range 

<h3>Relay2App</h3>h3>
Relay2App is a message processing System that was initially build to relay ad-hoc messages/data to a listener Server for interim-storage instant-retrieval.

The App has classic Web page layout that is optimised as per device screen size.
It also has an online terminal which gives the look and feel of an old-school terminal essentially exhibiting the same functionality.
There are 2 REST APIs also available which can Send as well as Receive messages.

Architecture:
The app itself is build using flask. Flask is a micro web framework written in Python that can be used to rapidly develop apps with relatively less hassle on the web/UI components, thus ensuring that the core-focus can be maintained on the application business logic enhancement while a descent Web-UI is still available.
The Colorful front end web-UI/homepage is build using HTML/CSS with bootstrap to manage the layout. 
since its a flask app, the entire app can be condensed to a single file.
The old School UI is build using jQuery Terminal, which is Free and Open Source JavaScript library for creating command line interpreters in your applications.(https://terminal.jcubic.pl/) It can be used to create cool looking interactive portfolio website, that look like GNU/Linux, MacOSX or Windows WSL terminal.
The REST API is implemented using flask_restful package which is Flask's own simplified way of implementing REST APIs for a flask app.
There are 2 REST API i.e. SendMsg and ReadMsg.
Both the methods can be invoked using any programming language that supports invoking web-requests using GET and POST methods.
database management:
The database management is done using Mongo DB hosted on GCP servers. The Rest APIs and UI can interact directly with the MongoDb.
Web hosting:
The App is hosted on a PythonAnywhere Server which is again a simplifed web hosting service that can be used to deploy app rapidly into production.


<h3>MangaDataProcessing System</h3>
MangaDataProcessing is a python data processing system that performs the pattern recognition whist taking the feed in the form on raw text/HTML files.
We've implemented a customed algorithm to clean, extract transform, load and analyse the data for short and medium sized pattenrs. Algorithm works is buidl in 2 parts.
Part 1 ingests input raw data, cleans it and converts it into a list of Serialised JSON objects for efficient storage and processing. After processing, essentially, what remains is a long string of numbers for ease in computation. This list of JSON obejcts is fed through to second part of the system.
Part 2 performs the pattern recognition based on the sequences provided by the earlier process.
The app reads the data converts it into Pandas DataFrames for processing. In fact, the entire data can be converted to a pandas DataFrames for parallel processing to ensure maximum speed.

 
