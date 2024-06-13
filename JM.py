from judge import Judge 
import json
import socket
import os

class JudgeMachine():

	def __init__(self, coreSplit):
		socket_path = '/tmp/my_socket'
		self.port = 1024
		self.client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.client.connect(socket_path)

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
			response = self.client.recv(self.port)
			submission = json.loads(json.load(response.decode()))
			self.newSubmission(submission, judge)

	def newSubmission(self, submission, judge):
		self.judges[judge].compile(submission)

	def reportSubmission(self):
		while True:
			for judge in judges: 
				testSubmission = self.judges[judge].testSubmission
				compileSubmission = self.judges[judge].compileSubmission
				if compileSubmission == None:
					self.reportNew()
				self.report(testSubmission)
				self.report(compileSubmission)
			sleep(100)

	def report(self, submission):
		res = dict()
		res['verdict'] = submission['verdict']
		res['id'] = submission['id']
		res['test'] = submission['test']
		res['checkerResult'] = submission['checkerResult']
		res['maxTL'] = submission['maxTL']
		res['maxML'] = submission['maxML']
		res['IOI'] = submission['IOI']
		self.client.sendall(json.dumps(res).encode())
	def reportNew(self):
		pass


