from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class TicketSearchEngine:

    def __init__(self, excel_file="data/historical_tickets.xlsx"):
        self.df = pd.read_excel(excel_file)
        print(f"Loaded {len(self.df)} historical tickets")

        self.chroma_client = chromadb.Client()
        self._initialize_db_and_collection()
        self._index_tickets()


    def _initialize_db_and_collection(self): 
        """ Initializes the chromadb and collection"""
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key = os.getenv("OPENAI_API_KEY"),
                model_name = "text-embedding-3-small"
        )
        
        self.collection = self.chroma_client.get_or_create_collection(
                name="support_ticketS",
                embedding_function = openai_ef
        )

    def _index_tickets(self):
        """ Converts all tickets into searchable vectors """
        try:
            self.chroma_client.delete_collection("support_tickets")
            self._initialize_db_and_collection()
        except:
            pass

        for idx, row in self.df.iterrows():
            self.collection.add(
                    documents = [row['issue']],
                    metadatas = [{
                        "ticket_id": row['ticket_id'],
                        "category": row['category'],
                        "solution": row['solution']
                    }],
                    ids=[row['ticket_id']]
            )
        print(f"Indexed {len(self.df)} tickets for semantic search")

    def search_similar_tickets(self, query, top_k=3):
        """ Finds similar tickets based on issue description """
        
        results = self.collection.query(
                query_texts = [query],
                n_results = top_k
        )

        similar_tickets = []

        for i in range(len(results['ids'][0])):
            ticket = {
                'ticket_id': results['ids'][0][i],
                'issue': results['documents'][0][i],
                'category': results['metadatas'][0][i]['category'],
                'solution': results['metadatas'][0][i]['solution'],
                'similarity_score': 1 - results['distances'][0][i]  # Convert distance to similarity
            }

        return similar_tickets


if __name__ == "__main__":
    print("Initializing TicketSearchEngine ...\n")
    search_engine = TicketSearchEngine()

    print("="*70)
    print("TEST1: New Ticket about login problems")
    print("="*70)

    new_issue = "User can't sign into their account, error message shows authentication failed"

    print(f"\nNew Issue: {new_issue}\n")
    print("Finding similar past tickets...\n")

    results = search_engine.search_similar_tickets(new_issue, top_k=3)

    for i, ticket in enumerate(results, 1):
        print(f"\nMatch #{i} (Similarity: {ticket['similarity_score']:.2%})")
        print(f"Ticket ID: {ticket['ticket_id']}")
        print(f"Past Issue: {ticket['issue']}")
        print(f"Category: {ticket['category']}")
        print(f"Solution: {ticket['solution']}")
        print("-" * 70)

    print("\n" + "="*70)
    print("TEST 2: New ticket about slow performance")
    print("="*70)

    new_issue2 = "The system is very slow and pages take forever to load"
    results2 = search_engine.search_similar_tickets(new_issue2, top_k=3)
    
    for i, ticket in enumerate(results2, 1):
        print(f"\nMatch #{i} (Similarity: {ticket['similarity_score']:.2%})")
        print(f"Ticket ID: {ticket['ticket_id']}")
        print(f"Past Issue: {ticket['issue']}")
        print(f"Solution: {ticket['solution']}")
        print("-" * 70)    
