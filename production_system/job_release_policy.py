from abc import ABC, abstractmethod
from job_generator import create_job_generator
from job import Job
from collections.abc import Iterable, Iterator
from collections.abc import Generator
import simpy
import random

agent_wake_up_frequency = 1  # unit of time days


class JobReleasePolicy(ABC):
    def __init__(self, env: simpy.Environment) -> None:
        self.env = env
        self.job_released_event: simpy.Event = env.event()

    @abstractmethod
    def run(self) -> None:
        pass


class PushJobReleasePolicy(JobReleasePolicy):
    def __init__(self, env: simpy.Environment) -> None:
        super().__init__(env)
        job_iterable: Iterable[Job] = create_job_generator()
        self.job_iterator: Iterator[Job] = iter(job_iterable)

    def __push_process(self) -> Generator[simpy.Event, None, None]:
        while True:
            try:
                job = next(self.job_iterator)
                yield self.env.timeout(job.inter_arrival_time)
                self.job_released_event.succeed(job)
                self.job_released_event = self.env.event()
            except Exception as e:
                print(f"Error: {e}")

    def run(self) -> None:
        self.env.process(self.__push_process())


class PspJobReleasePolicy(JobReleasePolicy):
    def __init__(self, env: simpy.Environment) -> None:
        super().__init__(env)
        self.job_queue = simpy.Store(env)
        job_iterable: Iterable[Job] = create_job_generator()
        self.job_iterator: Iterator[Job] = iter(job_iterable)

    def __push_decision(self) -> bool:
        return random.choice([True, False])  # TODO: put RL agent inference here

    def __job_creations_process(self) -> Generator[simpy.Event, None, None]:
        while True:
            try:
                job = next(self.job_iterator)
                yield self.env.timeout(job.inter_arrival_time)
                yield self.job_queue.put(job)
            except Exception as e:
                print(f"Error: {e}")

    def __push_process(self) -> Generator[simpy.Event, None, None]:
        while True:
            try:
                yield self.env.timeout(agent_wake_up_frequency)
                push_job = self.__push_decision()

                if push_job:
                    job = yield self.job_queue.get()
                    self.job_released_event.succeed(job)
                    self.job_released_event = self.env.event()

            except Exception as e:
                print(f"Error: {e}")

    def run(self) -> None:
        self.env.process(self.__job_creations_process())
        self.env.process(self.__push_process())


def __event_handler(release_policy: JobReleasePolicy):
    while True:
        try:
            job = yield release_policy.job_released_event
            print(job)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    env = simpy.Environment()
    release_policy = PushJobReleasePolicy(env)
    release_policy.run()
    env.process(__event_handler(release_policy))
    env.run(until=2)
