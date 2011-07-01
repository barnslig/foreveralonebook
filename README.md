foreveralonebook
================
A selfsocial network for those who wants to be alone -- Have a Microblog just for yourself.

It's based on [Python](http://python.org) in combination with the [Flask](http://flask.pocoo.org)-Framework for testing an application made with these things with fastCGI.

License
-------
The Code is licensed under the [GPLv3](http://www.gnu.org/licenses/gpl.html)-License. 

Some icons are from [famfamfams](http://www.famfamfam.com/lab/icons/silk/) Silk-Collection which is under [(cc) by](http://creativecommons.org/licenses/by/2.5/).

The big Forever Alone is a rage comic character. Look at [knowyourmeme](http://knowyourmeme.com/memes/forever-alone). It seems that there is no license on it.

Installation
------------
The requirements of this are: [flask](http://flask.pocoo.org), a database, a webserver with fastCGI support.

First you need the database. The code is designed for MySQL, but it's not hard to change the database engine because the python database modules seems to have the same API. Just put the schema.sql-file into MySQL.

Now you have to fit the configuration to your setup. The configuration is placed in the `foreveralonebook.py` after the `# CONFIGURATION`-comment. You have to change the SECRET_KEY for a secure system.

Create a temporary directory for the avatar-uploads in /tmp/, name it feab. Short: Create /tmp/feab.

Also you need to set the rights of the static/avatars-directory, set the owner to the user of your webserver (and fastCGI).

It's time to set up your webserver for fastCGI. How to do this is on [this page](http://flask.pocoo.org/docs/deploying/). The fastCGI-Server is the foreveralonebook.fcgi, start it as the user of your webserver, otherwise it won't work.

Now you have a working foreveralone-installation. Fully decentralised aloneness :3
