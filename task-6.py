
class ExaminationEligibilitySystem:

    def __init__(
        self,
        minimum_attendance=75.0,
        minimum_internal_marks=40.0,
        maximum_internal_marks=100.0
    ):
        self.minimum_attendance = minimum_attendance
        self.minimum_internal_marks = minimum_internal_marks
        self.maximum_internal_marks = maximum_internal_marks

    def validate(self, attendance, lab_completed,
                 internal_marks, fees_cleared):

        if not 0 <= attendance <= 100:
            raise ValueError(
                "Attendance must be between 0 and 100."
            )

        if not isinstance(lab_completed, bool):
            raise ValueError(
                "Laboratory completion must be True or False."
            )

        if not (
            0 <= internal_marks <= self.maximum_internal_marks
        ):
            raise ValueError(
                f"Internal marks must be between 0 and "
                f"{self.maximum_internal_marks}."
            )

        if not isinstance(fees_cleared, bool):
            raise ValueError(
                "Fee clearance must be True or False."
            )

    def check_eligibility(
        self,
        student_name,
        attendance,
        lab_completed,
        internal_marks,
        fees_cleared
    ):
        # Validate all input values
        self.validate(
            attendance,
            lab_completed,
            internal_marks,
            fees_cleared
        )

        unmet_requirements = []

        # Stage 1: Attendance check
        if attendance < self.minimum_attendance:
            unmet_requirements.append(
                f"Attendance is {attendance:.1f}%; "
                f"minimum required is "
                f"{self.minimum_attendance:.1f}%."
            )

        # Stage 2: Laboratory completion check
        if not lab_completed:
            unmet_requirements.append(
                "Required laboratory work is incomplete."
            )

        # Stage 3: Internal assessment check
        if internal_marks < self.minimum_internal_marks:
            unmet_requirements.append(
                f"Internal assessment marks are {internal_marks}; "
                f"minimum required is "
                f"{self.minimum_internal_marks}."
            )

        # Stage 4: Fee clearance check
        if not fees_cleared:
            unmet_requirements.append(
                "Outstanding fees must be cleared."
            )

        # Generate final decision
        eligible = len(unmet_requirements) == 0

        return {
            "student_name": student_name,
            "attendance": attendance,
            "lab_completed": lab_completed,
            "internal_marks": internal_marks,
            "fees_cleared": fees_cleared,
            "eligible": eligible,
            "unmet_requirements": unmet_requirements
        }

    def display_result(self, result):
        print("\n===== EXAMINATION ELIGIBILITY REPORT =====")
        print("Student Name:", result["student_name"])
        print("Attendance:", f'{result["attendance"]:.1f}%')
        print(
            "Laboratory Completed:",
            "Yes" if result["lab_completed"] else "No"
        )
        print("Internal Marks:", result["internal_marks"])
        print(
            "Fees Cleared:",
            "Yes" if result["fees_cleared"] else "No"
        )

        print("\nFinal Decision:")

        if result["eligible"]:
            print("ELIGIBLE for the final examination.")
            print("All requirements have been satisfied.")
        else:
            print("NOT ELIGIBLE for the final examination.")
            print("\nUnmet Requirements:")

            for number, requirement in enumerate(
                result["unmet_requirements"], start=1
            ):
                print(f"{number}. {requirement}")

        print("==========================================")


def get_yes_no(prompt):
    """Read a valid yes/no response."""
    while True:
        answer = input(prompt).strip().lower()

        if answer in ("yes", "y"):
            return True
        elif answer in ("no", "n"):
            return False
        else:
            print("Invalid input. Enter yes or no.")


def main():
    system = ExaminationEligibilitySystem(
        minimum_attendance=75.0,
        minimum_internal_marks=40.0,
        maximum_internal_marks=100.0
    )

    print("MULTI-STAGE EXAMINATION ELIGIBILITY SYSTEM")

    try:
        student_name = input("Enter student name: ").strip()

        if not student_name:
            raise ValueError("Student name cannot be empty.")

        attendance = float(
            input("Enter attendance percentage: ")
        )

        lab_completed = get_yes_no(
            "Is laboratory work completed? (yes/no): "
        )

        internal_marks = float(
            input("Enter internal assessment marks: ")
        )

        fees_cleared = get_yes_no(
            "Are all fees cleared? (yes/no): "
        )

        result = system.check_eligibility(
            student_name,
            attendance,
            lab_completed,
            internal_marks,
            fees_cleared
        )

        system.display_result(result)

    except ValueError as error:
        print("Input Error:", error)


if __name__ == "__main__":
    main()
