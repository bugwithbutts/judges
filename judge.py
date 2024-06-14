import threading
from multiprocessing import Process, Manager, Lock
from multiprocessing import freeze_support, set_start_method
import os
import psutil
import multiprocessing
import time
class Judge():

	def __init__(self, numberOfJudges, cpuShift):
		self.compileSubmission = Manager().dict()
		self.testSubmission = Manager().dict()
		self.readySubmissions = Manager().list()
		self.numberOfJudges = numberOfJudges - 1
		self.cpuShift = cpuShift

	def compile(self, submission):
		for i, j in submission.items():
			self.compileSubmission[i] = j
		process = Process(target=self.compileOnCore)
		process.start()

	def compileOnCore(self):
		p = psutil.Process()
		p.cpu_affinity([self.numberOfJudges * 2, self.numberOfJudges * 2 + 1])
		self.compileSubmission['verdict'] = "C"
		# check compiler
		submission_id = self.compileSubmission['id']
		f = open(f'{submission_id}.cpp', 'w') # Where?
		f.write(self.compileSubmission['code'])
		f.close()
		print("almost compiled")
		ret = os.system(f'g++ -O3 -o {submission_id}.exe {submission_id}.cpp')
		ret = 0
		self.compileSubmission['exe'] = f'{submission_id}.exe'
		if ret != 0:
			self.compileSubmission['verdict'] = "CE"
			return
		while len(self.testSubmission) != 0:
			pass
		print("compiled")
		for i, j in self.compileSubmission.items():
			self.testSubmission[i] = j
		self.compileSubmission.clear()
		testingThread = Process(target=self.test)
		testingThread.start()
		testingThread.join()

	def test(self):
		print('test')
		pid = os.getpid()
		self.testSubmission['verdict'] = "T"
		self.testSubmission['test'] = 1
		self.freeCores = Manager().Queue()
		for core in range(self.cpuShift, self.cpuShift + self.numberOfJudges):
			self.freeCores.put(core)
		for i in range(self.testSubmission['numberOfTests']):
			# print(i)
			self.testSubmission['test'] = i
			if self.testSubmission['verdict'] != 'T':
				break
			p = Process(target=self.testOnCore, args=(self.freeCores.get(block=True), self.testSubmission['exe'], i,))
			p.start()
		while self.freeCores.qsize() != self.numberOfJudges:
			pass
		self.readySubmissions.append(self.testSubmission)
		self.testSubmission.clear()
		print('all')
		
	def testOnCore(self, core, submission, test):
		p = psutil.Process()
		p.cpu_affinity([core * 2, core * 2 + 1])
		for i in range(10):
			cnt = 1
			for j in range(10000000):
				cnt *= j
		self.freeCores.put(core)
    	# change verdict only when it was on early tests