#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from simulation_config import ParseConfig
from web_results import ProcessResults
from web_results_xparm import ProcessResultsXparm

class Main():
	def __init__(self):
		if len(sys.argv) < 3 or len(sys.argv) > 4:
			print str.format('Usage: {} <config.conf> <resultdir> [<xparm>]', sys.argv[0])
			sys.exit(1)
		conffile = sys.argv[1]
		resultdir = sys.argv[2]
		xparm = ""
		if len(sys.argv) == 4:
			xparm = sys.argv[3]
		pc = ParseConfig(conffile)
		if not xparm:
			pd = ProcessResults(pc, resultdir, 'default')
			pr = ProcessResults(pc, resultdir, 'relations')
		else:
			pd = ProcessResultsXparm(pc, resultdir, 'default', xparm)
			pr = ProcessResultsXparm(pc, resultdir, 'relations', xparm)
		pd.start()
		pr.start()
		pd.join()
		pr.join()
		return

if __name__ == '__main__':
	Main()
