# Mock Web Service

This repository contains a simple web service that can be used for testing.

The service exposes the following methods

| path | description | parameters | returns |
| ---- | ----------- | ---------- | ------- |
| /    | returns a simple message | | { "message" : "Hello, World!" } |
| /echo | returns a configurable message | message - a string to send back, defaults to "" | {"method" : (the http method used), "message" : (the message value) } |
| /delay | waits for a configurable amount of time and returns a message | seconds - the number of seoconds to wait, defaults to 5 | { "seconds" : (the number of seonds waited) } |
| /code | returns a response with a given status code | responsecode - the response code to use, defaults to 200 | {"responsecode" : (the response code)}
