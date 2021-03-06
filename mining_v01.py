‘’’
This script mines full tweets and saves to disk ie not entities or keywords are extracted out, thus we get more information but bigger files
Daniel phillis Fri sept 30th 2016
‘’’
import sys
import time
import datetime
import twitter
import io
import json
import datetime

from prettytable import PrettyTable

#------------------------------------------------------------------
def oauthlogin():
  CONSUMER_KEY = 'SIeOam4mLD8sZWr7QHmE67zHi'
  CONSUMER_SECRET = '444wPQutVPhns6ff8gdiWCrifgxkw4A6itsiPl3EQw5MhcQRDc'
  OAUTH_TOKEN = '29954818-FRyNn2iHYP9QsK1srs2SQTWdxRPBygkm1mb6Fda2x'
  OAUTH_TOKEN_SECRET = 'RUk8dVC5QJaXK9um6ADZvPSuGlzRiOSpusYs8SACRN6Yq'

  auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
  CONSUMER_KEY, CONSUMER_SECRET)
  twitter_api = twitter.Twitter(auth=auth)
  return twitter_api



def save_json(filename, inc, data):
    
	#file = filename + str(inc)
	#basename is twitterdata
	#filename = + filename
    
	with io.open('tweets_{0}'.format(filename),
            	'a', encoding ='utf-8') as f:
    	#f.write(unicode('\n<newTweet>\n'))
    	f.write(unicode(json.dumps(data, ensure_ascii=0)))
#0 was previously ‘false’ but didnt work

	print("wrote to: " + filename)

def load_data(filename):
  with io.open('file_to_read{0}.json'.format(filename),
           	encoding ='utf-8') as f:
	return f.read();
 
def twitter_search(twitter_api, q,max_results=100, **kw):
  # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
  search_results = twitter_api.search.tweets(q=q, count=100, **kw)
 
  statuses = search_results['statuses']

  #enforce a reasonable limit to searches
  max_results = min(1000, max_results)

  for _ in range(count):#10 * 100 = 1000
	try:
  	next_results = search_results['search_metadata']['next_results']
	except KeyError, e: # No more results when next_results doesn't exist
  	break
	#key word arguments, create a dictionary from next results
	#[1:] means from results 1 to how ever many there are
	kwargs = dict([ kv.split('=')
                	for kv in next_results[1:].split("&") ])
    
	search_results = twitter_api.search.tweets(**kwargs)
	statuses += search_results['statuses']

	if len(statuses) > max_results:
  	break
    
  return statuses

def get_time_series_data(q,secs_per_interval, max_intervals):
	interval = 0
	index = 0
    
	while True:
    	now = str(datetime.datetime.now()).split(".")[0]
    	index+=1
    	#TAsK to do over and over
    	data = twitter_search(twitter_api, q, max_results=100)
    	save_json(q,index, data)

    	print >> sys.stderr, "Zzzz..."
    	print >> sys.stderr.flush()

    	time.sleep(secs_per_interval) #seconds
    	interval +=1

    	if interval >=15:
        	break
   	 
#sign in--------------------------------------------------------------
twitter_api = oauthlogin()
count = 15

#print json.dumps(results[0], indent=1)
'''
part = 0

for slice in results:
  #write to file
  part+=1
  save_json(q,part,slice)
  #save_json('slide',slice)

#instead of appending each slice we can simply write all slices to disk
save_json('slice',slice)
'''

'''
q = '#Apple'
get_time_series_data(q,60,15) #
print('done' + q)

q = '#iPhone7'
get_time_series_data(q,60,15) #
print('done' + q)

q = '#Samsung'
get_time_series_data(q,60,15) #
print('done' + q)

q = '#GalaxyS7'
get_time_series_data(q,60,15) #
print('done' + q)

q = '#iWatch'
get_time_series_data(q,60,15) #
print('done' + q)
'''
q = '#SamsungNote7'
get_time_series_data(q,60,15) #
print('done' + q)