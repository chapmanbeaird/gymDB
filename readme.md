create_db.py - this file when run will create the sqlite database from the database setup in setup.sql and the data inserted into the database from insert_data.sql

db_bot.py - this file when run first gets the schema of the db we are working with. It then will send the schema and predefined questions to openai for the LLM to generate a sql query that gets the information in the question. It then runs the sql query against the database and gets the output from that. It then sends that output data back to the LLM so it can explain the result of the sql query in natural language. 

schema.png - an outline of the schema specificied in setup.sql

results.json - the output of the program when db_bot.py is run