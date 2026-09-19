 # EthosClient

[![PyPI version](https://badge.fury.io/py/EthosClient.svg)](https://badge.fury.io/py/EthosClient)

Python Client Library for interfacing with Ellucian Ethos.

 ## Aims

This library can:

 - Handle Ethos authorizations (JWT token etc.)
 - Create, update, and delete resources
 - Query resources individually and in groups
 - Fetch change notification from Ethos
 - Provide helper methods for spercific resource types 
 
 ## Usage examples

 - For a quick start usage example using the python REPL console follow the [Quickstart](./docs/QUICKSTART.md) guide.
 - For examples of getting mutiple resources see [Resource Iterator Guide](./docs/RESOURCEITERATORS.md)
 - For examples of using the poller functionality see [Poller Guide](./docs/POLLERGUIDE.md)
 - Examples of direclty calling Ethos API see [Direct Call](./docs/DIRECTCALL.md)
 - For a script matching every request in the included Postman collection see [Postman Collection Examples](./docs/POSTMANEXAMPLES.md)
 - For sample scripts see [Sample scripts directory](./samples)

 ## Background

I started this project from rmetcalf9’s (Robert Metcalf) EllucianEthosPythonClient. Since Robert didn’t have time to update the project for newer versions of Python, I decided to create a new branch and continue its development so it can support newer Python versions and be useful to others working with Ellucian Ethos.

I hope publishing this library will be helpful to other Ethos users, and I look forward to collaborating with the community to improve it further.

Please feel free to submit feedback, report issues, or contribute pull requests. Any contributions and suggestions are welcome!
  
 

