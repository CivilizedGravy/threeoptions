from flask import Flask, render_template, request, url_for
import json
import os
from application import app

@app.route('/new', methods=['GET', 'POST'])
def new():
    
    arg = lambda x: request.args.get(x) if request.args.get(x) else ""
    presentation_title = arg('ptitle')
    
    title1 = arg('title1')
    title2 = arg('title2')
    title3 = arg('title3')
    
    price1 = arg('price1')
    price2 = arg('price2')
    price3 = arg('price3')
    
    monthly1 = arg('monthly1')
    monthly2= arg('monthly2')
    monthly3 = arg('monthly3')
    
    benefits1 = arg('benefits1')
    benefits2 = arg('benefits2')
    benefits3 = arg('benefits3')
	
    return render_template('index.html',ptitle = presentation_title, b1 = benefits1,b2 =benefits2, b3 = benefits3, m1 = monthly1, m2 = monthly2 ,m3 = monthly3, p1 = price1, p2 = price2 ,p3 = price3, t1 = title1, t2 = title2, t3 = title3)
	
	
@app.route('/present')
def present():
    print(request.args.to_dict())
    arg = lambda x: request.args.get(x)
    
    presentation_title = arg('ptitle')
    
    title1 = arg('title1')
    title2 = arg('title2')
    title3 = arg('title3')
    
    price1 = arg('price1')
    price2 = arg('price2')
    price3 = arg('price3')
    
    monthly1 = arg('monthly1')
    monthly2= arg('monthly2')
    monthly3 = arg('monthly3')
    
    benefits1 = arg('benefits1').split(',')
    benefits2 = arg('benefits2').split(',')
    benefits3 = arg('benefits3').split(',')
    
    
    
    
    option1 = {'title':'Good' ,'price':15000, 'monthly' : True, 'benefits' : [  '14 SEER Heat Pump',
                                '10 year parts warranty',
                                '2 year labor warranty',
                                'Free Heroes Club Membership']}
    return render_template('present.html',b1 = benefits1,b2 =benefits2, b3 = benefits3, m1 = monthly1, m2 = monthly2 ,m3 = monthly3, p1 = price1, p2 = price2 ,p3 = price3, t1 = title1, t2 = title2, t3 = title3 )
    
    
@app.route('/saveoptions')
#http://127.0.0.1:5000/saveoptions?ptitle={{t['ptitle']}}&title1={{t['title1']}}&price1={{t['price1']}}&benefits1={{t['benefits1']}}&title2={{t['title2']}}&price2={{t['price2']}}&benefits2={{t['benefits2']}}&title3={{t['title3']}}&price3={{t['price3']}}&benefits3={{t['benefits3']}}
def saveoptions():
    print(request.args.to_dict())
    arg = lambda x: request.args.get(x)
    f = open(os.getcwd()+'/o.json', 'r')
    
    json_temps=json.loads(f.read())
    f.close()
    
    json_temps.append(request.args.to_dict())
    
    f = open(os.getcwd()+'/o.json', 'w')
    f.write(json.dumps(json_temps, indent=4))
    f.close()
    
    return 'Saved!'
    
@app.route('/')
def temps():
    
    t = open(os.getcwd()+'/o.json', 'r')
    saved_temps = json.loads(t.read())
    
    return render_template('templates.html', saved_templates = saved_temps)
    
    
if __name__ == '__main__':
	app.run(debug=True)
