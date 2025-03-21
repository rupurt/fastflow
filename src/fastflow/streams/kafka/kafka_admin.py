from contextlib import asynccontextmanager
from typing import List, Optional

from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from aiokafka.protocol.api import Response

from fastflow.settings import KafkaSettings

from .errors import KafkaAdminError
from .new_kafka_topic import NewKafkaTopic


class KafkaAdmin:
    settings: KafkaSettings

    def __init__(self, settings: KafkaSettings):
        self.settings = settings

    async def list_topics(self):
        async with self._admin_client() as admin_client:
            return await admin_client.list_topics()

    async def create_topics(
        self,
        new_topics: List[NewKafkaTopic],
        timeout_ms: Optional[int] = None,
        validate_only: bool = False,
    ):
        new_aio_topics = self._new_aio_topics(new_topics)
        async with self._admin_client() as admin_client:
            response = await admin_client.create_topics(
                new_aio_topics, timeout_ms, validate_only
            )
            errors: List[str] = []
            for _, error_code, error_message in response.topic_errors:
                if error_code > 0:
                    errors.append(error_message)
            if len(errors) > 0:
                raise KafkaAdminError(" ".join(errors))

    async def delete_topics(self, topics: List[str]):
        prefixed_topics = [f"{self.settings.topic_prefix}.{topic}" for topic in topics]
        async with self._admin_client() as admin_client:
            response = await admin_client.delete_topics(prefixed_topics)
            errors: List[str] = []
            for topic, error_code in response.topic_error_codes:
                if error_code > 0:
                    errors.append(f"topic={topic} error_code={error_code}.")
            if len(errors) > 0:
                raise KafkaAdminError(" ".join(errors))

    @asynccontextmanager
    async def _admin_client(self):
        admin_client = AIOKafkaAdminClient(
            bootstrap_servers=self.settings.bootstrap_servers
        )
        try:
            await admin_client.start()
            yield admin_client
        finally:
            await admin_client.close()

    def _new_aio_topics(self, new_topics: List[NewKafkaTopic]):
        new_aio_topics = []
        for new_topic in new_topics:
            new_aio_topic = NewTopic(
                name=f"{self.settings.topic_prefix}.{new_topic.name}",
                num_partitions=new_topic.num_partitions,
                replication_factor=new_topic.replication_factor,
                replica_assignments=new_topic.replica_assignments,
                topic_configs=new_topic.topic_configs,
            )
            new_aio_topics.append(new_aio_topic)
        return new_aio_topics

    def _check_response(self, response: Response):
        print(response)
