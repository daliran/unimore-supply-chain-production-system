from collections import OrderedDict
from typing import Optional


class Job:
    def __init__(
        self,
        id: int,
        familyName: str,
        inter_arrival_time: float,
        work_centers_routing: OrderedDict[str, float],
        due_date: float,
    ) -> None:
        self.id = id
        self.familyName = familyName
        self.inter_arrival_time = inter_arrival_time
        self.work_centers_routing = work_centers_routing
        self.due_date = due_date

        self.working_center_iterator = iter(work_centers_routing)
        self.current_working_center_name: Optional[str] = next(
            self.working_center_iterator
        )
        # self.completed_work_centers_names: list[str] = []
        # self.completed = False

    def mark_work_center_completed(self, work_center_name: str) -> None:
        """if work_center_name in self.completed_work_centers_names:
        raise ValueError(
            f"Work center {work_center_name} has already been completed"
        )
        """

        if work_center_name != self.current_working_center_name:
            raise ValueError(
                f"Unexpected work center completion: {work_center_name}. "
                f"Expected: {self.current_working_center_name}"
            )

        # self.completed_work_centers_names.append(work_center_name)

        try:
            self.current_working_center_name = next(self.working_center_iterator)
        except StopIteration:
            self.current_working_center_name = None
            # self.completed = True

    def __str__(self) -> str:
        return (
            f"id: {self.id}, "
            f"family: {self.familyName}, "
            f"inter arrival time: {self.inter_arrival_time}, "
            f"routing: {self.work_centers_routing}, "
            f"due date: {self.due_date}"
        )
