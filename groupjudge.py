import threading
from multiprocessing import Process
import os
import psutil
from queue import Queue
class Judge():
	def compile(self, submission):
		process = psutil.Process(os.getppid())
    	process.cpu_affinity(self.numberOfJudges)
		f = open("{submission.id}.cpp", 'w')
		f.write(submission.code)
		f.close()
		exec("g++ -std=c++20 -O3 -o {submission.id} {submission.id}.cpp")

	def testOnJudge(self, judge, submission, test):
		process = psutil.Process(os.getppid())
    	process.cpu_affinity(judge)
    	exec("checker.exe < tests/{test}");

	def test(self, submission):
		freeCores = Queue()
		for core in range(self.cpuShift + self.numberOfJudges):
			freeCores.put(core)
		for i in range(submission.numberOfTests):
			p = Process(target=self.testOnJudge, args=(freeCores.get(block=True), submission, i))
			p.start()
			# After for
			p.join()
			# Check verdict
		return "OK"

	def newSubmission(self, submission):
		self.queueToCompile.put(submission)

	def queueToCompileHandler(self):
		while True:
			submission = self.queueToCompile.get(block=True)
			p = Process(target=self.compile, args=(submission))
			p.start()
			p.join()
			# Check compilation
			# self.queueToTest.append(submission)

	def queueToTestHandler(self):
		while True:
			submission = self.queueToCompile.get(block=True)
			verdict = self.test(submission)

	def __init__(numberOfJudges, cpuShift):
		self.queueToCompile = Queue()
		self.queueToTest = Queue()
		self.numberOfJudges = numberOfJudges - 1
		self.cpuShift = cpuShift
		compilationThread = threading.Thread(target=self.queueToCompileHandler)
		testingThread = threading.Thread(target=self.queueToTestHandler)
		compilationThread.start()
		testingThread.start()

class JudgeMachine():
	def __init__(coreSplit):
		self.coreSplit = coreSplit
		self.judges = []
		acc = 0
		for cores in coreSplit:
			self.judges.append(Judge(cores, cpuShift=acc))
			acc += cores
		submissionListener = threading.Thread(target=self.submissionListener)
		submissionListener.start()

	def newSubmission(submission):
		mn = 1e6
		pos = -1
		for i in range(len(self.judges)):
			if mn > len(self.judges[i].queueToCompile):
				mn = len(self.judges[i].queueToCompile)
				pos = i
		self.judges[pos].newSubmission(submission)

	def submissionListener():
		pass

def __main__():
	coreSplit = [5, 5, 5]
	jm = JudgeMachine(coreSplit)