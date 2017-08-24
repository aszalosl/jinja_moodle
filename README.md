# jinja_moodle
Generate Moodle XML files with Jinja2 templates.

Moodle quizzes can be generated from hand-made or from generated YAML files.
Python script uses a Jinja2 template file to generate the XML file.
The options of the script file:

    i: input file (YAML)
    o: output file (XML)
    t: template file (jinja)
    p: prefix (for inner ID)
    c: category of the quizzes
    n: number of quizzes generated from one problem.
    
YAML format for MCQ type quizzes

    questions:
    - question: text of the question
      feedback: general feedback
      good:
      - answer: 1st good answer for the question
      - answer: 2nd good answer
        hint: some feedback (optional)
      - answer: several other good answers
        ...
      bad:
      - answer: 1st bad answer
        hint: some feedback (required)
      - answer: 2nd bad answer
        hint: some feedback
        ...
    - question: text of second question, etc.
      ...
