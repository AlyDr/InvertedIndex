import pickle
import argparse


class InvertedIndex:
    def __init__(self, inverted_indexes):
        self.inverted_indexes = inverted_indexes

    def query(self, words):
        common_articles = [
            self.inverted_indexes.get(word, set())
            for word in words
        ]

        return set(set.intersection(*common_articles))

    def dump(self, filepath):
        with open(filepath, "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, filepath):
        with open(filepath, 'rb') as file:
            inverted_index_object = pickle.load(file)
        return inverted_index_object


def load_document(filepath):
    articles = dict()
    with open(filepath, encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            ind = int(line.split('\t', 1)[0])
            words = line.split('\t', 1)[1]
            articles.update({int(ind): words.strip()})
    return articles


def build_inverted_index(articles):
    inverted_indexes = {}
    for article_ind, string in articles.items():
        for word in set(string.split()):
            article_ids = inverted_indexes.setdefault(word, set())
            article_ids.add(int(article_ind))

    return InvertedIndex(inverted_indexes)


def build(args):
    articles = load_document(args.dataset)
    inverted = build_inverted_index(articles)
    inverted.dump(args.index)


def query(args):
    inverted = InvertedIndex.load(args.index)
    with open(args.query_file, "r", encoding="utf-8") as file:
        for line in file:
            print(*sorted(
                inverted.query(line.split())),
                sep=",", end="\n")


def parse(command_line):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    build_parser = subparsers.add_parser(
        "build", help="builds an inverted index")
    build_parser.add_argument("--dataset", type=str)
    build_parser.add_argument("--index", type=str)
    build_parser.set_defaults(function=build)

    query_parser = subparsers.add_parser(
        "query", help="queries articles from inverted index")
    query_parser.add_argument("--index", type=str)
    query_parser.add_argument("--query_file", type=str)
    query_parser.set_defaults(function=query)

    return parser.parse_args(command_line)


def main(command_line=None):
    parsed_command = parse(command_line)
    parsed_command.function(parsed_command)


if __name__ == "__main__":
    main()
