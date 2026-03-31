from dataclasses import dataclass, field
from typing import Dict, List, Optional

ADMIN_PASSWORD = "admin123"
RATE_PER_CREDIT = 300.00


@dataclass
class Student:
    id: str
    name: str
    major: str
    enrolled_courses: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        return f"{self.name} ({self.id}) - {self.major}"


@dataclass
class Course:
    code: str
    title: str
    credits: int
    capacity: int
    time: str
    prerequisites: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        prereq = ", ".join(self.prerequisites) if self.prerequisites else "None"
        return f"{self.code:10} {self.title:40} {self.credits:8} {self.capacity:12} {self.time:18} {prereq}"


class EnrollmentSystem:
    def __init__(self) -> None:
        self.students: Dict[str, Student] = {}
        self.courses: Dict[str, Course] = {}
        self._seed_default_data()

    def _seed_default_data(self) -> None:
        self.courses["CS101"] = Course("CS101", "Intro to Computer Science", 3, 30, "MWF 09:00-10:00")
        self.courses["MATH201"] = Course("MATH201", "Calculus I", 4, 25, "TTh 10:00-11:30")
        self.students["s001"] = Student("s001", "Alice Johnson", "Computer Science")

    def get_student(self, student_id: str) -> Optional[Student]:
        return self.students.get(student_id)

    def add_student(self, student: Student) -> None:
        self.students[student.id] = student

    def update_student(self, student_id: str, name: Optional[str], major: Optional[str]) -> None:
        student = self.get_student(student_id)
        if student is None:
            return
        if name:
            student.name = name
        if major:
            student.major = major

    def get_all_courses(self) -> List[Course]:
        return list(self.courses.values())

    def get_course(self, code: str) -> Optional[Course]:
        return self.courses.get(code)

    def get_student_schedule(self, student_id: str) -> List[Course]:
        student = self.get_student(student_id)
        if student is None:
            return []
        return [self.courses[code] for code in student.enrolled_courses if code in self.courses]

    def register_course(self, student_id: str, course_code: str) -> str:
        student = self.get_student(student_id)
        course = self.get_course(course_code)
        if student is None:
            return "Student not found."
        if course is None:
            return f"Course {course_code} not found."
        if course_code in student.enrolled_courses:
            return "Already enrolled in that course."
        if len([s for s in self.students.values() if course_code in s.enrolled_courses]) >= course.capacity:
            return "Course is full."
        student.enrolled_courses.append(course_code)
        return "Registered successfully."

    def drop_course(self, student_id: str, course_code: str) -> str:
        student = self.get_student(student_id)
        if student is None:
            return "Student not found."
        if course_code not in student.enrolled_courses:
            return "You are not enrolled in that course."
        student.enrolled_courses.remove(course_code)
        return "Dropped successfully."

    def calculate_tuition(self, student_id: str) -> float:
        schedule = self.get_student_schedule(student_id)
        return sum(course.credits for course in schedule) * RATE_PER_CREDIT

    def get_course_roster(self, course_code: str) -> List[Student]:
        return [student for student in self.students.values() if course_code in student.enrolled_courses]

    def get_all_students(self) -> List[Student]:
        return list(self.students.values())


