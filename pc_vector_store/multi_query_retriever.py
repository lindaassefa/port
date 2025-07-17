from typing import List
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from llms.chatgpt import llm
from pc_vector_store.retriever import retriever

# Output parser
class LineListOutputParser(BaseOutputParser[List[str]]):
    """Output parser for a list of lines."""

    def parse(self, text: str) -> List[str]:
        lines = text.strip().split("\n")
        return [line.strip() for line in lines if line.strip()]

# Prompt template
query_prompt = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant. Your task is to generate five 
    different versions of the given user question to retrieve relevant documents from a vector 
    database. By generating multiple perspectives on the user question, your goal is to help
    the user overcome some of the limitations of the distance-based similarity search. 
    Provide these alternative questions separated by newlines.
    Original question: {question}""",
)

output_parser = LineListOutputParser()
multi_query_chain = query_prompt | llm | output_parser

# result = multi_query_chain.invoke(
#     {"question": "What is Dr.Visa's research"},
# )

# print(result)

# Initialize the multi-query retriever
multi_query_retriever = MultiQueryRetriever(
    retriever=retriever, llm_chain=multi_query_chain, parser_key="lines"
)  