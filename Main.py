import pandas as pd
import random as rd

from itertools import product
import numpy as np

import time

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

def create_wins_dict():
	
	charizard = {symbol:{i:0 for i in range(20)} for symbol in range(10)}
	charizard['coins'] = {i:0 for i in range(20)}
	# print(charizard)
	return(charizard)

winsDict = create_wins_dict()


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
		hasWin = False
		if count >= 4:			
			wins[count][symbol] += 1
			hasWin = True
			
		nineInWindow = False

		global winsDict		
		coins = 0
		if not hasWin:
			
			#let's check for a 9
			for col in range(5):
				for row in range(windowSize[col]):
					if window[col][row] == 9:
						nineInWindow = True			
					if window[col][row] == 6:
						coins+=1
		else:
			winsDict['coins'][0] += 1


		if nineInWindow:

			winsDict['coins'][0] += 1
		else:
			winsDict['coins'][coins] += 1


coinWins = 0
wins = pd.DataFrame(np.zeros(shape = (12,20)))

def play(reel,reelLengths):
	count = 1
	start = time.time()

	for stop in product(np.arange(0,40,1),repeat = 5):
		# if stop == [4,4,4,4,4]:
			# print('fouuurrr')
		if count %1000000 == 0:
			print(count, wins, winsDict['coins'],str(time.time() - start ) + 'seconds have elapsed')
		# stop = [4]*5
		window = get_window(reel,stop,windowSize,reelLengths)
		get_counts(window,allSpots)
		count += 1
	# print(wins,stop)

	return(wins)


reel1,reel1Lengths = clean_reels(file)

def create_wins_dict():
	
	charizard = {symbol:{i:0 for i in range(20)} for symbol in range(10)}
	charizard['coins'] = {i:0 for i in range(20)}
	# print(charizard)
	return(charizard)

winsDict = create_wins_dict()


x = play(reel1,reel1Lengths)
print(coinWins)
x.iloc[10,10] = coinWins
x.to_csv('results.csv')

print(winsDict)
for i in range(20):
	x.iloc[9,i] = winsDict['coin'][i]

x.to_csv('resultswithcoins.csv')
