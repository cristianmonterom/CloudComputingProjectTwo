COMP90024 - Cluster and Cloud Computing
=======================================

Twitter harvesting and analysis of Singapore
-------------------------------

## GROUP 21

Members:

1. Cristian Montero (647640)
2. Quang Dang Nguyen (650616)
3. Santiago Villagómez (649887)
4. Saranya Nagarajan (673057)
5. Sravya Jammula (675210)

### Directory description

**Regions**

Classes used to determine tweet location, according to Singapore suburbs.

    - PlanningArea. It contains bounding boxes which defines borders for every Singapore's suburbs.
    - EvaluateRegion. It determines to which suburb belong a tweet (If tweet has location information).

**UpdateDB**

Contains processing scripts which will generate additional information, to each tweet, required for our scenario of results. These scripts are used to modified tweets that were not pre processed during harvesting.

    - removeColumns. As its name states it will remove columns generated. 
    - SuburbUpdate. Multi-threading process to generate information for each tweet. 

**Harvesting**

Contains the classes for database management as well as scripts required for gather stream tweets using Twitter API and Tweepy together. Also, it will generated information of each tweet for our scenario. Contained files are described as follows:

    - DatabaseHandler. Class for database connection handling.
    - dataPreprocessor. Class which generate required information for our scenario, such as: bag of words, polarity and suburb.
    - HarvestingTweets. Gather historic tweets from Twitter users.
    - StoringUser. Generate a DB which contains how many tweets have been gathered from each user.
    - TweetsCity. Main class for harvesting tweets. It access to Twitter API using OAuth information.
    - TwitterStore. It creates and connect to a Couchdb instance.
  
**Orchestration**

Contains scripts to install requirements for three kind of instances we require in our project:

    - Database. VM which contains main database for our project.
    - Instance. VM which is responsible of harvesting tweets procedure.
    - Web server. VM which will be located our front end.

