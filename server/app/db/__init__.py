""" Create DB Connection """
import peewee as pw

DB = pw.MySQLDatabase("stalky", host="db", port=3306, user="stalky", passwd="stalky", charset='utf8mb4', use_speedups=False)

# to be able to store emojis in the database:
DB.execute_sql("ALTER DATABASE stalky DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci")
