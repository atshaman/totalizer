#!env python
"""Реализация тоталайзера, который считает сумму значений по тегам и записывает результат в другой тег"""
import click
import service
import sys
import json
from loguru import logger


@click.command(help="Сервис для реализации totalizer")
@click.option('-v', '--verbose', help='Уровень логгирования', default='INFO',
              type=click.Choice(['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL'],
                                case_sensitive=False), envvar='DEBUG')
@click.option('-i', '--interface', help='Имя интерфейса для запуска службы', default='0.0.0.0', envvar='LISTEN_ON')
@click.option('-p', '--port', help='Порт для работы веб-сервиса', default=8080, envvar='HTTP_PORT')
@click.option('--context-path', 'context_path', help='Контекст для запуска сервиса', default='/')
@click.option('--bootstrap-server', 'bootstrap', help='Bootstrap-сервер для доступа к кафке',
              default='172.22.159.225:30092', envvar='KAFKA_BOOTSTRAP_SERVERS')
@click.option('-t', '--topic', help='Топик для вычитывания', default='nifi-data', envvar='KAFKA_TOPIC')
@click.option('--consumer-group', 'consumer', default='totalizer',
              help='Имя consumer-group для вычитывания даных в kafka')
@click.option('-r', '--redis', 'redisuri', help='URI доступа к серверу REDIS', default='redis://localhost:6379')
@click.option('--tags', type=click.File(mode='r'), help='Имя файла с тегами', default=None)
def main(verbose, interface, port, context_path, bootstrap, topic, consumer, redisuri, tags):
    logger.remove()
    logger.add(sys.stdout, level=verbose)
    if tags:
        tags = json.load(tags)
    svc = service.Service(interface=interface, port=port, context_path=context_path, bootstrap=bootstrap, topic=topic,
                          consumer=consumer, redisuri=redisuri, data=tags)
    svc.run()


if __name__ == "__main__":
    main()
