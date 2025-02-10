import csv
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from csv import DictWriter


class SaveToCsv:
    @staticmethod
    def save(team_name, statistics_dict, descriptions) -> None:

        team_filepath: str = f"Output/{team_name}.csv"

        if os.path.exists(team_filepath):
            with open(team_filepath, mode="a", encoding="utf-8-sig", newline="") as file:
                writer: DictWriter = csv.DictWriter(file, fieldnames=descriptions)
                file.seek(0, os.SEEK_END)
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(statistics_dict)
        else:
            try:
                with open(team_filepath, mode="a", encoding="utf-8-sig", newline="") as file:
                    writer: DictWriter = csv.DictWriter(file, fieldnames=descriptions)
                    writer.writeheader()
                    writer.writerow(statistics_dict)
            except Exception as e:
                print(f"Cannot save file because {e}")
