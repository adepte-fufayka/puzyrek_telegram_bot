import datetime

from CONSTANTS import LINE_SPLITTER


class Bandit:
    name: str
    km: int
    voevat_suda: bool
    def __init__(self, name: str, km:int, voevat_suda: bool) -> None:
        self.voevat_suda = voevat_suda
        self.km = km
        self.name = name
    def __str__(self) -> str:
        return LINE_SPLITTER.join([self.name, str(self.km), str(self.voevat_suda)])

class Band:
    band_id: int
    band_name: str
    update_date:datetime.datetime
    band_members: list[Bandit]

    def __init__(self, band_id: int, band_name: str, update_date:datetime.datetime, band_members: list[Bandit]) -> None:
        self.band_members = band_members
        self.band_id = band_id
        self.update_date = update_date
        self.band_name = band_name
    def __str__(self) -> str:
        return LINE_SPLITTER.join([str(i) for i in self.band_members])
