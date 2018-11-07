"""
This is the logic module
"""

from repository import *
from model import *
from validation import *
from typing import *


class ChangesHandler:
    # @abstractmethod
    # def handleChanges(self, changes):
    pass


class DuplicateAssignment(CustomError):
    pass


class LogicComponent(ChangesHandler):
    """
    Provides all the logic functions of the software
    """

    def __init__(self, repository: Repository):
        self.__repository = repository
        self.__students: StudentCollection = repository.getStudents()
        self.__grades: GradeCollection = repository.getGrades()
        self.__assignments: AssignmentCollection = repository.getAssignments()
        self.__changesStack: ChangesStack = ChangesStack(self)
        self.populateRepository()

    def handleChanges(self, changes):
        pass

    def populateRepository(self):
        """
        Adds default data to the repository
        """
        studentList = [
            self.__students.addStudent(Student(0, 'Andrew', 915)),
            self.__students.addStudent(Student(0, 'Richard', 915)),
            self.__students.addStudent(Student(0, 'John', 917)),
            self.__students.addStudent(Student(0, 'Hori', 917))
        ]
        assignmentList = [
            self.__assignments.addAssignment(Assignment(0, 'Assignment 01', date(2018, 10, 10))),
            self.__assignments.addAssignment(Assignment(0, 'Assignment 02', date(2018, 10, 17))),
            self.__assignments.addAssignment(Assignment(0, 'Assignment 03-04', date(2018, 10, 31))),
            self.__assignments.addAssignment(Assignment(0, 'Assignment 05-07', date(2018, 11, 28)))
        ]

        self.__grades.assign(studentList[0], assignmentList[1])
        self.__grades.assign(studentList[0], assignmentList[3])
        self.__grades.assign(studentList[1], assignmentList[1])
        self.__grades.assign(studentList[1], assignmentList[2])
        self.__grades.assign(studentList[2], assignmentList[2])
        self.__grades.assign(studentList[2], assignmentList[3])
        self.__grades.assign(studentList[3], assignmentList[1])

    # Manage Students menu
    def listStudents(self) -> List[Student]:
        """
        Returns a list of students sorted in ascending order by their IDs
        """
        return sorted([student for student in self.__students], key=lambda student: student.getStudentId())

    def addStudent(self, name: str, group: str) -> Student:
        """
        Adds a student to the repository
        """
        group = self.parseInt(group, InvalidStudentGroup)
        student = Student(0, name, group)
        ValidationUtils.Student.validateStudent(student)
        return self.__students.addStudent(student)

    @staticmethod
    def parseInt(string: str, errorType: type) -> int:
        """
        Parses a number to an integer. If the conversion fails, raises the specified exception
        """
        try:
            return int(string)
        except ValueError:
            raise errorType()

    def removeStudent(self, studentId: str):
        """
        Removes a student from the repository
        """
        studentId = self.parseInt(studentId, InvalidStudentId)
        student = self.findStudent(studentId)
        del self.__students[student]

    def findStudent(self, studentId) -> Student:
        """
        Searches a student and returns it if found. Raises InvalidStudentId if not
        """
        studentId = self.parseInt(studentId, InvalidStudentId)
        if studentId not in [student.getStudentId() for student in self.__students]:
            raise InvalidStudentId
        else:
            return self.__students[studentId]

    def updateStudent(self, studentId, name: str, group: str):
        """
        Updates the student data
        """
        studentId = self.parseInt(studentId, InvalidStudentId)
        group = self.parseInt(group, InvalidStudentGroup)
        ValidationUtils.Student.validateStudent(Student(0, name, group))
        student = self.findStudent(studentId)
        student.setName(name)
        student.setGroup(group)

    # Manage Assignments Menu
    def listAssignments(self) -> List[Assignment]:
        """
        Returns a list of assignments sorted in ascending order by their IDs
        """
        return sorted([assignment for assignment in self.__assignments],
                      key=lambda assignment: assignment.getAssignmentId())

    def addAssignment(self, description: str, deadline: str) -> Assignment:
        """
        Adds a assignment to the repository
        """
        deadline = self.parseDate(deadline, InvalidAssignmentDeadline)
        assignment = Assignment(0, description, deadline)
        ValidationUtils.Assignment.validateAssignment(assignment)
        return self.__assignments.addAssignment(assignment)

    @staticmethod
    def parseDate(string: str, errorType: type) -> date:
        """
        Parses a string to a date. Valid format: day.month.year . If the conversion fails, raises the specified exception
        """
        try:
            symbols = string.split('.')
            if len(symbols) != 3:
                raise errorType()
            day = int(symbols[0])
            month = int(symbols[1])
            year = int(symbols[2])
            return date(year, month, day)
        except ValueError:
            raise errorType()

    def removeAssignment(self, assignmentId: str):
        """
        Removes an assignment from the repository
        """
        assignmentId = self.parseInt(assignmentId, InvalidAssignmentId)
        assignment = self.findAssignment(assignmentId)
        del self.__assignments[assignment]

    def findAssignment(self, assignmentId) -> Assignment:
        """
        Searches an assignment and returns it if found. Raises InvalidAssignmentId otherwise
        """
        assignmentId = self.parseInt(assignmentId, InvalidAssignmentId)
        if assignmentId not in [assignment.getAssignmentId() for assignment in self.__assignments]:
            raise InvalidAssignmentId
        else:
            return self.__assignments[assignmentId]

    def updateAssignment(self, assignmentId, description: str, deadline: str):
        """
        Updates the assignment data
        """
        assignmentId = self.parseInt(assignmentId, InvalidAssignmentId)
        deadline = self.parseDate(deadline, InvalidAssignmentDeadline)
        ValidationUtils.Assignment.validateAssignment(Assignment(0, description, deadline))
        assignment = self.findAssignment(assignmentId)
        assignment.setDescription(description)
        assignment.setDeadline(deadline)

    # Give assignments menu
    def assignToStudent(self, studentId, assignmentId):
        """
        Gives an assignment to a student
        """
        student = self.findStudent(studentId)
        assignment = self.findAssignment(assignmentId)
        try:
            self.__grades.assign(student, assignment)
        except KeyError:
            raise DuplicateAssignment

    def checkGroupExistence(self, group: str):
        """
        Checks if there are any students within the specified group
        """
        group = self.parseInt(group, InvalidStudentGroup)
        if group not in [student.getGroup() for student in self.__students]:
            raise InvalidStudentGroup

    def assignToGroup(self, group: str, assignmentId: str):
        """
        Gives an assignment to the specified group
        """
        group = self.parseInt(group, InvalidStudentGroup)
        groupStudents = [student for student in self.__students if student.getGroup() == group]
        for student in groupStudents:
            try:
                self.assignToStudent(student.getStudentId(), assignmentId)
            except DuplicateAssignment:
                pass


class ChangesStack:
    """
    The stack of changes committed to the repository
    """

    def __init__(self, changesHandler):
        self.__changesStack = []
        self.__changesHandler = changesHandler

    def beginCommit(self):
        pass

    def endCommit(self):
        pass

    def addChange(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass