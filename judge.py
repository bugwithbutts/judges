import threading
from multiprocessing import Process
import os
import psutil
from queue import Queue
class Judge():

	def __init__(self, numberOfJudges, cpuShift):
		self.compileSubmission = None
		self.testSubmission = None
		self.numberOfJudges = numberOfJudges - 1
		self.cpuShift = cpuShift

	def compile(self, submission):
		process = psutil.Process(os.getppid())
    	process.cpu_affinity(self.cpu_shift + self.numberOfJudges)
    	self.compileSubmission = submission 
		f = open("{submission.id}.cpp", 'w')
		f.write(submission['code'])
		f.close()
		ret = exec("g++ -std=c++20 -O3 -o {submission.id} {submission.id}.cpp")
		submission['exe'] = "{submission_id}"
		if ret != 0:
			self.compileSubmission['verdict'] = "CE"
			return
		while self.testSubmission != None:
			pass
		self.compileSubmission = None
		testingThread = threading.Thread(target=self.test, args=(submission))
		testingThread.start()

	def test(self, submission):
		self.testSubmission = submission
		freeCores = Queue()
		for core in range(self.cpuShift, self.cpuShift + self.numberOfJudges):
			freeCores.put(core)
		for i in range(submission['numberOfTests']):
			if submission.count('verdict'):
				break
			p = Process(target=self.testOnCore, args=(freeCores.get(block=True), submission['exe'], i))
			p.start()
		while freeCores.qsize() != self.numberOfJudges:
			pass
		self.testSubmission = None
		
	def testOnCore(self, submission, core, test):
		process = psutil.Process(os.getppid())
    	process.cpu_affinity(core)
    	exec("checker.exe < tests/{test}");
    	# change verdict only when it was on earely tests