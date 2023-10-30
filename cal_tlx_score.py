# NASA-TLXに基づいてワークロードを計算するクラス
# 2023/10/30 @Chansei

class tlx_score:
    def __init__(self, pairwise_comparisons, slider_results):
        """
            __init__：初期化関数
            
            引数:
            - pairwise_comparisons: 大きさが15のリスト．各要素は [option1, option2, selected_index] の形式．
            - slider_results: 大きさが6のリスト．各要素は [尺度名，数値] の形式．
        """
        
        self.pairwise_comparisons = pairwise_comparisons
        self.slider_results = slider_results
        self.weights = self.compute_weights()
    
    def compute_weights(self):
        """
            compute_weights：一対比較の結果に基づいて，各尺度の重要度を計算する関数．

            戻り値:
            各尺度の名前をキーとし，それぞれの重要度を値とする辞書．
        """

        dimensions = [
            "精神的欲求", "身体的要求", "時間切迫感", "作業達成度", "努力", "不満"
        ]
        
        weights = {dimension: 0 for dimension in dimensions}
        for comparison in self.pairwise_comparisons:
            selected_index = comparison[2]
            if selected_index == 1:
                weights[comparison[0]] += 1
            elif selected_index == 2:
                weights[comparison[1]] += 1

        return weights

    def compute_overall_workload(self):
        """
            compute_overall_workload：一対比較の重要度とスライダーの結果を使用して，全体のワークロードスコアを計算．
            
            戻り値:
            全体のワークロードスコア．
        """

        slider_dict = dict(self.slider_results)
        weighted_sum = sum([self.weights[dimension] * slider_dict[dimension] for dimension in self.weights.keys()])
        overall_score = weighted_sum / sum(self.weights.values())

        return overall_score
