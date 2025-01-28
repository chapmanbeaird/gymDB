This gym database tracks key information about a gym and its members such as, each member's phone number, type of membership, class attendance, etc. 


create_db.py - this file when run will create the sqlite database from the database setup in setup.sql and the data inserted into the database from insert_data.sql

db_bot.py - this file when run first gets the schema of the db we are working with. It then will send the schema and predefined questions to openai for the LLM to generate a sql query that gets the information in the question. It then runs the sql query against the database and gets the output from that. It then sends that output data back to the LLM so it can explain the result of the sql query in natural language. For each question asked, it is run three times with the following methods, zero-shot, single-domain few-shot, and cross-domain few-shot. These can be read more about at the following link:  https://arxiv.org/abs/2305.11853 . I noticed that each prompting strategy worked well with each outputting the same data for each question. This is likely due to the simple nature of the database we are using. If the database were more complex, I would imagine that single - domain few-shot would outperform due to the relevance of the examples to the database. 

schema.png - an outline of the schema specificied in setup.sql

results.json - the output of the program when db_bot.py is run. This shows the question, the sql query generated, the data returned from that query, and the final answer from the LLM. 