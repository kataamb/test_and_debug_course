#!/bin/bash
echo hi 
CONTAINER_NAME="adverts_db_container_v1"
DATA_DIR="/data_tables_uuid"
LOCAL_CSV_DIR="./csv_exports"  # Папка с CSV файлами на хосте

echo "🚀 Starting database initialization..."

# Проверяем что контейнер запущен
if ! docker ps | grep -q $CONTAINER_NAME; then
    echo "❌ Container $CONTAINER_NAME is not running!"
    exit 1
fi

# Создаем папку в контейнере
echo "📁 Creating directory $DATA_DIR in container..."
docker exec $CONTAINER_NAME mkdir -p $DATA_DIR

# Копируем CSV файлы в контейнер
echo "📤 Copying CSV files to container..."

# Список CSV файлов из твоего SQL скрипта
CSV_FILES=(
    "categories.csv"
    "profiles.csv" 
    "customers.csv"
    "sellers.csv"
    "adverts.csv"
    "deals.csv"
    "likes.csv"
    "history_deals.csv"
)

for csv_file in "${CSV_FILES[@]}"; do
    local_file="$LOCAL_CSV_DIR/$csv_file"
    
    if [ -f "$local_file" ]; then
        echo "  📄 Copying $csv_file..."
        docker cp "$local_file" $CONTAINER_NAME:$DATA_DIR/
    else
        echo "  ⚠️  Warning: $local_file not found, skipping"
    fi
done

echo "✅ CSV files copied successfully!"
echo ""
echo "📝 Next steps:"
echo "1. Connect to container: docker exec -it $CONTAINER_NAME bash"
echo "2. Execute SQL script manually: psql -U postgres -d adverts_db -f /path/to/your/init_script.sql"
echo "3. Or copy and paste the SQL commands manually"
echo ""
echo "📋 CSV files available in container at: $DATA_DIR/"
