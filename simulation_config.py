#!/usr/bin/python
# -*- coding: utf-8 -*-

class SimulationRuns:
	def __init__(self, parms, casename):
		self.P = parms
		self.cn = casename
		self.pdict = None
		return
	def getParms(self):
		if self.pdict == None:
			self.__genParmDict()
		return self.pdict
	def __genParmDict(self):
		auxdict = dict()
		for seed in self.P['seed']:
			runname = str.format('{}_seed:{}', self.cn, seed)
			auxdict[runname] = dict(seed=seed)
		for pk in sorted(self.P):
			if pk != 'seed':
				vlist = self.P[pk]
				newdict = dict()
				for ak in auxdict:
					for vi in vlist:
						runname = ak + str.format('_{}:{}', pk, vi)
						newdict[runname] = dict(auxdict[ak])
						newdict[runname][pk] = vi
				auxdict = newdict
		self.pdict = auxdict
		return

class ParseConfig:
	def __init__(self, confarq):
		self.ca = confarq
		self.cd = None
		return
	def getConfig(self):
		if self.cd == None:
			self.__getConfig()
		return self.cd
	def __getConfig(self):
		self.cd = dict()
		arq = open(self.ca, 'r')
		for linha in arq:
			auxQ = linha.strip().split('=')
			parm = auxQ[0].strip()
			auxV = auxQ[1].strip().split(';')
			self.cd[parm] = [x.strip() for x in auxV]
		arq.close()
		return
