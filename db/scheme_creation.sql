USE university;
CREATE TABLE Student (
	StudentID INT(10) PRIMARY KEY
	,YearStart INT(4) NOT NULL
	,YearEnd INT(4)
	);

CREATE TABLE Teacher (
	TeacherID INT(10) PRIMARY KEY
	,IsCurrent INT(1) NOT NULL CONSTRAINT check_IsCurrent CHECK (
		IsCurrent BETWEEN 0
			AND 1
		)
	);

CREATE TABLE Person (
	PersonID INT(10) PRIMARY KEY
	,FirstName VARCHAR(255) NOT NULL
	,LastName VARCHAR(255) NOT NULL
	,Gender CHAR(1) NOT NULL
	,DateOfBirth DATE
	);

CREATE TABLE Class (
	ClassID INT(10) PRIMARY KEY
	,TeacherID INT(10) NOT NULL
	,ClassName VARCHAR(255) NOT NULL
	,YearOffered INT(4) NOT NULL
	,TermOffered INT(1) NOT NULL CONSTRAINT check_TermOffered CHECK (
		TermOffered BETWEEN 1
			AND 2
		)
	,CONSTRAINT FK_Class_teacherID FOREIGN KEY (TeacherID) REFERENCES Teacher(TeacherID)
	);

CREATE TABLE Room (
	RoomID INT(10) PRIMARY KEY
	,RoomNum INT(4) NOT NULL
	,Floor INT(2) NOT NULL
	,Building VARCHAR(64) NOT NULL
	);

CREATE TABLE ClassStudent (
	ClassID INT(10) NOT NULL
	,StudentID INT(10) NOT NULL
	,FinalGrade INT(1) CONSTRAINT check_FinalGrade CHECK (
		FinalGrade BETWEEN 2
			AND 6
		)
	,CONSTRAINT PK_ClassStudent PRIMARY KEY (
		ClassID
		,StudentID
		)
	,CONSTRAINT FK_ClassStudent_classID FOREIGN KEY (ClassID) REFERENCES Class(ClassID)
	,CONSTRAINT FK_ClassStudent_studentID FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
	);

CREATE TABLE Schedule (
	ClassID INT(10) NOT NULL
	,RoomID INT(10) NOT NULL
	,FromTS VARCHAR(16) NOT NULL
	,ToTS VARCHAR(16) NOT NULL
	,CONSTRAINT PK_Schedule PRIMARY KEY (
		ClassID
		,RoomID
		,FromTS
		)
	,CONSTRAINT FK_Schedule_classID FOREIGN KEY (ClassID) REFERENCES Class(ClassID)
	,CONSTRAINT FK_Schedule_roomID FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
	);
    
