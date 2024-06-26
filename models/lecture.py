class Lecture:
    startDate: int  # unix timestamp
    endDate: int  # unix timestamp
    name: str
    location: str
    teacherName: str
    periods: float
    startIndex: int
    endIndex: int
    startHHMM: int
    endHHMM: int
    additionalInfo: dict[str, str]

    def __init__(
        self,
        startDate: int,
        endDate: int,
        name: str,
        location: str,
        teacherName: str,
        periods: float,
        startIndex: int,
        endIndex: int,
        startHHMM: int,
        endHHMM: int,
        additionalInfo: dict[str, str],
    ):
        self.startDate = startDate
        self.endDate = endDate
        self.name = name
        self.location = location
        self.teacherName = teacherName
        self.periods = periods
        self.startIndex = startIndex
        self.endIndex = endIndex
        self.startHHMM = startHHMM
        self.endHHMM = endHHMM
        self.additionalInfo = additionalInfo
