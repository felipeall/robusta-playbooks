import json
import logging as log
from typing import Tuple

from pydantic import BaseModel
from robusta.api import JobChangeEvent, JsonBlock, RobustaJob, action


class JobInfo(BaseModel):
    name: str
    labels: dict
    status: str
    message: str
    reason: str

    def dump(self) -> str:
        return json.dumps(self.dict())


def __get_job_details(job: RobustaJob) -> Tuple[str, str, str]:
    for condition in job.status.conditions:
        if condition.status == "True":
            return condition.type, condition.message, condition.reason
    return "", "", ""


@action
def parse_job_failure(event: JobChangeEvent):
    log.info("[parse_job_failure] JobChangeEvent triggered!")

    job: RobustaJob = event.get_job()
    name: str = job.metadata.name
    labels: dict = job.metadata.labels
    status, message, reason = __get_job_details(job)

    job_info: JobInfo = JobInfo(name=name, labels=labels, status=status, message=message, reason=reason)
    log.info(f"[parse_job_failure] Sending message to Kafka: {job_info.dict()}")

    event.add_enrichment([JsonBlock(json_str=job_info.dump())])
