# What's This?
This is an implementation of a feature request application detailed here:

  https://github.com/IntuitiveWebSolutions/EngineeringMidLevel

I have used most of the technologies mentioned in the repository, with Knockout.js being the one thing I've never touched. I also have very little knowledge on running tests against a frontend and have done little in the way of automated deployment beyond a basic Dockerfile. As such, this will provide a great learning experience and a chance to use a bunch of different skills. 

## Goals
The repository lists various suggestions/guidelines, most of which I hope to use or integrate into my project. I will be using Ubuntu on AWS, Python 3.6, Flask, SQL-Alchemy, Knockout.js, and Boostrap 4. Three of the guidelines include a decoupled backend, usability, and a MVVM frontend. A RESTful API and Knockout.js/Bootstrap frontend should take care of those with relative ease. Test suites and automated deployment will be a learning experience, and are probably my only real unknowns at the moment. Open source will of course be easy with the tools I'm using.

For features, a user management system will be incorporated using OAuth with Github for login and a basic interface will be created for the two (maybe three) roles the application will have. Client/Project management will also have a basic interface for adding/removing them. ~~Filters and sorting will require a more complex interface and use of the API, but shouldn't be an issue.~~ I had a sorting issue in the past and attempted to make sorting possible on the API end. I think I will be trying this on the client end this time around. Finally, discussion threads (and maybe a few other features) will be added to individual feature requests.

## Plan of Attack
As always, a plan helps to add some sort of direction to the development. This isn't a step by step, but covers broadly what I want to do and in what order.

* **Basics:**
  * ~~Environment Setup/Research~~
  * ~~Basic Flask instance~~
  * ~~MySQL/SQLAlchemy setup~~
  * ~~OAuth2 Setup (Github)~~
* **Planning and Design:**
  * ~~Database~~
  * ~~RESTful API~~ 
  * ~~Interface~~
* **RESTful API:** Create tests and implement the RESTful API. **GET,POST, and a few PUT methods have been implemented, though they are subject to change.**
  * ~~Feature Requests~~
  * Discussion Threads
  * To-do List
  * ~~User Management~~
  * ~~Client/Product Management~~
* **Knockout.js:**
  * ~~Learn about it!~~ Learning is ongoing, but I've got a good start.
  * Learn how to test Knockout.js applications
  * Implement the front end using the RESTful API **In Progress**
* **Automated Deployment:**
  * Learn/Deploy to AWS
  * Automate the deployment
* **Test:** Get some friends to jump on and test it! This will probably happen as I go, but some thorough  tests would be appreciated at this stage. 
* **Final Submission**

Now let’s get cracking!

## Local Testing
To deploy this locally, you must:
* Run 'pip install -r requirements.txt'.
* Add a config.py file next to app.py. This must have the variables SQLALCHEMY_DATABASE_URI, SECRET_KEY, CLIENT_ID, and CLIENT_SECRET set.
* Run 'python app.py --setup', this will create the database tables as needed.
* If so desired, basic dummy data can be added with 'python app.py --populate'.
* Run 'python app.py', afterwards you should be able to view the website at http://localhost:5000.

## Current Status
Currently I only have generated views for the feature requests, client list, user list, and product area list. The add/edit/delete buttons do not work at the moment.

A current copy of the code can be found at: http://featurerequest.us-west-2.elasticbeanstalk.com/. At the moment, it will automatically log you in as an admin since I don't have SSL setup for proper Github authentication.

![Current status](http://i.imgur.com/G4GzNC9.png)

![Current status](http://i.imgur.com/dYtoVti.png)

![Current status](http://i.imgur.com/8F3xF0T.png)

![Current status](http://i.imgur.com/Z5FMh66.png)