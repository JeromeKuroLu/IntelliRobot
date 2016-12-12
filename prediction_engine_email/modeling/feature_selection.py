from sklearn.feature_selection import SelectKBest, chi2


class FeatureSelection:
    @staticmethod
    def build_select_k_best(feature_names, contents, labels, score_fx=chi2, k_per=0.7):
        k_best = int(round(len(feature_names) * k_per))
        transformer = SelectKBest(score_fx, k=k_best).fit(contents, labels)

        return transformer
