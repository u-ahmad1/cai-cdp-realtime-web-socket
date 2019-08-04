# Kafka Web Socket

This is the service that would read the data from the kafka and then send it over the web socket to be shown on the dashboard.
This would read process all the suricata logs.

## Getting Started

### Description

Web Socket has been build in the Python (https://www.python.org/), 

There are 2 core functions of the Kafka Socket.

1. Read the Data from the kafka.
2. Send the data to the websocket.

### Prerequisites

For the kafka we are using `kafka-python`

For creation of the Yaml file we use `pyyaml`

For the websocket we are using `tornado==3.2.1`


## Configuration of the Kafka Web Socket

```
kafka:
  bootstrap_server: localhost:9092  // Kafka Server
  topic: d4n-ids-incidents          // The socket from where we want to read the data.
  offset: latest #latest for tailing and earliest for backlog

socket:
  host: 0.0.0.0  // Socket on which we want to listen
  port: 8888     // Port on which client would read
  name: /suri    // The name of the Socket
```


## Versioning

The versioning will start from now.

## Authors

* **Waseem ud din Farooqui** - *Initial work* - [Waseem Farooqui](https://github.com/Waseem-farooqui)


## License

This project License is not yet decided.