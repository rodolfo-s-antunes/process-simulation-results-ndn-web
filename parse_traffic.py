#!/usr/bin/python
# -*- coding: utf-8 -*-

class ParseTraffic:
	MANIFESTSIZE = 1
	def __init__(self, arqname):
		self.totaldata = dict()
		self.totalinterests = dict()
		self.totalmanifests = dict()
		self.ReadArq(arqname)
		self.GenerateResults()
		return
	def ReadArq(self, arqname):
		with open(arqname, 'r') as arq:
			arq.readline()
			for L in arq:
				Q = L.strip().split()
				if Q[3].find('=net') >= 0:
					if Q[4] == 'OutData':
						self.ProcessOutData(Q)
					elif Q[4] == 'OutInterests':
						self.ProcessOutInterests(Q)
					elif Q[4] == 'RecvManifests':
						self.ProcessRecvManifests(Q)
		return
	def ProcessOutData(self, Q):
		lnidx = Q[3][Q[3].find('=net(')+5:Q[3].find(')')]
		alink = '{}-{}'.format(Q[1], lnidx)
		if alink not in self.totaldata:
			self.totaldata[alink] = float(Q[6])
		else:
			self.totaldata[alink] += float(Q[6])
		return
	def ProcessOutInterests(self, Q):
		lnidx = Q[3][Q[3].find('=net(')+5:Q[3].find(')')]
		alink = '{}-{}'.format(Q[1], lnidx)
		if alink not in self.totalinterests:
			self.totalinterests[alink] = float(Q[6])
		else:
			self.totalinterests[alink] += float(Q[6])
		return
	def ProcessRecvManifests(self, Q):
		lnidx = Q[3][Q[3].find('=net(')+5:Q[3].find(')')]
		alink = '{}-{}'.format(Q[1], lnidx)
		if alink not in self.totalmanifests:
			self.totalmanifests[alink] = float(Q[5])*self.MANIFESTSIZE
		else:
			self.totalmanifests[alink] += float(Q[5])*self.MANIFESTSIZE
		return
	def GenerateResults(self):
		self.totalcombined = {ik: self.totaldata[ik]+self.totalmanifests[ik] for ik in self.totaldata}
		return
