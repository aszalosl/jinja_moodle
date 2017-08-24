#!/usr/bin/env python3

import sys, getopt, yaml
from jinja2 import Environment, FileSystemLoader, Template
import random

ENV = Environment(loader=FileSystemLoader('./', encoding="utf-8"))

ANSWERS = 4  # how many answers have a question?
PRIZE4 = [0.0, 100.0, 50.0, 33.333, 25.0]      # based on ASWERS
PENALTY4 = [0.0, -33.333, -50.0, -100.0, 0.0]  # based on ASWERS

def yaml2xml(input_file, output_file, template_file, prefix, category, number):
    """Generates Moodle XML file from the yaml datafile.

    Args:
        input_file: name of the yaml file
        output_file: name of the xml file
        template_file: name of the jinja2 template file
        prefix: common prefix in the Id of the questions
        category: category of the questions
        number: how many examples generated from one question?

    Returns:
        None. If some of the files aren't available, throw an error.
    """

    with open(input_file) as yaml_file:
        yaml_data =  yaml.load(yaml_file)

    counter = prefix
    generated = {}
    generated['title'] = "fonya/test"
    generated['questions'] = list()

    k = 0
    for i,question in enumerate(yaml_data['questions']):
        for j in range(number):  # we generate number problems from 1 question
            q = dict()
            q['name'] = counter + str(i) + '_' + str(j)
            q['generalfeedback'] = question['feedback']
            q['questiontext'] = question['question']
            good_answers = len(question['good'])
            bad_answers = len(question['bad'])
            nu_good = random.randrange(1, min(good_answers, ANSWERS))
            nu_bad = ANSWERS - nu_good
            #print(nu_good, nu_bad)
            answers = list()
            for answer in random.sample(question['good'], nu_good):
                a = dict()
                a['text'] = answer['answer']
                a['value'] = PRIZE4[nu_good]
                if 'hint' in answer:
                    a['feedback'] = answer['hint']
                answers.append(a)
            if (nu_bad > 0):
                for answer in random.sample(question['bad'], nu_bad):
                    a = dict()
                    a['text'] = answer['answer']
                    a['value'] = PENALTY4[nu_good]
                    a['feedback'] = answer['hint']
                    answers.append(a)
            q['answers'] = answers
            generated['questions'].append(q)
            k += 1

    template = ENV.get_template(template_file)
    with open(output_file, 'w') as xml_file:
        output_content = template.render(data=generated)
        xml_file.write(output_content)
    print("{} problems generated and written into {}".format(k,output_file))

def main(argv):
    help  = 'yaml2xml.py -i <inputfile> -o <outputfile> -t <templatefile> -p <prefix> -c <category> -n <number>'
    if not argv:
        print(help)
        sys.exit(2)

    ifile = ''
    ofile = ''
    tfile = ''
    pre   = 'XX'
    cat   = 'any/thing'
    n     = 5
    try:
        opts, args = getopt.getopt(argv,"hi:o:t:p:c:n:",
        ["ifile=","ofile=","tfile=","prefix=","category=","number="])
    except getopt.GetoptError:
        print(help)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            ifile = arg
        elif opt in ("-o", "--ofile"):
            ofile = arg
        elif opt in ("-t", "--tfile"):
            tfile = arg
        elif opt in ("-p", "--prefix"):
            pre = arg
        elif opt in ("-c", "--category"):
            cat = arg
        elif opt in ("-n", "--number"):
            n = arg

    if ifile!='' and ofile!='' and tfile !='':
        yaml2xml(ifile, ofile, tfile, pre, cat, n)

if __name__ == "__main__":
    main(sys.argv[1:])
