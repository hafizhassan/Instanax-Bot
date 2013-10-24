Instanax bot
============
Instanax bot is a fork of [Cranklin's Instagram Bot v.1.0](https://github.com/cranklin/Instagram-Bot). It has been forked by @ponsfrilus on October 24th 2013. The idea is to add some features and make the bot more usable. Main added feature are the possibility to use some argument when calling the script. Other added features are:
- added docopt parser (and added input args) (http://docopt.org)
- password is now prompted (getpass)
- hashtags list as dictionaries which can be choosen as input
- better output information
- some reference hashtags list based on tagsforlike information
- added max like limit
- random waiting time between two likes

If you like instanax, have a look to <http://instanax.donax.ch>
As I'm a likeaholic, please give me more instalikes here: <http://instagr.am/ponsfrilus>

Finaly, thanks Cranklin for this great script !

Cranklin's Instagram Bot v.1.0
==============================
Check www.cranklin.com for updates

Instagram bot that auto-likes photos by hashtag.  Written in Python using the Pycurl library.
This bot gets you more likes and followers on your Instagram account.ta
Requirements:
- python > 2.6 but < 3.0
- pycurl library
- web.stagram.com login prior to using the bot

Instructions:
- make sure you have the correct version of Python installed
- make sure you have the pycurl library installed
- log into web.stagram.com with your instagram account and approve the app
- edit between lines 42 and 52
- from the command line, run "python webstagram.py"
- enjoy!

v1.0 updates:
- added browser agent randomizer
- added optional sleep timer 
- added optional hashtag limiter
- added a couple extra additions for some people experiencing SSL errors.  (thanks Charlie)
*** thank you Nick, John, Max, Shahar, Charlie for the help
