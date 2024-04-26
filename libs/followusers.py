from libs.config import *
from libs.media import downloadThumb;

from classes.botconf import botConf;

import random
from datetime import datetime, tzinfo, date, timezone
import time
#import calendar


def followUser(conf, pk):
	confdir = conf["confdir"];
	localBotConf = botConf(conf);
	coolDownMaxValues = loadCoolDownValues(conf);

	cl=conf["cl"]

	a=bool(conf["cooldown_day"]["follows"] >= coolDownMaxValues["day_max_follows"]);
	d=bool(conf["cooldown_hour"]["follows"] >= coolDownMaxValues["hour_max_follows"]);
	if a or d:
		print("[followUser] Max cooldown reached, can't follow ")
		print("[followUser] Day: "+str(a)+", Hour: "+str(d))
		return;

	with open(os.path.join(confdir, 'followed.csv'), 'r') as f:
		if pk in f.read():
			return
	
	r2=random.randint(0,100)
	follower_count=0;
	# Get User Infos. 
	# And download profile picture thumb
	if r2<45:
		e_user_info = cl.user_info(pk);
		follower_count=e_user_info.follower_count;
		print("[followUser] "+e_user_info.username+" Got User infos");
		print("[followUser] "+e_user_info.username+" Download profile picture -> ", end='');
		try:
			downloadThumb(conf, e_user_info.pk, e_user_info.profile_pic_url)
		except:
			print("[followUser][ERROR] Error downloading Thumb");
			print(e_user_info);
		print()
	
	now_ts=str(time.mktime(time.strptime(str(datetime.now(timezone.utc)).split(".")[0], "%Y-%m-%d %H:%M:%S")))
	if follower_count < 1400:

		print("[followUser] Following user");
		# Append to file at last
		with open(os.path.join(confdir, 'followed.csv'), 'a') as f:
			f.write(now_ts+":"+pk+"\n")

		localBotConf.confAddFollow();
		cl.user_follow(pk) 

def followMediaLikers(conf, pk):
	cl = conf["cl"]
	confdir = conf["confdir"]

	print("[followMediaLikers] "+pk+" Get media likes ");
	e_media_likes = cl.media_likers(pk);
	i=0;
	r2=random.randint(0,4)
	for xx in e_media_likes:
		if i>=r2:
			print("[followMediaLikers] "+pk+" End media likes ")
			break;
		if random.randint(0,100) < 20:
			print("[followMediaLikers] Following user "+xx.username+" (in media likes)");
			# Append to file at last
			followUser(conf, xx.pk);
			i+=1;