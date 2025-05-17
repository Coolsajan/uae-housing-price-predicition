from flask import Flask,render_template,request
from src.pipeline.predicition_pipleline import PredictPrice,PredictionData

app=Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html") 

@app.route("/prediction",methods=["GET","POST"])
def prediction():
    if request.method =="GET":
        return render_template("prediction.html")
    else:
        data=PredictionData(
            bedroom=request.form.get("bedrooms"),
            bathroom=request.form.get("bathrooms"),
            area=request.form.get("area"),
            address=request.form.get("address"),
            propert_type=request.form.get("propert_type"),
            furnishing=request.form.get("furnishing"),
            completion=request.form.get("completion_status"),
            handover=request.form.get("handover"),
            project_name=request.form.get("project_name")
        )
        data=data.get_data_to_df()
        model=PredictPrice()
        price_predicition=model.initiate_price_prediciton(data)
        price_predicition=format(price_predicition, ",")
        return render_template("prediction.html",predicition_price=price_predicition)


if __name__=="__main__":
    app.run(host="0.0.0.0", port=7860)