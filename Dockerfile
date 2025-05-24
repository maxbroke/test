FROM postgres:15

# Allow overriding the Debian mirror for environments with limited
# connectivity. Specify `--build-arg APT_MIRROR=<mirror>` when building
# to choose a different mirror.
ARG APT_MIRROR=deb.debian.org
RUN sed -i "s|deb.debian.org|${APT_MIRROR}|g" /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing python3-pip && \
    pip3 install --no-cache-dir patroni[etcd] && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY patroni-entrypoint.sh /usr/local/bin/patroni-entrypoint.sh
RUN chmod +x /usr/local/bin/patroni-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/patroni-entrypoint.sh"]
