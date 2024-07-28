# custom
from src.config.log_handler import logger
from typing import List, Dict, Any


class QueryService:
    def __init__(self, db) -> None:
        self.db = db
        self.column_names = []

    def get_data(self, query: str) -> List[Dict[str, Any]]:
        try:
            with self.db.cursor() as cursor:
                cursor.execute(query)

                self.column_names = [
                    column[0]
                    for column in cursor.description
                ]

                rows = cursor.fetchall()

                result = []
                for row in rows:
                    result_dict = {}
                    for i, col_name in enumerate(self.column_names):
                        result_dict[col_name] = row[i]
                    result.append(result_dict)
                
                return result

        except Exception as e:
            logger.log_error(f"Error Executing SQL query: {e}")
            raise
