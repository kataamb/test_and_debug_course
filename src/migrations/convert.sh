#!/bin/bash

echo "🧹 Очистка формата дат в CSV файлах..."

CSV_DIR="./csv_exports"
CLEANED_DIR="./csv_cleaned"

mkdir -p "$CLEANED_DIR"

# Функция для очистки дат
clean_dates() {
    local input_file=$1
    local output_file=$2

    # Удаляем наносекунды из дат (все что после точки в datetime)
    sed -E 's/([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})\.[0-9]+/\1/g' "$input_file" > "$output_file"
}

# Очищаем все CSV файлы
for csv_file in "$CSV_DIR"/*.csv; do
    filename=$(basename "$csv_file")
    echo "Очистка: $filename"
    clean_dates "$csv_file" "$CLEANED_DIR/$filename"
done

echo "✅ Очистка завершена! Файлы сохранены в $CLEANED_DIR"