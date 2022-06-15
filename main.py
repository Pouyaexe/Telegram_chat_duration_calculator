# an app to convert jason to df
import json
import pandas as pd

#convert jason to df

import pandas as pd

# Read json from String
json_str = '{"Courses":{"r1":"Spark"},"Fee":{"r1":"25000"},"Duration":{"r1":"50 Days"}}'

df = pd.read_json('result.json', orient='records')
print(df)