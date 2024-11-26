FROM postgres:15

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
# Extracts the compressed file and copies it to the initdb directory
ADD movies.sql.tar.gz /docker-entrypoint-initdb.d/
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
