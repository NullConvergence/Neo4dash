# Copyright 2019 NullConvergence
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This module is an interface to the database.
In this case the db is a Neo4J."""

from neo4dash.singleton import Singleton
from neo4dash.constants import Constants
from neo4dash.logger import Logger
from neo4dash.queries import Queries

from py2neo import Graph

CT = Constants()
LG = Logger()
QR = Queries()


class Database(metaclass=Singleton):
  def __init__(self, *args, **kwargs):
    """Instantiates a database object"""
    try:
      self.graph = self._connect()
    except Exception as e:
      LG.log_and_raise(e)
    else:
      pass

  def _connect(self):
    """Connects to the db and returns a py2neo
    Graph object with the connection
    :returns: py2neo Graph object
    """
    return Graph(host=CT.DB_URL, user=CT.DB_USER, password=CT.DB_PWD, http_port=CT.PORT)

  def check_self(self):
    """Checks if there is a graph object and, if not,
    it tries to create one
    """
    try:
      if not self.graph:
        self._connect()
    except Exception as e:
      LG.log_and_raise(e)
    else:
      pass

  def get_all_data(self):
    """Returns the nodes and the relationships from
    Neo4j
    :returns:
    """
    self.check_self()
    res = self.graph.run(QR.ALL).data()
    nodes = [self._map_node(n['n']) for n in res if 'n' in n]
    relationships = []
    return nodes, relationships

  def _map_node(self, node):
    """Maps Neo4j Node to UI element
    :param node: dictionary with node elements
    :returns: dictionary with ui details
    """
    return {
      'data':{
        'id': node['hash'] if 'hash' in node else node['name'],
        'label': node['name']
      }
    }

  def _map_rels(self, rel):
    """Maps relationship:"""
    pass