class Main:
    def __init__(self) -> None:
        self.system = EnrollmentSystem()

    def run(self) -> None:
        self.print_banner()
        quit_program = False
        while not quit_program:
            quit_program = self.login_menu()

    def print_banner(self) -> None:
        print("=" * 70)
        print("       COURSE ENROLLMENT SYSTEM")
        print("=" * 70)

    def login_menu(self) -> bool:
        print()
        print("=" * 70)
        print("  LOGIN")
        print("=" * 70)
        print("  [1] Login as Student")
        print("  [2] Login as Admin")
        print("  [3] Exit")
        print("-" * 70)
        choice = input("  Select option: ").strip()
        if choice == "1":
            self.student_login()
        elif choice == "2":
            self.admin_login()
        elif choice == "3":
            print("  Thank you for using the Course Enrollment System. Goodbye!")
            print("=" * 70)
            return True
        else:
            print("  [!] Invalid option. Please enter 1, 2, or 3.")
        return False

    def student_login(self) -> None:
        print()
        print("  --- Student Login ---")
        student_id = input("  Enter your Student ID (or 'new' to create a new profile): ").strip()
        if student_id.lower() == "new":
            new_student = self.create_student_profile()
            if new_student:
                self.student_menu(new_student)
            return
        student = self.system.get_student(student_id)
        if student is None:
            print("  [!] Student ID not found. Type 'new' to create a new profile.")
            return
        print(f"  Welcome, {student.name}!")
        self.student_menu(student)

    def create_student_profile(self) -> Optional[Student]:
        print()
        print("  --- Create New Student Profile ---")
        student_id = input("  Student ID: ").strip()
        if not student_id:
            print("  [!] Student ID cannot be empty.")
            return None
        if self.system.get_student(student_id) is not None:
            print("  [!] Student ID already exists.")
            return None
        name = input("  Full Name : ").strip()
        if not name:
            print("  [!] Name cannot be empty.")
            return None
        major = input("  Major     : ").strip() or "Undeclared"
        student = Student(student_id, name, major)
        self.system.add_student(student)
        print(f"  [✓] New student profile created: {student}")
        return student

    def admin_login(self) -> None:
        print()
        print("  --- Admin Login ---")
        password = input("  Password: ").strip()
        if password != ADMIN_PASSWORD:
            print("  [!] Incorrect password.")
            return
        print("  Welcome, Administrator!")
        self.admin_menu()

    def student_menu(self, student: Student) -> None:
        while True:
            print()
            print("=" * 70)
            print(f"  STUDENT MENU  –  {student.name} [{student.id}]")
            print("=" * 70)
            print("  [1] View Course Catalog")
            print("  [2] Register for a Course")
            print("  [3] Drop a Course")
            print("  [4] View My Schedule")
            print("  [5] Billing Summary")
            print("  [6] Edit My Profile")
            print("  [7] Logout and Save")
            print("-" * 70)
            choice = input("  Select option: ").strip()
            if choice == "1":
                self.view_course_catalog()
            elif choice == "2":
                self.register_for_course(student)
            elif choice == "3":
                self.drop_course(student)
            elif choice == "4":
                self.view_schedule(student)
            elif choice == "5":
                self.billing_summary(student)
            elif choice == "6":
                self.edit_profile(student)
            elif choice == "7":
                print("  [✓] Changes saved.")
                break
            else:
                print("  [!] Invalid option.")

    def admin_menu(self) -> None:
        while True:
            print()
            print("=" * 70)
            print("  ADMIN MENU")
            print("=" * 70)
            print("  [1]  View Course Catalog")
            print("  [2]  View Class Roster")
            print("  [3]  View All Students")
            print("  [4]  Add New Student")
            print("  [5]  Edit Student Profile")
            print("  [6]  Add New Course")
            print("  [7]  Edit Course")
            print("  [8]  View Student Schedule")
            print("  [9]  Billing Summary (any student)")
            print("  [10] Logout and Save")
            print("-" * 70)
            choice = input("  Select option: ").strip()
            if choice == "1":
                self.view_course_catalog()
            elif choice == "2":
                self.admin_view_roster()
            elif choice == "3":
                self.admin_view_students()
            elif choice == "4":
                self.admin_add_student()
            elif choice == "5":
                self.admin_edit_student()
            elif choice == "6":
                self.admin_add_course()
            elif choice == "7":
                self.admin_edit_course()
            elif choice == "8":
                self.admin_view_schedule()
            elif choice == "9":
                self.admin_billing_summary()
            elif choice == "10":
                print("  [✓] Changes saved.")
                break
            else:
                print("  [!] Invalid option.")

    def view_course_catalog(self) -> None:
        print()
        print("=" * 70)
        print("  COURSE CATALOG")
        print("=" * 70)
        courses = self.system.get_all_courses()
        if not courses:
            print("  No courses available.")
            return
        print(f"  {'Code':10} {'Title':40} {'Credits':8} {'Seats':12} {'Time':18} Prerequisites")
        print("  " + "-" * 70)
        for course in courses:
            print(f"  {course}")

    def register_for_course(self, student: Student) -> None:
        print()
        print("  --- Register for a Course ---")
        self.view_course_catalog()
        course_code = input("\n  Enter course code to register (or press Enter to cancel): ").strip().upper()
        if not course_code:
            return
        message = self.system.register_course(student.id, course_code)
        status = "[✓]" if message.endswith("successfully.") else "[✗]"
        print(f"  {status} {message}")

    def drop_course(self, student: Student) -> None:
        print()
        print("  --- Drop a Course ---")
        schedule = self.system.get_student_schedule(student.id)
        if not schedule:
            print("  You are not enrolled in any courses.")
            return
        print("  Your current courses:")
        for course in schedule:
            print(f"    {course.code} – {course.title}")
        course_code = input("\n  Enter course code to drop (or press Enter to cancel): ").strip().upper()
        if not course_code:
            return
        message = self.system.drop_course(student.id, course_code)
        status = "[✓]" if message.endswith("successfully.") else "[✗]"
        print(f"  {status} {message}")

    def view_schedule(self, student: Student) -> None:
        print()
        print("=" * 70)
        print(f"  SCHEDULE FOR: {student.name} [{student.id}]")
        print("=" * 70)
        schedule = self.system.get_student_schedule(student.id)
        if not schedule:
            print("  You are not enrolled in any courses.")
            return
        self.view_course_catalog_header()
        for course in schedule:
            print(f"  {course}")
        total_credits = sum(course.credits for course in schedule)
        print()
        print(f"  Total Credits Enrolled: {total_credits}")

    def view_course_catalog_header(self) -> None:
        print(f"  {'Code':10} {'Title':40} {'Credits':8} {'Seats':12} {'Time':18} Prerequisites")
        print("  " + "-" * 70)

    def billing_summary(self, student: Student) -> None:
        print()
        print("=" * 70)
        print(f"  BILLING SUMMARY FOR: {student.name} [{student.id}]")
        print("=" * 70)
        schedule = self.system.get_student_schedule(student.id)
        if not schedule:
            print("  You are not enrolled in any courses. Tuition: $0.00")
            return
        print(f"  {'Code':10} {'Title':40} {'Credits'}")
        print("  " + "-" * 70)
        total_credits = 0
        for course in schedule:
            print(f"  {course.code:10} {course.title:40} {course.credits}")
            total_credits += course.credits
        tuition = self.system.calculate_tuition(student.id)
        print("  " + "-" * 70)
        print(f"  Total Credits : {total_credits}")
        print(f"  Rate per Credit: ${RATE_PER_CREDIT:.2f}")
        print(f"  {'TOTAL TUITION:':42} ${tuition:.2f}")

    def edit_profile(self, student: Student) -> None:
        print()
        print("  --- Edit My Profile ---")
        print(f"  Current: {student}")
        print("  (Press Enter to keep current value)")
        name = input(f"  New Name  [{student.name}]: ").strip()
        major = input(f"  New Major [{student.major}]: ").strip()
        self.system.update_student(student.id, name or None, major or None)
        print("  [✓] Profile updated.")
        print(f"  Updated: {student}")

    def admin_view_roster(self) -> None:
        print()
        print("  --- Class Roster ---")
        self.view_course_catalog()
        course_code = input("\n  Enter course code (or press Enter to cancel): ").strip().upper()
        if not course_code:
            return
        course = self.system.get_course(course_code)
        if course is None:
            print(f"  [!] Course not found: {course_code}")
            return
        roster = self.system.get_course_roster(course_code)
        print()
        print("=" * 70)
        print(f"  ROSTER: {course.code} – {course.title}")
        print("=" * 70)
        if not roster:
            print("  No students enrolled.")
            return
        print(f"  {'ID':15} {'Name':25} {'Major'}")
        print("  " + "-" * 70)
        for student in roster:
            print(f"  {student.id:15} {student.name:25} {student.major}")
        print(f"\n  Total enrolled: {len(roster)} / {course.capacity}")

    def admin_view_students(self) -> None:
        print()
        print("=" * 70)
        print("  ALL STUDENTS")
        print("=" * 70)
        students = self.system.get_all_students()
        if not students:
            print("  No students registered.")
            return
        print(f"  {'ID':15} {'Name':25} {'Major':20} Enrolled Courses")
        print("  " + "-" * 70)
        for student in students:
            enrolled = ", ".join(student.enrolled_courses) if student.enrolled_courses else "None"
            print(f"  {student.id:15} {student.name:25} {student.major:20} {enrolled}")

    def admin_add_student(self) -> None:
        print()
        print("  --- Add New Student ---")
        student_id = input("  Student ID: ").strip()
        if not student_id:
            print("  [!] Student ID cannot be empty.")
            return
        if self.system.get_student(student_id) is not None:
            print("  [!] Student ID already exists.")
            return
        name = input("  Full Name : ").strip()
        major = input("  Major     : ").strip() or "Undeclared"
        self.system.add_student(Student(student_id, name, major))
        print("  [✓] Student added.")

    def admin_edit_student(self) -> None:
        print()
        print("  --- Edit Student Profile ---")
        self.admin_view_students()
        student_id = input("\n  Enter Student ID to edit (or press Enter to cancel): ").strip()
        if not student_id:
            return
        student = self.system.get_student(student_id)
        if student is None:
            print(f"  [!] Student not found: {student_id}")
            return
        print(f"  Current: {student}")
        print("  (Press Enter to keep current value)")
        name = input(f"  New Name  [{student.name}]: ").strip()
        major = input(f"  New Major [{student.major}]: ").strip()
        self.system.update_student(student_id, name or None, major or None)
        print(f"  [✓] Profile updated: {student}")

    def admin_add_course(self) -> None:
        print()
        print("  --- Add New Course ---")
        code = input("  Course Code    : ").strip().upper()
        if not code:
            print("  [!] Course code cannot be empty.")
            return
        if self.system.get_course(code) is not None:
            print(f"  [!] Course code already exists: {code}")
            return
        title = input("  Title          : ").strip()
        credits = self._parse_int(input("  Credits        : ").strip(), 3)
        capacity = self._parse_int(input("  Capacity       : ").strip(), 30)
        days = input("  Days (e.g. MWF): ").strip()
        start = input("  Start Time (HH:mm): ").strip()
        end = input("  End Time   (HH:mm): ").strip()
        prereq_input = input("  Prerequisites (comma-separated codes, or blank): ").strip()
        time = f"{days} {start}-{end}" if days and start and end else "TBD"
        prerequisites = [code.strip().upper() for code in prereq_input.split(",") if code.strip()] if prereq_input else []
        self.system.courses[code] = Course(code, title, credits, capacity, time, prerequisites)
        print(f"  [✓] Course added: {code} - {title}")

    def admin_edit_course(self) -> None:
        print()
        print("  --- Edit Course ---")
        self.view_course_catalog()
        course_code = input("\n  Enter course code to edit (or press Enter to cancel): ").strip().upper()
        if not course_code:
            return
        course = self.system.get_course(course_code)
        if course is None:
            print(f"  [!] Course not found: {course_code}")
            return
        print(f"  Current: {course}")
        print("  (Press Enter to keep current value)")
        title = input(f"  New Title    [{course.title}]: ").strip() or course.title
        credits = self._parse_int(input(f"  New Credits  [{course.credits}]: ").strip(), course.credits)
        capacity = self._parse_int(input(f"  New Capacity [{course.capacity}]: ").strip(), course.capacity)
        course.title = title
        course.credits = credits
        course.capacity = capacity
        print(f"  [✓] Course updated: {course}")

    def admin_view_schedule(self) -> None:
        print()
        print("  --- View Student Schedule ---")
        self.admin_view_students()
        student_id = input("\n  Enter Student ID (or press Enter to cancel): ").strip()
        if not student_id:
            return
        student = self.system.get_student(student_id)
        if student is None:
            print(f"  [!] Student not found: {student_id}")
            return
        self.view_schedule(student)

    def admin_billing_summary(self) -> None:
        print()
        print("  --- Billing Summary ---")
        self.admin_view_students()
        student_id = input("\n  Enter Student ID (or press Enter to cancel): ").strip()
        if not student_id:
            return
        student = self.system.get_student(student_id)
        if student is None:
            print(f"  [!] Student not found: {student_id}")
            return
        self.billing_summary(student)

    def _parse_int(self, value: str, default: int) -> int:
        try:
            parsed = int(value)
            return parsed if parsed > 0 else default
        except ValueError:
            return default


def main() -> None:
    Main().run()


if __name__ == "__main__":
    main()
