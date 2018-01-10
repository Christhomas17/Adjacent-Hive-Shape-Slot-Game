import pandas as pd
import random as rd

from itertools import product
import numpy as np

import time

# print(time.time())

file = 'ReelSet1.txt'
windowSize = [3,4,3,4,3]

def clean_reels(file):
	reel = pd.read_table(file, header = 0, sep = '\t')
	reel.columns = [0,1,2,3,4]

	lengths = [len(reel.iloc[:,col]) for col in reel]

	reel = reel.to_dict(orient = 'dict')
	
	return(reel, lengths)


def get_stop(lengths):
	return([rd.randint(0,lengths[col] - 1) for col in range(len(lengths))])


def get_window(reels,stop,windowSize,lengths):		
	return([[reels[col][(stop[col] + row)%lengths[col]] for row in range(windowSize[col])] for col in range(5)])

allSpots = [(0,0),(0,1),(0,2),
            (1,0),(1,1),(1,2),(1,3),
            (2,0),(2,1),(2,2),
            (3,0),(3,1),(3,2),(3,3),
            (4,0),(4,1),(4,2)]




adjs = {(0,0):[(1,0),(1,1),(0,1)],
(0,1):[(0,0),(1,1),(1,2),(0,2)],
(0,2):[(0,1),(1,2),(1,3)],
(1,0):[(2,0),(1,1),(0,0)],
(1,1):[(1,0),(2,0),(2,1),(1,2),(0,1),(0,0)],
(1,2):[(1,1),(2,1),(2,2),(1,3),(0,2),(0,1)],
(1,3):[(0,2),(1,2),(2,2)],
(2,0):[(3,0),(3,1),(2,1),(1,1),(1,0)],
(2,1):[(3,1),(3,2),(2,2),(1,2),(1,1),(2,1),(2,0)],
(2,2):[(1,3),(1,2),(2,1),(3,2),(3,3)],
(3,0):[(4,0),(3,1),(2,0)],
(3,1):[(4,0),(4,1),(3,2),(2,1),(2,0),(3,0)],
(3,2):[(4,1),(4,2),(3,3),(2,2),(2,1),(3,1)],
(3,3):[(2,2),(3,2),(4,2)],
(4,0):[(4,1),(3,1),(3,0)],
(4,1):[(4,2),(3,2),(3,1),(4,0)],
(4,2):[(3,3),(3,2),(4,1)]}

def remove_matched(spots,matched):
	for item in matched:
		if item in spots:
			spots.remove(item)
	return(spots)

# matched = [(2,2),(1,0)]

# print(remove_matched(allSpots,matched))

def check_adjacents(spot,matched,checked,symbol,window):
	global adjs
	# print(spot, 'spot')
	# print(adjs[spot], 'adjs')
	for curSpot in adjs[spot]:
		# print(curSpot, 'cur spot')
		if curSpot not in checked and curSpot not in matched:
			checked.append(curSpot)
			col,row = curSpot

			if window[col][row] == symbol:
				matched.append(curSpot)
	return(matched,checked)

def get_counts(window,allSpots):

	global wins

	spotsToCheck = [x for x in allSpots]
	# print(spotsToCheck)
	matched = []
	checked = []
	for spot in spotsToCheck:
		# print(spot)
		i = 0 
		matched = [spot]
		checked = [spot]
		col,row = spot
		# print(col,row)
		symbol = window[col][row]
		continu = True	
		# print(matched[i], adjs[matched[i]])
		while continu == True:
			# print(matched, matched[i], 'matched',i)
			# print(type(matched[i]), matched[i], adjs[matched[i]])
			# matched,checked = check_adjacents(matched[i],matched,checked,symbol)
			# print(matched,matched[i])

			# if symbol == 1:
				# print(matched)

			matched,checked = check_adjacents(matched[i],matched,checked,symbol,window)
			i+=1
			if i >= len(matched):
				continu = False


		
		for Spot in matched:
			try:
				# print(Spot)
				spotsToCheck.remove(Spot)
			except:
				pass

		count = len(matched)

		if count >= 4:
			# pass
			# print(symbol,len(matched),window)
			wins[count][symbol] += 1
		# print(matched,symbol)


