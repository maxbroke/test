# PostgreSQL Cluster with Patroni

This repository provides a sample Docker Swarm stack to run a PostgreSQL
cluster managed by Patroni. The cluster consists of a master node and
replicas with automatic failover.

## Features

- **Replication**: Patroni ensures that one node is elected as the leader
  (master) while the remaining nodes act as replicas.
- **Failover**: When the master node fails, Patroni automatically
  promotes one of the replicas.
- **Easy scaling**: Adjust the total number of nodes by changing a single
  environment variable when deploying the stack.

## Usage

1. Build the `postgres-patroni` image from the provided `Dockerfile`:

   ```bash
   docker build -t postgres-patroni .
   ```

2. Initialize a Docker Swarm if you have not done so already:

   ```bash
   docker swarm init
   ```

3. Deploy the stack using the provided `docker-stack.yml`. The number of
   nodes can be configured through the `PG_NODES` variable. By default it
   starts four nodes (one master and three replicas):

   ```bash
   PG_NODES=4 docker stack deploy -c docker-stack.yml pg-cluster
   ```

   Change `PG_NODES` to scale the cluster with a single line.

4. Verify that the services are running:

   ```bash
   docker stack ps pg-cluster
   ```

The stack uses a custom image built from the official `postgres` image
with Patroni installed. An `etcd` service is included to provide Patroni
with a distributed configuration store.

To remove the stack:

```bash
docker stack rm pg-cluster
```

## Notes

- The stack creates an overlay network named `pgnet` for inter-service
  communication.
- Persistent storage volumes are not configured in this example. For
  production usage you should add volumes for data persistence.
