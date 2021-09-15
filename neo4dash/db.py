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
from neo4dash.config import Config
from neo4dash.logger import Logger
from neo4dash.queries import Queries
from py2neo import Graph, NodeMatcher, RelationshipMatcher

LG = Logger()
QR = Queries()


class Database(metaclass=Singleton):
  def __init__(self, *args, **kwargs):
    """Instantiates a database object"""
    self.config = Config()

  def configure(self, db_url="localhost",
                port=13000, db_user="neo4j",
                db_pwd="neo4j"):
    """Sets the application constants and connects to db"""
    try:
        # TODO: validate inputs
      self.config.DB_URL = db_url
      self.config.PORT = port
      self.config.DB_USER = db_user
      self.config.DB_PWD = db_pwd
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
    self.config.check_config()
    graph = Graph(host=self.config.DB_URL, user=self.config.DB_USER,
                  password=self.config.DB_PWD, http_port=self.config.PORT)
    self._set_matchers(graph)
    return graph

  def _set_matchers(self, graph):
    """Sets the node an relationship matchers
    :param graph: py2neo graph
    """
    self.node_matcher = NodeMatcher(graph)
    self.rel_matcher = RelationshipMatcher(graph)

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

  def get_all_data(self, merge=False):
    """Returns the nodes and the relationships from
    Neo4j
    :param merge: Concatenates nodes an relationships
    :returns: if merge is False it retunrns a tuple with two
      arrays: the first with nodes, the second with relationships
      if merge is True it returns only one array
    """
    self.check_self()
    nodes = self.node_matcher.match()
    nodes = [self._map_node(n) for n in nodes]
    # add position - this is dependent on the view and the layeout
    # you choose
    # nodes = self._position_nodes(nodes)

    rels = self.rel_matcher.match()
    rels = [self._map_rels(r) for r in rels]

    if merge is False:
      return nodes, rels
    else:
      return nodes+rels

  def _map_node(self, node):
    """Maps Neo4j Node to UI element
    :param node: dictionary with node elements
    :returns: dictionary with UI details
    """
    return {
        'data': {
            'id': self._get_id(node),
            'label': self._get_label(node),
            'type': list(node._labels)[0] if len(node._labels) > 0 else "",
            'name': node['name']
        }
    }

  def _position_nodes(self, nodes):
    """Adds position to nodes
    :param nodes: array of dicts
    :returns: array of dicts with new position key
    """
    years = [x for x in nodes if x['data']['type'] == 'Year']
    sorted_years = sorted(years, key=lambda k: k['data']['name'])
    # arrange years from left to right
    for index, year in enumerate(sorted_years):
      year['position'] = {'x': 20*index, 'y': 50}
    # replace years in nodes
    nodes = self._replace_by_id(nodes, sorted_years)
    return nodes

  def _replace_by_id(self, first_array, second_array):
    """Replaces the elements from the first array with elements
    from the second array matching them by id
    :param first_array: larger array
    :param second_array: smaller array
    :returns: array
    """
    for second in second_array:
      for first in first_array:
        if first['data']['id'] == second['data']['id']:
          first = second
    return first_array

  def _map_rels(self, rel):
    """Maps Neo4j Relationship to UI element
    :param rel: Neo4j relationship
    :returns: dictionary with UI details
    """
    return {
        'data': {
            'source': self._get_id(rel.start_node),
            'target': self._get_id(rel.end_node),
            'label': list(rel.labels)[0],
            'id': rel.identity
        }
    }

  def _get_id(self, node):
    """Returns node identity
    :param node: Py2neo Node object
    :returns: string
    """
    # return node['hash'] if 'hash' in node else node['name']
    return node.identity

  def _get_label(self, node):
    """Returns a node UI label
    :param node: Py2neo Node object
    :returns: string
    """
    return node['name'] if node['name'] else node['hash']

  def _get_unique(self, list, key='id'):
    """Returns the unique elemnts of a list of dicts"""
    return list({v['data'][key]: v for v in list}.values())
