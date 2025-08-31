import simpy
from job_release_policy import JobReleasePolicy, PushJobReleasePolicy
from factory import Factory
from random_seed_generation import generate_seed_pool, set_global_seed

def job_events_process(release_policy: JobReleasePolicy, factory: Factory):
    while True:
        try:
            job = yield release_policy.job_released_event
            factory.handle_job(job)
        except Exception as e:
            print(f"Error: {e}")

def run_push_simulation():  
    seed_pool = generate_seed_pool(42, 100)
    #seed = seed_pool[experiment_id % len(seed_pool)]
    set_global_seed(seed_pool[0])

    env = simpy.Environment()
    release_policy = PushJobReleasePolicy(env)
    release_policy.run()

    factory = Factory(env)
    factory.run()

    env.process(job_events_process(release_policy, factory))

    # time unit = day
    env.run(until=30)

if __name__ == "__main__":
    run_push_simulation()
