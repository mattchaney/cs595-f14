# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


from math import sqrt
from numpy import mean
from operator import itemgetter
from pprint import pprint
from sys import stdout

# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs,person1,person2):
  # Get the list of shared_items
  si={}
  for item in prefs[person1]: 
	if item in prefs[person2]: si[item]=1

  # if they have no ratings in common, return 0
  if len(si)==0: return 0

  # Add up the squares of all the differences
  sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) 
					  for item in prefs[person1] if item in prefs[person2]])

  return 1/(1+sum_of_squares)

# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs, p1, p2):
	# Get the list of mutually rated items
	si={}
	for item in prefs[p1]: 
		if item in prefs[p2]: 
			si[item]=1

	# if they are no ratings in common, return 0
	if len(si)==0: return 0

	# Sum calculations
	n=len(si)

	# Sums of all the preferences
	sum1=sum([prefs[p1][it] for it in si])
	sum2=sum([prefs[p2][it] for it in si])

	# Sums of the squares
	sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
	sum2Sq=sum([pow(prefs[p2][it],2) for it in si])	

	# Sum of the products
	pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

	# Calculate r (Pearson score)
	num=pSum-(sum1*sum2/n)
	den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
	if den==0: return 0

	r=num/den

	return r

# Returns the best matches for person from the prefs dictionary. 
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other) 
				  for other in prefs if other!=person]
  scores.sort()
  scores.reverse()
  return scores[0:n]

# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
  totals={}
  simSums={}
  for other in prefs:
	# don't compare me to myself
	if other==person: continue
	sim=similarity(prefs,person,other)

	# ignore scores of zero or lower
	if sim<=0: continue
	for item in prefs[other]:
		
	  # only score movies I haven't seen yet
	  if item not in prefs[person] or prefs[person][item]==0:
		# Similarity * Score
		totals.setdefault(item,0)
		totals[item]+=prefs[other][item]*sim
		# Sum of similarities
		simSums.setdefault(item,0)
		simSums[item]+=sim

  # Create the normalized list
  rankings=[(total/simSums[item],item) for item,total in totals.items()]

  # Return the sorted list
  rankings.sort()
  rankings.reverse()
  return rankings

def transformPrefs(prefs):
  result={}
  for person in prefs:
	for item in prefs[person]:
	  result.setdefault(item,{})
	  
	  # Flip item and person
	  result[item][person]=prefs[person][item] 
  return result

def calculateSimilarItems(prefs,n=10,similarity=sim_distance):
  # Create a dictionary of items showing which other items they
  # are most similar to.
  result={}
  # Invert the preference matrix to be item-centric
  itemPrefs=transformPrefs(prefs)
  c=0
  for item in itemPrefs:
	# Status updates for large datasets
	c+=1
	if c%100==0: print "%d / %d" % (c,len(itemPrefs))
	# Find the most similar items to this one
	scores=topMatches(itemPrefs,item,n=n,similarity=similarity)
	result[item]=scores
  return result

def calcSimilarUsers(prefs, n=10, similarity=sim_distance):
	result = {}
	itemPrefs = prefs
	c=0
	for item in itemPrefs:
		c+=1
		if c%100==0: print "%d / %d" % (c, len(itemPrefs))
		scores = topMatches(itemPrefs, item, n=n, similarity=similarity)
		result[item]=scores
	return result

def getRecommendedItems(prefs,itemMatch,user):
  userRatings=prefs[user]
  scores={}
  totalSim={}
  # Loop over items rated by this user
  for (item,rating) in userRatings.items( ):

	# Loop over items similar to this one
	for (similarity,item2) in itemMatch[item]:

	  # Ignore if this user has already rated this item
	  if item2 in userRatings: continue
	  # Weighted sum of rating times similarity
	  scores.setdefault(item2,0)
	  scores[item2]+=similarity*rating
	  # Sum of all the similarities
	  totalSim.setdefault(item2,0)
	  totalSim[item2]+=similarity

  # Divide each total score by total weighting to get an average
  rankings=[(score/totalSim[item],item) for item,score in scores.items( )]

  # Return the rankings from highest to lowest
  rankings.sort( )
  rankings.reverse( )
  return rankings

def loadMovieLens():
	# Get movie titles
	movies={}
	for line in open('u.item'):
		(id,title)=line.split('|')[0:2]
		movies[id]=title

	# Load data
	prefs={}
	for line in open('u.data'):
		(user,movieid,rating,ts)=line.split('\t')
		prefs.setdefault(user,{})
		prefs[user][movies[movieid]]=float(rating)

	users={}
	for line in open('u.user'):
		(user, age, gender, job, zipcode) = line.split('|')
		users.setdefault(user, {})
		users[user] = {'age': age, 'gender': gender, 'job': job, 'zipcode': zipcode}
	return prefs, movies, users

