import simpy
from collections.abc import Generator
from job import Job
from typing import cast

number_of_work_centers = 6


class WorkCenter:
    def __init__(self, name: str, env: simpy.Environment) -> None:
        self.name = name
        self.env = env
        self.queue = simpy.Store(env)

        self.busy = False
        self.job_being_processed = None
        self.job_processing_start_time = 0

    def enqueue_job(self, job: Job):
        self.queue.put(job)

    def run(self) -> None:
        self.env.process(self.__main_loop())

    def __main_loop(self) -> Generator[simpy.Event, None, None]:

        while True:
            try:
                # this blocks if there is no job, otherwise it immediately returns one
                item = yield self.queue.get()
                job = cast(Job, item)

                self.busy = True
                self.job_processing_start_time = self.env.now
                self.job_being_processed = job

                processing_time = job.work_centers_routing[self.name]

                yield self.env.timeout(processing_time)

                self.job_processing_start_time = 0
                self.job_being_processed = None
                self.busy = False
            except Exception as e:
                print(f"Error: {e}")


class Factory:
    def __init__(self, env: simpy.Environment) -> None:
        self.env = env

        self.work_centers = [
            WorkCenter("WC{}".format(i + 1), env) for i in range(number_of_work_centers)
        ]

    def run(self) -> None:
        for work_center in self.work_centers:
            work_center.run()

    def handle_job(self, job: Job):
        pass
