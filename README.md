# Практическая работа №6: мониторинг и логирование в DevOps

Проект поднимает контейнеризированное Flask-приложение, Prometheus, Grafana, Loki и Promtail.

## Состав проекта

- `app.py` - Flask-приложение с логами и endpoint `/metrics`.
- `Dockerfile` - сборка контейнера приложения.
- `docker-compose.yml` - запуск приложения, Prometheus, Grafana, Loki и Promtail.
- `prometheus.yml` - сбор метрик приложения.
- `loki-config.yml` - конфигурация Loki.
- `promtail-config.yml` - отправка логов Docker-контейнера в Loki.
- `grafana/provisioning` - автоматическое подключение Prometheus и Loki.
- `grafana/dashboards/flask-monitoring.json` - готовая панель Grafana.

## Запуск

```bash
docker compose up -d --build
```

Если используется старая версия Docker Compose:

```bash
docker-compose up -d --build
```

## Проверка

Приложение:

```text
http://localhost:5000
```

Метрики приложения:

```text
http://localhost:5000/metrics
```

Prometheus:

```text
http://localhost:9090
```

Grafana:

```text
http://localhost:3000
```

Логин и пароль Grafana:

```text
admin / admin
```

В Grafana уже будут добавлены источники данных:

- Prometheus: `http://prometheus:9090`
- Loki: `http://loki:3100`

Готовый dashboard находится в папке `DevOps Practice 6` и называется `Flask Monitoring`.

## Команды для генерации данных

Откройте приложение несколько раз:

```bash
curl http://localhost:5000/
curl http://localhost:5000/error
```

После этого в Grafana появятся:

- метрики количества запросов;
- p95 задержки запросов;
- логи Flask-приложения;
- error-лог после вызова `/error`.

## Дополнительно: уведомления

Для Telegram-уведомлений в Grafana:

1. Создайте бота через `@BotFather` и получите Bot API Token.
2. Узнайте Chat ID через `@userinfobot`.
3. Откройте Grafana: `Alerting -> Contact points`.
4. Создайте contact point типа Telegram.
5. Создайте alert rule по метрике:

```promql
sum(rate(flask_http_requests_total{http_status=~"5.."}[1m])) > 0
```

6. Привяжите правило к Telegram contact point.

## Остановка

```bash
docker compose down
```
