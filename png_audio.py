import numpy as np
from scipy.io.wavfile import read
from scipy.io.wavfile import write
import cv2
import math
import queue
from threading import Thread
import time
###
def png_encode(list):#pass a list of size 3; 1. 2D, signed, 16bit integer array 2. image hieght 3. image length : converts to a BGR array to be used for a png file
	print('============================================================')
	print('============================================================')
	
	print('file read, encoding waveform')
	print(list[0].size)
	
	pic_array = np.zeros((int(list[1]), int(list[2]), 3), dtype=int)#creating an empty BGR array to be filled with values
	z=0
	y=0
	place_holder = [0, 0, 0]
	for x in list[0]:#png BGR values range from 0-255; reduces the 16bit integers to 8bit and then stores the sign data in the red value; 16bit values below 128 are reduced to 1
		if (x[0] < 0) and (x[1] < 0):
			place_holder =  [math.ceil(x[0]/np.negative(128)), math.ceil(x[1]/np.negative(128)), 25]
			
		elif (x[0] > 0) and (x[1] > 0):
			place_holder =  [math.ceil(x[0]/128), math.ceil(x[1]/128), 50]
			
		elif (x[0] > 0) and (x[1] < 0):
			place_holder =  [math.ceil(x[0]/128), math.ceil(x[1]/np.negative(128)), 75]
		
		elif (x[0] < 0) and (x[1] > 0):
			place_holder =  [math.ceil(x[0]/np.negative(128)), math.ceil(x[1]/128), 100]
			
		pic_array[z][y] = place_holder
		z+=1
		if z >= int(list[1]):
			z=0
			y+=1
	print('done')
	return (pic_array)
###
def wav_to_png(filename):#converts a wav file to a png file
	list = read(filename, 1)
	begin = time.time()
	
	if math.ceil(math.sqrt(list[1].size))%12 == 0: #png_decode makes use of 6 threads for faster decoding, this makes sure the png file produces a BGR array that can be evenly split between the threads
		length = math.ceil(math.sqrt(list[1].size))
		heigth = math.ceil(math.sqrt(list[1].size))
	elif math.ceil(math.sqrt(list[1].size))%12 == 1:
		length = math.ceil(math.sqrt(list[1].size)) + 11
		heigth = math.ceil(math.sqrt(list[1].size)) + 11
	elif math.ceil(math.sqrt(list[1].size))%12 == 2:
		length = math.ceil(math.sqrt(list[1].size)) + 10
		heigth = math.ceil(math.sqrt(list[1].size)) + 10
	elif math.ceil(math.sqrt(list[1].size))%12 == 3:
		length = math.ceil(math.sqrt(list[1].size)) + 9
		heigth = math.ceil(math.sqrt(list[1].size)) + 9
	elif math.ceil(math.sqrt(list[1].size))%12 == 4:
		length = math.ceil(math.sqrt(list[1].size))+8
		heigth = math.ceil(math.sqrt(list[1].size))+8
	elif math.ceil(math.sqrt(list[1].size))%12 == 5:
		length = math.ceil(math.sqrt(list[1].size))+7
		heigth = math.ceil(math.sqrt(list[1].size))+7
	elif math.ceil(math.sqrt(list[1].size))%12 == 6:
		length = math.ceil(math.sqrt(list[1].size))+6
		heigth = math.ceil(math.sqrt(list[1].size))+6
	elif math.ceil(math.sqrt(list[1].size))%12 == 7:
		length = math.ceil(math.sqrt(list[1].size))+5
		heigth = math.ceil(math.sqrt(list[1].size))+5
	elif math.ceil(math.sqrt(list[1].size))%12 == 8:
		length = math.ceil(math.sqrt(list[1].size))+4
		heigth = math.ceil(math.sqrt(list[1].size))+4
	elif math.ceil(math.sqrt(list[1].size))%12 == 9:
		length = math.ceil(math.sqrt(list[1].size))+3
		heigth = math.ceil(math.sqrt(list[1].size))+3
	elif math.ceil(math.sqrt(list[1].size))%12 == 10:
		length = math.ceil(math.sqrt(list[1].size))+2
		heigth = math.ceil(math.sqrt(list[1].size))+2
	elif math.ceil(math.sqrt(list[1].size))%12 == 11:
		length = math.ceil(math.sqrt(list[1].size))+1
		heigth = math.ceil(math.sqrt(list[1].size))+1
	
	pic_array = png_encode([list[1],length,heigth])
	
	print('waveform encoded, writing file')
	cv2.imwrite('output/'+filename.replace('wav', 'png'), pic_array, [cv2.IMWRITE_PNG_COMPRESSION, 20])
	print('file created, time elapsed: '+str(time.time()-begin))
