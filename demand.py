import numpy as np
import pandas as pd
from calendar import monthrange
from collections import OrderedDict, deque


def Demand_Planning(file, Annual_CB_demand):

    df = pd.read_excel(file, sheet_name='Planning_Cycle')

    # creating dictionaries to store data
    month_keys = [('Apr', 4, 2023), ('May', 5, 2023), ('Jun', 6, 2023), ('Jul', 7, 2023), ('Aug', 8, 2023), ('Sep', 9, 2023),
                  ('Oct', 10, 2023), ('Nov', 11, 2023), ('Dec', 12, 2023), ('Jan', 1, 2024), ('Feb', 2, 2024), ('Mar', 3, 2024)]
    operating_days = OrderedDict()
    total_days = OrderedDict()
    monthly_demand = OrderedDict()

    for i in month_keys:
        total_days[i[0]] = monthrange(i[2], i[1])[1]

    for i in df.index:

        operating_days[df['Month'][i]] = total_days[df['Month']
                                                    [i]] - df['Total Non-operating days'][i]
        #monsoon_factor[df['Month'][i]] = df['Monsoon Factor for Month'][i]

    total_operating_days = sum(operating_days.values())

    for i in df.index:
        monthly_demand[df['Month'][i]] = round(
            Annual_CB_demand * operating_days[df['Month'][i]] / total_operating_days)

    diff = Annual_CB_demand - sum(monthly_demand.values())
    monthly_demand['Mar'] += diff

    data = {'Month': df['Month'], 'Operating Days': operating_days.values(
    ), 'Monthly Demand': monthly_demand.values()}

    df2 = pd.DataFrame(data)

    data = {'Month': 'Total', 'Operating Days': str(df2['Operating Days'].sum()).split(
        '.')[0], 'Monthly Demand': str(df2['Monthly Demand'].sum()).split('.')[0]}

    df2 = df2.append(data, ignore_index=True)

    df2 = df2.T

    df2.to_excel('result.xlsx')

    return [df2, monthly_demand]
