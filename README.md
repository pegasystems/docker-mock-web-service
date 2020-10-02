# Mock Web Service

This repository contains a simple web service that can be used for testing.

[![Build Status](https://travis-ci.org/pegasystems/docker-mock-web-service.svg?branch=master)](https://travis-ci.org/pegasystems/docker-mock-web-service)

For testing purposes, the server runs on two ports 8080 and 8089. Both ports have the same content

The service exposes the following methods

| path | description | parameters | returns |
| ---- | ----------- | ---------- | ------- |
| /    | returns a simple message | | { "message" : "Hello, World!" } |
| /echo | returns a configurable message | message - a string to send back, defaults to "" | {"method" : (the http method used), "message" : (the message value) } |
| /delay | waits for a configurable amount of time and returns a message | seconds - the number of seoconds to wait, defaults to 5 | { "seconds" : (the number of seonds waited) } |
| /code | returns a response with a given status code | responsecode - the response code to use, defaults to 200 | {"responsecode" : (the response code)}
| /hostinfo | returns hostname and ip of server | | {"hostname": "09d79b1445bd", "hostip": "172.17.0.2"} | 
| /metrics | returns prometheus metrics for the server | |

