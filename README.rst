Project Jarvis
==============

`AJ Minich`_

Jarvis is a personal assistant that uses natural language processing and a database 
of pre-programmed functionality to respond to user requests. Jarvis is driven by a 
Java-based backend that performs core operations, and can be used through various 
interfaces.

Jarvis is named after Tony Stark's automated assistant in the *Ironman_* series.

Plans
-----

The following are on my list of things to implement:

* Console
  * run in background
  * incorporate Jarvis into the login and logout functions
  * have Jarvis warn if any of the directories are getting full (df -h)
  * more importantly: make it possible to tell Jarvis to shut up
* Centralization
  * always available online
  * all clients interact through a REST interface with a single instance
* Engine
  * bring in the NLP software from http://nlp.stanford.edu/software/index.shtml
  * allow basic commands to be parsed and responded to
  * consider using data from Freebase Quad Dump (http://aws.amazon.com/datasets/2052645406658757)
* voice interface
  * consider bringing in soundbites from http://www.wavsource.com/movies/iron_man.htm

Architecture
------------

The initial parsing engine will be simple. In fact, the first version will be pretty 
much just a command-line abstraction layer that reduces the need to type commands exactly.

The operations will be:

* Determine the action
* Determine the object
* Look through the database of available operations, and determine if any of them match the action and the object
  * action: "open", "close", "delete"

Behavior
--------

Here are some examples of anticipated behavior::

  > jarvis
  Yes sir?

.. _AJ Minich: http://ajminich.com/projects
.. _Ironman: http://en.wikipedia.org/wiki/Edwin_Jarvis#Film
