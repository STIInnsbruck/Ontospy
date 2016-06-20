# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

from . import *  # imports __init__
from .. import ontospy
import json

# TEMPLATE: D3 PACK HIERARCHY
# http://mbostock.github.io/d3/talk/20111116/pack-hierarchy.html
# https://github.com/d3/d3/wiki/Pack-Layout
# http://bl.ocks.org/nilanjenator/4950148



# ===========
# June 20, 2016 : notes
# ===========
# ....



def run(graph, save_on_github=False):
	"""
	"""
	try:
		ontology = graph.ontologies[0]
		uri = ontology.uri
	except:
		ontology = None
		uri = graph.graphuri

	# ontotemplate = open("template.html", "r")
	ontotemplate = open(ontospy.ONTOSPY_VIZ_TEMPLATES + "d3_packhierarchy.html", "r")
	t = Template(ontotemplate.read())

	jsontree_classes = _buildJSON_standardTree(graph.toplayer, MAX_DEPTH=99)
	c_total = len(graph.classes)


	if len(graph.toplayer) == 1:
		# the first element can be the single top level
		JSON_DATA_CLASSES = json.dumps(jsontree_classes[0])
	else:
		# hack to make sure that we have a default top level object
		JSON_DATA_CLASSES = json.dumps({'children': jsontree_classes, 'name': 'OWL:Thing',})

	c = Context({
					"ontology": ontology,
					"main_uri" : uri,
					"STATIC_PATH": ontospy.ONTOSPY_VIZ_STATIC,
					"save_on_github" : save_on_github,
					'JSON_DATA_CLASSES' : JSON_DATA_CLASSES,
					"TOTAL_CLASSES": c_total,
				})

	rnd = t.render(c)

	return safe_str(rnd)









# ===========
# Utilities
# ===========



def _buildJSON_standardTree(old, MAX_DEPTH, level=1):
	"""
	  For d3s viz like the expandable tree
	  all we need is a json with name, children and size .. eg

	  {
	 "name": "flare",
	 "children": [
	  {
	   "name": "analytics",
	   "children": [
		{
		 "name": "cluster",
		 "children": [
		  {"name": "AgglomerativeCluster", "size": 3938},
		  {"name": "CommunityStructure", "size": 3812},
		  {"name": "HierarchicalCluster", "size": 6714},
		  {"name": "MergeEdge", "size": 743}
		 ]
		},
		etc...
	"""
	out = []
	for x in old:
		d = {}
		# print "*" * level, x.label
		d['name'] = x.bestLabel(quotes=False).replace("_", " ")
		d['fullname'] = x.bestLabel(quotes=False)
		if True or not x.children():
			d['size'] = 1000 # len(x.children()) or 1
		# d['size'] = x.npgarticlestot or 10	 # setting 10 as default size
		if x.children() and level < MAX_DEPTH:
			d['children'] = _buildJSON_standardTree(x.children(), MAX_DEPTH, level+1)
		out += [d]

	return out







if __name__ == '__main__':
	import sys
	try:
		# script for testing - must launch this module
		# >python -m ontospy.viz.viz_packh

		func = locals()["run"] # main func dynamically
		run_test_viz(func)

		sys.exit(0)

	except KeyboardInterrupt as e: # Ctrl-C
		raise e

