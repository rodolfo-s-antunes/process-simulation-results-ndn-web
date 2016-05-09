#!/usr/bin/python
# -*- coding: utf-8 -*-

import math, operator

import numpy as np
import scipy as sp
import scipy.stats as sps

def confInt(vector, confidence=0.95):
	if len(vector) < 1:
		return 0
	else: 
		data = np.array(vector)
		m = np.mean(data)
		return sp.stats.sem(data) * sps.t._ppf((1.0+confidence)/2.0, len(data)-1)

def SumList(points):
	return float(sum(points))

def AverageList(points):
	return float(sum(points))/float(len(points))

def SumDict(points):
	return float(sum(points.values()))

def AverageDict(points):
	return float(sum(points.values()))/float(len(points))

def Eccentricity(pointlist):
	auxlist = list()
	for it in pointlist:
		auxlist += it
	auxarray = np.array(auxlist)
	return dict(min=auxarray.min(), max=auxarray.max(), median=np.median(auxarray))

def mergeXparmCurves(curvedict):
	res = dict()
	for ik in curvedict:
		res[ik] = dict()
		res[ik]['avg'] = np.average(np.array(curvedict[ik]))
		res[ik]['stddev'] = np.std(np.array(curvedict[ik]))
		res[ik]['conf'] = confInt(curvedict[ik])
	return res

def concatCurves(curvelist, revsort=True, sortres=True):
	result = list()
	for it in curvelist:
		result += it
	if sortres: result.sort(reverse=revsort)
	return result

def concatTupleList(tuplist, revsort=True, sortres=True):
	result = list()
	for it in tuplist:
		result += it
	if sortres: result.sort(key=operator.itemgetter(0), reverse=revsort)
	return result

def mergeCurves(curvelist, revsort=True, sortres=True, ceiling=False):
	maxcurve = 0
	for ic in curvelist:
		if len(ic) > maxcurve: maxcurve = len(ic)
	result = list()
	pc = 0
	while pc < maxcurve:
		auxlist = list()
		for ic in curvelist:
			if pc<len(ic):
				auxlist.append(ic[pc])
		if len(auxlist) < 1:
			result.append(0)
		else:
			auxavg = sum(auxlist)/float(len(auxlist))
			if ceiling:
				result.append(math.ceil(auxavg))
			else:
				result.append(auxavg)
		pc += 1
	if sortres: result.sort(reverse=revsort)
	return result

def mergeDictCurves(curvelist):
	idxlist = list()
	for ck in curvelist:
		for ick in ck:
			if ick not in idxlist: idxlist.append(ick)
	result = dict()
	for idx in idxlist:
		auxlist = list()
		for ck in curvelist:
			if idx in ck:
				auxlist.append(ck[idx])
		result[idx] = sum(auxlist)/float(len(auxlist))
	return result

def WriteLine(arqout, datalist):
	with open(arqout, 'w') as out:
		counter = 1
		for it in datalist:
			out.write('{:.8f}\t{:.8f}\n'.format(counter, it))
			counter += 1
	return

def WriteLineNormalized(arqout, datalist, normvert=False, normhoriz=True):
	counter = 1.0
	numpts = float(len(datalist))
	sumpts = float(sum(datalist))
	with open(arqout, 'w') as out:
		for it in datalist:
			if normhoriz:
				hp = counter/numpts
			else:
				hp = counter
			if normvert:
				out.write('{:.8f}\t{:.8f}\n'.format(hp, it/sumpts))
			else:
				out.write('{:.8f}\t{:.8f}\n'.format(hp, it))
			counter += 1.0
	return

def WriteXparmData(arqout, datadict):
	with open(arqout, 'w') as out:
		for xk in sorted(datadict):
			d = datadict[xk]
			out.write('{:.8f}\t{:.8f}\t{:.8f}\t{:.8f}\n'.format(xk, d['avg'], d['stddev'], d['conf']))
	return

def WriteDictData(arqout, datadict):
	with open(arqout, 'w') as out:
		for it in datadict:
			out.write('{}\t{:.8f}\n'.format(it, datadict[it]))
	return

def WriteDictDataBar(arqout, datadict, offset=1.00):
	with open(arqout, 'w') as out:
		count = offset
		for it in datadict:
			out.write('{}\t{}\t{:.8f}\n'.format(count, it, datadict[it]))
			count += offset
	return

def WriteTupleData(arqout, tuplist):
	with open(arqout, 'w') as out:
		counter = 1
		for it in tuplist:
			out.write('{}'.format(counter))
			for itt in it:
				out.write('\t{:.8f}'.format(itt))
			out.write('\n')
			counter += 1
	return