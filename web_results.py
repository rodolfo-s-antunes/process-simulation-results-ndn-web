#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import os.path
from multiprocessing import Process

from simulation_config import *
from parse_utils import *
from parse_clients import ParseClients
from parse_traffic import ParseTraffic
from parse_cache import ParseCache

BASEDIR = '/progs/ndnSIM/ns-3'
CODEDIR = BASEDIR+'/scratch'
TRACEDIR = BASEDIR+'/trace'
MYDIR = os.getcwd()

class ProcessResults(Process):
	def __init__(self, runparms, resultdir, name):
		Process.__init__(self)
		sr = SimulationRuns(runparms.getConfig(), name)
		self.P = sr.getParms()
		self.name = name
		self.rd = resultdir
		return
	def run(self):
		# print "Processing traffic {}...".format(self.name)
		# self.ProcessTraffic()
		# print "Processing caches {}...".format(self.name)
		# self.ProcessCaches()
		print "Processing clients {}...".format(self.name)
		self.ParseClients()
		print "Generating outputs {}...".format(self.name)
		self.GenOutput()
		return
	def ProcessTraffic(self):
		trafficlist = list()
		interestlist = list()
		manifestlist = list()
		combinedlist = list()
		for pk in self.P:
			arqname = self.rd+'/raw/traffic-'+pk+'.txt'
			if os.path.exists(arqname):
				auxres = ParseTraffic(arqname)
				trafficlist.append(auxres.totaldata)
				interestlist.append(auxres.totalinterests)
				manifestlist.append(auxres.totalmanifests)
				combinedlist.append(auxres.totalcombined)
		self.traffic = mergeDictCurves(trafficlist)
		self.interests = mergeDictCurves(interestlist)
		self.manifesttraffic = mergeDictCurves(manifestlist)
		self.combinedtraffic = mergeDictCurves(combinedlist)
		return
	def ProcessCaches(self):
		hitratiolist = list()
		for pk in self.P:
			arqname = self.rd+'/raw/cache-'+pk+'.txt'
			if os.path.exists(arqname):
				auxres = ParseCache(arqname)
				hitratiolist.append(auxres.hitratio)
		self.hitratio = mergeDictCurves(hitratiolist)
		return
	def ParseClients(self):
		delaycdf = list()
		delaytuples = list()
		contentdelaycdf = list()
		contenthopscdf = list()
		manifestdelaycdf = list()
		manifesthopcdf = list()
		hopsratio = list()
		reqlist = list()
		hopstopub = list()
		serverrequests = list()
		serverdata = list()
		sizes = list()
		requestsperpart = dict(data=list(), layout=list(), code=list())
		for pk in self.P:
			arqname = self.rd+'/raw/out-'+pk
			if os.path.exists(arqname):
				auxres = ParseClients(arqname)
				delaycdf.append(auxres.delays)
				delaytuples.append(auxres.delaytuples)
				contentdelaycdf.append(auxres.contentdelays)
				contenthopscdf.append(auxres.contenthops)
				manifestdelaycdf.append(auxres.manifestdelays)
				manifesthopcdf.append(auxres.manifesthops)
				hopsratio.append(auxres.hopsratio)
				hopstopub.append(auxres.hopstopub)
				reqlist.append([x[1] for x in auxres.requests])
				serverrequests.append(auxres.serverrequests)
				serverdata.append(auxres.serverdata)
				sizes.append(auxres.sizes)
				for ip in auxres.partrequests: requestsperpart[ip].append(auxres.partrequests[ip])
		self.delaycdf = concatCurves(delaycdf)
		self.delaytuples = concatTupleList(delaytuples)
		self.contentdelaycdf = concatCurves(contentdelaycdf)
		self.contenthopscdf = mergeCurves(contenthopscdf, revsort=False)
		self.manifestdelaycdf = concatCurves(manifestdelaycdf)
		self.manifesthopcdf = mergeCurves(manifesthopcdf, revsort=False)
		self.hopsratio = mergeCurves(hopsratio, revsort = False)
		self.hopstopub = mergeCurves(hopstopub, revsort=False, ceiling=True)
		self.reqdist = mergeCurves(reqlist)
		self.servreq = mergeCurves(serverrequests, sortres=False)
		self.servdata = mergeCurves(serverdata, sortres=False)
		self.sizes = mergeDictCurves(sizes)
		self.partrequests = mergeXparmCurves(partrequests)
		print 'Median eccentricity', self.name, Eccentricity(hopstopub)
		return
	def GenOutput(self):
		# Traffic Stuff
		out = '{}/contenttraffic-{}.txt'.format(self.rd, self.name)
		WriteDictData(out, self.traffic)
		out = '{}/manifesttraffic-{}.txt'.format(self.rd, self.name)
		WriteDictData(out, self.manifesttraffic)
		out = '{}/traffic-{}.txt'.format(self.rd, self.name)
		WriteDictData(out, self.combinedtraffic)
		# Cache Stuff
		out = '{}/hitratio-{}.txt'.format(self.rd, self.name)
		WriteDictData(out, self.hitratio)
		# Client Stuff
		out = '{}/contenthops-{}.txt'.format(self.rd, self.name)
		WriteLineNormalized(out, self.contenthopscdf)
		out = '{}/manifesthops-{}.txt'.format(self.rd, self.name)
		WriteLineNormalized(out, self.manifesthopcdf)
		out = '{}/hopsratio-{}.txt'.format(self.rd, self.name)
		WriteLineNormalized(out, self.hopsratio)
		out = '{}/hopstopub-{}.txt'.format(self.rd, self.name)
		WriteLineNormalized(out, self.hopstopub)		
		out = '{}/requestdist-{}.txt'.format(self.rd, self.name)
		WriteLineNormalized(out, self.reqdist)
		out = '{}/serverrequests-{}.txt'.format(self.rd, self.name)
		WriteLine(out, self.servreq)
		out = '{}/serverdata-{}.txt'.format(self.rd, self.name)
		WriteLine(out, self.servdata)
		out = '{}/delaycomponents-{}.txt'.format(self.rd, self.name)
		WriteTupleData(out, self.delaytuples)
		out = '{}/delaycdf-{}.txt'.format(self.rd, self.name)
		WriteLineNormalized(out, self.delaycdf)
		out = '{}/contentdelaycdf-{}.txt'.format(self.rd, self.name)
		WriteLineNormalized(out, self.contentdelaycdf)
		out = '{}/manifestdelaycdf-{}.txt'.format(self.rd, self.name)
		WriteLineNormalized(out, self.manifestdelaycdf)
		out = '{}/contentsizes-{}.txt'.format(self.rd, self.name)
		WriteDictData(out, self.sizes)
		out = '{}/requestsperpart-{}.txt'.format(self.rd, self.name)
		WriteDictDataBar(out, self.requestsperpart)
		return
