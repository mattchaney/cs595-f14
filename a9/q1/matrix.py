import feedparser
import re

def get_next(d):
	for item in d.feed.links:
		if item['rel'] == u'next':
			return item['href']
	return None

def getwords(text):
	txt = re.compile(r'<[^>]+>').sub('', text)
	words = re.compile(r'[^A-Z^a-z]+').split(txt)
	return [word.lower() for word in words if word != '']

def get_titles(url):
	print('processing {}'.format(url))
	next = url
	wc = {}
	while next is not None:
		d = feedparser.parse(next)
		for e in d.entries:
			words = getwords(e.title.encode('utf-8'))
			for word in words:
				wc.setdefault(word, 0)
				wc[word] += 1
		next = get_next(d)
		print('next {}'.format(next))
	return d.feed.title + ': ' + d.feed.subtitle[:50], wc

if __name__ == '__main__':
	apcount = {}
	wordcounts = {}
	feedlist = [line.strip() for line in file('blog_urls')]
	for feedurl in feedlist:
		try:
			title, wc = get_titles(feedurl)
			wordcounts[title] = wc
			for word, count in wc.items():
				apcount.setdefault(word,0)
				apcount[word] += count
		except Exception, e:
			print('Exception {} occured when attempting to parse {}'.format(e, feedurl))

	wordlist = []
	for w, bc in sorted(apcount.items(), key=lambda x: x[1], reverse=True):
		frac = float(bc) / len(feedlist)
		if frac > 0.1 and frac < 0.5:
			wordlist.append(w)

	with open('blogdata1.txt','w') as out:
		out.write('Blog')
		for word in wordlist[:500]: 
			out.write('\t%s' % word)
		out.write('\n')
		for blog, wc in wordcounts.items():
			print blog
			out.write(blog.encode('utf-8'))
			for word in wordlist[:500]:
				if word in wc: 
					out.write('\t{}'.format(wc[word]))
				else: out.write('\t0')
			out.write('\n')
