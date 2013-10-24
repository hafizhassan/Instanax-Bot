#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""instanax command line - based on Cranklin's Instagram Bot v.1.0
                           https://github.com/cranklin/Instagram-Bot

Usage:
  instanax.py <user> [--hashtags=default] [--sleeptimer=auto] [--likelimit=50] [--maxlikelimit=unlimited]
  instanax.py (-h | --help)
  instanax.py --version

Options:
  <user>                    The valid webstagram user.
  --hashtags=default        The hashtags disctionary. [default: default]
  --sleeptimer=auto         The sleeptimer between two likes in seconds. Set value to 0 if you don't want it to sleep at all. Set value to auto to have a random timer. [default: auto]
  --likelimit=50            The like limit for each tags. [default: 50]
  --maxlikelimit=unlimited  The global like limit. [default: unlimited]
  -h --help                 Show this screen.
  --version                 Show version.

"""


# Notes:
#   instanx bot is based on Cranklin's Instagram Bot v.1.0 https://github.com/cranklin/Instagram-Bot
#   and I (ponsfrilus) added some features:
#       - added docopt parser (and added input args) (http://docopt.org)
#       - password is now prompted (getpass)
#       - hashtags list as dictionaries which can be choosen as input
#       - better output information
#       - some reference hashtags list based on tagsforlike information
#       - added max like limit
#       - random waiting time between two likes
#   TODO:
#       - put curl stuff in a function
#       - get hashtags from a file (and remove the need to edit this file)

import os
import pycurl
import cStringIO
import re
import random
import time

import getpass
from docopt import docopt

##### EDIT THESE BELOW

# your list of hashtags
hashtags = {}

# Default : most popular tags according to tagsforlike
hashtags['default'] = hashtags['MostPopular'] = ["love","TFLers","tweegram","photooftheday","20likes","amazing","followme","follow4follow","like4like","look","instalike","igers","picoftheday","food","instadaily","instafollow","like","girl","iphoneonly","instagood","bestoftheday","instacool","instago","all_shots","follow","webstagram","colorful","style","swag"]

hashtags['2ndPopular'] = ["fun","instagramers","food","smile","pretty","followme","nature","lol","dog","hair","onedirection","sunset","swag","throwbackthursday","instagood","beach","statigram","friends","hot","funny","blue","life","art","instahub","photo","cool","pink","bestoftheday","clouds"]

hashtags['3rdPopular'] = ["amazing","like","all_shots","textgram","family","instago","igaddict","awesome","girls","instagood","my","bored","baby","music","red","green","water","harrystyles","bestoftheday","black","party","white","yum","flower","2012","night","instalove","niallhoran","jj_forum"]

hashtags['Nature'] = ["nature","sky","sun","summer","beach","beautiful","pretty","sunset","sunrise","blue","flowers","night","tree","twilight","clouds","beauty","light","cloudporn","photooftheday","love","green","skylovers","dusk","weather","day","red","iphonesia","mothernature"]

hashtags['Clouds'] = ["clouds","cloud","cloudporn","weather","lookup","sky","skies","skyporn","cloudy","instacloud","instaclouds","instagood","nature","beautiful","gloomy","skyline","horizon","overcast","instasky","epicsky","crazyclouds","photooftheday","cloud_skye","skyback","insta_sky_lovers","iskyhub"]

hashtags['Art'] = ["art","illustration","drawing","draw","picture","photography","artist","sketch","sketchbook","paper","pen","pencil","artsy","instaart","beautiful","instagood","gallery","masterpiece","creative","photooftheday","instaartist","graphic","graphics","artoftheday"]

hashtags['Photo'] = ["photography","photo","photos","pic","pics","picture","pictures","snapshot","art","beautiful","instagood","picoftheday","photooftheday","color","all_shots","exposure","composition","focus","capture","moment"]

hashtags['BW'] = ["blackandwhite","bnw","monochrome","instablackandwhite","monoart","insta_bw","bnw_society","bw_lover","bw_photooftheday","photooftheday","bw","instagood","bw_society","bw_crew","bwwednesday","insta_pick_bw","bwstyles_gf","irox_bw","igersbnw","bwstyleoftheday","monotone","monochromatichashtags","noir","fineart_photobw"]

hashtags['Archi'] = ["architecture","building","architexture","city","buildings","skyscraper","urban","design","minimal","cities","town","street","art","arts","architecturelovers","abstract","lines","instagood","beautiful","archilovers","architectureporn","lookingup","style","archidaily","composition","geometry","perspective","geometric","pattern"]

hashtags['StreetArt'] = ["streetart","street","streetphotography","sprayart","urban","urbanart","urbanwalls","wall","wallporn","graffitiigers","stencilart","art","graffiti","instagraffiti","instagood","artwork","mural","graffitiporn","photooftheday","stencil","streetartistry","photography","stickerart","pasteup","instagraff","instagrafite","streetarteverywhere"]

hashtags['Food'] = ["food","foodporn","yum","instafood","yummy","amazing","instagood","photooftheday","sweet","dinner","lunch","breakfast","fresh","tasty","food","delish","delicious","eating","foodpic","foodpics","eat","hungry","foodgasm","hot","foods"]

hashtags['lausanne'] = ["lausanne","igerslausanne","iglausanne","lausannecity","lausannecitation","lausannestreetart"]

hashtags['test'] = ["eVooh3lu"]

##### NO NEED TO EDIT BELOW THIS LINE

browsers = ["IE ","Mozilla/","Gecko/","Opera/","Chrome/","Safari/"]
operatingsystems = ["Windows","Linux","OS X","compatible","Macintosh","Intel"]

def login():
    try:
        os.remove("instanax.txt")
    except:
        pass

    # getting username and password
    username = arguments['<user>']
    password = getpass.getpass()
    
    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, "http://web.stagram.com")
    c.setopt(pycurl.COOKIEFILE, "instanax.txt")
    c.setopt(pycurl.COOKIEJAR, "instanax.txt")
    c.setopt(pycurl.WRITEFUNCTION, buf.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.ENCODING, "")
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    useragent = random.choice(browsers) + str(random.randrange(1,9)) + "." + str(random.randrange(0,50)) + " (" + random.choice(operatingsystems) + "; " + random.choice(operatingsystems) + "; rv:" + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + ")"
    c.setopt(pycurl.USERAGENT, useragent)
    c.perform()
    curlData = buf.getvalue()
    buf.close()

    clientid = re.findall(ur"href=\"https:\/\/api.instagram.com\/oauth\/authorize\/\?client_id=([a-z0-9]*)&redirect_uri=http:\/\/web.stagram.com\/&response_type=code&scope=likes\+comments\+relationships\">LOG IN",curlData)
    instagramlink = re.findall(ur"href=\"([^\"]*)\">LOG IN",curlData)

    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, instagramlink[0])
    c.setopt(pycurl.COOKIEFILE, "instanax.txt")
    c.setopt(pycurl.COOKIEJAR, "instanax.txt")
    c.setopt(pycurl.WRITEFUNCTION, buf.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.ENCODING, "")
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    useragent = random.choice(browsers) + str(random.randrange(1,9)) + "." + str(random.randrange(0,50)) + " (" + random.choice(operatingsystems) + "; " + random.choice(operatingsystems) + "; rv:" + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + ")"
    c.setopt(pycurl.USERAGENT, useragent)
    c.perform()
    curlData = buf.getvalue()
    buf.close()

    postaction = re.findall(ur"action=\"([^\"]*)\"",curlData)
    csrfmiddlewaretoken = re.findall(ur"name=\"csrfmiddlewaretoken\" value=\"([^\"]*)\"",curlData)

    postdata = 'csrfmiddlewaretoken='+csrfmiddlewaretoken[0]+'&username='+username+'&password='+password

    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, "https://instagram.com"+postaction[0])
    c.setopt(pycurl.COOKIEFILE, "instanax.txt")
    c.setopt(pycurl.COOKIEJAR, "instanax.txt")
    c.setopt(pycurl.WRITEFUNCTION, buf.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.ENCODING, "")
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    c.setopt(pycurl.REFERER, "https://instagram.com/accounts/login/?next=/oauth/authorize/%3Fclient_id%3D"+clientid[0]+"%26redirect_uri%3Dhttp%3A//web.stagram.com/%26response_type%3Dcode%26scope%3Dlikes%2Bcomments%2Brelationships")
    useragent = random.choice(browsers) + str(random.randrange(1,9)) + "." + str(random.randrange(0,50)) + " (" + random.choice(operatingsystems) + "; " + random.choice(operatingsystems) + "; rv:" + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + ")"
    c.setopt(pycurl.USERAGENT, useragent)
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, postdata)
    c.setopt(pycurl.POSTFIELDSIZE, len(postdata))
    #c.setopt(pycurl.VERBOSE, True)
    c.perform()
    curlData = buf.getvalue()
    buf.close()



def like():
    likecount = 0
    sleepcount = 0
    likelimit = int(arguments['--likelimit'])

    if not (arguments['--maxlikelimit'] == 'unlimited'):
        maxlikelimit = int(arguments['--maxlikelimit'])
    else:
        maxlikelimit = 0

    print "Hashtag dictionnary: "+str(hashtags[arguments['--hashtags']])
    print "Will try to like "+str(arguments['--likelimit'])+" of each of these tags until "+str(arguments['--maxlikelimit'])+"."
    print "----"

    for tag in hashtags[arguments['--hashtags']]:

        print ": Liking: %s" % bold(tag)

        hashtaglikes = 0
        nextpage = "http://web.stagram.com/tag/"+tag+"/?vm=list"
        #enter hashtag like loop
        while nextpage != False and (likelimit == 0 or (likelimit > 0 and hashtaglikes < likelimit)):
            buf = cStringIO.StringIO()
            c = pycurl.Curl()
            c.setopt(pycurl.URL, nextpage)
            c.setopt(pycurl.COOKIEFILE, "instanax.txt")
            c.setopt(pycurl.COOKIEJAR, "instanax.txt")
            c.setopt(pycurl.WRITEFUNCTION, buf.write)
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.setopt(pycurl.ENCODING, "")
            c.setopt(pycurl.SSL_VERIFYPEER, 0)
            c.setopt(pycurl.SSL_VERIFYHOST, 0)
            useragent = random.choice(browsers) + str(random.randrange(1,9)) + "." + str(random.randrange(0,50)) + " (" + random.choice(operatingsystems) + "; " + random.choice(operatingsystems) + "; rv:" + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + ")"
            c.setopt(pycurl.USERAGENT, useragent)
            c.perform()
            curlData = buf.getvalue()
            buf.close()

            nextpagelink = re.findall(ur"<a href=\"([^\"]*)\" rel=\"next\">Earlier<\/a>",curlData)
            if len(nextpagelink)>0:
                nextpage = "http://web.stagram.com"+nextpagelink[0]
            else:
                nextpage = False

            likedata = re.findall(ur"<span class=\"like_button\" id=\"like_button_([^\"]*)\">",curlData)
            if len(likedata)>0:
                for imageid in likedata:

                    if likelimit > 0 and hashtaglikes >= likelimit:
                        break

                    repeat = True
                    while repeat:
                        randomint = random.randint(1000,9999)

                        postdata = 'pk='+imageid+'&t='+str(randomint)
                        buf = cStringIO.StringIO()
                        c = pycurl.Curl()
                        c.setopt(pycurl.URL, "http://web.stagram.com/do_like/")
                        c.setopt(pycurl.COOKIEFILE, "instanax.txt")
                        c.setopt(pycurl.COOKIEJAR, "instanax.txt")
                        c.setopt(pycurl.WRITEFUNCTION, buf.write)
                        c.setopt(pycurl.FOLLOWLOCATION, 1)
                        c.setopt(pycurl.ENCODING, "")
                        c.setopt(pycurl.SSL_VERIFYPEER, 0)
                        c.setopt(pycurl.SSL_VERIFYHOST, 0)
                        useragent = random.choice(browsers) + str(random.randrange(1,9)) + "." + str(random.randrange(0,50)) + " (" + random.choice(operatingsystems) + "; " + random.choice(operatingsystems) + "; rv:" + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + ")"
                        c.setopt(pycurl.USERAGENT, useragent)
                        c.setopt(pycurl.POST, 1)
                        c.setopt(pycurl.POSTFIELDS, postdata)
                        c.setopt(pycurl.POSTFIELDSIZE, len(postdata))
                        #c.setopt(pycurl.VERBOSE, True)
                        c.perform()
                        postData = buf.getvalue()
                        buf.close()
                        if postData == '''{"status":"OK","message":"LIKED"}''':
                            likecount += 1
                            hashtaglikes += 1
                            # print " - You liked #"+tag+" image "+imageid+"! Like count: "+str(likecount)+" (http://web.stagram.com/p/"+imageid+")"
                            likemsg = " - You liked http://web.stagram.com/p/"+imageid+"! "
                            print likemsg.ljust(68, ' ')+"Like count: "+str(likecount).rjust(3,' ')

                            repeat = False
                            sleepcount = 0
                            st = 0
                            if (arguments['--sleeptimer'] == 'auto'):
                                st = random.uniform(1, 10)
                                time.sleep(st)
                            elif arguments['--sleeptimer'] > 0:
                                st = float(arguments['--sleeptimer'])
                                time.sleep(st)

                            print "   ...slept for "+str(st)+" seconds"
                                
                        else:
                            sleepcount += 1
                            print "Your account has been rate limited. Sleeping on "+tag+" for "+str(sleepcount*10)+" minutes. Liked "+str(likecount)+" photos until now..."
                            time.sleep(10*60)

                        if maxlikelimit > 0 and maxlikelimit <= likecount:
                            print ": Max Like Limit reached, exiting"
                            return
                            
def bold(msg):
    return u'\033[1m%s\033[0m' % msg

def main():
    print "Hello %s!" % bold(str(arguments['<user>']))
    print "----"
    print "# Login process started"
    print ": Connect with user: "+str(arguments['<user>'])
    login()
    print "# Login process ended"
    print "----"
    print "# Liking process started"
    like()
    print "# Liking process ended"
    print "----"
    print "Bye bye"
    print ""
    print "PS: if you like instanax, have a look to http://instanax.donax.ch"
    print "PPS: I'm a likeaholic, please give me more likes: http://instagr.am/ponsfrilus"

if __name__ == "__main__":
    arguments = docopt(__doc__, version='Instanax 0.1')
    #print(arguments)
    print """
         _           _                         
        (_)         | |                        
         _ _ __  ___| |_ __ _ _ __   __ ___  __
        | | '_ \/ __| __/ _` | '_ \ / _` \ \/ /
        | | | | \__ \ || (_| | | | | (_| |>  < 
        |_|_| |_|___/\__\__,_|_| |_|\__,_/_/\_\CLI
                                     by ponsfrilus
                          http://instanax.donax.ch
                                       """
    print "----"
    main()