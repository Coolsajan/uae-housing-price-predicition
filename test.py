from src.pipeline.predicition_pipleline import InputData,PredictPrice
from src.pipeline.training_pipeline import ModelTrainingPipeline


model=ModelTrainingPipeline()
model.run_piple()

data=InputData(bedroom=3,
               bathroom=4,
               area=1208,
               country="uae",
               city="Dubai",
               address=" DAMAC Hills 2 (Akoya by DAMAC)",
               propert_type="Townhouse",
               purpose="sale",
               furnishing="Unfurnished",
               completion="Off-Plan",
               handover="Q2 2025",
               project_name="Camelia Villas")

print(data)
data_df=InputData.get_data_to_df(data)

model=PredictPrice()

calculated_price=model.initia_price_prediciton(input_df=data_df)

print(calculated_price)