def get_avg(prefs, mid, user_filter=lambda x: True):
	ratings = []
	for user, user_ratings in prefs.iteritems():
		if user_filter(users[user]) and user_ratings.has_key(movies[mid]):
			ratings.append(user_ratings[movies[mid]])
	if not ratings:
		return 0.0
	return mean(ratings)

def get_top(sorted_list, key=lambda x, i: x[i][1], n=5):
	top = key(sorted_list, 0)
	top_items = []
	i = 0
	while i < n or key(sorted_list, i) == top:
		top_items.append(sorted_list[i])
		if i < n and key(sorted_list, i) != top:
			top = key(sorted_list, i)
		i += 1
	return top_items

def count_movie_ratings(prefs, mid, transform=False):
	num = 0
	for user, user_ratings in prefs.iteritems():
		if user_ratings.has_key(movies[mid]):
			num += 1
	return num

def get_sim_ratings(title, similar, top_key=lambda x, i: x[i][1], n=2000):
	itemPrefs = transformPrefs(prefs)
	matches = topMatches(itemPrefs, title, n=n, similarity=sim_pearson)
	sorted_m = sorted(matches, key=itemgetter(0), reverse=similar)
	return get_top(sorted_m, key=top_key, n=20)

def tabulate(tuples, caption, label, colnames, output):
	output.write('\\begin{table}[h!]\n')
	output.write('\\centering\n')
	opts = '| ' + ' | '.join(['l' for i in xrange(len(tuples[0]))]) + ' |'
	output.write('\\begin{{tabular}}{{{0}}}\n'.format(opts))
	output.write('\\hline\n')
	header = ' & '.join(['{}' for i in xrange(len(tuples[0]))]).format(*colnames)
	output.write(header + ' \\\\\n\\hline\n')
	for item in tuples:
		temp = ' & '.join(['{}' for i in xrange(len(item))])
		output.write(temp.format(*item) + ' \\\\\n')
	output.write('\\hline\n\\end{tabular}\n')
	output.write('\\caption{{{0}}}\n'.format(caption))
	output.write('\\label{{tab:{0}}}\n'.format(label))
	output.write('\\end{table}\n\n')
print "Parsing data"
prefs, movies, users = loadMovieLens()

def flatten(tup, f=lambda x: (x[0], x[1][0][1], x[1][0][0])):
	return f(tup)

