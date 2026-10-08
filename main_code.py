"""Student grade management system.

Provides a ``Student`` class that stores numeric grades (0-100), computes the
average, letter grade, pass/fail status and honor roll flag, and can produce a
formatted summary report.
"""

MIN_GRADE = 0.0
MAX_GRADE = 100.0
PASSING_AVERAGE = 60.0
HONOR_ROLL_AVERAGE = 90.0
LETTER_THRESHOLDS = ((90.0, "A"), (80.0, "B"), (70.0, "C"), (60.0, "D"))
FAILING_LETTER = "F"


def _is_number(value):
    """Return True if value is an int or float (booleans are rejected)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


class Student:
    """A student with an ID, a name and a list of grades."""

    def __init__(self, student_id, name):
        """Create a student.

        Raises:
            ValueError: if the ID or the name is empty.
            TypeError: if the ID or the name is not a string.
        """
        self._student_id = self._validate_text(student_id, "Student ID")
        self._name = self._validate_text(name, "Student name")
        self._grades = []

    @staticmethod
    def _validate_text(value, field_name):
        """Return the stripped text or raise if it is not a non-empty string."""
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string.")
        value = value.strip()
        if not value:
            raise ValueError(f"{field_name} cannot be empty.")
        return value

    @property
    def student_id(self):
        """Return the student ID."""
        return self._student_id

    @property
    def name(self):
        """Return the student name."""
        return self._name

    @property
    def grades(self):
        """Return a read-only copy of the grades."""
        return tuple(self._grades)

    def add_grade(self, grade):
        """Add a grade.

        Raises:
            TypeError: if the grade is not a number.
            ValueError: if the grade is outside the 0-100 range.
        """
        if not _is_number(grade):
            raise TypeError(f"Grade must be a number, got {grade!r}.")
        if not MIN_GRADE <= grade <= MAX_GRADE:
            raise ValueError(
                f"Grade must be between {MIN_GRADE:g} and {MAX_GRADE:g}, got {grade}."
            )
        self._grades.append(float(grade))

    def remove_grade_by_value(self, value):
        """Remove the first grade equal to value.

        Raises:
            TypeError: if value is not a number.
            ValueError: if the grade does not exist.
        """
        if not _is_number(value):
            raise TypeError(f"Grade must be a number, got {value!r}.")
        try:
            self._grades.remove(float(value))
        except ValueError:
            raise ValueError(f"Grade {value} was not found.") from None

    def remove_grade_by_index(self, index):
        """Remove the grade at a zero-based index.

        Raises:
            TypeError: if index is not an integer.
            IndexError: if the index is out of bounds.
        """
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError(f"Index must be an integer, got {index!r}.")
        if not 0 <= index < len(self._grades):
            raise IndexError(
                f"Index {index} is out of range (student has {len(self._grades)} grades)."
            )
        del self._grades[index]

    @property
    def average(self):
        """Return the average grade (0.0 if there are no grades)."""
        if not self._grades:
            return 0.0
        return sum(self._grades) / len(self._grades)

    @property
    def letter_grade(self):
        """Return the letter grade for the current average."""
        average = self.average
        for threshold, letter in LETTER_THRESHOLDS:
            if average >= threshold:
                return letter
        return FAILING_LETTER

    @property
    def is_passed(self):
        """Return True if the average is at least the passing average."""
        return self.average >= PASSING_AVERAGE

    @property
    def is_honor_roll(self):
        """Return True if the average reaches the honor roll threshold."""
        return self.average >= HONOR_ROLL_AVERAGE

    def summary_report(self):
        """Return a formatted summary report of the student."""
        status = "Passed" if self.is_passed else "Failed"
        lines = [
            "=" * 34,
            f"Student ID    : {self.student_id}",
            f"Student Name  : {self.name}",
            f"Grades Count  : {len(self._grades)}",
            f"Average Grade : {self.average:.2f}",
            f"Letter Grade  : {self.letter_grade}",
            f"Status        : {status}",
            f"Honor Roll    : {self.is_honor_roll}",
            "=" * 34,
        ]
        return "\n".join(lines)


def _attempt(description, action, *args):
    """Run action(*args) and print a clear message instead of crashing."""
    try:
        action(*args)
    except (TypeError, ValueError, IndexError) as error:
        print(f"  [ERROR] {description}: {error}")
    else:
        print(f"  [OK] {description}")


def _section(title):
    """Print a section title."""
    print(f"\n--- {title} ---")


def main():
    """Demonstrate every functional requirement."""
    _section("1. Add students (valid)")
    student = Student("2021001", "Ana Torres")
    print(f"  Created: {student.student_id} - {student.name}")

    _section("2. Add grades (numeric, 0-100)")
    for grade in (95.0, 72.5, 88, 100):
        _attempt(f"add_grade({grade})", student.add_grade, grade)
    print(f"  Grades: {list(student.grades)}")

    _section("3-5. Average, letter grade, pass/fail")
    print(f"  Average      : {student.average:.2f}")
    print(f"  Letter grade : {student.letter_grade}")
    print(f"  Result       : {'Passed' if student.is_passed else 'Failed'}")

    _section("6. Invalid inputs (no crashes)")
    _attempt('Student("", "Luis")', Student, "", "Luis")
    _attempt('Student("2021002", "   ")', Student, "2021002", "   ")
    _attempt('add_grade("Fifty")', student.add_grade, "Fifty")
    _attempt("add_grade(150)", student.add_grade, 150)
    _attempt("add_grade(-5)", student.add_grade, -5)
    _attempt("add_grade(True)", student.add_grade, True)
    _attempt("add_grade(None)", student.add_grade, None)

    _section("7. Honor roll (boolean flag)")
    print(f"  {student.name} honor roll: {student.is_honor_roll}")
    top = Student("2021005", "Maria Vera")
    for grade in (95, 92.5):
        top.add_grade(grade)
    print(f"  {top.name} honor roll: {top.is_honor_roll} (average {top.average:.2f})")
    failing = Student("2021003", "Carlos Ruiz")
    for grade in (40, 55.5, 62):
        failing.add_grade(grade)
    print(
        f"  {failing.name} honor roll: {failing.is_honor_roll} "
        f"(average {failing.average:.2f}, letter {failing.letter_grade})"
    )

    _section("8. Remove a grade (by value and by index)")
    _attempt("remove_grade_by_value(72.5)", student.remove_grade_by_value, 72.5)
    _attempt("remove_grade_by_value(33)", student.remove_grade_by_value, 33)
    _attempt("remove_grade_by_index(0)", student.remove_grade_by_index, 0)
    _attempt("remove_grade_by_index(9)", student.remove_grade_by_index, 9)
    _attempt("remove_grade_by_index(-1)", student.remove_grade_by_index, -1)
    print(f"  Grades now: {list(student.grades)}")

    _section("9. Summary reports")
    print(student.summary_report())
    print(failing.summary_report())
    print(Student("2021004", "Sin Notas").summary_report())


if __name__ == "__main__":
    main()
