## Design
* Vocab
    * Homogenous - of the same kind; alike
    * Heterogeneous - diverse in character or content; being of different kinds
    * Coupling v.s. cohesion:
        * Coupling refers to the interdependencies between modules,
        * Cohesion describes how related the functions within a single module are.
* Fallacies:
    * The network is reliable
    * Latency is zero
        * Latency is how much time it takes for data to move from one place to another
    * Bandwidth is infinite
        * Bandwidth which is how much data we can transfer during that (latency) time.
    * The network is secure
    * Transport cost is zero
    * The network is homogeneous
    * See: [Fallacies of Distributed Computing Explained](https://pages.cs.wisc.edu/~zuyu/files/fallacies.pdf)
* Service contracts
    * See Swagger and OpenAPI to define forma & solid contracts
* Loggin at all levels of each service is vital for debug and maintainability
    * E.g. managed services for log aggregation: Loggy, Splunk, Sumo Logic. Or run in-house with ELK stack 
      ([Elasticsearch](https://www.elastic.co/elasticsearch/), [Logstash](https://www.elastic.co/logstash/), & [Kibana](https://www.elastic.co/kibana/))
* Early uService layers will be flat - similar level of abstraction. Later services will include aggregators and coordinators:
    * *Aggregator*: joins data from underlying services
    * *Coordinator*: orchestrates behavior by issing commands to downstream services
* Build *smart enpoints* and *dumb pipes*.
* Events
    * *Synchronous*:
        * Good when next step is dependent on result of the current step.
        * Drawbacks:
            * Bad when latency is an issue because cannot be parallelized (effectively increasing bandwidth)
            * Introduce tighter coupling between services as services must be aware of their collaborators
            * Dont have strong broad|multi-cast or pub/sub models
            * Can result in deep dependency chains.
    * *Asynchronous*
        * Event driven - easier to exent system because services no longer need to know about downstream consumers
            * Loose coupling between services.
        * Typically needs *communications broker*: *event bus*.
            * E.g. RabbitMQ, Redis, Kafka.
        * Patterns:
            * Job Queue
            * Publish-Subscript (Pub/Sub)
* Service discovery:
    * AWS ELB - assigns DNS names and manages health of nodes.
    * or [Consul](https://www.consul.io) - for more complex scenarios
    * or Kubernetes ClusterIP services.
    * ...`
