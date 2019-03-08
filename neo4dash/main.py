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
import dash
import dash_cytoscape as cyto
import dash_html_components as html

from neo4dash.db import Database

app = dash.Dash(__name__)

# data muggling
DB = Database()
nodes, rel = DB.get_all_data()


def build_layout():
  """Builds the view from the Neo4j data"""
  app.layout = html.Div([
      cyto.Cytoscape(
          id='cytoscape-two-nodes',
          layout={'name': 'preset'},
          style={'width': '100%', 'height': '400px'},
          elements=nodes
      )
  ])


if __name__ == '__main__':
  build_layout()
  app.run_server(debug=True)