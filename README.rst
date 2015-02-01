*************************************************************
pynessus-api: A library and CLI for using the Nessus REST API
*************************************************************

pynessus-api contains two modules. *nessusapi* is a library for
representing Nessus objects (e.g. scans, templates) as Python objects.
*nessusinterface* is a collection of scripts using the *nessusapi*
library that provide an easy-to-use user interface on the command line
to the Nessus server. It can be used by itself, integrated into other
scripts, or used as a reference.

*nessusapi* was recently rewriten to be more pythonic. This may have
caused serious breaking changes in existing code.

pynessus-api aims to support Python 2.6+ and Python 3+

=======
Purpose
=======

Started as a port of the `Ruby Nessus API`_ to Python. It was written
with the goal of being integrated with the `Nessus Parser`_.

=====
To-Do
=====

* Improve API coverage (nessusapi)
* Improve test coverage (tests)
* Create full CLI interface (nessusinterface)

.. _Ruby Nessus API: https://github.com/sait-berkeley-infosec/nessus_api

.. _Nessus Parser: https://github.com/sait-berkeley-infosec/nessus-parser
