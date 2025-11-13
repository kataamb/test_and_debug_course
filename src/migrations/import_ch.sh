#!/bin/bash

# Копируем очищенные CSV файлы
docker cp ./csv_cleaned/ clickhouse_container:/tmp/csv_cleaned/

# Импортируем с указанием разделителя ;
docker exec clickhouse_container bash -c '
    cd /tmp/csv_cleaned
    for csv_file in *.csv; do
        table_name=$(basename "$csv_file" .csv)

        clickhouse-client --format_csv_delimiter=";" \
            --query="INSERT INTO adv_uuid.$table_name FORMAT CSVWithNames" < "$csv_file"

        count=$(clickhouse-client --query="SELECT count() FROM adv_uuid.$table_name")
    done
    rm -rf /tmp/csv_cleaned
'

