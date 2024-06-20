import threading
from multiprocessing import Process, Manager, Lock
from multiprocessing import freeze_support, set_start_method
import os
import psutil
import multiprocessing
import time
class Judge():

	def __init__(self, numberOfJudges, cpuShift):
		# Manager is used to share resources among processes
		self.compileSubmission = Manager().dict()
		self.testSubmission = Manager().dict()
		self.readySubmissions = Manager().list()

		# Last core is for compilation
		self.numberOfJudges = numberOfJudges - 1
		self.cpuShift = cpuShift
		self.lock = Lock()

	# Compile submission
	def compile(self, submission):
		# Copy submission to compileSubmissiob
		with self.lock:
			for i, j in submission.items():
				self.compileSubmission[i] = j

		# Start compilation process on compile core
		process = Process(target=self.compileOnCore)
		process.start()

	# Compile compileSubmission on compile core
	def compileOnCore(self):
		# Setting compile core
		p = psutil.Process()
		p.cpu_affinity([self.cpuShift + self.numberOfJudges])


		self.compileSubmission['verdict'] = "C"
		submission_id = self.compileSubmission['id']

		# G++ compilation
		if self.compileSubmission['compiler'] == "g++":
			f = open(f'{submission_id}.cpp', 'w') # Where?
			f.write(self.compileSubmission['code'])
			f.close()
			ret = os.system(f'g++ -O3 -o {submission_id}.exe {submission_id}.cpp')
			self.compileSubmission['exe'] = f'{submission_id}.exe'

			# Compilation error 
			if ret != 0:
				self.compileSubmission['verdict'] = "CE"
				# Add tested submission to readySubmissions list
				with self.lock:
					self.readySubmissions.append(dict(self.compileSubmission))
					self.compileSubmission.clear()
				
		print("almost compiled")

		# Wait for previous submission stops testing
		while len(self.testSubmission) != 0:
			pass
		print("compiled")

		# Copy compileSubmission to testSubmission 
		with self.lock:
			for i, j in self.compileSubmission.items():
				self.testSubmission[i] = j
			self.compileSubmission.clear()

		# Start testing process and wait while it ends
		testingThread = Process(target=self.test)
		testingThread.start()
		testingThread.join()

	# Launch testing of each test
	def test(self):
		print('test')

		self.testSubmission['verdict'] = "T"
		self.testSubmission['test'] = 1

		# Free for testing cores are storing in queue  
		self.freeCores = Manager().Queue()
		for core in range(self.cpuShift, self.cpuShift + self.numberOfJudges):
			self.freeCores.put(core)

		# Iterate through tests and launch them
		for i in range(int(self.testSubmission['numberOfTests'])):
			self.testSubmission['test'] = i

			# If the submission has already failed some test
			if self.testSubmission['verdict'] != 'T':
				break

			# Get free core or wait for it appearence
			core = self.freeCores.get(block=True)

			# Start process of testing i test on core
			p = Process(target=self.testOnCore, args=(core, self.testSubmission['exe'], i,))
			p.start()

		# Wait for all cores stop testing
		while self.freeCores.qsize() != self.numberOfJudges:
			pass

		# If submission has not failed any test, set verdict to OK  
		if self.testSubmission['verdict'] == 'T':
			self.testSubmission['verdict'] = 'OK'

		# Add tested submission to readySubmissions list
		with self.lock:
			self.readySubmissions.append(dict(self.testSubmission))
			self.testSubmission.clear()
		print('all')
		
	# Run submission file on test on core and change verdict if necessary 
	def testOnCore(self, core, submission, test):
		# Setting testing core
		p = psutil.Process()
		p.cpu_affinity([core])
		
		for i in range(10):
			cnt = 1
			for j in range(10000000):
				cnt *= j
		self.freeCores.put(core)
    	# change verdict only when it was on early tests
