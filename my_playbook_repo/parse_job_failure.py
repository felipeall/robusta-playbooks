import json
import logging

from pydantic import BaseModel
from robusta.api import JobChangeEvent, JsonBlock, RobustaJob, action


class JobInfo(BaseModel):
    job_name: str
    job_labels: dict

    def dump(self) -> str:
        return json.dumps(self.dict())


@action
def parse_job_failure(event: JobChangeEvent):
    logging.info("[parse_job_failure] JobChangeEvent triggered!")

    job: RobustaJob = event.get_job()
    job_name: str = job.metadata.name
    job_labels: dict = job.metadata.labels
    job_info: JobInfo = JobInfo(job_name=job_name, job_labels=job_labels)

    logging.info(f"[parse_job_failure] Sending message to Kafka: {job_info.dict()}")

    event.add_enrichment([JsonBlock(json_str=job_info.dump())])
