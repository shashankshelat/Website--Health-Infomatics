
import time
import sys
import os
import csv
import arff
from flask import Flask,render_template,request, send_from_directory
import aprioroo


#================================================================================

def filetobereadfrom(nameoffileinput, bing):
	if bing !=None:
		with open(nameoffileinput, 'rb') as tempone:
		    readfrom = csv.DictReader(tempone)
		    arrayone = [row for row in readfrom if row['ADMITTING_DIAGNOSIS_CODE'] == bing]
		output = {}
		for row in arrayone:
			for column, value in row.items():
				output.setdefault(column, []).append(value)
		return output
		return output
	else:
		readfrom = csv.DictReader(open(nameoffileinput))
		output = {}
		for row in readfrom:
			for column, value in row.items():
				output.setdefault(column, []).append(value)
		return output


#======================================================================




def read(nameoffileinput):
    with open(nameoffileinput+".csv") as doctorfile:
        reader = [row for row in csv.reader(doctorfile.read().splitlines())]
    datatable= list(reader)
    tabheader= datatable[0]
    del datatable[0]
    return tabheader,datatable



#======================================================================

app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
@app.route("/")
def deal():
	header=filetobereadfrom('6339_Dataset.csv', None)
	header=header.keys()
	if header:
		operation=[]
		for key in range(len(header)):
			operation.append(dict([('name',header[key])]))
	print(operation)
	return render_template('firstpage.html', bucket_list=operation)
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('document', 'static/')





#======================================================================




@app.route('/task',methods=['GET','POST'])
def task4():
	output={}
	support=request.form['sup']
	confidence=request.form['confi']
	bing=request.form["Adig"]
	data=filetobereadfrom("6339_Dataset.csv",bing)
	features=['ADMITTING_DIAGNOSIS_CODE','DIAGNOSIS_CODE_1']
	for row in features:
		output.update({row:data[row]})
	with open("result.csv", "wb") as outtofile:
	   writer = csv.writer(outtofile)
	   writer.writerow(output.keys())
	   writer.writerows(zip(*output.values()))
	header,datatable=read("result")
	L, support_data = aprioroo.apriori(datatable, minsupport=float(support))
	rules=aprioroo.generateRules(L, support_data,min_confidence=float(confidence))
	if rules:
		rules_list=[]
		for key in range(len(rules)):
				X=iter(rules[key][1]).next()
				Y=iter(rules[key][0]).next()
				for i in range(len(data['SEX'])):
					if X==data['DIAGNOSIS_CODE_1'][i] and bing==Y:
						rules_list.append(dict([('A',Y),('B',X),('conf',rules[key][2]),('sup',rules[key][3]),('AGE',data['AGE'][i]),('SEX',data['SEX'][i]),('RACE',data['RACE'][i])]))
		return render_template('secondpage.html', rules_list	=rules_list)
	else:
		rules_list=[]
		return render_template('secondpage.html', rules_list	=rules_list)
		return render_template('secondpage.html', rules_list	=rules_list)
	return render_template('firstpage.html')
if __name__ == "__main__":
    app.debug = True 
    app.run(host='localhost', port=5000)