if __name__ == '__main__':
	with open('output.tex', 'w') as outfile:
		question1 = '1. What 5 movies have the highest average ratings?'
		averages_all = {movie: get_avg(prefs, mid) for mid, movie in movies.iteritems()}
		sorted_avg_all = sorted(averages_all.items(), key=itemgetter(1), reverse=True)
		top_all = get_top(sorted_avg_all)
		tabulate(top_all, 'Question 1: Highest Average Rating', 'hiavgrat', ('Title', 'Rating'), 
		         outfile)
		print "done with 1"

		question2 = "2. What 5 movies received the most ratings? Show the movies and the number of ratings sorted by number of ratings."
		movie_counts = {movie: count_movie_ratings(prefs, mid) for mid, movie in movies.iteritems()}
		sorted_counts = sorted(movie_counts.items(), key=itemgetter(1), reverse=True)
		top_movie_counts = get_top(sorted_counts)
		tabulate(top_movie_counts, 'Question 2: Most Ratings', 'mratings', ('Title', 'Ratings Count'), outfile)
		print "done with 2"

		question3 = "3. What 5 movies were rated the highest on average by women? Show the movies and their ratings sorted by ratings."
		averages_w = {movie: get_avg(prefs, mid, user_filter=lambda x: x['gender']=='F') for mid, movie in movies.iteritems()}
		sorted_avg_w = sorted(averages_w.items(), key=itemgetter(1), reverse=True)
		top_avg_w = get_top(sorted_avg_w)
		tabulate(top_avg_w, 'Question 3: Highest Ratings by Women', 'hwratings', ('Title', 'Rating'), outfile)
		print "done with 3"

		question4 = "4. What 5 movies were rated the highest on average by men? Show the movies and their ratings sorted by ratings."
		averages_m = {movie: get_avg(prefs, mid, user_filter=lambda x: x['gender']=='M') for mid, movie in movies.iteritems()}
		sorted_avg_m = sorted(averages_m.items(), key=itemgetter(1), reverse=True)
		top_avg_m = get_top(sorted_avg_m)
		tabulate(top_avg_m, 'Question 4: Highest Ratings by Men', 'hmratings', ('Title', 'Rating'), outfile)
		print "done with 4"

		question5 = "5. What movie received ratings most like Top Gun?"
		sim_top_gun = get_sim_ratings("Top Gun (1986)", similar=True, top_key=lambda x, i: x[i][0])
		tabulate(sim_top_gun, 'Question 5: Most like Top Gun', 'mltg', ('Pearson\'s r', 'Title'), outfile)
		print "done with 5"
		
		question55 = "5 cont'd. Which movie received ratings that were least like Top Gun (negative correlation)"
		dissim_top_gun = get_sim_ratings("Top Gun (1986)", similar=False, top_key=lambda x, i: x[i][0])
		tabulate(dissim_top_gun, 'Question 5.5: Least like Top Gun', 'lltg', ('Pearson\'s r', 'Title'), outfile)
		print "done with 5.5"

		question6 = "6. Which 5 raters rated the most films? Show the raters' IDs and the number of films each rated."
		counts = {user: len(user_ratings) for user, user_ratings in prefs.iteritems()}
		sorted_counts = sorted(counts.items(), key=itemgetter(1), reverse=True)
		top_rater_counts = get_top(sorted_counts)
		tabulate(top_rater_counts, 'Question 6: Most Opinionated Viewers', 'opinion', ('Rater ID', 'Ratings Count'), outfile)
		print "done with 6"

		question7 = "7. Which 5 raters most agreed with each other? Show the raters' IDs and Pearson's r, sorted by r."
		raters_sim = calcSimilarUsers(prefs, n=1, similarity=sim_pearson)
		sorted_sim = sorted(raters_sim.items(), key=lambda x: x[1][0], reverse=True)
		top_sim_raters = get_top(sorted_sim, key=lambda x,i: x[i][1][0])
		top_sim_raters = [flatten(rater) for rater in top_sim_raters]
		tabulate(top_sim_raters, 'Question 7: Bandwagoners', 'band', ('User 1 ID', 'User 2 ID', 'Pearson\'s r'), outfile)
		print "done with 7"

		question8 = "8. Which 5 raters most disagreed with each other (negative correlation)? Show the raters' IDs and Pearson's r, sorted by r"
		sorted_dissim = sorted(raters_sim.items(), key=lambda x: x[1][0])
		top_dissim_raters = get_top(sorted_dissim, key=lambda x,i: x[i][1][0])
		top_dissim_raters = [flatten(rater) for rater in top_dissim_raters]
		tabulate(top_dissim_raters, 'Question 8: Nemeses', 'cont', ('User 1 ID', 'User 2 ID', 'Pearson\'s r'), outfile)
		print "done with 8"

		question9 = "9.  What movie was rated highest on average by men over 40?"
		averages_mo = {movie: get_avg(prefs, mid, user_filter=lambda x: x['gender']=='M' and int(x['age'])>40) for mid, movie in movies.iteritems()}
		sorted_avg_mo = sorted(averages_mo.items(), key=itemgetter(1), reverse=True)
		top_avg_mo = get_top(sorted_avg_mo)
		tabulate(top_avg_mo, 'Question 9: Highest Ratings by Men aged > 40', 'hrbom', ('Title', 'Rating'), outfile)
		print "done with 9"

		question95 = "9 cont'd. By men under 40?"
		averages_mu = {movie: get_avg(prefs, mid, user_filter=lambda x: x['gender']=='M' and int(x['age'])<40) for mid, movie in movies.iteritems()}
		sorted_avg_mu = sorted(averages_mu.items(), key=itemgetter(1), reverse=True)
		top_avg_mu = get_top(sorted_avg_mu)
		tabulate(top_avg_mu, 'Question 9.5: Highest Ratings by Men aged < 40', 'hrbaom', ('Title', 'Rating'), outfile)
		print "done with 9.5"

		question10 = "10. What movie was rated highest on average by women over 40?"
		averages_wo = {movie: get_avg(prefs, mid, user_filter=lambda x: x['gender']=='F' and int(x['age'])>40) for mid, movie in movies.iteritems()}
		sorted_avg_wo = sorted(averages_wo.items(), key=itemgetter(1), reverse=True)
		top_avg_wo = get_top(sorted_avg_wo)
		tabulate(top_avg_wo, 'Question 10: Highest Ratings by Women aged > 40', 'hrbow', ('Title', 'Rating'), outfile)
		print "done with 10"

		question105 = "10. cont'd. By women under 40?"
		averages_wu = {movie: get_avg(prefs, mid, user_filter=lambda x: x['gender']=='F' and int(x['age'])<40) for mid, movie in movies.iteritems()}
		sorted_avg_wu = sorted(averages_wu.items(), key=itemgetter(1), reverse=True)
		top_avg_wu = get_top(sorted_avg_wu)
		tabulate(top_avg_wu, 'Question 10.5: Highest Ratings by Women aged < 40', 'hrbaow', ('Title', 'Rating'), outfile)
		print "done with 10.5"