wins = pd.DataFrame(np.zeros(shape = (12,20)))

# window = [[0,0,1],
# [0,0,1,2],
# [1,1,2],
# [0,0,0,2],
# [0,0,2]]

# get_counts(window,allSpots)
# print(wins)

# x = (2,0)
# print(adjs[x])

# for key,value in adjs.items():
# 	print(key,value)


def play(reel,reelLengths):
	count = 1
	start = time.time()

	for stop in product(np.arange(0,40,1),repeat = 5):
		# if stop == [4,4,4,4,4]:
			# print('fouuurrr')
		if count %1000000 == 0:
			print(count, wins, str(time.time() - start ) + 'seconds have elapsed')
		# stop = [4]*5
		window = get_window(reel,stop,windowSize,reelLengths)
		get_counts(window,allSpots)
		count += 1
	# print(wins,stop)

	return(wins)


reel1,reel1Lengths = clean_reels(file)
# print(reel1)
# window = get_window(reel1,[4]*5,windowSize,reel1Lengths)
# print(window)
# get_counts(window,allSpots)
# print(wins)

x = play(reel1,reel1Lengths)
x.to_csv('results.csv')

















# def check_adjacent_spots(adjs,start,matched,checked,count,symbol,window):
# 	# continu = False
# 	continu = True
# 	for curSpot in adjs[start]:
# 		if curSpot not in checked and curSpot not in matched:
# 			checked.append(curSpot)
# 			col,row = curSpot
# 			if window[col][row] == symbol:
# 				count += 1
# 				matched.append(curSpot)
# 				continu = True
# 	return(continu,matched,checked)


# def check_window(window,adjs):
# 	allMatched = []
# 	for col in range(5):
# 		for row in range(windowSize[col]):
# 			# col = 0
# 			# row = 0
# 			symbol = window[col][row]

# 			#let's keep track of the spots where adjacent symbols are
# 			spot = (col,row)
# 			# print(symbol, 'sym')
# 			matched = [spot]
# 			checked = [spot]
# 			count = 1
# 			# continu = True
# 			i = 0

# 			if spot not in allMatched:
# 				continu = True
# 			while  continu:
# 					spot = matched[i]
# 					# print(spot, 'spot')
# 					continu,matched,checked = check_adjacent_spots(adjs,spot,matched,checked,count,symbol,window)
# 					# print(matched, 'hi')
# 					i+=1

# 					if i >(len(matched)-1):
# 						continu = False

# 			symCount = len(matched)


# 			global wins

# 			if symCount >=4:
# 				# print('hi')
# 				wins[symCount][symbol] += 1

# 			# global winsDict
# 			# if symCount >= 4:
# 			# 	try:
# 			# 		winsDict[symbol][symCount] += 1
# 			# 	except:
# 			# 		winsDict[symbol][symCount] = 1
			
# 			# print(matched, 'matched', str(len(matched)) + 'count')
# 			allMatched.extend(matched)


# 		# print(window[col][row],spot)




# wins = pd.DataFrame(np.zeros(shape = (12,20)))

# def play():
# 	count = 1
	
# 	for stop in product(np.arange(0,40,1),repeat = 5):

# 		if count %100000 == 0:
# 			print(count, wins)

# 		window = get_window(reel1,stop,windowSize,reel1Lengths)
# 		check_window(window,adjs)
# 		count += 1
# 	print(wins,stop)

# 	return(wins)


##stop = [17,20,17,17,17]
##window = get_window(reel1,stop,windowSize,reel1Lengths)
##print(window)
##check_window(window,adjs)
##print(wins)

# x = play()
# print(x)
# x.to_csv('results.csv')



