# encoding=utf-8
import jieba


if __name__ == "__main__":
    # https://github.com/fxsjy/jieba
    s = "让我们荡起双桨"
    print(s)
    scenarios = jieba.cut(s, cut_all=True)
    for scenario in scenarios:
        if len(scenario) > 0:
            print(":", scenario)

