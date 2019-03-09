# Neo4dash
This tool uses [Dash](https://plot.ly/products/dash/) to visualize the graph indexed with [GraphRepo](https://github.com/NullConvergence/GraphRepo).
Please look at [GraphRepo](https://github.com/NullConvergence/GraphRepo) before for mapping a Github repository to Neo4j.


### Running:
Follow the 1.1-1.3 instructions from [GraphRepo](https://github.com/NullConvergence/GraphRepo) to index a repository in Neo4j.
Make sure your Docker image is running, then follow these instructions:

````
$ git clone https://github.com/NullConvergence/Neo4dash
$ cd neo4dash/
$ conda create neo4dash python=3.5
$ pip3 install requirements.txt
$ python graphrepo/main.py
````

Then access the visualization at [http://localhost:8050](http://localhost:8050).
