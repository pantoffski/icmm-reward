#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import argparse
import sqlite3
import os
from db import UserDB

def main(args):
	# Read source
	if args.source_type == "excel":
		df = pd.read_excel(open(args.source,'rb'), sheet_name=args.sheet_name, encoding='utf-8')
	else:
		df = pd.read_csv(args.source)

	UserDB.connect(args.db_path)
	UserDB.initSchema()
	# Iterate data
	users = []
	for row in df.values:
		bibNumber = row[0]
		firstName = row[3]
		lastName = row[4]
		bibName = row[6]
		telNumber = row[7]
		raceCategory = row[9]
		challenge = row[10]
		try:
			UserDB.insertUser(firstName, lastName, bibName, challenge, raceCategory, telNumber, bibNumber)
		except Exception as e:
			print("Error %s: %s" % (str(e), bibNumber))
	UserDB.close()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("source", help="Path to csv or excel", action="store", type=str)
	parser.add_argument("db_path", help="Path to sqlite3 database ex. ./users.db", action="store", type=str)
	parser.add_argument("--source-type", help="Type of source (default is excel)", action="store",
						choices=["csv", "excel"], default="excel", dest="source_type", type=str)
	parser.add_argument("--sheet-name", help="Sheet name for excel (default is Sheet1)", action="store",
						default="Sheet1", dest="sheet_name", type=str)
	args = parser.parse_args()
	main(args)