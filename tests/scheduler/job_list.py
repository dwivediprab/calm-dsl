from calm.dsl.builtins import Job
from calm.dsl.cli.scheduler import JobScheduler

start_date_time = "2050-10-08 16:17:15"
time_zone = "America/Jamaica"

RUNBOOK_NAME = "job_list"


class JobOneTimeListSpec(Job):
    """One Time Job for Executing a Runbook"""

    schedule_info = JobScheduler.ScheduleInfo.oneTime(start_date_time, time_zone)
    executable = JobScheduler.Exec.runbook(RUNBOOK_NAME, False)
