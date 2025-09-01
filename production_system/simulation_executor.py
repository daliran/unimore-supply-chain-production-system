import simpy
from job_release_policy import JobReleasePolicy, PushJobReleasePolicy
from factory import Factory
from random_seed_generation import generate_seed_pool, set_global_seed


def run_push_simulation():
    seed_pool = generate_seed_pool(42, 100)
    # seed = seed_pool[experiment_id % len(seed_pool)]
    set_global_seed(seed_pool[0])

    env = simpy.Environment()

    factory = Factory(env, verbose_log=False)
    factory.run()

    release_policy = PushJobReleasePolicy(env, factory.input_jobs_queue)
    release_policy.run()

    # time unit = day
    env.run(until=10)


if __name__ == "__main__":
    run_push_simulation()
