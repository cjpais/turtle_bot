import json
import urllib2
import os
import re

request_url = 'https://api.tumblr.com/v2/tagged?tag=turtle&before={}&api_key=fuiKNFp9vQFvjLNvx4sUwti4Yb5yGutBN4Xh10LXZhhRKjWlV4' 

request = urllib2.urlopen(request_url.format(""))

blog_posts = json.load(request)['response']

num_found = 0

while num_found < 1000:
	for blog in blog_posts:
		if blog['type'] != 'photo':
			continue
		for p in blog['photos']:
			num_found += 1
			image = urllib2.urlopen(p['original_size']['url']).read()

			match = re.search('[^/]+$',p['original_size']['url'])
			image_name = match.group(0)

			with open('turtles/{}'.format(image_name), 'w') as new_turtle:
				new_turtle.write(image)

	last_timestamp = blog_posts[-1]['timestamp']
	request = urllib2.urlopen(request_url.format(last_timestamp))
	blog_posts = json.load(request)['response']