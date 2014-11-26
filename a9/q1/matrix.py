import feedparser
import futures
import md5
import re
import sys
import json

def get_next(d):
	for item in d.feed.links:
		if item['rel'] == u'next':
			return item['href']
	return None

def getwords(text):
	txt = re.compile(r'<[^>]+>').sub('', text)
	words = re.compile(r'[^A-Z^a-z]+').split(txt)
	return [word.lower() for word in words if word != '']

def get_titles(uri):
	print('processing {}'.format(uri))
	next = uri
	wc = {}
	pages = 0
	while next is not None:
		d = feedparser.parse(next)
		for e in d.entries:
			words = getwords(e.title.encode('utf-8'))
			for word in words:
				wc.setdefault(word, 0)
				wc[word] += 1
		pages += 1
		next = get_next(d)
		print('next {}'.format(next))
	title = d.feed.title.encode('utf-8')
	subtitle = d.feed.subtitle[:50].encode('utf-8')
	print('finished: {}: {}'.format(title, subtitle))
	return uri, title, subtitle, pages, wc

if __name__ == '__main__':
	with open('blog_uris') as infile:
		uris = [line.strip() for line in infile]
	if len(sys.argv) == 2 and sys.argv[1] == 'get':
		with futures.ThreadPoolExecutor(max_workers=8) as executor:
			uri_futures = [executor.submit(get_titles, uri) for uri in uris]
			for future in futures.as_completed(uri_futures):
				uri, title, subtitle, pages, wc = future.result()
				with open('wcs/' + md5.new(uri).hexdigest(), 'w') as out:
					out.write(title + ': ' + subtitle + '\t' + str(pages) + '\t')
					json.dump(wc, out)
	else:
		apcount = {}
		wordcounts = {}
		pagecounts = {}
		for uri in uris:
			with open('wcs/' + md5.new(uri).hexdigest()) as infile:
				try:
					lines = infile.read().split('\t')
					title = lines[0]
					pages = int(lines[1])
					wc = json.loads(lines[2])
				except Exception, e:
					print('*** {} generated an exception: {}'.format(uri, e))
					continue
			wordcounts[title] = wc
			pagecounts[title] = pages
			for word, count in wc.items():
				apcount.setdefault(word, 0)
				apcount[word] += count
		wordlist = []
		for w, bc in sorted(apcount.items(), key=lambda x: x[1], reverse=True):
			frac = float(bc) / len(uris)
			if frac > 0.1 and frac < 0.5:
				wordlist.append(w)
		if len(sys.argv) == 2 and sys.argv[1] == 'pages':
			with open('pagecounts', 'w') as outfile:
				outfile.write('blog\tpages\n')
				for blog, pagecount in pagecounts.iteritems():
					outfile.write("\"" + blog.replace("\"", "") + "\"" + '\t' + str(pagecount) + '\n')
		if len(sys.argv) == 2 and sys.argv[1] == 'wc':
			with open('blogdata1.txt', 'w') as out:
				out.write('Blog')
				for word in wordlist[:500]: 
					out.write('\t%s' % word)
				out.write('\n')
				for blog, wc in wordcounts.items():
					print blog
					out.write(blog)
					for word in wordlist[:500]:
						if word in wc: 
							out.write('\t{}'.format(wc[word]))
						else: out.write('\t0')
					out.write('\n')
