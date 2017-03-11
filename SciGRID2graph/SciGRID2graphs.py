#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017
# Johannes K. Fichte, TU Wien, Austria
#
# SciGrid2graphs is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.  SciGrid2graphs is
# distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.  You should have received a copy of the
# GNU General Public License along with SciGrid2graphs.  If not, see
# <http://www.gnu.org/licenses/>.
#

import cStringIO
import csv
import os
from utils.graph import Graph

path = '~/benchmark/suites/powergrid/SciGRID/data/03_network/'
path = os.path.expanduser(path)

def create_graph(filepath):
    g=Graph()
    with open(filepath) as csvfile:
        reader  = csv.DictReader(csvfile)
        #print reader.fieldnames
        for row in reader:
            g.add_edge(row['v_id_1'],row['v_id_2'])
    return g

def write_graph(graph,output_file, filename,output_type='gr'):
    output = cStringIO.StringIO()
    symtab=labels=False
    if output_type == 'gr':
        from utils.graph_output import write_gr as write_graph
        write_graph(graph, symtab=symtab, labels=labels, output=output, gtfs_filename=filename)
    elif output_type == 'gml':
        from utils.graph_output import write_gml as write_graph
        write_graph(graph, symtab=symtab, labels=labels, output=output, gtfs_filename=filename)
    if output_file!='-':
        #logging.warning('Writing output to file')
        with open(output_file, 'w') as f:
            f.write(output.getvalue())
            f.flush()
        #logging.warning('Output written to: %s' % output_file)
    else:
        print output.getvalue()


import os
for filename in os.listdir(path):
    if not filename.endswith('.csvdata'):
        continue
    if filename.startswith('vertices'):
        continue
    filepath=os.path.join(path,filename)
    print 'filepath=', filepath
    basename = os.path.basename(filepath)
    g=create_graph(filepath)
    #write_graph(graph=g,filename='test.gr')
    write_graph(output_file='%s.gr'%filename, graph=g,filename=basename, output_type='gr')
    #write_graph(output_file='%s.gml'%filename, graph=g,filename=basename, output_type='gml')

