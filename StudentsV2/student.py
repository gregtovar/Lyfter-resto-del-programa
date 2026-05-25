
#
# student.py
# Defines the Student class used throughout the system.
#
#
#


#
#  Represents a single student with name, section, and four subject grades.
#
class Student:
     

    SUBJECTS = ["spanish", "english", "social_studies", "science"]

    def __init__(self, name: str, section: str,
                 spanish: float, english: float,
                 social_studies: float, science: float):
        self.name          = name
        self.section       = section
        self.spanish       = spanish
        self.english       = english
        self.social_studies = social_studies
        self.science       = science

    
    def get_average(self) -> float:
        #Return the arithmetic mean of the four subject grades.
        return (self.spanish + self.english + self.social_studies + self.science) / 4

    def to_dict(self) -> dict:
        #Convert to a plain dictionary (used for CSV export).
        return {
            "name":           self.name,
            "section":        self.section,
            "spanish":        self.spanish,
            "english":        self.english,
            "social_studies": self.social_studies,
            "science":        self.science,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Student":
        #Create a Student from a dictionary (used when importing CSV file).
        return cls(
            name           = d["name"],
            section        = d["section"],
            spanish        = float(d["spanish"]),
            english        = float(d["english"]),
            social_studies = float(d["social_studies"]),
            science        = float(d["science"]),
        )

    def __str__(self) -> str:
        return (f"{self.name} | {self.section} | "
                f"ES {self.spanish:.1f}  EN {self.english:.1f}  "
                f"SS {self.social_studies:.1f}  SC {self.science:.1f} | "
                f"Avg {self.get_average():.2f}")
