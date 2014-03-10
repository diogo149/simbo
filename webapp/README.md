Requirements
---

This was tested on:

- Python 2.7.6

- Packages in requirements.txt

- requirements of [python-nvd3](https://github.com/areski/python-nvd3)

Running
---

`python server.py`

Usage
---

1. Start a new experiment, or enter the id of an existing one.
2. Enter the schema for your dataset.
3. Send GET requests to your experiment's sample url to get a set of parameters to use.
4. Send POST requests with the _id of those parameters and the result of your objective function (with key _obj) to the same url.

That's it. The parameters should get better and better over time. Feel free to change the schema at any time (make sure each parameter has a unique name) and look at the visualizations to see the results so far.

Future Plans
---
1. Use a real database. (The initial prototype was made during a hackathon, hence a little hacked together).
1. Redo the web interface.
1. Add more kinds of distributions for the parameters.
1. Use online models for the SMBO.
1. Allow for personalization.