###	
def png_decode(BGR_array):#pass png's BGR array : converts to a signed 16 bit waveform to be used for a wav file
	x=0
	y=0
	audio_array = np.zeros((int(BGR_array.shape[1]*BGR_array.shape[0]), 2), dtype=int)#empty waveform array to be populated
	for audi in audio_array:
		if BGR_array[x][y][2] == 25:#png BGR values range from 0-255; increases the 8bit integers to 16bit and then retrieves the sign data from the red value
			audi[0]=BGR_array[x][y][0]*np.negative(128)
			audi[1]=BGR_array[x][y][1]*np.negative(128)
		elif (BGR_array[x][y][2] == 50):
			audi[0]=BGR_array[x][y][0]*128
			audi[1]=BGR_array[x][y][1]*128
		elif (BGR_array[x][y][2] == 75):
			audi[0]=BGR_array[x][y][0]*128
			audi[1]=BGR_array[x][y][1]*np.negative(128)
		elif (BGR_array[x][y][2] == 100):
			audi[0]=BGR_array[x][y][0]*np.negative(128)
			audi[1]=BGR_array[x][y][1]*128
		x+=1
		if x >= BGR_array.shape[0]:
			x=0
			y+=1
	cleaned_list = []#removes BGR values of [0, 0, 0] from the decoded png
	for x in range(int(audio_array.size/2)):
		if not(audio_array[x][0] == 0 and audio_array[x][1] == 0):
				cleaned_list.append(audio_array[x][0])
				cleaned_list.append(audio_array[x][1])
			
	cleaned_array = np.asarray(cleaned_list, dtype=np.int16)
	return cleaned_array
###
def png_to_wav(filename):#converts a png file to a wav file
	im = cv2.imread(filename, 1)
	print('============================================================')
	print('============================================================')
	print('decoding waveform')
	begin = time.time()
	
	splt = np.split(im,2, axis=1)#splits the BGR array into 6 parts that are then passed into 6 threads for decoding 
	splt1 = np.split(splt[0],3, axis=1)
	splt2 = np.split(splt1[0],2, axis=1)
	splt3 = np.split(splt1[1],2, axis=1)
	splt4 = np.split(splt1[2],2, axis=1)
			
	que1 = queue.Queue()
	que2 = queue.Queue()
	que3 = queue.Queue()
	que4 = queue.Queue()
	que5 = queue.Queue()
	que6 = queue.Queue()
	
	t1 = Thread(target = lambda q, arg1: q.put(png_decode(arg1)), args=(que1, splt2[0]))
	t2 = Thread(target = lambda q, arg1: q.put(png_decode(arg1)), args=(que2, splt2[1]))
	t3 = Thread(target = lambda q, arg1: q.put(png_decode(arg1)), args=(que3, splt3[0]))
	t4 = Thread(target = lambda q, arg1: q.put(png_decode(arg1)), args=(que4, splt3[1]))
	t5 = Thread(target = lambda q, arg1: q.put(png_decode(arg1)), args=(que5, splt4[0]))
	t6 = Thread(target = lambda q, arg1: q.put(png_decode(arg1)), args=(que6, splt4[1]))
	
	t1.start()
	t2.start()
	t3.start()
	t4.start()
	t5.start()
	t6.start()
	
	t1.join()
	t2.join()
	t3.join()
	t4.join()
	t5.join()
	t6.join()
	
	result1 = que1.get()
	result2 = que2.get()
	result3 = que3.get()
	result4 = que4.get()
	result5 = que5.get()
	result6 = que6.get()
		
	print('writing file')
	write('output/'+filename.replace('png', 'wav'), 88200, np.concatenate((result1, result2, result3, result4, result5, result6)))
	print('file created, elapsed time '+str(time.time()-begin))
###
answer = input('convert wav to png[1] or png to wav[2]?')
if answer == str(1):
	filename = input('name of file?:	')
	wav_to_png(filename)
	png_to_wav('output/'+filename.replace('wav', 'png'),)
elif answer == str(2):
	filename = input('name of file?:	')
	png_to_wav(filename)
