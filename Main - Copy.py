import pandas as pd
import random as rd

from itertools import product
import numpy as np

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



adjs = {(0,0):[(1,0),(1,1),(0,1)],(0,1):[(0,0),(1,1),(1,2),(0,2)],(0,2):[(0,1),(1,2),(1,3)],
(1,0):[(2,0),(1,1),(0,0)],
(1,1):[(1,0),(2,0),(2,1),(1,2),(0,1),(0,0)],
(1,2):[(1,1),(2,1),(2,2),(1,3),(0,2),(0,1)],
(1,3):[(0,2),(1,2),(2,2)],
(2,0):[(3,0),(3,1),(2,1),(1,1),(1,0)],
(2,1):[(3,1),(3,2),(2,2),(1,2),(1,1),(2,1)],
(2,2):[(1,3),(1,2),(2,1),(3,2),(3,3)],
(3,0):[(4,0),(3,1),(2,0)],
(3,1):[(4,0),(4,1),(3,2),(2,1),(2,0),(3,0)],
(3,2):[(4,1),(4,2),(3,3),(2,2),(2,1),(3,1)],
(3,3):[(2,2),(3,2),(4,2)],
(4,0):[(4,1),(3,1),(3,0)],
(4,1):[(4,2),(3,2),(3,1),(4,0)],
(4,2):[(3,3),(3,2),(4,1)]}






def check_adjacent_spots(adjs,start,matched,checked,count,symbol,window):
	# continu = False
	continu = True
	for curSpot in adjs[start]:
		if curSpot not in checked and curSpot not in matched:
			checked.append(curSpot)
			col,row = curSpot
			if window[col][row] == symbol:
				count += 1
				matched.append(curSpot)
				continu = True
	return(continu,matched,checked)


def check_window(window,adjs):
	allMatched = []
	for col in range(5):
		for row in range(windowSize[col]):
			# col = 0
			# row = 0
			symbol = window[col][row]

			#let's keep track of the spots where adjacent symbols are
			spot = (col,row)
			# print(symbol, 'sym')
			matched = [spot]
			checked = [spot]
			count = 1
			# continu = True
			i = 0

			if spot not in allMatched:
				continu = True
			while  continu:
					spot = matched[i]
					# print(spot, 'spot')
					continu,matched,checked = check_adjacent_spots(adjs,spot,matched,checked,count,symbol,window)
					# print(matched, 'hi')
					i+=1

					if i >(len(matched)-1):
						continu = False

			symCount = len(matched)


			global wins

			if symCount >=4:
				# print('hi')
				wins[symCount][symbol] += 1

			# global winsDict
			# if symCount >= 4:
			# 	try:
			# 		winsDict[symbol][symCount] += 1
			# 	except:
			# 		winsDict[symbol][symCount] = 1
			
			# print(matched, 'matched', str(len(matched)) + 'count')
			allMatched.extend(matched)


		# print(window[col][row],spot)




wins = pd.DataFrame(np.zeros(shape = (12,20)))

def play():
	count = 1
	
	for stop in product(np.arange(0,40,1),repeat = 5):

		if count %100000 == 0:
			print(count, wins)

		window = get_window(reel1,stop,windowSize,reel1Lengths)
		check_window(window,adjs)
		count += 1
	print(wins,stop)

	return(wins)


##stop = [17,20,17,17,17]
##window = get_window(reel1,stop,windowSize,reel1Lengths)
##print(window)
##check_window(window,adjs)
##print(wins)

x = play()
print(x)
x.to_csv('results.csv')




