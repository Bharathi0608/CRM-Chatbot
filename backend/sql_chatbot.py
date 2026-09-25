# from database import db
# from langchain_groq import ChatGroq
# from dotenv import load_dotenv
# import os

# load_dotenv()

# # -----------------------------
# # Initialize LLM
# # -----------------------------

# llm = ChatGroq(
#     model="openai/gpt-oss-120b",
#     temperature=0,
#     api_key=os.getenv("GROQ_API_KEY")

# )


# # -----------------------------
# # Generate SQL
# # -----------------------------

# def generate_sql(question):

#     schema = db.get_table_info()

#     prompt = f"""
# You are an expert PostgreSQL SQL developer.

# You are working with a CRM database.

# Database schema:

# {schema}

# User question:

# {question}

# Generate a PostgreSQL SQL query that answers the user's question.

# Rules:

# 1. Only use tables and columns present in the schema.
# 2. Never invent columns.
# 3. Only generate SELECT queries.
# 4. Do not generate INSERT, UPDATE, DELETE, DROP,
#    ALTER, TRUNCATE or CREATE queries.
# 5. Use PostgreSQL syntax.
# 6. Return ONLY the SQL query.
# 7. Do not explain the query.
# 8. If the user asks for the highest value,
#    use ORDER BY DESC and LIMIT 1.
# 9. If the user asks for the lowest value,
#    use ORDER BY ASC and LIMIT 1.
# 10. For counting records, use COUNT().
# 11. For totals, use SUM().
# 12. For averages, use AVG().
# 13. For categories, use GROUP BY.

# SQL:
# """

#     response = llm.invoke(prompt)

#     sql = response.content.strip()

#     # Remove markdown code blocks
#     sql = sql.replace("```sql", "")
#     sql = sql.replace("```", "")

#     return sql.strip()


# # -----------------------------
# # Execute SQL
# # -----------------------------

# def execute_sql(sql):

#     return db.run(sql)


# # -----------------------------
# # Test chatbot
# # -----------------------------

# if __name__ == "__main__":

#     print("\n===================================")
#     print("       CRM SQL AI CHATBOT")
#     print("===================================")

#     while True:

#         question = input("\nAsk a question: ")

#         if question.lower() in ["exit", "quit"]:

#             print("Goodbye!")
#             break

#         try:

#             sql = generate_sql(question)

#             print("\nGenerated SQL:")
#             print(sql)

#             result = execute_sql(sql)

#             print("\nDatabase Result:")
#             print(result)

#         except Exception as e:

#             print("\nError:")
#             print(e)

from database import db
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from .env file")


# ============================================================
# INITIALIZE LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=GROQ_API_KEY
)


# ============================================================
# GENERATE SQL
# ============================================================

def generate_sql(question):

    schema = db.get_table_info()

    prompt = f"""
You are an expert PostgreSQL SQL developer.

You are working with a CRM database.

DATABASE SCHEMA:

{schema}


USER QUESTION:

{question}


YOUR TASK:

Generate a PostgreSQL SQL query that answers the user's question.


RULES:

1. Only use tables and columns that exist in the database schema.
2. Never invent table names or column names.
3. Only generate SELECT queries.
4. Never generate INSERT queries.
5. Never generate UPDATE queries.
6. Never generate DELETE queries.
7. Never generate DROP queries.
8. Never generate ALTER queries.
9. Never generate TRUNCATE queries.
10. Never generate CREATE queries.
11. Use valid PostgreSQL syntax.
12. If the user asks for the highest value, use ORDER BY DESC.
13. If the user asks for the lowest value, use ORDER BY ASC.
14. If the user asks for the top results, use LIMIT.
15. For counting records, use COUNT().
16. For totals, use SUM().
17. For averages, use AVG().
18. For categories, use GROUP BY.
19. Return ONLY the SQL query.
20. Do not explain the SQL query.
21. Do not use markdown code blocks.


SQL QUERY:
"""

    response = llm.invoke(prompt)

    sql = response.content.strip()

    # Remove accidental markdown formatting
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")

    return sql.strip()


# ============================================================
# SQL SECURITY VALIDATION
# ============================================================

def validate_sql(sql):

    sql_upper = sql.upper().strip()

    # Only SELECT statements are allowed
    if not sql_upper.startswith("SELECT"):
        raise ValueError(
            "Unsafe SQL query rejected. Only SELECT queries are allowed."
        )

    # Dangerous SQL keywords
    forbidden_keywords = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "GRANT",
        "REVOKE",
        "EXEC",
        "EXECUTE"
    ]

    for keyword in forbidden_keywords:

        if keyword in sql_upper:
            raise ValueError(
                f"Unsafe SQL detected: {keyword}"
            )

    return True


# ============================================================
# EXECUTE SQL
# ============================================================

def execute_sql(sql):

    # Validate before executing
    validate_sql(sql)

    result = db.run(sql)

    return result


# ============================================================
# GENERATE NATURAL LANGUAGE ANSWER
# ============================================================

def generate_answer(question, sql, result):

    prompt = f"""
You are a CRM data analyst.

USER QUESTION:

{question}


SQL QUERY USED:

{sql}


DATABASE RESULT:

{result}


TASK:

Give the user a clear and concise natural-language answer.

RULES:

1. Use ONLY the information contained in the database result.
2. Do not invent any information.
3. Do not generate another SQL query.
4. Do not mention internal implementation details.
5. Explain numbers clearly.
6. If multiple rows are returned, you MUST summarize them using a properly formatted Markdown Table (with columns and rows).
7. Keep the answer easy to understand.
"""

    response = llm.invoke(prompt)

    return response.content.strip()


# ============================================================
# COMPLETE CRM QUESTION FLOW
# ============================================================

def ask_crm(question):

    # Step 1: Generate SQL
    sql = generate_sql(question)

    # Step 2: Validate + Execute SQL
    result = execute_sql(sql)

    # Step 3: Convert result into natural language
    answer = generate_answer(
        question,
        sql,
        result
    )

    return {
        "question": question,
        "sql": sql,
        "result": result,
        "answer": answer
    }


# ============================================================
# TERMINAL CHATBOT
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 60)
    print("              CRM SQL AI CHATBOT")
    print("=" * 60)

    print("\nConnected to CRM database.")
    print("Table: accounts")
    print("Records: 85")

    print("\nYou can ask questions about the CRM data.")
    print("Type 'exit' or 'quit' to stop.")

    while True:

        question = input("\nAsk a question: ").strip()

        # Exit
        if question.lower() in ["exit", "quit"]:

            print("\nGoodbye!")
            break

        # Empty question
        if not question:

            print("Please enter a question.")
            continue

        try:

            # Complete AI pipeline
            response = ask_crm(question)

            # Display question
            print("\n" + "-" * 60)
            print("QUESTION")
            print("-" * 60)

            print(response["question"])


            # Display generated SQL
            print("\n" + "-" * 60)
            print("GENERATED SQL")
            print("-" * 60)

            print(response["sql"])


            # Display database result
            print("\n" + "-" * 60)
            print("DATABASE RESULT")
            print("-" * 60)

            print(response["result"])


            # Display natural language answer
            print("\n" + "-" * 60)
            print("AI ANSWER")
            print("-" * 60)

            print(response["answer"])

            print("\n" + "=" * 60)

        except Exception as e:

            print("\n" + "-" * 60)
            print("ERROR")
            print("-" * 60)

            print(str(e))

            print("\nPlease try another question.")