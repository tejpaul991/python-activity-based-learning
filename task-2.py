
from dataclasses import dataclass
from typing import Dict


# -----------------------------------------
# Examination Policy
# -----------------------------------------

@dataclass
class ExamPolicy:
    pass_percentage: float = 35.0
    max_grace_per_subject: int = 5
    max_total_grace: int = 10
    max_marks_per_subject: int = 100
    distinction_percentage: float = 75.0
    first_class_percentage: float = 60.0
    second_class_percentage: float = 50.0


# -----------------------------------------
# Examination Result System
# -----------------------------------------

class ExaminationResultSystem:

    def __init__(self, policy: ExamPolicy):
        self.policy = policy

    def validate_marks(self, marks: Dict[str, int]) -> None:
        if not marks:
            raise ValueError("At least one subject is required.")

        for subject, score in marks.items():
            if not subject.strip():
                raise ValueError("Subject name cannot be empty.")

            if not isinstance(score, int) or isinstance(score, bool):
                raise ValueError(
                    f"Marks for {subject} must be integers."
                )

            if score < 0 or score > self.policy.max_marks_per_subject:
                raise ValueError(
                    f"Marks for {subject} must be between 0 and "
                    f"{self.policy.max_marks_per_subject}."
                )

        if not 0 <= self.policy.pass_percentage <= 100:
            raise ValueError("Invalid pass percentage.")

        if not 0 <= self.policy.max_grace_per_subject:
            raise ValueError("Grace limit per subject cannot be negative.")

        if not 0 <= self.policy.max_total_grace:
            raise ValueError("Total grace limit cannot be negative.")

        if not (
            0 <= self.policy.second_class_percentage
            <= self.policy.first_class_percentage
            <= self.policy.distinction_percentage
            <= 100
        ):
            raise ValueError("Invalid classification thresholds.")

    def calculate_results(self, marks: Dict[str, int]) -> dict:
        self.validate_marks(marks)

        pass_marks = (
            self.policy.max_marks_per_subject
            * self.policy.pass_percentage
            / 100
        )

        # Round up so a student must meet the minimum
        # whole-number mark required to pass.
        required_marks = int(pass_marks)
        if required_marks < pass_marks:
            required_marks += 1

        final_marks = marks.copy()
        grace_awarded = {subject: 0 for subject in marks}
        grace_used = 0

        # Give grace only to subjects where the student is
        # below the pass mark and within the allowed grace limit.
        for subject, score in marks.items():
            deficit = required_marks - score

            if deficit <= 0:
                continue

            grace = min(
                deficit,
                self.policy.max_grace_per_subject,
                self.policy.max_total_grace - grace_used,
                self.policy.max_marks_per_subject - score
            )

            if grace > 0:
                final_marks[subject] += grace
                grace_awarded[subject] = grace
                grace_used += grace

        # Verify subject-wise results after grace marks.
        subject_results = {}
        for subject, score in final_marks.items():
            subject_results[subject] = (
                "PASS" if score >= required_marks else "FAIL"
            )

        total_marks = sum(final_marks.values())
        maximum_total = (
            len(final_marks) * self.policy.max_marks_per_subject
        )

        percentage = (total_marks / maximum_total) * 100

        # Overall result: every subject must be passed.
        if any(result == "FAIL" for result in subject_results.values()):
            classification = "FAIL"
        elif percentage >= self.policy.distinction_percentage:
            classification = "DISTINCTION"
        elif percentage >= self.policy.first_class_percentage:
            classification = "FIRST CLASS"
        elif percentage >= self.policy.second_class_percentage:
            classification = "SECOND CLASS"
        else:
            classification = "PASS"

        return {
            "original_marks": marks,
            "final_marks": final_marks,
            "grace_awarded": grace_awarded,
            "total_grace_used": grace_used,
            "subject_results": subject_results,
            "required_pass_marks": required_marks,
            "total_marks": total_marks,
            "maximum_total": maximum_total,
            "percentage": round(percentage, 2),
            "classification": classification,
        }


# -----------------------------------------
# Main Program
# -----------------------------------------

if __name__ == "__main__":

    policy = ExamPolicy(
        pass_percentage=35,
        max_grace_per_subject=5,
        max_total_grace=10,
        max_marks_per_subject=100,
        distinction_percentage=75,
        first_class_percentage=60,
        second_class_percentage=50,
    )

    exam_system = ExaminationResultSystem(policy)

    # Example marks for multiple subjects
    student_marks = {
        "Mathematics": 32,
        "Science": 34,
        "English": 65,
        "Computer Science": 80,
        "Social Studies": 55,
    }

    try:
        result = exam_system.calculate_results(student_marks)

        print("\n===== EXAMINATION RESULT =====")

        print("\nSubject-wise Details:")
        for subject in result["original_marks"]:
            print(
                f"{subject}: "
                f"Original = {result['original_marks'][subject]}, "
                f"Grace = {result['grace_awarded'][subject]}, "
                f"Final = {result['final_marks'][subject]}, "
                f"Result = {result['subject_results'][subject]}"
            )

        print("\nTotal Grace Marks:", result["total_grace_used"])
        print(
            "Total Marks:",
            f"{result['total_marks']}/{result['maximum_total']}"
        )
        print("Percentage:", f"{result['percentage']}%")
        print("Final Classification:", result["classification"])

    except ValueError as error:
        print("Validation Error:", error)
