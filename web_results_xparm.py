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

class ProcessResultsXparm(Process):
	def __init__(self, runparms, resultdir, name, xparm):
		Process.__init__(self)
		sr = SimulationRuns(runparms.getConfig(), name)
		self.P = sr.getParms()
		self.name = name
		self.rd = resultdir
		self.xparm = xparm
		return
	def run(self):
		print "Processing traffic {}...".format(self.name)
		self.ProcessTraffic()
		print "Processing cache {}...".format(self.name)
		self.ProcessCache()
		print "Processing client {}...".format(self.name)
		self.ProcessClients()
		print "Generating outputs {}...".format(self.name)
		self.GenOutput()
		return
	def ProcessTraffic(self):
		trafficlist = dict()
		interestlist = dict()
		manifestlist = dict()
		combinedlist = dict()
		for pk in self.P:
			arqname = self.rd+'/raw/traffic-'+pk+'.txt'
			if os.path.exists(arqname):
				xval = float(self.P[pk][self.xparm])
				auxres = ParseTraffic(arqname)
				if xval not in trafficlist: trafficlist[xval] = list()
				trafficlist[xval].append(SumDict(auxres.totaldata))
				if xval not in interestlist: interestlist[xval] = list()
				interestlist[xval].append(SumDict(auxres.totalinterests))
				if xval not in manifestlist: manifestlist[xval] = list()
				manifestlist[xval].append(SumDict(auxres.totalmanifests))
				if xval not in combinedlist: combinedlist[xval] = list()
				combinedlist[xval].append(SumDict(auxres.totalcombined))
		self.traffic = mergeXparmCurves(trafficlist)
		self.interests = mergeXparmCurves(interestlist)
		self.manifesttraffic = mergeXparmCurves(manifestlist)
		self.combinedtraffic = mergeXparmCurves(combinedlist)
		return
	def ProcessCache(self):
		hitratiolist = dict()
		for pk in self.P:
			arqname = self.rd+'/raw/cache-'+pk+'.txt'
			if os.path.exists(arqname):
				xval = float(self.P[pk][self.xparm])
				auxres = ParseCache(arqname)
				if xval not in hitratiolist: hitratiolist[xval] = list()
				hitratiolist[xval].append(AverageDict(auxres.hitratio))
		self.hitratio = mergeXparmCurves(hitratiolist)
		return
	def ProcessClients(self):
		delaycdf = dict()
		contentdelaycdf = dict()
		contenthopscdf = dict()
		manifestdelaycdf = dict()
		manifesthopcdf = dict()
		serverrequests = dict()
		serverdata = dict()
		for pk in self.P:
			arqname = self.rd+'/raw/out-'+pk
			if os.path.exists(arqname):
				xval = float(self.P[pk][self.xparm])
				auxres = ParseClients(arqname)
				if xval not in delaycdf: delaycdf[xval] = list()
				delaycdf[xval].append(AverageList(auxres.delays))
				if xval not in contentdelaycdf: contentdelaycdf[xval] = list()
				contentdelaycdf[xval].append(AverageList(auxres.contentdelays))
				if xval not in contenthopscdf: contenthopscdf[xval] = list()
				contenthopscdf[xval].append(AverageList(auxres.contenthops))
				if xval not in manifestdelaycdf: manifestdelaycdf[xval] = list()
				manifestdelaycdf[xval].append(AverageList(auxres.manifestdelays))
				if xval not in manifesthopcdf: manifesthopcdf[xval] = list()
				manifesthopcdf[xval].append(AverageList(auxres.manifesthops))
				if xval not in serverrequests: serverrequests[xval] = list()
				serverrequests[xval].append(AverageList(auxres.serverrequests))
				if xval not in serverdata: serverdata[xval] = list()
				serverdata[xval].append(SumList(auxres.serverdata))
		self.delaycdf = mergeXparmCurves(delaycdf)
		self.contentdelaycdf = mergeXparmCurves(contentdelaycdf)
		self.contenthopscdf = mergeXparmCurves(contenthopscdf)
		self.manifestdelaycdf = mergeXparmCurves(manifestdelaycdf)
		self.manifesthopcdf = mergeXparmCurves(manifesthopcdf)
		self.servreq = mergeXparmCurves(serverrequests)
		self.servdata = mergeXparmCurves(serverdata)
		return
	def GenOutput(self):
		out = '{}/contenttraffic-{}.txt'.format(self.rd, self.name)
		WriteXparmData(out, self.traffic)
		out = '{}/manifesttraffic-{}.txt'.format(self.rd, self.name)
		WriteXparmData(out, self.manifesttraffic)
		out = '{}/traffic-{}.txt'.format(self.rd, self.name)
		WriteXparmData(out, self.combinedtraffic)
		out = '{}/hitratio-{}.txt'.format(self.rd, self.name)
		WriteXparmData(out, self.hitratio)
		out = '{}/contenthops-{}.txt'.format(self.rd, self.name)
		WriteXparmData(out, self.contenthopscdf)
		out = '{}/manifesthops-{}.txt'.format(self.rd, self.name)
		WriteXparmData(out, self.manifesthopcdf)
		out = '{}/serverrequests-{}.txt'.format(self.rd, self.name)
		WriteXparmData(out, self.servreq)
		out = '{}/serverdata-{}.txt'.format(self.rd, self.name)
		WriteXparmData(out, self.servdata)
		out = '{}/delaycdf-{}.txt'.format(self.rd, self.name)
		WriteXparmData(out, self.delaycdf)
		out = '{}/contentdelaycdf-{}.txt'.format(self.rd, self.name)
		WriteXparmData(out, self.contentdelaycdf)
		out = '{}/manifestdelaycdf-{}.txt'.format(self.rd, self.name)
		WriteXparmData(out, self.manifestdelaycdf)
