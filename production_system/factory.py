import simpy
from collections.abc import Generator
from job import Job
from typing import cast

number_of_work_centers = 6


class WorkCenter:
    def __init__(
        self,
        env: simpy.Environment,
        name: str,
        job_completion_queue: simpy.Store,
    ) -> None:
        self.name = name
        self.job_completion_queue = job_completion_queue
        self.env = env
        self.input_job_queue = simpy.Store(env)

        self.busy = False
        self.job_being_processed = None
        self.job_processing_start_time = 0

    def enqueue_job(self, job: Job) -> Generator[simpy.Event, None, None]:
        yield self.input_job_queue.put(job)

    def run(self) -> None:
        self.env.process(self.__main_loop())

    def __main_loop(self) -> Generator[simpy.Event, None, None]:

        while True:
            try:
                item = yield self.input_job_queue.get()
                job = cast(Job, item)

                self.busy = True
                self.job_processing_start_time = self.env.now
                self.job_being_processed = job

                processing_time = job.work_centers_routing[self.name]

                yield self.env.timeout(processing_time)
                yield self.job_completion_queue.put((self.name, job))

                self.job_processing_start_time = 0
                self.job_being_processed = None
                self.busy = False
            except Exception as e:
                print(f"Error: {e}")


class Factory:
    def __init__(self, env: simpy.Environment, verbose_log: bool) -> None:
        self.env = env
        self.verbose_log = verbose_log
        self.input_jobs_queue: simpy.Store = simpy.Store(env)
        self.job_completion_queue: simpy.Store = simpy.Store(env)
        self.work_centers: dict[str, WorkCenter] = {}

        for i in range(number_of_work_centers):
            work_center_name = "WC{}".format(i + 1)
            work_center = WorkCenter(env, work_center_name, self.job_completion_queue)
            self.work_centers[work_center_name] = work_center

    def run(self) -> None:
        self.env.process(self.__handle_job_completion())
        self.env.process(self.__handle_input_jobs())

        for work_center in self.work_centers.values():
            work_center.run()

    def __handle_input_jobs(self) -> Generator[simpy.Event, None, None]:
        while True:
            try:
                item = yield self.input_jobs_queue.get()
                job = cast(Job, item)

                if self.verbose_log:
                    print(
                        f"Job {job.id} pushed with working centers {list(job.work_centers_routing.keys())}"
                    )

                if job.current_working_center_name is None:
                    raise ValueError(f"Trying to process a completed job")

                work_center = self.work_centers[job.current_working_center_name]
                yield from work_center.enqueue_job(job)

            except Exception as e:
                print(f"Error: {e}")

    def __handle_job_completion(self) -> Generator[simpy.Event, None, None]:
        while True:
            try:
                item = yield self.job_completion_queue.get()
                completed_job = cast(tuple[str, Job], item)

                work_center_name = completed_job[0]
                job = completed_job[1]

                job.mark_work_center_completed(work_center_name)

                if self.verbose_log:
                    print(f"Job {job.id} - {work_center_name} step completed")

                if job.current_working_center_name is not None:
                    work_center = self.work_centers[job.current_working_center_name]
                    yield from work_center.enqueue_job(job)

            except Exception as e:
                print(f"Error: {e}")
