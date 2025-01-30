import pandas as pd

state = ["California", "Texas", "Florida", "New York"] 
population = [39613493, 29730311, 21944577, 19299981]

dict_state = {"States": state, "Population": population} 

df_states = pd.DataFrame.from_dict(dict_state) 
# print(df_states) 
df_states.to_csv("web-scraping-basic/states_sample.csv", index=False) 