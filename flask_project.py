import pandas as pd

from distutils.log import debug

from flask import Flask,render_template,request

from sklearn.linear_model import LinearRegression


app = Flask(__name__,template_folder='template')
data = pd.read_excel("Survey For NAAC Project (Responses).xlsx")
df=pd.read_excel("Survey For NAAC Project (Responses).xlsx")


@app.route('/')

def index():
    
    Residence_Type = ["","Shared Room","Single Room","Flat with 2 room","Flat with 3 room","Flat with 4 room"]

    check_Bathroom = ["","Yes","No"]

    check_kitchen  = ["","Yes","No"]

    check_Shoping = ["","Yes","No"]

    check_Transport = ["","Yes","No"]

    check_Medical = ["","Yes","No"]

    time_Market = ["","less than 5 min","less than 10 min","less than 15 min"]

    time_College = ["","less than 5 min","less than 10 min","less than 15 min"]

    check_Play = ["","Yes","No"]

    return render_template("index.html",Residence = Residence_Type,bathroom = check_Bathroom,
     kitchens = check_kitchen
    , Shopping = check_Shoping, Transport  = check_Transport,Medical = check_Medical,market = time_Market,
    college = time_College,
    Playground = check_Play)

@app.route('/predict', methods = ['POST'])
def predict():
    Residence_Type = request.form.get('Residence')
    check_Bathroom = request.form.get('bathroom')
    check_kitch = request.form.get('kitchens')
    check_Shoping = request.form.get('Shopping')
    check_Transport = request.form.get('Transport')
    check_Medical = request.form.get('Medical')
    Food_store = request.form.get('food')
    time_Market = request.form.get('market')
    time_College = request.form.get('college')
    check_Play = request.form.get('Playground')

    #"Single Room","Flat with 2 room","Flat with 3 room","Flat with 4 room"
    if Residence_Type == "Shared Room":
        Residence_Type = 0.5
    elif Residence_Type == "Single Room":
        Residence_Type = 1
    elif Residence_Type == "Flat with 2 room":
        Residence_Type = 2
    elif Residence_Type == "Flat with 3 room":
        Residence_Type = 3
    elif Residence_Type == "Flat with 4 room":
        Residence_Type = 4
    
    Residence_Type = float(Residence_Type)

    if check_Bathroom == 'Yes':
        check_Bathroom = 1
    elif check_Bathroom == 'No':
        check_Bathroom = 0

    if check_kitch == 'Yes':
        check_kitch = 1
    elif check_kitch == 'No':
        check_kitch = 0

    if check_Shoping == 'Yes':
        check_Shoping = 1
    elif check_Shoping == 'No':
        check_Shoping = 0

    if check_Transport == 'Yes':
        check_Transport = 1
    elif check_Transport == 'No':
        check_Transport = 0
    
    if check_Medical == 'Yes':
        check_Medical = 1
    elif check_Medical == 'No':
        check_Medical = 0

    if check_Play == 'Yes':
        check_Play = 1
    elif check_Play == 'No':
        check_Play = 0
    
   
    Food_store = float(Food_store)

    if  time_Market == 'less than 5 min':
        time_Market= 5
    elif time_Market == 'less than 10 min':
        time_Market= 10
    elif time_Market == 'less than 15 min':
        time_Market = 15
    
    if  time_College == 'less than 5 min':
        time_College= 15
    elif time_College == 'less than 10 min':
        time_College= 10
    elif time_College == 'less than 15 min':
        time_College = 5

    x_val=df.drop('house_rent',axis=1)
    del x_val['Residence Type']
    y_val=df['house_rent']
    lm=LinearRegression()
    lm.fit(x_val,y_val)

    Residence_Type = Residence_Type*lm.coef_[0]
    check_Bathroom= check_Bathroom*lm.coef_[1]
    check_kitch=check_kitch*lm.coef_[2]
    check_Shoping=check_Shoping*lm.coef_[3]
    check_Transport=check_Transport*lm.coef_[4]
    check_Medical=check_Medical*lm.coef_[5]
    Food_store=Food_store*lm.coef_[6]
    time_Market= time_Market*lm.coef_[7]
    time_College=time_College*lm.coef_[8]
    check_Play=check_Play*lm.coef_[9]

    
    
    sum = Residence_Type + check_Bathroom +check_kitch+check_Shoping+check_Transport+ check_Medical+Food_store+time_Market+ time_College+ check_Play +lm.intercept_
    sum = round(sum)

    low = sum - 198
    up = sum + 300
    
    low = str(low)
    up = str(up)
    return low+" to "+up

if __name__ == "__main__":
    app.run(debug = True, port = 5500)
