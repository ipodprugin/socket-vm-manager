FROM postgres

WORKDIR /

COPY tables.sql /docker-entrypoint-initdb.d/tables.sql

EXPOSE 5432
