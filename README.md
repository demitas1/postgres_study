# PostgresSQL study

## Setup

- build and start containers

```console
$ mkdir pgdata
$ docker-compose up -d
```

- shutdown

```console
docker compose down -v --remove-orphans
```

データベースも削除する場合

```console
docker compose down -v --remove-orphans && sudo rm -rf pgdata
```

## Test

- python コンテナから実行

```console
$ docker exec python_dev python src/main.py
```

- psql コマンドから実行

```console
$ psql -h localhost -p 5432 -U postgres -d mydatabase
Password for user postgres: 
psql (14.15 (Ubuntu 14.15-0ubuntu0.22.04.1), server 15.10 (Debian 15.10-1.pgdg120+1))
WARNING: psql major version 14, server major version 15.
         Some psql features might not work.
Type "help" for help.

mydatabase=# \dt
         List of relations
 Schema | Name  | Type  |  Owner   
--------+-------+-------+----------
 public | users | table | postgres
(1 row)

mydatabase=# \d users
                                       Table "public.users"
   Column   |           Type           | Collation | Nullable |              Default              
------------+--------------------------+-----------+----------+-----------------------------------
 id         | integer                  |           | not null | nextval('users_id_seq'::regclass)
 username   | character varying(100)   |           | not null | 
 email      | character varying(255)   |           | not null | 
 created_at | timestamp with time zone |           |          | CURRENT_TIMESTAMP
Indexes:
    "users_pkey" PRIMARY KEY, btree (id)
    "users_email_key" UNIQUE CONSTRAINT, btree (email)

mydatabase=# select * from users;
 id | username  |      email       |          created_at           
----+-----------+------------------+-------------------------------
  1 | test_user | test@example.com | 2025-01-22 08:22:53.630195+00
  2 | demo_user | demo@example.com | 2025-01-22 08:22:53.630195+00
(2 rows)

mydatabase=# \q
```

