#!/bin/bash
set -e

# Default path for Patroni configuration directory
export PATRONI_POSTGRESQL_DATA_DIR=${PATRONI_POSTGRESQL_DATA_DIR:-/var/lib/postgresql/data}

exec patroni
