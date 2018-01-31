import pandas as pd
import random as rd

from itertools import product
import numpy as np

# file = 'ReelSet1.txt'
windowSize = [3,4,3,4,3]

pays = pd.read_table("Paytable.txt", header = 0)
pays.columns = pd.to_numeric(pays.columns)
pays = pays.to_dict(orient = 'index')
# print(pays)

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
	windowWin = 0 
	allMatched = []
	winInWindow = False

	hasWin = False
	
	global pays

	for col in range(5):
		# print(col, 'col')
		for row in range(windowSize[col]):
			# print(col,row)

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
			
	
			
			if symCount >=4:
				# print(symbol, ',',symCount)
				windowWin += pays[symbol][symCount]
		        
				winInWindow = True				
				# wins[symCount][symbol] += 1				
				winsDict[symbol][symCount] += 1
				
				hasWin = True

			allMatched.extend(matched)
	return(windowWin)

			# nineInWindow = False

			# global winsDict		
			# coins = 0

			# if hasWin:
			# 	winsDict['coins'][0] += 1
	# if not hasWin:
		
	# 	#let's check for a 9
	# 	for col2 in range(5):
	# 		for row2 in range(windowSize[col2]):
	# 			if window[col2][row2] == 9:
	# 				nineInWindow = True			
	# 			if window[col2][row2] == 6:
	# 				coins+=1

	# 	if nineInWindow:
	# 		winsDict['coins'][0] += 1
	# 	else:
	# 		winsDict['coins'][coins] += 1

		
	# else:
	# 	winsDict['coins'][0] += 1


			
	

# def play():
# 	count = 1
# 	reel1,reel1Lengths = clean_reels(file)
	
# 	for stop in product(np.arange(0,40,1),repeat = 5):

# 		if count %1000000 == 0:
# 			print(count)
# 			#print(winsDict)		

# 		window = get_window(reel1,stop,windowSize,reel1Lengths)
# 		check_window(window,adjs)
# 		count += 1
# 	print(winsDict,stop)


# play()

# def nested_dict_to_df(dic):
# 	df = pd.DataFrame(np.zeros(shape = (20,20)))
# 	for key,value in dic.items():
# 		for k,v in value.items():
# 			k = int(k)
# 			if key == 'coins':
# 				key = int(9)
# 			key = int(key)
# 			v = int(v)
			
# 			df.iloc[key,k] = v
			
# 	return(df)

# ##print(x)
# df = nested_dict_to_df(winsDict)
# df.to_csv('main bestest.csv')


def nested_dict_to_df(dic):
	df = pd.DataFrame(np.zeros(shape = (20,20)))
	for key,value in dic.items():
		for k,v in value.items():
			k = int(k)
			if key == 'coins':
				key = int(9)
			key = int(key)
			v = int(v)
			
			df.iloc[key,k] = v
			
	return(df)

# def play(file):
# 	totalPay = 0 
# 	count = 1
	

# 	position = (0,0)
# 	reel1,reel1Lengths = clean_reels(file)

# 	for stop in product(np.arange(0,40,1),repeat = 5):

# 		if count %1000000 == 0:
# 			print(count)
# 			#print(winsDict)		

# 		window = get_window(reel1,stop,windowSize,reel1Lengths)
# 		#let's set the selected spot to a random symbol. This symbol will lock
# 		lockingSymbol = 
# 		window[stop] = 'apple'

# 		check_window(window,adjs)
# 		count += 1
# 	print(winsDict,stop)

# 	df = nested_dict_to_df(winsDict)

# 	nameToPrint = file.split('.')[0]
# 	df.to_csv(nameToPrint + '.csv')



# print(reels)
# print(reelLengths)
# play(fileName)


# def locking_window(oldWindow,newWindow,symbol):
# 	return([[reels[col][(stop[col] + row)%lengths[col]] for row in range(windowSize[col])] for col in range(5)])

# 	for col in range(5):
# 		for row in range(windowSize[col]):


def locked_window(oldWindow,newWindow,symbol):
	for col in range(5):
		for row in range(windowSize[col]):
			if oldWindow[col][row] == symbol:
				newWindow[col][row] = symbol
			
	return(newWindow)


def one_position(position,symbol, reels,reelLengths):
	positionWin = 0


	window = [['apple' for row in range(windowSize[col])] for col in range(5)]
	window[position[0]][position[1]] = symbol
	
	# positionWin += check_window(window,adjs)
	

	for i in range(4):
		newWindow = get_window(reels,get_stop(reelLengths),windowSize,reelLengths)
		window = locked_window(window,newWindow,symbol)
		# print(window)

		positionWin += check_window(window,adjs)
		# print(window,positionWin)
		# print(newWindow)
		# print(window)
		# print(i)
	# print(positionWin, 'positionWin')
	return(positionWin)
	# print(newWindow)
	# # oldWindow[0][2] = 'hi'
	# print(oldWindow)

	# print(newWindow[position[0]][position[1]])

	# for i in range(5):
	# 	# stop = get_stop(reelLengths)
	# 	newWindow = get_window(reels,get_stop(reelLengths),windowSize,reelLengths)
	# 	row,col = position
	# 	window[row][col] = 'apple'
	# 	print(window)




# play()


# for i in range(1,5+1,1):
# 	fileName = 'ReelSet' + str(i) + '.txt'
# 	play(fileName)
# 	print(fileName)


##print(x)

# pays = pd.read_table("Paytable.txt", header = 0)
# pays.columns = pd.to_numeric(pays.columns)
# pays = pays.to_dict(orient = 'index')
# # print(pays)



# one_position((2,0),0,reels,reelLengths)










# fileName = 'Set 0.txt'
# reels,reelLengths  = clean_reels(fileName)






numReelSets = 9

df = pd.DataFrame(columns = ['Set ' + str(reelSet) for reelSet in range(numReelSets)])
winPercents = pd.DataFrame(columns = ['Set ' + str(reelSet) for reelSet in range(numReelSets)])

import time
start_time = time.time()
for reelSet in range(numReelSets):
	# print(df)
	fileName = 'Set ' + str(reelSet) + '.txt'
	# print(fileName)
	reels,reelLengths = clean_reels(fileName)

	x = []
	y = []

	for col in range(5):
		for row in range(windowSize[col]):
			
			its = 1000000
			totWin = 0
			count = 1
			for it in range(its):
				
				# if count % 1000 == 0:
				# 	print(totWin/count)
				totWin += one_position((col,row),reelSet,reels,reelLengths)
				count += 1

			rowInfo = [col,row,totWin/its]

			x.append(rowInfo)
			y.append(totWin/its)
	print(reelSet)
	print(y)
	df['Set ' + str(reelSet)] = x
	winPercents['Set ' + str(reelSet)] = y
	# print(df)
	# print(winPercents)

	print('You have finished {} reel sets and it took you {}'.format(reelSet + 1, time.strftime("%H:%M:%S",time.gmtime(time.time() - start_time))))

			# print(totWin/its, (col,row))

df.to_csv('AllData.csv')
winPercents.to_csv('Percents.csv')
