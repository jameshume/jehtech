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

## Sagas
A saga is:

> a coordinated series of local transactions; a previous step triggers each step in a saga.
> ... Each local transaction is atomic - but not the saga as a whole

* Distributed transactions and locks are not favoured as they can reduce availablilty.
  Thus sagas are favoured.
* Without transactions, sagas must implement workflows to handle errors so that system
  can return to a consistent (but maybe not the same as before the saga started) state.
    * Each task in a saga requires a *compensating action* that can be used to "undo" it.
* Two types:
    * Choreographed sagas:
        * Events trigger all actions.
        * The state machine is distributed across all the interacting services
        * Rollbacks of events may return the system to a consistent state but not necessarily
          exactly the same state as before the saga happended.
        * Pros:
            * Low coupling: participating services dont need to know about eachother - they
              just respond to events.
        * Cons:
            * No single service has the whole picture of how the entire transaction works.
              Distributed knowledge and state makes resoning hard!
            * Can introduct cyclic dependencies between services.
            * Must havily invest in monitoring and tracing to understand execution flow.
            * Difficult to know % complete of executing process.
    * Orchestrated sagas:
        * One service takes on role of orchestrator, responsible for executing saga and
          all rollbacks etc.
        * Pros:
            * All sequencing logic in one place - easier to reason about.
            * Can simplify individual services, reducing complexity of states they need
              to manage.
            * 
        * Cons:
            * Coordinator can become too "fat" - holds too much logic.
        * See: [AWS Step Workflows](https://aws.amazon.com/step-functions/)
        * See: [Netflix Conductor](https://netflix.github.io/conductor/), which has this to say:
          > Why not peer to peer choreography?
          >
          > With peer to peer task choreography, we found it was harder to scale with growing business needs and complexities.
          > Pub/sub model worked for simplest of the flows, but quickly highlighted some of the issues associated with the approach:<br>
          > <div style="margin-left:2rem;">
          > 1. Process flows are "embedded" within the code of multiple application. <br>
          > 2. Often, there is tight coupling and assumptions around input/output, SLAs etc, making it harder to adapt to changing needs. <br>
          > 3. Almost no way to systematically answer "How much are we done with process X"? <br>
          > </div>
* A saga is not isolated like an ACID transaction would be - intermediate state *is* visible.


### Eventual Consistency
* See [this article on eventual consistency](https://www.allthingsdistributed.com/2008/12/eventually_consistent.html)

> In an ideal world there would be only one consistency model: when an update is made all observers would see that update.

The above would be called *Strong consistency*. After an update completes, any subsequent read, by anyone, will return that\
update.

* Pre 90s distributed solutions wanted *distribution transparency*: user things s/he is interacting with one system
  even if many "behind it". Felt it was better to fail the entire system than break this illusion.
* Mid 90's onwards: availablility more important than single-service illusion.
    * Eric Brewer: CAP theorm:
        * Three properties of shared-data systems:
            * Data consistency
                * Consistency means that all clients see the same data at the same time, no matter which node they connect to. 
            * System availability
                * Availability means that that any client making a request for data gets a response.
            * Tolerance to network partition
                * A partition is a communications break within a distributed system: a lost or temporarily delayed connection between two nodes. 
        * CAP says only 2 can be achieved at once.
        * ACID v.s. BASE
            * ACID = **A**tomic, **C**onsistent, **I**solation, **D**urable
                * Atomic: Operation is done and undone as one indivisible unit - all changes are done as if one single operation.
                * Consistent: At start and end.
                * Isolation: No one can observe the intermediate states of the transaction.
                * Durable: Changes persist after transaction and are not undone even in event of system failure.
            * BASE = **B**asically **A**vailable **S**oft-state **E**ventual consistency
            * Forfeit "C" and "I" in ACID for availability, graceful degredation, and performance.
        > An important observation is that in larger distributed-scale systems, network partitions are a given; therefore, consistency and availability cannot be achieved at the same time. This means that there are two choices on what to drop: relaxing consistency will allow the system to remain highly available under the partitionable conditions, whereas making consistency a priority means that under certain conditions the system will not be available.

The distributed systems, mostly across fallable networks, led to *eventual consistency* models, which are a form of *weak consistency*.

*Weak consistency* means that if Alice updates the the data store, and then Bob and Paul read it, they are 
not guaranteed to see the most recent value. Conditions need to be met before the value will be returned.

*Eventual consistency* is a slightly stronger form where if *no new updates occur*, eventuall all accesses
return the last updated value.

### Command Query Response Segregation (CQRS)

* See [Martin Folwer's article](https://martinfowler.com/bliki/CQRS.html).
* See [CQRS facts and myths explained](https://event-driven.io/en/cqrs_facts_and_myths_explained/).


### Database Per Service Pattern