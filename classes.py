import asyncio
import json
import aiokafka
import redis
import pandas
import aiocron
import datetime
from loguru import logger

KEYS = ("12", "23")


class Points(dict):
    def __init__(self, bootstrap, topic, consumer):
        super().__init__()
        self.points = []
        self.bootstrap = bootstrap
        self.topic = topic
        self.consumer = consumer
        self.loop = asyncio.get_running_loop()
        self.cron = aiocron.crontab("* * * * * */10", self.produce, loop=self.loop)

    async def consume(self):
        consumer = aiokafka.AIOKafkaConsumer(
            self.topic, bootstrap_servers=self.bootstrap, group_id=self.consumer
        )
        dataframe = []
        await consumer.start()
        logger.success(f'Consumer started...')
        try:
            async for msg in consumer:
                data = json.loads(msg.value)
                print(data)
                for item in filter(lambda x: x[0] in KEYS, data.items()):
                    for value in item[1]:
                        dataframe.append(
                            (
                                item[0],
                                datetime.datetime.fromtimestamp(
                                    int(value["timestamp"] // 1000000000)
                                ),
                                float(value["valueDbl"]),
                            )
                        )
                print(dataframe)
        finally:
            await consumer.stop()
            logger.success('Consumer stopped...')

    async def produce(self):
        logger.success(f"Produced!!! {datetime.datetime.now()}")
        # global dataframe
        # print(dataframe)
        # print(pandas.DataFrame(dataframe).groupby(0).mean(2))
        # dataframe = []

    async def cache(self):
        logger.success('Cache synced!')


class Point:
    def __init__(self):
        self.hour = []
        self.shift = []
        self.month = []

    def totalize(self):
        pass
