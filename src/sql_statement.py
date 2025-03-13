"""
File to write SQL statements for database creation and management.
All SQL statements are defined here for better organisation and maintainability.
"""

LIMIT_TIME_0 = 10
NUMBER_QUESTION_0 = 3

### DATABASE PATH AND NAME###
DB_PATH = "brainup.db"

### CREATES TABLES ###
CREATE_TABLE_PLAYERS = """
            CREATE TABLE IF NOT EXISTS players (
                "id_player" INTEGER PRIMARY KEY AUTOINCREMENT,
                "username" TEXT NOT NULL UNIQUE,
                "birthday" DATE NOT NULL
            );"""

CREATE_TABLE_SCORES = """
            CREATE TABLE IF NOT EXISTS scores (
                "id_score" INTEGER PRIMARY KEY AUTOINCREMENT,
                "id_player" INTEGER,
                "date_time" DATETIME DEFAULT CURRENT_TIMESTAMP,
                "age" INTEGER NOT NULL,
                "current_score" INTEGER DEFAULT 0,
                FOREIGN KEY (id_player) REFERENCES players(id_player) ON DELETE CASCADE
            );
            """
CREATE_TABLE_QUESTIONS = """
            CREATE TABLE IF NOT EXISTS questions (
                "id_question" INTEGER PRIMARY KEY AUTOINCREMENT,
                "category" TEXT NOT NULL,
                "question" TEXT NOT NULL,
                "option_1" TEXT NOT NULL,
                "option_2" TEXT NOT NULL,
                "option_3" TEXT NOT NULL,
                "option_4" TEXT NOT NULL,
                "correct_answer" INTEGER NOT NULL,
                "hint" TEXT NOT NULL
            );
            """
CREATE_SETUP = """
            CREATE TABLE IF NOT EXISTS setup (
                "time_limit" INTEGER,
                "num_questions" INTEGER
            );
            """

### CHECKS ###
CHECK_USERNAME = """
                SELECT * FROM players WHERE username = ? 
                """

CHECK_IF_QUESTION_EXISTS = """
                SELECT * FROM questions WHERE question = ? 
                """

### INSERTS ###
INSERT_PLAYER = """
                INSERT INTO players (username, birthday) VALUES (?, ?) 
                """

INSERT_SCORE = """
                INSERT INTO scores (id_player, age, current_score) VALUES (?, ?, ?) 
                """

INSERT_AGE_TO_SCORES = """
                INSERT INTO scores (id_player, age) VALUES (?, ?) 
                """

INSERT_QUESTIONS = """
                INSERT INTO questions (category, question, option_1, option_2, option_3, option_4, correct_answer, hint)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """

INSERT_SETUP = f"""
                INSERT INTO setup (time_limit, num_questions) 
                VALUES ({LIMIT_TIME_0}, {NUMBER_QUESTION_0}) """
                # deaful values for initial load

### SELECTS ###
SELECT_ALL_QUESTIONS = """
                SELECT * FROM questions
                """

SELECT_QUESTIONS_BY_CATEGORY = """
                SELECT * FROM questions WHERE category = ? 
                """

SELECT_PLAYER_BY_USERNAME = """
                SELECT * FROM players WHERE username = ? 
                """

SELECT_ALL_PLAYERS_WITH_AGE = """
                SELECT username, 
                   (strftime('%Y', 'now') - strftime('%Y', birthday)) - 
                   (strftime('%m-%d', 'now') < strftime('%m-%d', birthday)) AS age
                FROM 
                   players
                """
SELECT_RANKING = """
                SELECT p.username, s.age, s.date_time, s.current_score
                FROM players p
                JOIN scores s ON p.id_player = s.id_player
                ORDER BY s.current_score DESC, s.age ASC
                LIMIT 20
                """

SELECT_SETUP = """
                SELECT COUNT(*) FROM setup
               """

SELECT_SETUP2 = """
                SELECT * FROM setup
               """

SELECT_ID_QUESTIONS = """
                SELECT id_question FROM questions
                WHERE question = ?
                """

### UPDATES ###
UPDATE_SETUP = """
                UPDATE setup SET time_limit = ?, num_questions = ?
                """

### DELETES ###
DELETE_PLAYER = """
                DELETE FROM players WHERE username = ? 
                """

UPDATE_QUESTIONS = """
                UPDATE questions SET category = ?, question = ?, option_1 = ?, option_2 = ?, option_3 = ?, option_4 = ?, correct_answer = ?, hint = ?
                WHERE id_question = ?
                """

### CREATE EXECUTABLE FILE ### will create at the directory dist. Assure that questions.json file is in the same directory of executable
# pyinstaller --onefile --add-data "sounds;sounds" --name 'brainup' main.py
# pyinstaller --onefile --add-data "sounds/bonus.mp3;sounds" --add-data "sounds/tic-tac.wav;sounds" --add-data "sounds/buzz.mp3;sounds" --add-data "sounds/winner.wav;sounds" --name "brainup" main.py
# pyinstaller --name 'brainup' main.py

