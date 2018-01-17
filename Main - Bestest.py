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
(2,1):[(3,1),(3,2),(2,2),(1,2),(1,1),(2,0)],
(2,2):[(1,3),(1,2),(2,1),(3,2),(3,3)],
(3,0):[(4,0),(3,1),(2,0)],
(3,1):[(4,0),(4,1),(3,2),(2,1),(2,0),(3,0)],
(3,2):[(4,1),(4,2),(3,3),(2,2),(2,1),(3,1)],
(3,3):[(2,2),(3,2),(4,2)],
(4,0):[(4,1),(3,1),(3,0)],
(4,1):[(4,2),(3,2),(3,1),(4,0)],
(4,2):[(3,3),(3,2),(4,1)]}

def create_wins_dict():
	
	charizard = {symbol:{i:0 for i in range(20)} for symbol in range(10)}
	charizard['coins'] = {i:0 for i in range(20)}
	# print(charizard)
	return(charizard)

winsDict = create_wins_dict()

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
	winInWindow = False
	for col in range(5):
		for row in range(windowSize[col]):
			
			symbol = window[col][row]

			#let's keep track of the spots where adjacent symbols are
			spot = (col,row)
			
			matched = [spot]
			checked = [spot]
			count = 1
			
			i = 0

			if spot not in allMatched:
				continu = True
			while  continu:
					spot = matched[i]
					
					continu,matched,checked = check_adjacent_spots(adjs,spot,matched,checked,count,symbol,window)
					
					i+=1

					if i >(len(matched)-1):
						continu = False

			symCount = len(matched)
			
			global winsDict

			if symCount >=4:
				return(None)
                
				winInWindow = True				
				wins[symCount][symbol] += 1				
				winsDict[symbol][symCount] += 1

			allMatched.extend(matched)
	#maybe nines are ok so I am going to not check for nines
	if not winInWindow:
		coins = 0
		#let's check for a 9
		for col in range(5):
			for row in range(windowSize[col]):			
				if window[col][row] == 6:
					coins+=1
	
		winsDict['coins'][coins] += 1

def play():
	count = 1
	reel1,reel1Lengths = clean_reels(file)
	
	for stop in product(np.arange(0,40,1),repeat = 5):

		if count %1000000 == 0:
			print(count)
		# if count == 10003:
		# 	return(winsDict)

		window = get_window(reel1,stop,windowSize,reel1Lengths)
		check_window(window,adjs)
		count += 1
	print(winsDict,stop)


play()

def nested_dict_to_df(dic):
	df = pd.DataFrame(np.zeros(shape = (20,20)))
	for key,value in dic.items():
		for k,v in value.items():
			k = int(k)
			if key == 'coins':
				key = int(9)
			key = int(key)
			v = int(v)
			# if key == 'coins':
			# 	df.iloc[9,k] = v
			# else:
			# 	print(key,k,v)
			df.iloc[key,k] = v
			# print(key,k,v)
	return(df)

##print(x)
df = nested_dict_to_df(winsDict)
df.to_csv('myresultsnew.csv')
