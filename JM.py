from judge import Judge 
import json
import socket
import os

class JudgeMachine():

	def __init__(self, coreSplit, judgeShift):
		socket_path = '/tmp/my_socket1'
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
			response = self.client_submission.recv(self.port)
			submission = json.loads(json.load(response.decode()))
			self.newSubmission(submission, judge)

	def newSubmission(self, submission, judge):
		self.judges[judge].compile(submission)

	def reportSubmission(self):
		while True:
			for num, judge in enumerate(judges, 0): 
				testSubmission = self.judges[judge].testSubmission
				compileSubmission = self.judges[judge].compileSubmission
				readySubmissions = self.judges[judge].readySubmissions
				if len(compileSubmission) == 0:
					self.reportNew(num)
				else:
					self.report(compileSubmission)
				if len(j.compileSubmission) != 0:
					self.report(testSubmission)
				for sub in readySubmissions:
					self.report(sub)
				self.judges[judge].readySubmissions.clear()
			sleep(100)

	def report(self, submission):
		res = dict()
		res['type'] = "submission"
		res['verdict'] = submission['verdict']
		res['id'] = submission['id']
		res['test'] = submission['test']
		res['checkerResult'] = submission['checkerResult']
		res['maxTL'] = submission['maxTL']
		res['maxML'] = submission['maxML']
		res['IOI'] = submission['IOI']
		self.client_submission.sendall(json.dumps(res).encode())
		
	def reportNew(self, judge):
		res = dict()
		res['type'] = "judge"
		res['judge'] = judge + self.judgeShift
		self.client_judge.sendall(json.dumps(res).encode())


