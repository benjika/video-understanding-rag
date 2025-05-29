import os
import psycopg2
from google import genai
from dotenv import load_dotenv


load_dotenv()


class DBManager:
    def __init__(self):
            self.conn = psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT", "5432")
            )
            self.cursor = self.conn.cursor()
            self.ensure_table_exists()


    def ensure_table_exists(self):
        self.cursor.execute("""
            CREATE EXTENSION IF NOT EXISTS vector;

            CREATE TABLE IF NOT EXISTS video_highlights (
                id SERIAL PRIMARY KEY,
                video_id TEXT,
                timestamp FLOAT,
                description TEXT,
                embedding VECTOR(768),
                summary TEXT
            );
        """)
        self.conn.commit()
            
    def get_embedding(self, text: str) -> list[float]:
        client = genai.Client()
        response = client.models.embed_content(
            model="text-embedding-004",
            contents=[
                text,
            ],)
        if not response.embeddings or response.embeddings[0] is None:
            raise ValueError("Embedding response is None or empty.")
        return response.embeddings[0].values # type: ignore
    

    def save_highlight(self, video_id: str, timestamp: float, description: str, summary: str):
        
        """
        Save a video highlight to the database.
        Args:
            video_id (str): The ID of the video.
            timestamp (float): The timestamp of the highlight.
            description (str): The description of the highlight.
            summary (str): The summary of the video.
        """

        text_to_emmbed= f"""
        video_id: {video_id},\n
        timestamp: {timestamp},\n
        description: {description}\n
        summary: {summary}\n
        """
        embedding = self.get_embedding(text_to_emmbed)
        self.cursor.execute(
            """
            INSERT INTO video_highlights (video_id, timestamp, description, embedding, summary)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (video_id, timestamp, description, embedding, summary)
        )
        self.conn.commit()
        
    def search_similar_highlights(self, query: str, limit: int = 5):
        """
        Search for similar video highlights based on a query.
        Args:
            query (str): The query to search for.
            limit (int): The maximum number of results to return.
        Returns:
            list: A list of similar video highlights.
        """
        query_embedding = self.get_embedding(query)
        self.cursor.execute(
            """
            SELECT video_id, timestamp, description, summary, embedding <-> %s::vector AS distance
            FROM video_highlights
            ORDER BY distance
            LIMIT %s
            """,
            (query_embedding, limit)
        )
        rows = self.cursor.fetchall()
        
        return [
            {
                "video_id": row[0],
                "timestamp": row[1],
                "description": row[2],
                "summary": row[3]
            }
            for row in rows
        ]

    def close(self):
        """
        Close the database connection.
        """
        self.cursor.close()
        self.conn.close()