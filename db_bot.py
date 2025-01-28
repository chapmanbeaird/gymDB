import os
import sqlite3
import openai
import json

# Load OpenAI credentials
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

DB_PATH = os.path.join(os.path.dirname(__file__), "gym.db")



def get_schema():
    setup_sql_path = os.path.join(os.path.dirname(__file__), "setup.sql")
    with open(setup_sql_path, "r") as f:
        schema = f.read()
    return schema



def generate_sql_from_gpt(user_question, schema, strategy, examples=None):
    
    base_system_prompt = (
        "You are an expert SQL assistant. "
        "You are given the schema of a SQLite database. "
        "Given a user question, you must produce a valid SQL query that answers it. "
        "Only use the tables/columns that appear in the schema. "
        f"Schema:\n\n{schema}\n"
    )

    if strategy == "Zero-shot":
        messages = [
            {"role": "system", "content": base_system_prompt},
            {"role": "user", "content": f"The user asked: {user_question}\n\nReturn ONLY the SQL query that answers the question."}
        ]
    elif strategy == "Single-domain Few-shot" and examples:
        example_prompts = "\n".join(
            f"Q: {ex['question']}\nA: {ex['sql']}" for ex in examples
        )
        messages = [
            {"role": "system", "content": base_system_prompt + f"Examples:\n{example_prompts}\n"},
            {"role": "user", "content": f"The user asked: {user_question}\n\nReturn ONLY the SQL query that answers the question."}
        ]
    elif strategy == "Cross-domain Few-shot" and examples:
        example_prompts = "\n".join(
            f"Q: {ex['question']}\nA: {ex['sql']}" for ex in examples
        )
        messages = [
            {"role": "system", "content": base_system_prompt + "The examples are from a different database:\n\n" + example_prompts},
            {"role": "user", "content": f"The user asked: {user_question}\n\nReturn ONLY the SQL query that answers the question."}
        ]
    else:
        raise ValueError("Invalid strategy or missing examples for few-shot setting.")

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.0
    )

    sql_query = response.choices[0].message.content.strip()
    return getJustSql(sql_query)



def getJustSql(value):
    gptStartSqlMarker = "```sql"
    gptEndSqlMarker = "```"
    if gptStartSqlMarker in value:
        value = value.split(gptStartSqlMarker)[1]
    if gptEndSqlMarker in value:
        value = value.split(gptEndSqlMarker)[0]

    return value



def run_sql_query(sql_query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        conn.commit()
    except Exception as e:
        rows = [("ERROR", str(e))]
    finally:
        conn.close()

    return rows




def convert_data_to_natural_language(user_question, sql_query, results):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who can interpret SQL results and explain them."
        },
        {
            "role": "user",
            "content": (
                f"User Question: {user_question}\n\n"
                f"SQL Query: {sql_query}\n\n"
                f"Results: {results}\n\n"
                "Please summarize these results in plain English."
            )
        }
    ]

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2
    )

    answer = response.choices[0].message.content.strip()
    return answer

def main():
    schema = get_schema()
    
    # Few-shot examples for single-domain and cross-domain
    single_domain_examples = [
        {"question": "What are the names of all gym members?", "sql": "SELECT name FROM members;"},
        {"question": "When did Alice Johnson join the gym?", "sql": "SELECT join_date FROM members WHERE name = 'Alice Johnson';"}
    ]

    cross_domain_examples = [
        {"question": "What is the title of the book?", "sql": "SELECT title FROM books;"},
        {"question": "Who is the author of '1984'?", "sql": "SELECT author FROM books WHERE title = '1984';"}
    ]
    
    questions = [
        "What are the names of all gym members?", 
        "When did Alice Johnson join the gym?", 
        "Which members can receive SMS messages?",
        "Which members attended more than one class and what are the names of the classes they attended?",
        "What is the total revenue generated from memberships for each plan, and how many members are currently subscribed to each plan?"
    ]

    strategies = ["Zero-shot", "Single-domain Few-shot", "Cross-domain Few-shot"]

    results = []

    for question in questions:
        for strategy in strategies:
            print(f"\n=== Strategy: {strategy} ===")
            if strategy == "Single-domain Few-shot":
                examples = single_domain_examples
            elif strategy == "Cross-domain Few-shot":
                examples = cross_domain_examples
            else:
                examples = None
            
            sql_query = generate_sql_from_gpt(question, schema, strategy, examples)
            query_results = run_sql_query(sql_query)
            final_answer = convert_data_to_natural_language(question, sql_query, query_results)

            # Save result in the list
            results.append({
                "question": question,
                "strategy": strategy,
                "sql_query": sql_query,
                "query_results": query_results,
                "final_answer": final_answer
            })

    # Save results to JSON file
    output_path = os.path.join(os.path.dirname(__file__), "results.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    main()
