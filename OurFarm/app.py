from flask import Flask, request, render_template     #for building the web application
import sklearn          #for the machine learning algos
import pickle           #for loading the pre-trained model
import pandas as pd     #for the data manipulation
import os               #for the file operations

app = Flask(__name__)   #  It creates a Flask web application instance named "app."

# The script loads a pre-trained machine learning model from a file named "RFmodel.pkl" using the pickle.load() method.
model = pickle.load(open("RFmodel.pkl","rb"))

#This route corresponds to the home page of the web application and returns the "home.html" template.
@app.route("/")    
def home():
    return render_template("home.html")
    
#This route handles the prediction logic. It expects both GET and POST requests. When the user submits a form, 
#it retrieves the form data and uses it to make crop predictions.
@app.route("/predict", methods = ["GET", "POST"])
def predict():
    if request.method == "POST":    #checks if the request method is POST.
        
        #It retrieves user inputs for various parameters like nitrogen, phosphorus, 
            #potassium, temperature, humidity, pH level, and rainfall using request.form
        # Nitrogen
        nitrogen = float(request.form["nitrogen"])
        
        # Phosphorus
        phosphorus = float(request.form["phosphorus"])
        
        # Potassium
        potassium = float(request.form["potassium"])
        
        # Temperature
        temperature = float(request.form["temperature"])
        
        # Humidity Level
        humidity = float(request.form["humidity"])
        
        # PH level
        phLevel = float(request.form["ph-level"])
        
        # Rainfall
        rainfall = float(request.form["rainfall"])
        
        # Making predictions from the values:
        #It uses the loaded machine learning model to make predictions based on the input values
        predictions = model.predict([[nitrogen, phosphorus, potassium, temperature, humidity, phLevel, rainfall]])

        #The function generates a statement indicating the recommended crop and its sowing season based on the prediction.
        output = predictions[0]
        finalOutput = output.capitalize()
        
        if (output == "rice" or output == "blackgram" or output == "pomegranate" or output == "papaya"
            or output == "cotton" or output == "orange" or output == "coffee" or output == "chickpea"
            or output == "mothbeans" or output == "pigeonpeas" or output == "jute" or output == "mungbeans"
            or output == "lentil" or output == "maize" or output == "apple"):
            cropStatement = finalOutput + " should be harvested. It's a Kharif crop, so it must be sown at the beginning of the rainy season e.g between April and May."
                            

        elif (output == "muskmelon" or output == "kidneybeans" or output == "coconut" or output == "grapes" or output == "banana"):
            cropStatement = finalOutput + " should be harvested. It's a Rabi crop, so it must be sown at the end of monsoon and beginning of winter season e.g between September and October."
            
        elif (output == "watermelon"):
            cropStatement = finalOutput + " should be harvested. It's a Zaid Crop, so it must be sown between the Kharif and rabi season i.e between March and June."
        
        elif (output == "mango"):
            cropStatement = finalOutput + " should be harvested. It's a cash crop and also perennial. So you can grow it anytime."
        
              
    #The result is displayed in an HTML template called "CropResult.html," and 
    #the cropStatement is passed to the template to display the recommendation.    
    return render_template('CropResult.html', prediction_text=cropStatement)


#It runs the application in debug mode, which is helpful for development.
if __name__ == '__main__':
    app.run(debug=True)
