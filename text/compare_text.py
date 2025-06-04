import pandas as pd
from rapidfuzz import process, fuzz
from typing import Callable


def fuzzy_match_column(
        df: pd.DataFrame,
        source_col: str,
        candidate_col: str,
        scorer: Callable = fuzz.token_sort_ratio,
        result_col_match: str = "最佳匹配",
        result_col_score: str = "相似度"
) -> pd.DataFrame:
    """
    对 DataFrame 中 source_col 的每一项，在 candidate_col 中找到最相似的一项。

    参数:
    - df: pandas DataFrame 对象
    - source_col: 需要匹配的列（字符串）
    - candidate_col: 候选匹配值所在的列（字符串）
    - scorer: 匹配算法，默认为 fuzz.token_sort_ratio
    - result_col_match: 输出的匹配结果列名
    - result_col_score: 输出的匹配得分列名

    返回:
    - 增加了匹配结果和分数的新 DataFrame
    """
    candidates = df[candidate_col].dropna().unique().tolist()

    matches = []
    scores = []

    for val in df[source_col]:
        if pd.isna(val):
            matches.append(None)
            scores.append(None)
        else:
            match = process.extractOne(val, candidates, scorer=scorer)
            if match:
                best_match, score, _ = match
                matches.append(best_match)
                scores.append(f"{score:.2f}")
            else:
                matches.append(None)
                scores.append(None)

    df[result_col_match] = matches
    df[result_col_score] = scores
    return df

if __name__=="__main__":
    # 示例数据
    data = {
        "订单地址": ["珠海店荷塘物语11栋1601", "广州店天河路123号"],
        "门店地址": ["珠海店+荷塘物语11栋1601", "广州店-天河路123"]
    }
    df = pd.DataFrame(data)

    # 调用匹配函数
    df_result = fuzzy_match_column(
        df,
        source_col="订单地址",
        candidate_col="门店地址"
    )

    print(df_result)
