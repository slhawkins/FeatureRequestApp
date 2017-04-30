# What's This?
This is an implementation of a feature request application detailed here:

  https://github.com/IntuitiveWebSolutions/EngineeringMidLevel

I have used most of the technologies mentioned in the repository, with Knockout.js being the one thing I've never touched. I also have very little knowledge on running tests against a frontend and have done little in the way of automated deployment beyond a basic Dockerfile. As such, this will provide a great learning experience and a chance to use a bunch of different skills. 

## Goals
The repository lists various suggestions/guidelines, most of which I hope to use or integrate into my project. I will be using Ubuntu on AWS, Python 3.6, Flask, SQL-Alchemy, Knockout.js, and Boostrap 4. Three of the guidelines include a decoupled backend, usability, and a MVVM frontend. A RESTful API and Knockout.js/Bootstrap frontend should take care of those with relative ease. Test suites and automated deployment will be a learning experience, and are probably my only real unknowns at the moment. Open source will of course be easy with the tools I'm using.

For features, a user management system will be incorporated using OAuth with Github for login and a basic interface will be created for the two (maybe three) roles the application will have. Client/Project management will also have a basic interface for adding/removing them. Filters and sorting will require a more complex interface and use of the API, but shouldn't be an issue. Finally, discussion threads (and maybe a few other features) will be added to individual feature requests.

## Plan of Attack
As always, a plan helps to add some sort of direction to the development. This isn't a step by step, but covers broadly what I want to do and in what order.

* **Basics:**
  * ~~Environment Setup/Research~~
  * ~~Basic Flask instance~~
  * ~~MySQL/SQLAlchemy setup~~
  * ~~OAuth2 Setup (Github)~~
* **Planning and Design:**
  * ~~Database~~
  * RESTful API
  * Interface
* **RESTful API:** Create tests and implement the RESTful API. This includes:
  * Feature Requests
  * Discussion Threads
  * To-do List
  * User Management
  * Client/Project Management
* **Knockout.js:**
  * Learn about it! This includes learning what I can do for automated testing
  * Implement the front end using the RESTful API
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
* Run 'python app.py', afterwards you should be able to view the website at http://localhost:5000.
