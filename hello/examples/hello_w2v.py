import gensim

def run_w2v(in_str):
    events = in_str.replace("\n", " ").split(" ")
    model = gensim.models.Word2Vec([events], sg=1, size=350, window=30, min_count=1, workers=20)
    return model.wv


if __name__ == "__main__":
    wv = run_w2v("aa bb cc dd\naa bb cc aa bb aa cc bb bb aa")

    pass
