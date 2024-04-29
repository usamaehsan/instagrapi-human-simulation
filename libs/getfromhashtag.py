import urllib
import urllib.request
import random
import time
from libs.media import *
from libs.followusers import *

def getFromHashtag(conf, cursor=None):
	tags = conf["tags"].split(";");
	confdir = conf["confdir"]
	cl = conf["cl"];
	refreshed=False;
	
	r1=random.randint(24, 32)
	
	tag = ""
	while len(tag) == 0:
		r2=random.randint(0, len(tags)-1)	
		tag=tags[r2]
		
	print("Getting "+str(r1)+" medias for tag "+tag);
	# medias = cl.hashtag_medias_recent(tag, amount=r1)
	if cursor is None:
		medias, cursor = cl.hashtag_medias_v1_chunk(tag, max_amount=r1, tab_key='recent')
	else:
		refreshed=True;
		medias, cursor = cl.hashtag_medias_v1_chunk(tag, max_amount=r1, tab_key='recent', max_id=cursor)

	try:
		# Hastags Download all thumbnails
		print("[getHashtag] Downloading "+str(r1)+" thumbs -> ", end='')
		for x in medias:
			thumb_url = x.thumbnail_url
			if not thumb_url:
				image_versions = x.image_versions2
				# Access the 'candidates' list
				candidates = image_versions['candidates']
				# print("got candidates")
				# Get the first thumbnail URL (index 0)
				thumb_url = candidates[0]['url']
			print('thumbbbbbbbbbbbbb', thumb_url, '\n')
			# print(x,'\n')
			downloadThumb(conf, x.id, str(thumb_url))

			
		time.sleep(random.randint(1,5))
		print("")

		# Hashtags liking medias
		for x in medias:
			print("");
			print("[getHashtag] >>> User "+x.user.username)
			print("[getHashtag] + mediaId: "+x.id+", mediaType: "+str(x.media_type), end=', ')

			with open(os.path.join(confdir, 'medias_seen.csv')) as f:
				if str(x.id) in f.read():
					print("next")
					continue
				
			# media checked
			with open(os.path.join(confdir, 'medias_seen.csv'), 'a') as f:
				f.write(str(x.id)+"\n")
			
			# print(x.dict())
			r1=random.uniform(0, 15);
			print("Random: "+str(r1));

			if (len(conf["forced_words"]) > 0):
				for forced_word in conf["forced_words"].split(";"):
					if forced_word in x.user.username:
						print("[getHashtag] User "+x.user.username+" contains forced word: "+forced_word+" so force Random=0.1");
						r1=0.1;
						break;
					else:
						r1=15;

			if r1<4:
				downloadMedia(conf, x.pk, x.media_type, x.product_type);
				s=random.randrange(1,10)
				time.sleep(s);

			if r1<3.5:
				likeMedia(conf, x.pk, x.product_type)
				s=random.uniform(1,20)
				time.sleep(s);

			if r1<3.3:
				# followUser(conf, x.user.pk);
				# r2=random.randint(0,100)
				# if r2<20:
				followMediaLikers(conf, x.pk);
				# s=random.uniform(.2,2)
				# time.sleep(s);
					
				s=random.randrange(1,6)
				time.sleep(s);

			if r1<2:
				# checking user media
				e_user_medias = cl.user_medias_v1(x.user.pk, 9)
				print("[getHashtag] "+x.user.username+" Getting user medias ")
				print("[getHashtag] "+x.user.username+" Downloading thumbnails user medias ", end = '')
				for xx in e_user_medias:	
					print("o", end = '')
					# print(xx.thumbnail_url);
					if xx.thumbnail_url is not None:
						urllib.request.urlretrieve(xx.thumbnail_url, os.path.join(conf['basedwndir'], 'temp_thumb'))
				print("")
				
				s=random.randrange(2,9)
				time.sleep(s);
				
				for xx in e_user_medias:	
					r2=random.randint(0,100)
					if r2<20:

						print("[getHashtag] "+x.user.username+" Downloading user media "+xx.pk);
						downloadMedia(conf, xx.pk, xx.media_type, xx.product_type)
						
						s=random.randrange(1,3)
						time.sleep(s);

						if r2<10:
							print("[getHashtag] "+x.user.username+" Liking user media "+xx.pk)
							likeMedia(conf, xx.pk, xx.product_type)

						s=random.randrange(2,9)
						time.sleep(s);

				s=random.randrange(2,9)
				time.sleep(s);
	except Exception as e:
		print("Some error occurred in execution")
		print(e)

	s=random.randrange(0,10)
	if (s>5 and refreshed==False):
		print("[getHashtag] REFREEEEEEEEEEEEEEEEEEEEEESH ")
		s=random.randrange(5,15)
		time.sleep(s);
		getFromHashtag(conf, cursor)
		



