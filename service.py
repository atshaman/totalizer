import asyncio
import aiohttp.web
import classes
from loguru import logger


class Service:
    def __init__(self, interface, port, context_path, bootstrap, topic, consumer, redisuri, data):
        self.points, self.app = None, None
        self.interface, self.port = interface, port
        self.bootstrap, self.topic, self.consumer = bootstrap, topic, consumer
        # self.redis = redis.asyncio.from_url(redisuri)
        if not context_path.endswith("/"):
            self.context_path = context_path + "/"
        else:
            self.context_path = context_path
        self.routes = [
            aiohttp.web.get(self.context_path + "health/liveness", self.health),
            aiohttp.web.get(self.context_path + "health/readiness", self.health),
        ]
        if context_path != "/":
            self.routes += [
                aiohttp.web.get("/health/liveness", self.health),
                aiohttp.web.get("/health/readiness", self.health),
            ]
        if data:
            pass

    async def health(self, request):
        """Запрос проб"""
        logger.debug(request)
        return aiohttp.web.json_response({"status": "UP"})

    async def loadconfig(self, request):
        """Загрузка конфигурации методом POST """
        pass

    async def getconfig(self, request):
        """Получение работающей конфигурации """
        pass

    async def putconfig(self, request):
        """Изменение загруженной конфигурации """
        pass

    async def getvalue(self, request):
        """Получение значений тоталайзера по тегам """
        pass

    async def background(self, app):
        """Инициализация массива отслеживаемых точек. Выполняется в фоне, т.к. требуется event loop """
        self.points = classes.Points(self.bootstrap, self.topic, self.consumer)
        # self.app['redis'] = asyncio.create_task(self.checkredis())
        # self.task = asyncio.create_task(self.points.consume())
        # yield
        # self.task.cancel()
        # with contextlib.suppress(asyncio.CancelledError):
        #     await self.task

    async def cleanup_background(self, app):
        self.app['redis'].cancel()

    async def on_shutdown(self, app):
        pass

    def run(self):
        """Запуск event loop. Создание фоновой задачи по инициализации массива тегов """
        self.app = aiohttp.web.Application()
        self.app.add_routes(self.routes)
        # Добавляем фоновые задачи
        self.app.on_startup.append(self.background)
        self.app.on_cleanup.append(self.cleanup_background)
        self.app.on_shutdown.append(self.on_shutdown)
        logger.info(
            f"Сервис запущен на порту {self.interface}:{self.port}, context={self.context_path}"
        )
        logger.debug(self.routes)
        aiohttp.web.run_app(self.app, port=self.port, host=self.interface)


if __name__ == '__main__':
    pass
