import sqlite3
conn = sqlite3.connect('app.db')
#conn = sqlite3.connect(':memory:')

c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")
# projects table
c.execute('''CREATE TABLE Projects
                (   id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_name TEXT NOT NULL UNIQUE,
                    video_path TEXT NOT NULL,
                    analysed_frames INTEGER DEFAULT 0,
                    total_frames INTEGER DEFAULT 0,
                    fps INTEGER DEFAULT 30,
                    face_recog INTEGER DEFAULT 1
                )''')
conn.commit()

# Comparison Images
c.execute('''CREATE TABLE Comparison_Images
                (   project_id TEXT NOT NULL,
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_name TEXT NOT NULL UNIQUE,
                    image_path TEXT NOT NULL,
                    encoding BLOB NOT NULL,
                    FOREIGN KEY(project_id) REFERENCES Projects(id) ON DELETE CASCADE
                )''')
conn.commit()

# Face recog data
c.execute('''CREATE TABLE Face_Recog_Data
                (   project_id INTEGER NOT NULL,
                    person_id INTEGER NOT NULL,
                    frame_number INTEGER NOT NULL,
                    analysed INTEGER NOT NULL,
                    face_distance REAL NOT NULL,
                    x1 INTEGER NOT NULL,
                    y1 INTEGER NOT NULL,
                    x2 INTEGER NOT NULL,
                    y2 INTEGER NOT NULL,
                    FOREIGN KEY(project_id) REFERENCES Projects(id) ON DELETE CASCADE
                    FOREIGN KEY(person_id) REFERENCES Comparison_Images(id) ON DELETE CASCADE
                )''')

conn.commit()

# color bar data
c.execute('''CREATE TABLE Color_Bar
                (   project_id INTEGER NOT NULL,
                    image_id INTEGER NOT NULL,
                    number INTEGER NOT NULL,
                    face_distance REAL NOT NULL,
                    FOREIGN KEY(project_id) REFERENCES Projects(id) ON DELETE CASCADE
                    FOREIGN KEY(image_id) REFERENCES Comparison_Images(id) ON DELETE CASCADE
                )''')

conn.commit()

# Table for all flags
c.execute('''CREATE TABLE Flags
                (   flag_name TEXT NOT NULL UNIQUE,
                    value TEXT NOT NULL UNIQUE
                )''')

# settings rquired flags
c.execute("INSERT INTO Flags(flag_name, value) VALUES ('current_project', 'None')")
c.execute("INSERT INTO Flags(flag_name, value) VALUES ('analysing', 'false')")

conn.commit()

#test lines below to pupulate fake data uncomment to check

# c.execute("INSERT INTO Projects(project_name, video_path) VALUES ('test video name1', './this/is/a/test/path.tst')")

# c.execute("INSERT INTO Comparison_Images(project_id, image_name, image_path) VALUES (1, 'john', './test/path.tst')")
# c.execute("INSERT INTO Comparison_Images(project_id, image_name, image_path) VALUES (1, 'doe', './test/path.tst')")

# c.execute("SELECT id FROM Projects WHERE project_name='test video name1'")
# project_id = c.fetchone()[0]
# c.execute("SELECT id FROM Comparison_Images WHERE image_name='doe'")
# person_id = c.fetchone()[0]
# c.execute(f"INSERT INTO Face_Recog_Data(project_id, person_id, frame_number, face_distance, x1, y1, x2, y2) VALUES ({project_id}, {person_id}, 1, 0.3, 200, 400, 350, 560)")
# c.execute(f"INSERT INTO Face_Recog_Data(project_id, person_id, frame_number, face_distance, x1, y1, x2, y2) VALUES ({project_id}, {person_id}, 2, 0.3, 200, 400, 350, 560)")
# c.execute(f"INSERT INTO Face_Recog_Data(project_id, person_id, frame_number, face_distance, x1, y1, x2, y2) VALUES ({project_id}, {person_id}, 3, 0.3, 200, 400, 350, 560)")

# c.execute("SELECT id FROM Projects WHERE project_name='test video name1'")
# project_id = c.fetchone()[0]
# c.execute("SELECT id FROM Comparison_Images WHERE image_name='doe'")
# person_id = c.fetchone()[0]
# c.execute(f"INSERT INTO Face_Recog_Data(project_id, person_id, frame_number, face_distance, x1, y1, x2, y2) VALUES ({project_id}, {person_id}, 50, 0.3, 200, 400, 350, 560)")
# c.execute(f"INSERT INTO Face_Recog_Data(project_id, person_id, frame_number, face_distance, x1, y1, x2, y2) VALUES ({project_id}, {person_id}, 100, 0.3, 200, 400, 350, 560)")
# c.execute(f"INSERT INTO Face_Recog_Data(project_id, person_id, frame_number, face_distance, x1, y1, x2, y2) VALUES ({project_id}, {person_id}, 450, 0.3, 200, 400, 350, 560)")

# conn.commit()

# for row in c.execute("SELECT * FROM Projects"):
#     print("testing")
#     print(row)
# c.execute("SELECT id FROM Comparison_Images WHERE image_name='doe'")
# person_id = c.fetchone()[0]
# for row in c.execute(f"SELECT * FROM Face_Recog_Data WHERE person_id={person_id}"):
#     print("testing")
#     print(row)

# c.execute("SELECT x1, y1, x2, y2 FROM Face_Recog_Data WHERE person_id=2")
# print(c.fetchall())

# for row in c.execute("SELECT * FROM Comparison_Images"):
#     print("testing")
#     print(row)

# c.execute("UPDATE Face_Recog_Data SET x1 = 100 WHERE person_id = 2 AND frame_number = 50")

# c.execute("SELECT x1, y1, x2, y2 FROM Face_Recog_Data WHERE person_id=2")
# print(c.fetchall())


# c.execute("UPDATE Comparison_Images SET image_name = 'lee' WHERE image_name = 'doe'")

# for row in c.execute("SELECT * FROM Comparison_Images"):
#     print("testing")
#     print(row)

# conn.commit()
conn.close()