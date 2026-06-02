# Islands(Polygons) Discovery

Программа для поиска замкнутых циклов (островов) в GeoJSON-данных. 
Принимает FeatureCollection из LineString, возвращает FeatureCollection с полигонами островов и общей границей.

## Требования
- Docker

## Сборка
`docker build -t island-service .`

## Запуск контейнера
`docker run -p 8080:8080 island-service`

## Тест
`curl -X POST http://localhost:8080/process -H "Content-Type: application/json" -d @samples/re_12021310131033.json`

### Пример ответа
`{
  "type": "FeatureCollection",
  "features": [...]
}`

## Визуальная проверка
Скопируйте ответ в geojson.io для просмотра.
