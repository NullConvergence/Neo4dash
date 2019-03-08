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

""" This mpdule stores all config constants"""
from neo4dash.singleton import Singleton


class Constants(metaclass=Singleton):
  """ Class with all constants
  """
  DB_URL = 'localhost'
  PORT = 13000
  DB_USER = 'neo4j'
  DB_PWD = 'letmein'
