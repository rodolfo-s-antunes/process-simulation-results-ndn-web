#!/usr/bin/python
# -*- coding: utf-8 -*-

import operator

class ParseClients:
	HOPDELAY = 1.0
	MANMULT = 1.0
	def __init__(self, arqname):
		self.delaydict = dict()
		self.sizedict = dict()
		self.requestdict = dict()
		self.serverrequestdict = dict()
		self.contentdelaysdict = dict()
		self.contenthops = list()
		self.manifestdelaysdict = dict()
		self.manifesthops = list()
		self.hopsratio = list()
		self.hopstopub = list()
		self.requestperpart = dict(data=dict(), layout=dict(), code=dict())
		self.ReadArq(arqname)
		self.GenerateResults()
		del self.delaydict
		del self.manifestdelaysdict
		del self.contentdelaysdict
		del self.sizedict
		del self.requestdict
		del self.serverrequestdict
		del self.requestperpart
		return
	def ReadArq(self, arqname):
		with open(arqname, 'r') as arq:
			for L in arq:
				Q = L.strip().split()
				if len(Q) > 6:
					if Q[6] == 'DownloadDelays':
						self.ProcessDownloadDelays(Q)
					elif Q[6] == 'DownloadHops':
						self.ProcessDownloadHops(Q)
					elif Q[6] == 'ManifestLatency':
						self.ProcessManifestLatency(Q)
					elif Q[6] == 'ManifestPath':
						self.ProcessManifestHops(Q)
				if len(Q) > 4:
					if Q[4] == 'ObjectRequest':
						self.ProcessObjectRequest(Q)
				if len(Q) > 2:
					if Q[2] == 'DataServed':
						self.ProcessDataServed(Q)
					elif Q[2] == 'ManifestServed':
						self.ProcessManifestServed(Q)
		return
	def ProcessDownloadDelays(self, Q):
		contentid = '{}-{}'.format(Q[2], Q[4])
		auxdelay = self.HOPDELAY
		for it in xrange(8,len(Q)):
			auxdelay += float(Q[it])
		self.contentdelaysdict[contentid] = auxdelay
		if contentid not in self.delaydict:
			self.delaydict[contentid] = 0.0
		self.delaydict[contentid] += auxdelay
		return
	def ProcessDownloadHops(self, Q):
		hopsaccum = 0.0
		hopscount = 0.0
		hopstopub = float(Q[8])
		for it in xrange(10,len(Q)):
			hopsaccum += float(Q[it])
			hopscount += 1.0
		auxhops = (hopsaccum/hopscount)
		self.contenthops.append(auxhops)
		self.hopsratio.append(auxhops/hopstopub)
		self.hopstopub.append(hopstopub)
		return
	def ProcessManifestLatency(self, Q):
		contentid = '{}-{}'.format(Q[2], Q[4])
		auxdelay = float(Q[7]) * self.MANMULT
		self.manifestdelaysdict[contentid] = auxdelay
		if contentid not in self.delaydict:
			self.delaydict[contentid] = 0.0
		self.delaydict[contentid] += auxdelay
		return
	def ProcessManifestHops(self, Q):
		auxhops = float(Q[7])
		self.manifesthops.append(auxhops)
		return
	def ProcessDataServed(self, Q):
		auxobj = '{}-{}-{}'.format(Q[5],Q[4],Q[6])
		if auxobj not in self.serverrequestdict:
			self.serverrequestdict[auxobj] = 1.0
		else:
			self.serverrequestdict[auxobj] += 1.0
		return
	def ProcessObjectRequest(self, Q):
		auxcon = '{}-{}-{}'.format(Q[5],Q[6],Q[8])
		if auxcon not in self.requestdict:
			self.requestdict[auxcon] = 1.0
		else:
			self.requestdict[auxcon] += 1.0
		auxpart = '{}-{}'.format(Q[5],Q[8])
		if auxpart not in self.requestperpart[Q[6]]:
			self.requestperpart[Q[6]][auxpart] = 1.0
		else:
			self.requestperpart[Q[6]][auxpart] += 1.0
		return
	def ProcessManifestServed(self, Q):
		self.sizedict['{}-{}-{}'.format(Q[4], 'data', Q[7])] = float(Q[10])
		self.sizedict['{}-{}-{}'.format(Q[4], 'layout', Q[8])] = float(Q[11])
		self.sizedict['{}-{}-{}'.format(Q[4], 'code', Q[9])] = float(Q[12])
		return
	def SummarizeContentRequests(self):
		self.partrequests = dict()
		self.partrequests['data'] = AverageDict(self.requestperpart['data'])
		self.partrequests['layout'] = AverageDict(self.requestperpart['layout'])
		self.partrequests['code'] = AverageDict(self.requestperpart['code'])
		return
	def SummarizeContentSizes(self):
		self.sizes = dict(data=0.0, layout=0.0, code=0.0)
		for itk in self.sizedict:
			if itk.find('layout') >= 0:
				self.sizes['layout'] += self.sizedict[itk]
			elif itk.find('code') >= 0:
				self.sizes['code'] += self.sizedict[itk]
			elif itk.find('data') >= 0:
				self.sizes['data'] += self.sizedict[itk]
		return
	def GenerateResults(self):
		self.contentdelays = sorted(self.contentdelaysdict.values())
		self.contenthops.sort()
		self.manifestdelays = sorted(self.manifestdelaysdict.values())
		self.manifesthops.sort()
		self.hopsratio.sort()
		self.hopstopub.sort()
		self.delaytuples = list()
		for it in self.delaydict:
			if (it in self.contentdelaysdict) and (it in self.manifestdelaysdict):
				self.delaytuples.append(tuple([self.delaydict[it], self.contentdelaysdict[it], self.manifestdelaysdict[it]]))
		self.delaytuples.sort(key=operator.itemgetter(0), reverse=True)
		self.delays = sorted(self.delaydict.values())
		self.requests = sorted(self.requestdict.iteritems(), key=operator.itemgetter(1), reverse=True)
		poporder = [x[0] for x in self.requests]
		self.serverrequests = list()
		self.serverdata = list()
		for itk in poporder:
			if itk in self.serverrequestdict and itk in self.sizedict:
				serversize = self.serverrequestdict[itk]*self.sizedict[itk]
				reqsize = self.requestdict[itk]*self.sizedict[itk]
				self.serverrequests.append(serversize/reqsize)
				self.serverdata.append(serversize)
		self.SummarizeContentSizes()
		self.SummarizeContentRequests()
		return
