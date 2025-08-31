from job import Job
import simulation_parameters
import random
from collections.abc import Iterable, Iterator
from collections import OrderedDict


class JobFamilyParameters:
    def __init__(
        self,
        family_name: str,
        processing_time_gamma_alpha_beta: tuple[float, float],  # gamma distribution
        work_centers_routing_probabilies: dict[str, float],
    ) -> None:
        self.family_name = family_name
        self.processing_time_gamma_alpha_beta = processing_time_gamma_alpha_beta
        self.work_centers_routing_probabilies = work_centers_routing_probabilies


job_families_probabilies = [0.10, 0.52, 0.38]

job_families_parameters = [
    JobFamilyParameters(
        "F1", (2, 2), {"WC1": 1, "WC2": 1, "WC3": 0, "WC4": 1, "WC5": 1, "WC6": 1}
    ),
    JobFamilyParameters(
        "F2",
        (4, 0.5),
        {"WC1": 0.8, "WC2": 0.8, "WC3": 1, "WC4": 0.8, "WC5": 0.8, "WC6": 0.75},
    ),
    JobFamilyParameters(
        "F3",
        (6, 1 / 6),
        {"WC1": 0, "WC2": 0, "WC3": 1, "WC4": 0, "WC5": 0, "WC6": 0.75},
    ),
]

job_due_date_uniform_low_high: tuple[float, float] = (30, 50)  # uniform distribution


def get_random_family_index() -> int:
    indexes_range = range(len(job_families_probabilies))
    selected_index = random.choices(indexes_range, weights=job_families_probabilies)[0]
    return selected_index


def create_job_generator() -> Iterable[Job]:
    while True:
        try:
            family_index = get_random_family_index()
            family_parameters = job_families_parameters[family_index]

            work_centers_routing = OrderedDict(
                [  # ordered list of work center - processing time pairs
                    (
                        k,  # the key is the name of the work center
                        random.gammavariate(  # the value is the processing time of the work center
                            *family_parameters.processing_time_gamma_alpha_beta
                        ),
                    )
                    for k, p in family_parameters.work_centers_routing_probabilies.items()
                    if random.random() < p
                ]
            )

            item = Job(
                familyName=family_parameters.family_name,
                inter_arrival_time=random.expovariate(
                    1 / simulation_parameters.job_arrival_rate_exponential_lambda
                ),
                work_centers_routing=work_centers_routing,
                due_date=random.uniform(*job_due_date_uniform_low_high),
            )

            yield item

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    job_iterable: Iterable[Job] = create_job_generator()
    job_iterator: Iterator[Job] = iter(job_iterable)
    for _ in range(10):
        job = next(job_iterator)
        print(f"{job}")
