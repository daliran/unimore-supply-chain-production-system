from collections import OrderedDict

class Job:
    def __init__(
        self,
        familyName: str,
        inter_arrival_time: float,
        work_centers_routing: OrderedDict[str, float],
        due_date: float,
    ) -> None:
        self.familyName = familyName
        self.inter_arrival_time = inter_arrival_time
        self.work_centers_routing = work_centers_routing
        self.due_date = due_date

        

    def __str__(self) -> str:
        return f"f: {self.familyName}, iat: {self.inter_arrival_time}, wcr: {self.work_centers_routing}, dd: {self.due_date}"