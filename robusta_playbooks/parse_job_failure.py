import logging
from robusta.api import action, PodEvent, JsonBlock


@action
def my_action(event: PodEvent):
    pod = event.get_pod()
    pod_name = pod.metadata.name
    pod_labels = pod.metadata.labels

    logging.info(f"PodEvent triggered! {pod_name=} {pod_labels=}")

    event.add_enrichment([
        JsonBlock(f"pod_name: {pod_name}, pod_labels: {pod_labels}"),
    ])