def get_one_page():


def getFromPage(conf):
	tags = conf["tags"].split(";");
	pages = conf['pages'].split(";")
	confdir = conf["confdir"]
	cl = conf["cl"];
	refreshed=False;
	
	r1=random.randint(24, 32)
	
	page = ""
	while len(page) == 0:
		r2=random.randint(0, len(pages)-1)	
		page=pages[r2]
	p1 = page
	page = cl.user_id_from_username(page)
		
	print("Getting "+str(r1)+" medias for page "+p1);
	# medias = cl.hashtag_medias_recent(tag, amount=r1)
	medias = None
	try:
		medias= cl.user_medias_gql(page, amount=r1)
	except Exception as e:
		try:
			medias= cl.user_medias(page, amount=r1)
		except Exception as e1:
			print(e1)
			print("can not get media22")
			medias = cl.user_medias_v1(page, amount=r1)

	if medias:
		try:
			# Hastags Download all thumbnails
			print("[getPage] Downloading "+str(r1)+" thumbs -> ", end='')
			for x in medias:
				thumb_url = x.thumbnail_url
				if not thumb_url:
					image_versions = x.image_versions2
					# Access the 'candidates' list
					try:
						candidates = image_versions['candidates']
					except:
						print("candidate not found")
						continue
					# print("got candidates")
					# Get the first thumbnail URL (index 0)
					thumb_url = candidates[0]['url']
				print('thumbbbbbbbbbbbbb', thumb_url, '\n')
				# print(x,'\n')
				downloadThumb(conf, x.id, str(thumb_url))

				
			time.sleep(random.randint(1,5))
			print("")

			# Hashtags liking medias
			for x in medias:
				print("");
				print("[getHashtag] >>> User "+x.user.username)
				print("[getHashtag] + mediaId: "+x.id+", mediaType: "+str(x.media_type), end=', ')

				with open(os.path.join(confdir, 'medias_seen.csv')) as f:
					if str(x.id) in f.read():
						print("next")
						continue
					
				# media checked
				with open(os.path.join(confdir, 'medias_seen.csv'), 'a') as f:
					f.write(str(x.id)+"\n")
				
				# print(x.dict())
				r1=random.uniform(0, 15);
				print("Random: "+str(r1));

				if (len(conf["forced_words"]) > 0):
					for forced_word in conf["forced_words"].split(";"):
						if forced_word in x.user.username:
							print("[getHashtag] User "+x.user.username+" contains forced word: "+forced_word+" so force Random=0.1");
							r1=0.1;
							break;
						else:
							r1=15;

				if r1<4:
					downloadMedia(conf, x.pk, x.media_type, x.product_type);
					s=random.randrange(1,10)
					time.sleep(s);

				if r1<3.5:
					likeMedia(conf, x.pk, x.product_type)
					s=random.uniform(1,20)
					time.sleep(s);

				if r1<3.3:
					# followUser(conf, x.user.pk);
					# r2=random.randint(0,100)
					# if r2<20:
					followMediaLikers(conf, x.pk);
					# s=random.uniform(.2,2)
					# time.sleep(s);
						
					s=random.randrange(1,6)
					time.sleep(s);

				if r1<2:
					# checking user media
					e_user_medias = cl.user_medias_v1(x.user.pk, 9)
					print("[getHashtag] "+x.user.username+" Getting user medias ")
					print("[getHashtag] "+x.user.username+" Downloading thumbnails user medias ", end = '')
					for xx in e_user_medias:	
						print("o", end = '')
						# print(xx.thumbnail_url);
						if xx.thumbnail_url is not None:
							urllib.request.urlretrieve(xx.thumbnail_url, os.path.join(conf['basedwndir'], 'temp_thumb'))
					print("")
					
					s=random.randrange(2,9)
					time.sleep(s);
					
					for xx in e_user_medias:	
						r2=random.randint(0,100)
						if r2<20:

							print("[getHashtag] "+x.user.username+" Downloading user media "+xx.pk);
							downloadMedia(conf, xx.pk, xx.media_type, xx.product_type)
							
							s=random.randrange(1,3)
							time.sleep(s);

							if r2<10:
								print("[getHashtag] "+x.user.username+" Liking user media "+xx.pk)
								likeMedia(conf, xx.pk, xx.product_type)

							s=random.randrange(2,9)
							time.sleep(s);

					s=random.randrange(2,9)
					time.sleep(s);
		except Exception as e:
			print("Some error occurred in execution")
			print(e)

		s=random.randrange(0,10)
		if (s>5 and refreshed==False):
			print("[getHashtag] REFREEEEEEEEEEEEEEEEEEEEEESH ")
			s=random.randrange(5,15)
			time.sleep(s);
			getFromPage(conf)
		


