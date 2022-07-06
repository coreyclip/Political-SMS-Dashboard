DROP TABLE sms_backup;
CREATE TABLE "sms_backup" (
	"SmsId"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"SenderPhoneNumber"	INTEGER,
	"Sender"	TEXT,
	"text"	TEXT,
	"timestamp"	TEXT,
	"month_name"	TEXT,
	"day_name"	TEXT,
  "month" INTEGER,
	"day"	INTEGER,
	"hour"	INTEGER,
	"weekday"	INTEGER,
	"week"	INTEGER,
	"year"	INTEGER,
	"polarity"	REAL,
	"subjectivity"	REAL,
	"negativity"	REAL,
	"neutrality"	REAL,
	"positivity"	REAL,
	"compound"	REAL,
	"nouns"	TEXT,
	"tags"	TEXT,
	"word_count"	INTEGER
)
;

INSERT INTO sms_backup 
SELECT * FROM sms;
