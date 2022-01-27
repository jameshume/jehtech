## Intro
* See: https://github.com/codingexplained/complete-guide-to-elasticsearch
* See: https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro.html
* > Elasticsearch is the distributed search and analytics engine ... Elasticsearch provides near real-time search and analytics for all types of data. 
* Often used for Application Performance Management (APM)
    * Analayse application logs and system metrics, most often to detect errors or understand resource usage etc.
* Log stash
    * Input > Filters > Output
    * Each stage can have plugins
    * E.g. reading in log files
        * File is input and log stash treats each line as an event
        * Filter stage parses the input data to make sense of it: i.e., structure unstructured data
            * E.g. use of "grok pattern"
            * Take raw line and turn into fields, to send for eg to ElasticSearch
    * Allows seperation of concerns - the apps sending the data don't need to known about how it should
      be processed - logstash handles that logic.
* X-Pack
    * Add user authentication and access control to ElasticStash
    * Monitoring
    * Reporting
    * Elasticsearch SQL
        * Normally used Query DSL - this makes it easier for SQL-familiaar developers
        * Translates SQL to Query DSL.
        * Translate APIs also exist
        * Helper tool to get started - Query DSL probably best to use once familiar
* Beats
    * Collection of light weight data shippers
    * Single pupose - send data to logstash or ES.
        * e.g. FileBeat - sends log files to ES
        * e.g. MetricBeat - sends resource usage info to ES.
* Single node Docker image [for learning](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html):
    * `docker pull docker.elastic.co/elasticsearch/elasticsearch:7.16.3`
    * `docker run -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.16.3`
        * Took quite some time to start up for me on an i7 with 16bg ram although system was doing other things.
    * `curl http://127.0.0.1:9200` to figure out if it is running okay
* Run Kibana and ES:
    * See https://www.elastic.co/guide/en/kibana/current/docker.html
    * ```docker network create elastic
         docker pull docker.elastic.co/elasticsearch/elasticsearch:7.16.3
         docker run --name es01-test --net elastic -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.16.3```
    * ```docker pull docker.elastic.co/kibana/kibana:7.16.3
         docker run --name kib01-test --net elastic -p 127.0.0.1:5601:5601 -e "ELASTICSEARCH_HOSTS=http://es01-test:9200" docker.elastic.co/kibana/kibana:7.16.3```
    * To access Kibana, go to http://localhost:5601
* Some ES directory structure:
    * Notable `bin` utils
       ```
        |-- bin
        |   |-- ...
        |   |-- elasticsearch-cli
        |   |-- elasticsearch-plugin     # Install plugins
        |   |-- elasticsearch-sql-cli    # Do SQL-like queries instead of using Query DSM
        |   
       ```
    * Config
       ```
       |-- config
       |   |-- elasticsearch-plugins.example.yml
       |   |-- elasticsearch.keystore
       |   |-- elasticsearch.yml                 #<<< This is the main config file
       |   |-- jvm.options                       #<<< Runs on JVM - HEAP size best thing to mod.
       |   |-- jvm.options.d
       |   |-- log4j2.file.properties
       |   |-- log4j2.properties
       |   |-- role_mapping.yml
       |   |-- roles.yml
       |   |-- users
       |   `-- users_roles
       ```
            *  `elasticsearch.yaml'
                * Commented out by default so defaults are used
                * `cluster.name`: Best practice to set this!
                * `node.name`: Best practice to set this!
* Basic Architecture
    * *Node*: Esentially an ES instance
        * Can run many nodes. Each node can store part of data set: distributed storage = large storage.
        * Node == ES instance so can run many nodes on one machine.
        * Each node belongs to a *cluster*
        * Node is *always* part of a cluster, even if single node in cluster.
    * *Cluster* - collection of nodes.
        * Split is normally for logical seperation.
        * *Document* - A unit of data stored in a cluster.
            * JSON object.
            * *Index*: Every document is stored within an index.
                * Groups documents together logicially.
                * Provide scalability and availablility settings.
                * Search queries are run against indicies.
* Basic cURL queries (Kibana makes this waaay easier!)
    * Local ES
        * `curl -XGET "http://localhost:9200/_cluster/health"`
        * `curl -XGET "http://localhost:9208/_cat/indicies?v"`
        * `curl -XGET "http://localhost:9208/.kibana/_search" -H 'Content-Type: applicaton/json' -d'{ "query": {  "match_all": {} }}'`
    * Cloud ES - needs authentication
        * `curl -XGET -u username:password "https://3aodfff....sa.eu-central.aws.cloud.es.io:9243/.kibana/_search" -H 'Content-Type: applicaton/json' -d'{ "query": {  "match_all": {} }}'
* Sharding & Scalability
    * To store 1TB can use 2 nodes of 0.5TB - can aggregate node storage
        * Done using **sharding**.
        * Sharding is a way to divide *inidicies* into smaller pieces, where each piece is a **shard**
        * Done at the index level!
            * One shard must be on a single node and can be placed on any node. Many to one.
        * Horizontally scale the data volume.
        * Each shard in an Apache Lucene index
        * Can improve performance by running queries on multiple shards at the same time.