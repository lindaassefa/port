from langchain.chains.combine_documents import create_stuff_documents_chain
from pc_vector_store.context_retriever import history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from llms.chatgpt import llm

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
