import json
import logging

from robusta.api import action, JobChangeEvent, JsonBlock, RobustaJob


@action
def parse_job_failure(event: JobChangeEvent):
    job: RobustaJob = event.get_job()
    job_name: str = job.metadata.name

    logging.info(f"JobChangeEvent triggered! {job_name=} {job.metadata=}")

    event.add_enrichment([
        JsonBlock(json.dumps({"job_name": job_name})),
    ])
