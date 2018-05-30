#!/usr/bin/python
from collections import OrderedDict
import subprocess
import os

ROOT_DIR = '/opt/tensorflow/syntaxnet'
PARSER_EVAL = 'bazel-bin/syntaxnet/parser_eval'
MODEL_DIR = 'syntaxnet/models/parsey_mcparseface'


MODELS = [l.strip() for l in os.getenv('PARSEY_MODELS', 'English').split(',')]
BATCH_SIZE = os.getenv('PARSEY_BATCH_SIZE', '1')


def split_tokens(parse):
    # Format the result.
    def format_token(line):
        x = OrderedDict(zip(
            ["id", "form", "lemma", "upostag", "xpostag",
             "feats", "head", "deprel", "deps", "misc"],
            line.split("\t")
        ))
        for key, val in x.items():
            if val == "_":
                del x[key]  # = None
        x['id'] = int(x['id'])
        x['head'] = int(x['head'])
        return x

    return [format_token(line) for line in parse.strip().split("\n")]


def conll_to_dict(conll):
    conll_list = conll.strip().split("\n\n")
    sentences = map(split_tokens, conll_list)
    return [{w['id']:w for w in sentence} for sentence in sentences]


def open_parser_eval(args):
    return subprocess.Popen(
        [PARSER_EVAL] + args,
        cwd=ROOT_DIR,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )


def send_input(process, input_str, num_lines):
    input_str = input_str.encode('utf8')
    process.stdin.write(input_str)
    process.stdin.write(b"\n\n")  # signal end of documents
    process.stdin.flush()
    response = b""
    while num_lines > 0:
        line = process.stdout.readline()
        # print("line: %s" % line, file=sys.stderr)
        if line.strip() == b"":
            # empty line signals end of output for one sentence
            num_lines -= 1
        response += line
    return response.decode('utf8')


def load_postagger():
    pos_tagger = open_parser_eval([
        "--input=stdin",
        "--output=stdout-conll",
        "--hidden_layer_sizes=64",
        "--arg_prefix=brain_tagger",
        "--graph_builder=structured",
        "--task_context=%s/context.pbtxt" % MODEL_DIR,
        "--model_path=%s/tagger-params" % MODEL_DIR,
        "--slim_model",
        "--batch_size=%s" % BATCH_SIZE,
        "--alsologtostderr"])
    return pos_tagger

ptagger = load_postagger()

def parse_sentences(sentences, request_args):
    sentences = sentences.strip() + '\n'
    num_lines = sentences.count('\n')

    pos_tags = send_input(ptagger, sentences, num_lines)
    return conll_to_dict(pos_tags)
