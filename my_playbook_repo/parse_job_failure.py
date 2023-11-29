import json
import logging

from robusta.api import action, JobChangeEvent, JsonBlock, RobustaJob


@action
def parse_job_failure(event: JobChangeEvent):
    logging.info(f"JobChangeEvent triggered!")

    job: RobustaJob = event.get_job()
    job_name: str = job.metadata.name
    logging.info(f"{job_name=}")
    job_labels: dict = job.metadata.labels
    logging.info(f"{job_labels=}")

    logging.info(f"{event=}")
    logging.info(f"{event.get_context()=} {dir(event.get_context())}")
    logging.info(f"{event.get_all_sinks()=} {dir(event.get_all_sinks())}")
    logging.info(f"{event.get_resource()=} {dir(event.get_resource())}")
    logging.info(f"{event.get_scheduler()=} {dir(event.get_scheduler())}")
    logging.info(f"{event.get_source()=} {dir(event.get_source())}")
    logging.info(f"{event.get_subject()=} {dir(event.get_subject())}")
    logging.info(f"{event.description=}")
    logging.info(f"{event.response=}")
    logging.info(f"{event.operation=}")
    logging.info(f"{event.all_sinks=}")

    event.add_enrichment([
        JsonBlock(json.dumps({"job_name": job_name, "job_labels": job_labels})),
    ])
