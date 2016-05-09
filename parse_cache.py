#!/usr/bin/python
# -*- coding: utf-8 -*-

class ParseCache:
	def __init__(self, arqname):
		self.cachehits = dict()
		self.cachemisses = dict()
		self.ReadArq(arqname)
		self.GenerateResults()
		del self.cachehits
		del self.cachemisses
		return
	def ReadArq(self, arqname):
		with open(arqname, 'r') as arq:
			arq.readline()
			for L in arq:
				Q = L.strip().split()
				if Q[2] == 'CacheHits':
					self.ProcessCacheHits(Q)
				elif Q[2] == 'CacheMisses':
					self.ProcessCacheMisses(Q)
		return
	def ProcessCacheHits(self, Q):
		auxpop = Q[1][3:]
		if auxpop not in self.cachehits:
			self.cachehits[auxpop] = float(Q[3])
		else:
			self.cachehits[auxpop] += float(Q[3])
		return
	def ProcessCacheMisses(self, Q):
		auxpop = Q[1][3:]
		if auxpop not in self.cachemisses:
			self.cachemisses[auxpop] = float(Q[3])
		else:
			self.cachemisses[auxpop] += float(Q[3])
		return
	def GenerateResults(self):
		self.hitratio = dict()
		for ik in sorted(self.cachehits):
			auxreqs = self.cachemisses[ik] + self.cachehits[ik]
			if not auxreqs:
				self.hitratio[ik] = 0.0
			else:
				self.hitratio[ik] = self.cachehits[ik] / auxreqs
		return
