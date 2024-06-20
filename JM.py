from judge import Judge 
import json
import socket
import os
import threading
import time
from sock import send, recv
class JudgeMachine():

	def __init__(self, coreSplit, judgeShift):
		socket_path = './socket4'
		self.port = 1024
		self.client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.client.connect(socket_path)
		self.judgeShift = judgeShift
		self.coreSplit = coreSplit
		self.judges = []
		acc = 0
		for cores in coreSplit:
			self.judges.append(Judge(cores, cpuShift=acc))
			acc += cores
		submissionHandler = threading.Thread(target=self.submissionHandler)
		submissionHandler.start()
		reportHandler = threading.Thread(target=self.reportSubmission)
		reportHandler.start()

	def submissionHandler(self):
		while True:
			submission = json.loads(recv(self.client))
			self.newSubmission(submission, submission['judge'] - self.judgeShift)

	def newSubmission(self, submission, judge):
		if len(self.judges[judge].compileSubmission) == 0:
			self.judges[judge].compile(submission)

	def reportSubmission(self):
		while True:
			for num, judge in enumerate(self.judges, 0): 
				with judge.lock:
					testSubmission = judge.testSubmission
					compileSubmission = judge.compileSubmission
					readySubmissions = judge.readySubmissions
					if len(compileSubmission) == 0:
						self.reportNew(num)
					else:
						self.report(compileSubmission)
					if len(testSubmission) != 0:
						self.report(testSubmission)
				n = len(readySubmissions)
				for sub in range(n):
				    self.report(readySubmissions[0])
				    readySubmissions.pop(0)
			time.sleep(1) # Should do it periodical?

	def report(self, submission):
		res = dict()
		#print(submission)
		res['type'] = "submission"
		res['verdict'] = submission['verdict']
		res['id'] = submission['id']
		res['test'] = submission['test']
		res['checkerResult'] = submission['checkerResult']
		res['maxTL'] = submission['maxTL']
		res['maxML'] = submission['maxML']
		res['IOI'] = submission['IOI']
		send(json.dumps(res), self.client)
		
	def reportNew(self, judge):
		res = dict()
		res['type'] = "judge"
		res['judge'] = judge + self.judgeShift
		send(json.dumps(res), self.client)


