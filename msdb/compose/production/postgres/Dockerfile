FROM postgres:14

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
COPY movies.sql /docker-entrypoint-initdb.d/
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance

