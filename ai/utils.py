import os 
import openai
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def about_tasks()->str:
    tasks= """
    First task - SHOW:
        In this task usually people ask show or  order products.In this task you have to  run sql command Your response mustbe like this
        {
            'command':'SHOW',
            'reponse:sql response
        }
    Second task - ADD:
        In this task usually people ask add product to their basket.In this task you have to run sql command Your response mustbe like this
        {
            'command':'ADD',
            'reponse:sql response
        }
    Third task - OPEN:
        In this task usally people ask for you show their basket ,and bought products.In this task you haven't run sql command. You just return
        like this response {
            'command':'OPEN',
            'response':True
        } 
    Forth task - CLOSE_CART:
        In this task usually people ask close their basket, their cart. In this task you mustn't run sql command. You just return
        like this response {
            'command':'CLOSE',
            'response':False
        } 
    """
    return tasks


def get_sql_chain(db):
    template = """
    You are a sales asist  at a online E-commers website and you have greate data analys skils. You are interacting with a user who is asking you some help  about the shop's database.
    Based on the table schema below, write a SQL query that would answer the user's question.
    
    <SCHEMA>{schema}</SCHEMA>
   
    
    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
    
    For example:
    Question: show me all products
    SQL Query: SELECT * FROM products;
    Question: Order by price
    SQL Query: SELECT * FROM products ORDER BY price;
    Question: show me product number 12
    SQl Query: SELECT * FROM prodcuts WHERE id=12;
    Question: add product which product number 1 to my basket
    SQL Query: SELECT * FROM products WHERE product id=1;
    
    Your turn:
    
    Question: {question}
    SQL Query:
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    llm = ChatOpenAI(model="gpt-4-0125-preview")
  
    
    def get_schema(_):
        return db.get_table_info()
    
    return(
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )
    # return chain.invoke({'question':user_question})

def full_chain(user_query: str, db: SQLDatabase):
    sql_chain = get_sql_chain(db)
  
    template = """
    
    You are a sales asist  at a online E-commers website and you have greate data analys skils. You are interacting with a user who is asking you some help  about the shop's database.
    Based on the table schema below, question, sql query, and sql response, write a response. response must be json format and it has two element first task name and and response
    You can return only 4 kind of task . They are show , add prodct or open ,close card. More information about tasks here {tasks}

    
    <SCHEMA>{schema}</SCHEMA>

    SQL Query: <SQL>{query}</SQL>
    User question: {question}
    SQL Response: {response}"""
  
    prompt = ChatPromptTemplate.from_template(template)
    
    llm = ChatOpenAI(model="gpt-4-0125-preview")
    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
        schema=lambda _: db.get_table_info(),
        tasks= lambda _ : about_tasks(),
        response=lambda vars: db.run(vars["query"]),
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain.invoke({
        "question": user_query
    })
    