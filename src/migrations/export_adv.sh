#!/bin/bash


CURRENT_DIR=$(pwd)
CSV_DIR="$CURRENT_DIR/csv_exports"


mkdir -p "$CSV_DIR"
sudo chmod 777 "$CSV_DIR"  # Даем полные права

# Функция для экспорта
export_table() {
    local table_name=$1
    local schema=${2:-"adv_uuid"}

    # Экспортируем в контейнер
    docker exec adverts_db_container bash -c \
        "PGPASSWORD=1234 psql -U postgres -d adverts_db \
        -c \"\copy (SELECT * FROM $schema.$table_name) TO '/tmp/${table_name}.csv' WITH CSV HEADER DELIMITER ';'\""

    docker cp adverts_db_container:/tmp/${table_name}.csv "$CSV_DIR/"

    # Меняем права доступа
    sudo chown $USER:$USER "$CSV_DIR/${table_name}.csv"
    chmod 644 "$CSV_DIR/${table_name}.csv"
}

# Экспортируем все таблицы
export_table "profiles"
export_table "categories"
export_table "customers"
export_table "sellers"
export_table "adverts"
export_table "deals"
export_table "likes"
export_table "history_deals"

echo "✅ Экспорт завершен! Файлы сохранены в $CSV_DIR"