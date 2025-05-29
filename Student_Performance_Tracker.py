import json

# Define the file where student data will be stored
data_file = "students.json"

class Student:
    # Class to represent a student with name, roll number, and grades
    def __init__(self, name, roll_number, grades=None):
        self.name = name
        self.roll_number = roll_number
        self.grades = grades if grades is not None else {}

    def add_grade(self, subject, grade):
        # Add a grade for a specific subject
        if 0 <= grade <= 100:  # Ensure grade is valid
            self.grades[subject] = grade
        else:
            print("Invalid grade. Must be between 0 and 100.")

    def calculate_average(self):
        # Calculate the average grade of the student
        if self.grades:
            return sum(self.grades.values()) / len(self.grades)
        return 0

    def to_dict(self):
        # Convert student data to dictionary format for JSON storage
        return {"name": self.name, "roll_number": self.roll_number, "grades": self.grades}

class StudentTracker:
    # Class to manage multiple students
    def __init__(self):
        self.students = self.load_students()

    def load_students(self):
        # Load student data from the JSON file
        try:
            with open(data_file, "r") as file:
                return [Student(**data) for data in json.load(file)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_students(self):
        # Save student data to the JSON file
        with open(data_file, "w") as file:
            json.dump([student.to_dict() for student in self.students], file, indent=4)

    def add_student(self, name, roll_number):
        # Add a new student if the roll number is unique
        if any(student.roll_number == roll_number for student in self.students):
            print("Roll number already exists.")
            return
        self.students.append(Student(name, roll_number))
        self.save_students()
        print("Student added successfully!")

    def add_grade(self, roll_number, subject, grade):
        # Add a grade for a specific student
        for student in self.students:
            if student.roll_number == roll_number:
                student.add_grade(subject, grade)
                self.save_students()
                print("Grade added successfully!")
                return
        print("Student not found.")

    def view_student_details(self, roll_number):
        # Display details of a specific student
        for student in self.students:
            if student.roll_number == roll_number:
                print(f"Name: {student.name}, Roll Number: {student.roll_number}")
                print("Grades:")
                for subject, grade in student.grades.items():
                    print(f"  {subject}: {grade}")
                print(f"Average Grade: {student.calculate_average():.2f}")
                return
        print("Student not found.")

    def calculate_class_average(self):
        # Calculate the overall class average grade
        if not self.students:
            print("No students available.")
            return
        total_average = sum(student.calculate_average() for student in self.students) / len(self.students)
        print(f"Class Average Grade: {total_average:.2f}")

    def view_all_students_summary(self):
        # Display a summary of all students with their average grades
        if not self.students:
            print("No students available.")
            return
        print("\nAll Students Summary:")
        for student in self.students:
            print(f"Name: {student.name}, Roll Number: {student.roll_number}, Average Grade: {student.calculate_average():.2f}")

# Main menu to interact with the tracker
def main():
    tracker = StudentTracker()
    while True:
        print("\nChoose an option:")
        print("1. Add Student")
        print("2. Add Grade")
        print("3. View Student Details")
        print("4. View Class Average")
        print("5. View All Students Summary")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == "1":
            name = input("Enter student name: ")
            roll_number = input("Enter roll number: ")
            tracker.add_student(name, roll_number)
        elif choice == "2":
            roll_number = input("Enter roll number: ")
            subject = input("Enter subject: ")
            try:
                grade = float(input("Enter grade (0-100): "))
                tracker.add_grade(roll_number, subject, grade)
            except ValueError:
                print("Invalid grade. Please enter a number.")
        elif choice == "3":
            roll_number = input("Enter roll number: ")
            tracker.view_student_details(roll_number)
        elif choice == "4":
            tracker.calculate_class_average()
        elif choice == "5":
            tracker.view_all_students_summary()
        elif choice == "6":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
