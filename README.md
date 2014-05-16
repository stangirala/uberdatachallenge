datachallenge
=============

Private Repo for the Uber Data Challenge

Notes
-------------

* I have used flask for url routing. Gevent to serve the app at scale.
I've used requests to write quick test apps that hit the apis endpoints.
The test app represent a small subset of the quick and dirty tests
I used. I've also used loads for load testing. The API functions can
handle time based range operations.

* At scale the genvets has considerable performance improvements as
compared to the single threaded version. There are a couple of test
files for this in the tests directory.

* MongoDB us used as the backend datastore For the current
specification, document store seemed like a good choice for fast
inserts and heavy reads.

* To run the app out of the box, the top level main.py file should be used.

* The flask app is split into multiple view files using Blueprints.
The endpoint.py file under the views directory registers the endpoint
operations via their blueprints.

* The views directory has an init file that defines a few globals.

* The API is versioned in the url. I think this is a better approach
when compared to having it as state information being passed around in
the requests and responses. (Deprecating the current API would in this
case probably involve adding dispatch routes for in the endpoint.py
file.)

* The API supports JSON. JSON objects are passed around to represent states.

* The documentation of the code itself might be a bit fuzzy. I don't really
have a fixed style.

* Overall, the code should otherwise be mostly self-explanatory.

* Time based operations assume time since the unix epoch.

* I've used pymongo to interface with the backend data store.

* The "trips in the last hour" operation is the default operation for the
"trips in time range" operation. I have not explicitly defined the former
as per the initial specification.

* I've used two collections. One, 'ridescollection' to store the information
from the record trip operation. Two, 'clienttripcollection' is sort of a quick
retrival hash table that stores client\_id and the total miles travelled by
a client. In hindsight this table is not exactly necessary. I'm using it because
it's function is useful for the "total miles per client" operation. The next
iteration of the API will probably have this collection removed, unless the
specification scope is increased.
