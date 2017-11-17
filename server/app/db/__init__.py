""" Create DB Connection """
import peewee as pw

DB = pw.MySQLDatabase("stalky", host="db", port=3306, user="stalky", passwd="stalky", charset='utf8mb4', use_speedups=False)