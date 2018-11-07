from datetime import date
from unittest import TestCase
from repository import Repository
from logic import LogicComponent
from validation import InvalidStudentGroup, InvalidAssignmentDeadline


class TestLogicComponent(TestCase):

    def setUp(self):
        self.repository = Repository()
        self.logicComponent = LogicComponent(self.repository)

    def test_handleChanges(self):
        pass

    def test_populateRepository(self):
        self.logicComponent.populateRepository()
        assert len(self.logicComponent.listStudents()) != 0
        # assert len(self.logicComponent.listAssignments()) != 0
        repository = Repository()
        self.logicComponent = LogicComponent(repository)

    def testAddStudent(self):
        student = self.logicComponent.addStudent('Ricky', '7')
        assert student.getName() == 'Ricky'
        assert student.getGroup() == 7
        self.assertRaises(InvalidStudentGroup, self.logicComponent.addStudent, 'Ricky', -8)

    def testParseInt(self):
        assert self.logicComponent.parseInt('8', TypeError) == 8
        self.assertRaises(TypeError, self.logicComponent.parseInt, 'blah', TypeError)

    def testRemoveStudent(self):
        oldLength = len(self.logicComponent.listStudents())
        student = self.logicComponent.addStudent('Ricky', '7')
        self.logicComponent.removeStudent(str(student.getStudentId()))
        assert len(self.logicComponent.listStudents()) == oldLength

    def testFindStudent(self):
        student = self.logicComponent.addStudent('Ricky', '7')
        studentId = student.getStudentId()
        assert self.logicComponent.findStudent(studentId).getName() == 'Ricky'
        assert self.logicComponent.findStudent(studentId).getGroup() == 7

    def testUpdateStudent(self):
        student = self.logicComponent.addStudent('Ricky', '7')
        studentId = student.getStudentId()
        self.logicComponent.updateStudent(studentId, 'Andy', '11')
        assert self.logicComponent.findStudent(studentId).getName() == 'Andy'
        assert self.logicComponent.findStudent(studentId).getGroup() == 11

    def testAddAssignment(self):
        assignment = self.logicComponent.addAssignment('Project', '2.10.2018')
        assert assignment.getDescription() == 'Project'
        assert assignment.getDeadline() == date(2018, 10, 2)
        self.assertRaises(InvalidAssignmentDeadline, self.logicComponent.addAssignment, 'Project', "-9")

    def testParseDate(self):
        assert self.logicComponent.parseDate('2.10.2018', TypeError) == date(2018, 10, 2)
        self.assertRaises(TypeError, self.logicComponent.parseDate, '8', TypeError)

    def testRemoveAssignment(self):
        oldLength = len(self.logicComponent.listAssignments())
        assignment = self.logicComponent.addAssignment('Project', '2.10.2018')
        self.logicComponent.removeAssignment(str(assignment.getAssignmentId()))
        assert len(self.logicComponent.listAssignments()) == oldLength

    def testFindAssignment(self):
        assignment = self.logicComponent.addAssignment('Project', '2.10.2018')
        assignmentId = assignment.getAssignmentId()
        assert self.logicComponent.findAssignment(assignmentId).getDescription() == 'Project'
        assert self.logicComponent.findAssignment(assignmentId).getDeadline() == date(2018, 10, 2)

    def testUpdateAssignment(self):
        assignment = self.logicComponent.addAssignment('Project', '2.10.2018')
        assignmentId = assignment.getAssignmentId()
        self.logicComponent.updateAssignment(assignmentId, 'Project 2', '2.11.2018')
        assert self.logicComponent.findAssignment(assignmentId).getDescription() == 'Project 2'
        assert self.logicComponent.findAssignment(assignmentId).getDeadline() == date(2018, 11, 2)

    def testAssignToStudent(self):
        student = self.logicComponent.addStudent('Ricky', '7')
        assignment = self.logicComponent.addAssignment('Project', '2.10.2018')
        assert len(self.repository.getGrades().getStudentGrades(student)) == 0
        assert len(self.repository.getGrades().getAssignmentGrades(assignment)) == 0
        self.logicComponent.assignToStudent(student.getStudentId(), assignment.getAssignmentId())
        assert len(self.repository.getGrades().getStudentGrades(student)) == 1
        assert len(self.repository.getGrades().getAssignmentGrades(assignment)) == 1
        assert self.repository.getGrades()[student.getStudentId(), assignment.getAssignmentId()] is not None

    def testCheckGroupExistence(self):
        group = 0
        while group in [student.getGroup() for student in self.repository.getStudents()]:
            group += 1
        self.logicComponent.addStudent('Ricky', group)
        self.logicComponent.checkGroupExistence(group)
        while group in [student.getGroup() for student in self.repository.getStudents()]:
            group += 1
        self.assertRaises(InvalidStudentGroup, self.logicComponent.checkGroupExistence, group)

    def testAssignToGroup(self):
        group = 0
        while group in [student.getGroup() for student in self.repository.getStudents()]:
            group += 1
        student1 = self.logicComponent.addStudent('Ricky', group)
        student2 = self.logicComponent.addStudent('Alfred', group)
        student3 = self.logicComponent.addStudent('Alex', group)
        assignment = self.logicComponent.addAssignment('Project', '2.10.2018')
        self.logicComponent.assignToStudent(student1.getStudentId(), assignment.getAssignmentId())
        self.logicComponent.assignToGroup(group, assignment.getAssignmentId())
        assert self.repository.getGrades()[student1.getStudentId(), assignment.getAssignmentId()] is not None
        assert self.repository.getGrades()[student2.getStudentId(), assignment.getAssignmentId()] is not None
        assert self.repository.getGrades()[student3.getStudentId(), assignment.getAssignmentId()] is not None