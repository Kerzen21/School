BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS `Students` (
	`studentid`	INTEGER,
	`firstname`	TEXT,
	`lastname`	TEXT,
	`email`	TEXT,
	`birth_year`	INTEGER,
	PRIMARY KEY(`studentid`)
);

CREATE TABLE IF NOT EXISTS `Subjects` (
	`subjectid`	INTEGER,
	`teacherid`	INTEGER,
	`title`	TEXT,
	`coef`	INTEGER,
	PRIMARY KEY(`subjectid`),
	FOREIGN KEY(teacherid) REFERENCES Teachers(teacherid) ON DELETE SET NULL
	FOREIGN KEY(teacherid) REFERENCES Teachers(teacherid) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `Grades` (
	`gradeid` INTEGER,
	`subjectid`	INTEGER,
	`studentid`	INTEGER,
	`grade`	INTEGER,
	PRIMARY KEY(`gradeid`),
	FOREIGN KEY (studentid) REFERENCES Students(studentid) ON DELETE CASCADE,
	FOREIGN KEY (subjectid) REFERENCES Subjects(subjectid) ON DELETE CASCADE,
	FOREIGN KEY (studentid) REFERENCES Students(studentid) ON UPDATE CASCADE,
	FOREIGN KEY (subjectid) REFERENCES Subjects(subjectid) ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS `Teachers` (
	`teacherid`	INTEGER,
	`name` TEXT,
	PRIMARY KEY(`teacherid`)
);


COMMIT;
#LF will be replaced by CRLF in school.sql.
#The file will have its original line endings in your working directory