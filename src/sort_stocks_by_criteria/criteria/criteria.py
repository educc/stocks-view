import pandas as pd

class Criteria:

    def name(self) -> str:
        return "criteria"

    def process(self, df: pd.DataFrame) -> float:
        return None
