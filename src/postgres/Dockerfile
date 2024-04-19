FROM postgres:13

# Copy SQL script to initialize the database schema
COPY /postgres/init.sql /docker-entrypoint-initdb.d/
