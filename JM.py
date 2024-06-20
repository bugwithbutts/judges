from judge import Judge 
import json
import socket
import os
import threading
import time
from sock import send, recv

# JudgeMachine manages judges on one computer
class JudgeMachine():

	def __init__(self, coreSplit, judgeShift):
		# Socket connection
		socket_path = './socket4'
		self.port = 1024
		self.client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.client.connect(socket_path)

		self.judgeShift = judgeShift
		self.coreSplit = coreSplit

		# Creating judges with shift for cpu cores
		self.judges = []
		shift = 0
		for cores in coreSplit:
			self.judges.append(Judge(cores, cpuShift=shift))
			shift += cores

		# Starting thread for submission checking
		submissionHandler = threading.Thread(target=self.submissionHandler)
		submissionHandler.start()

		# Starting thread for reporting about submissions on judges
		reportHandler = threading.Thread(target=self.reportSubmission)
		reportHandler.start()

	# Checking if new submission has been made
	def submissionHandler(self):
		while True:
			# Recieving new json
			raw = recv(self.client)

			# Parsing json to dict
			submission = json.loads(raw)

			self.newSubmission(submission, submission['judge'] - self.judgeShift)

	# Send submission to judge
	def newSubmission(self, submission, judge):
		if len(self.judges[judge].compileSubmission) == 0:
			self.judges[judge].compile(submission)

	# Report about submissions on judges
	def reportSubmission(self):
		while True:
			for num, judge in enumerate(self.judges, 0): 
				# Lock is used not to get partial-copied submission from judge
				with judge.lock:
					testSubmission = judge.testSubmission
					compileSubmission = judge.compileSubmission
					readySubmissions = judge.readySubmissions

					# If compile core is empty
					if len(compileSubmission) == 0:
						self.reportNew(num)
					# Report about compiling submission
					else:
						self.report(compileSubmission)

					# Report about testing submission
					if len(testSubmission) != 0:
						self.report(testSubmission)

				# Report about tested submissions and delete it from the list
				n = len(readySubmissions)
				for sub in range(n):
				    self.report(readySubmissions[0])
				    readySubmissions.pop(0)
			time.sleep(1) # Should do it periodical?

	# Report about submission status
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

		# Convert json to string and send it to socket
		send(json.dumps(res), self.client)
		
	# Report that judge has free compile core
	def reportNew(self, judge):
		res = dict()
		res['type'] = "judge"
		res['judge'] = judge + self.judgeShift

		# Convert json to string and send it to socket
		send(json.dumps(res), self.client)