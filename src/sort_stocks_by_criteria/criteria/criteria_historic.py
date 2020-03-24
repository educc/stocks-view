import pandas as pd
from .criteria import Criteria

class CriteriaHistoric(Criteria):

    def name(self) -> str:
        return "historico"

    def process(self, df: pd.DataFrame) -> float:
        it = df.iloc[[0, -1]]
        records = it.to_dict('records')

        if len(records) < 2:
            return None
        
        first = records[0]["close"]
        last = records[1]["close"]
        
        if not isinstance(first, float) or not isinstance(last, float):
            return None

        return last / first * 100 - 100