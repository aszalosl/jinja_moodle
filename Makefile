r1.xml: reg1.yaml mcq.j2 yaml2xml.py
	./yaml2xml.py -i $< -o $@ -t mcq.j2
