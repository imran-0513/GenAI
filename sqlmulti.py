# ###### inserting multiple values

# data = [
#     ('Darius', 'Data Science', 'A', 86),
#     ('Vikash', 'DEVOPS', 'A', 50),
#     ('Dipesh', 'DEVOPS', 'A', 35),
#     ('Alice', 'Machine Learning', 'B', 78),
#     ('Bob', 'Data Science', 'A', 92),
#     ('Charlie', 'Data Science', 'B', 88),
#     ('David', 'Machine Learning', 'A', 95),
#     ('Eva', 'DEVOPS', 'A', 42),
#     ('Frank', 'Machine Learning', 'B', 70),
#     ('Grace', 'DEVOPS', 'A', 55),
#     ('Hank', 'Data Science', 'A', 89),
#     ('Ivy', 'Machine Learning', 'A', 94),
#     ('Jack', 'DEVOPS', 'A', 60),
#     ('Kelly', 'Data Science', 'B', 77),
#     ('Leo', 'DEVOPS', 'B', 48),
#     ('Mia', 'Data Science', 'A', 91),
#     ('Nora', 'Machine Learning', 'A', 96),
#     ('Oscar', 'DEVOPS', 'B', 38),
#     ('Pam', 'Machine Learning', 'A', 85),
#     ('Quinn', 'Data Science', 'B', 79),
#     ('Rick', 'DEVOPS', 'A', 46),
#     ('Samantha', 'Data Science', 'A', 93),
#     ('Tom', 'Machine Learning', 'A', 97),
#     ('Uma', 'DEVOPS', 'B', 40),
#     ('Vincent', 'Data Science', 'A', 87),
#     ('Wendy', 'Machine Learning', 'A', 98),
#     ('Xander', 'DEVOPS', 'A', 53),
#     ('Yara', 'Data Science', 'B', 76),
#     ('Zane', 'Machine Learning', 'A', 99),
#     ('Ava', 'Data Science', 'A', 84),
#     ('Bryan', 'DEVOPS', 'B', 58),
#     ('Cara', 'Data Science', 'A', 82),
#     ('Derek', 'Machine Learning', 'A', 89),
#     ('Emma', 'DEVOPS', 'A', 44),
#     ('Finn', 'Machine Learning', 'B', 67),
#     ('Gina', 'DEVOPS', 'A', 51),
#     ('Henry', 'Data Science', 'A', 90),
#     ('Iris', 'Machine Learning', 'B', 73),
#     ('Jake', 'Data Science', 'A', 83),
#     ('Kylie', 'DEVOPS', 'A', 49),
#     ('Liam', 'Machine Learning', 'B', 65),
#     ('Megan', 'DEVOPS', 'B', 36),
#     ('Noah', 'Machine Learning', 'A', 92),
#     ('Olivia', 'Data Science', 'A', 88)
# ]

# for record in data:
#     cursor.execute('''
#         INSERT INTO student (name, field_of_study, grade, score)
#         VALUES ('Darius', 'Data Science', 'A', 86),
#         ('Vikash', 'DEVOPS', 'A', 50),
#         ('Dipesh', 'DEVOPS', 'A', 35),
#         ('Alice', 'Machine Learning', 'B', 78),
#         ('Bob', 'Data Science', 'A', 92),
#         ('Charlie', 'Data Science', 'B', 88),
#         ('David', 'Machine Learning', 'A', 95),
#         ('Eva', 'DEVOPS', 'A', 42),
#         ('Frank', 'Machine Learning', 'B', 70),
#         ('Grace', 'DEVOPS', 'A', 55),
#         ('Hank', 'Data Science', 'A', 89),
#         ('Ivy', 'Machine Learning', 'A', 94),
#         ('Jack', 'DEVOPS', 'A', 60),
#         ('Kelly', 'Data Science', 'B', 77),
#         ('Leo', 'DEVOPS', 'B', 48),
#         ('Mia', 'Data Science', 'A', 91),
#         ('Nora', 'Machine Learning', 'A', 96),
#         ('Oscar', 'DEVOPS', 'B', 38),
#         ('Pam', 'Machine Learning', 'A', 85),
#         ('Quinn', 'Data Science', 'B', 79),
#         ('Rick', 'DEVOPS', 'A', 46),
#         ('Samantha', 'Data Science', 'A', 93),
#         ('Tom', 'Machine Learning', 'A', 97),
#         ('Uma', 'DEVOPS', 'B', 40),
#         ('Vincent', 'Data Science', 'A', 87),
#         ('Wendy', 'Machine Learning', 'A', 98),
#         ('Xander', 'DEVOPS', 'A', 53),
#         ('Yara', 'Data Science', 'B', 76),
#         ('Zane', 'Machine Learning', 'A', 99),
#         ('Ava', 'Data Science', 'A', 84),
#         ('Bryan', 'DEVOPS', 'B', 58),
#         ('Cara', 'Data Science', 'A', 82),
#         ('Derek', 'Machine Learning', 'A', 89),
#         ('Emma', 'DEVOPS', 'A', 44),
#         ('Finn', 'Machine Learning', 'B', 67),
#         ('Gina', 'DEVOPS', 'A', 51),
#         ('Henry', 'Data Science', 'A', 90),
#         ('Iris', 'Machine Learning', 'B', 73),
#         ('Jake', 'Data Science', 'A', 83),
#         ('Kylie', 'DEVOPS', 'A', 49),
#         ('Liam', 'Machine Learning', 'B', 65),
#         ('Megan', 'DEVOPS', 'B', 36),
#         ('Noah', 'Machine Learning', 'A', 92),
#         ('Olivia', 'Data Science', 'A', 88)
#     ''', record)

#     ##### execute the query with multiple sets

#     cursor.executemany(query,data)
