import numpy as np
import pandas as pd
from calendar import monthrange
from collections import OrderedDict, deque


def Route_optimization_logic(MBR, capacity, Plant_demand, df):

    rt_MBR = MBR.copy()
    rt_capacity = capacity.copy()
    rt_plant_demand = Plant_demand

    # STEP-1 : sorting data in ascending order according to Total Route Cost for one ton of CB

    df = df.sort_values(by='Landed Cost')

    # STEP-2 : assigning mbr to each stakeholders

    MBR_Flag = 1

    Lowest_cost_route_id = {}
    current_lowest_route = {}
    route_capacity = {}
    df_index = {}
    allocation = {k: 0 for k in rt_MBR.keys()}

    # Iterate through each route from top to bottom

    while MBR_Flag != 0 and rt_plant_demand > 0:

        MBR_Flag = 0

        for i in df.index:

            df_index[df['S.No.'][i]] = i

            if df['Grower'][i] != '-' and df['HIT'][i] != '-' and df['LLE'][i] != '-' and df['TR'][i] != '-':

                current_route_capacity = min(rt_capacity[df['Grower'][i]], rt_capacity[df['HIT'][i]],
                                             rt_capacity[df['LLE'][i]], rt_capacity[df['TR'][i]], rt_plant_demand)

                if df['Grower'][i] not in Lowest_cost_route_id:
                    Lowest_cost_route_id[df['Grower'][i]] = []
                    Lowest_cost_route_id[df['Grower']
                                         [i]].append(df['S.No.'][i])

                else:
                    if df['S.No.'][i] not in Lowest_cost_route_id[df['Grower'][i]]:
                        Lowest_cost_route_id[df['Grower']
                                             [i]].append(df['S.No.'][i])

                if df['HIT'][i] not in Lowest_cost_route_id:
                    Lowest_cost_route_id[df['HIT'][i]] = []
                    Lowest_cost_route_id[df['HIT'][i]].append(df['S.No.'][i])

                else:
                    if df['S.No.'][i] not in Lowest_cost_route_id[df['HIT'][i]]:
                        Lowest_cost_route_id[df['HIT']
                                             [i]].append(df['S.No.'][i])

                if df['LLE'][i] not in Lowest_cost_route_id:
                    Lowest_cost_route_id[df['LLE'][i]] = []
                    Lowest_cost_route_id[df['LLE'][i]].append(df['S.No.'][i])

                else:
                    if df['S.No.'][i] not in Lowest_cost_route_id[df['LLE'][i]]:
                        Lowest_cost_route_id[df['LLE']
                                             [i]].append(df['S.No.'][i])

                if df['TR'][i] not in Lowest_cost_route_id:
                    Lowest_cost_route_id[df['TR'][i]] = []
                    Lowest_cost_route_id[df['TR'][i]].append(df['S.No.'][i])

                else:
                    if df['S.No.'][i] not in Lowest_cost_route_id[df['TR'][i]]:
                        Lowest_cost_route_id[df['TR']
                                             [i]].append(df['S.No.'][i])

                if current_route_capacity == 0:

                    if df['Grower'][i] in current_lowest_route and current_lowest_route[df['Grower'][i]] == df['S.No.'][i]:
                        current_lowest_route.pop(df['Grower'][i])
                    if df['HIT'][i] in current_lowest_route and current_lowest_route[df['HIT'][i]] == df['S.No.'][i]:
                        current_lowest_route.pop(df['HIT'][i])
                    if df['LLE'][i] in current_lowest_route and current_lowest_route[df['LLE'][i]] == df['S.No.'][i]:
                        current_lowest_route.pop(df['LLE'][i])
                    if df['TR'][i] in current_lowest_route and current_lowest_route[df['TR'][i]] == df['S.No.'][i]:
                        current_lowest_route.pop(df['TR'][i])
                    continue

                if df['Grower'][i] not in current_lowest_route:
                    current_lowest_route[df['Grower'][i]] = df['S.No.'][i]

                if df['HIT'][i] not in current_lowest_route:
                    current_lowest_route[df['HIT'][i]] = df['S.No.'][i]

                if df['LLE'][i] not in current_lowest_route:
                    current_lowest_route[df['LLE'][i]] = df['S.No.'][i]

                if df['TR'][i] not in current_lowest_route:
                    current_lowest_route[df['TR'][i]] = df['S.No.'][i]

                l = []
                names = []

                if rt_MBR[df['Grower'][i]] > 0:
                    l.append(rt_MBR[df['Grower'][i]])
                    names.append(df['Grower'][i])

                if rt_MBR[df['HIT'][i]] > 0:
                    l.append(rt_MBR[df['HIT'][i]])
                    names.append(df['HIT'][i])

                if rt_MBR[df['LLE'][i]] > 0:
                    l.append(rt_MBR[df['LLE'][i]])
                    names.append(df['LLE'][i])

                if rt_MBR[df['TR'][i]] > 0:
                    l.append(rt_MBR[df['TR'][i]])
                    names.append(df['TR'][i])

                while True:
                    if len(l) == 0:
                        break

                    x = min(l)
                    Min_MBR_Stakeholder = names[l.index(x)]

                    # Lowest_cost_route_id[Min_MBR_Stakeholder][0]:
                    if df['S.No.'][i] != current_lowest_route[Min_MBR_Stakeholder]:
                        names.remove(Min_MBR_Stakeholder)
                        l.remove(x)
                    else:
                        break

                if len(l) == 0:
                    continue

                x = min(x, current_route_capacity)

                if x >= rt_MBR[df['Grower'][i]]:
                    rt_MBR[df['Grower'][i]] = 0
                    current_lowest_route.pop(df['Grower'][i])
                else:
                    rt_MBR[df['Grower'][i]] -= x

                if x >= rt_MBR[df['HIT'][i]]:
                    rt_MBR[df['HIT'][i]] = 0
                    current_lowest_route.pop(df['HIT'][i])
                else:
                    rt_MBR[df['HIT'][i]] -= x

                if x >= rt_MBR[df['LLE'][i]]:
                    rt_MBR[df['LLE'][i]] = 0
                    current_lowest_route.pop(df['LLE'][i])
                else:
                    rt_MBR[df['LLE'][i]] -= x

                if x >= rt_MBR[df['TR'][i]]:
                    rt_MBR[df['TR'][i]] = 0
                    current_lowest_route.pop(df['TR'][i])
                else:
                    rt_MBR[df['TR'][i]] -= x

                rt_capacity[df['Grower'][i]] -= x
                rt_capacity[df['LLE'][i]] -= x
                rt_capacity[df['HIT'][i]] -= x
                rt_capacity[df['TR'][i]] -= x

                rt_plant_demand -= x
                df['Qty'][i] += x

                allocation[df['Grower'][i]] += x
                allocation[df['HIT'][i]] += x
                allocation[df['LLE'][i]] += x
                allocation[df['TR'][i]] += x

                current_route_capacity -= x

                if current_route_capacity == 0:

                    if df['Grower'][i] in current_lowest_route and current_lowest_route[df['Grower'][i]] == df['S.No.'][i]:
                        current_lowest_route.pop(df['Grower'][i])
                    if df['HIT'][i] in current_lowest_route and current_lowest_route[df['HIT'][i]] == df['S.No.'][i]:
                        current_lowest_route.pop(df['HIT'][i])
                    if df['LLE'][i] in current_lowest_route and current_lowest_route[df['LLE'][i]] == df['S.No.'][i]:
                        current_lowest_route.pop(df['LLE'][i])
                    if df['TR'][i] in current_lowest_route and current_lowest_route[df['TR'][i]] == df['S.No.'][i]:
                        current_lowest_route.pop(df['TR'][i])

                if x > 0:
                    MBR_Flag = 1

    remaining_MBR_Stakeholders = {}

    for i in rt_MBR:
        if rt_MBR[i] > 0:
            remaining_MBR_Stakeholders[i] = rt_MBR[i]

    remaining_Grower_MBR = {}
    for i in remaining_MBR_Stakeholders:
        if remaining_MBR_Stakeholders[i] > 0 and (i[0] == 'G' or i[0] == 'H'):
            remaining_Grower_MBR[i] = remaining_MBR_Stakeholders[i]

    for i in remaining_Grower_MBR:
        if remaining_Grower_MBR[i] == 0:
            remaining_MBR_Stakeholders.pop(i)
        else:
            remaining_MBR_Stakeholders[i] = remaining_Grower_MBR[i]

    if len(remaining_MBR_Stakeholders) > 0:

        for s in remaining_MBR_Stakeholders:

            while True:

                if len(Lowest_cost_route_id[s]) == 0:
                    break

                for i in df.index:

                    l = []

                    if df['Grower'][i] != '-':
                        l.append(rt_capacity[df['Grower'][i]])
                    if df['HIT'][i] != '-':
                        l.append(rt_capacity[df['HIT'][i]])
                    if df['LLE'][i] != '-':
                        l.append(rt_capacity[df['LLE'][i]])
                    if df['TR'][i] != '-':
                        l.append(rt_capacity[df['TR'][i]])

                    route_capacity[df['S.No.'][i]] = min(l)

                while remaining_MBR_Stakeholders[s] > 0 and len(Lowest_cost_route_id[s]) > 0:

                    if route_capacity[Lowest_cost_route_id[s][0]] >= remaining_MBR_Stakeholders[s]:

                        df['Qty'][df_index[Lowest_cost_route_id[s][0]]
                                  ] += remaining_MBR_Stakeholders[s]

                        if df['Grower'][df_index[Lowest_cost_route_id[s][0]]] != '-':
                            allocation[df['Grower'][df_index[Lowest_cost_route_id[s][0]]]
                                       ] += remaining_MBR_Stakeholders[s]

                        if df['HIT'][df_index[Lowest_cost_route_id[s][0]]] != '-':
                            allocation[df['HIT'][df_index[Lowest_cost_route_id[s][0]]]
                                       ] += remaining_MBR_Stakeholders[s]

                        if df['LLE'][df_index[Lowest_cost_route_id[s][0]]] != '-':
                            allocation[df['LLE'][df_index[Lowest_cost_route_id[s][0]]]
                                       ] += remaining_MBR_Stakeholders[s]

                        if df['TR'][df_index[Lowest_cost_route_id[s][0]]] != '-':
                            allocation[df['TR'][df_index[Lowest_cost_route_id[s][0]]]
                                       ] += remaining_MBR_Stakeholders[s]

                        rt_plant_demand -= remaining_MBR_Stakeholders[s]

                        remaining_MBR_Stakeholders[s] = 0
                    else:
                        Lowest_cost_route_id[s].pop(0)

                if len(Lowest_cost_route_id[s]) == 0:
                    break

                for i in reversed(df.index):

                    if rt_plant_demand == 0:
                        break

                    if True:
                        if df['Grower'][i] != '-' and df['HIT'][i] != '-' and df['LLE'][i] != '-' and df['TR'][i] != '-':

                            if allocation[df['Grower'][i]] - MBR[df['Grower'][i]] >= 0:
                                x1 = allocation[df['Grower']
                                                [i]] - MBR[df['Grower'][i]]
                            else:
                                x1 = 0

                            if allocation[df['HIT'][i]] - MBR[df['HIT'][i]] >= 0:
                                x2 = allocation[df['HIT'][i]] - \
                                    MBR[df['HIT'][i]]
                            else:
                                x2 = 0

                            if allocation[df['LLE'][i]] - MBR[df['LLE'][i]] >= 0:
                                x3 = allocation[df['LLE'][i]] - \
                                    MBR[df['LLE'][i]]
                            else:
                                x3 = 0

                            if allocation[df['TR'][i]] - MBR[df['TR'][i]] >= 0:
                                x4 = allocation[df['TR'][i]] - MBR[df['TR'][i]]
                            else:
                                x4 = 0

                            x = min(x1, x2, x3, x4, df['Qty'][i])

                            df['Qty'][i] -= x
                            allocation[df['HIT'][i]] -= x
                            allocation[df['LLE'][i]] -= x
                            allocation[df['Grower'][i]] -= x
                            allocation[df['TR'][i]] -= x
                            rt_plant_demand += x
                            route_capacity[df['S.No.'][i]] += x
                            rt_capacity[df['HIT'][i]] += x
                            rt_capacity[df['LLE'][i]] += x
                            rt_capacity[df['Grower'][i]] += x
                            rt_capacity[df['TR'][i]] += x

                        elif df['Grower'][i] != '-' and df['HIT'][i] != '-':

                            if allocation[df['Grower'][i]] - MBR[df['Grower'][i]] >= 0:
                                x1 = allocation[df['Grower']
                                                [i]] - MBR[df['Grower'][i]]
                            else:
                                x1 = 0

                            if allocation[df['HIT'][i]] - MBR[df['HIT'][i]] >= 0:
                                x2 = allocation[df['HIT'][i]] - \
                                    MBR[df['HIT'][i]]
                            else:
                                x2 = 0

                            x = min(x1, x2, df['Qty'][i])

                            df['Qty'][i] -= x
                            allocation[df['HIT'][i]] -= x
                            allocation[df['Grower'][i]] -= x
                            rt_plant_demand += x
                            route_capacity[df['S.No.'][i]] += x
                            rt_capacity[df['HIT'][i]] += x
                            rt_capacity[df['Grower'][i]] += x

                if rt_plant_demand < 0:

                    df['Qty'][df_index[Lowest_cost_route_id[s][0]]
                              ] += rt_plant_demand

                    remaining_MBR_Stakeholders[s] -= rt_plant_demand

                    if df['Grower'][df_index[Lowest_cost_route_id[s][0]]] != '-':
                        allocation[df['Grower']
                                   [df_index[Lowest_cost_route_id[s][0]]]] += rt_plant_demand
                        rt_capacity[df['Grower']
                                    [df_index[Lowest_cost_route_id[s][0]]]] -= rt_plant_demand

                    if df['HIT'][df_index[Lowest_cost_route_id[s][0]]] != '-':
                        allocation[df['HIT'][df_index[Lowest_cost_route_id[s][0]]]
                                   ] += rt_plant_demand
                        rt_capacity[df['HIT'][df_index[Lowest_cost_route_id[s][0]]]
                                    ] -= rt_plant_demand

                    if df['LLE'][df_index[Lowest_cost_route_id[s][0]]] != '-':
                        allocation[df['LLE'][df_index[Lowest_cost_route_id[s][0]]]
                                   ] += rt_plant_demand
                        rt_capacity[df['LLE']
                                    [df_index[Lowest_cost_route_id[s][0]]]] -= rt_plant_demand

                    if df['TR'][df_index[Lowest_cost_route_id[s][0]]] != '-':
                        allocation[df['TR'][df_index[Lowest_cost_route_id[s][0]]]
                                   ] += rt_plant_demand
                        rt_capacity[df['TR'][df_index[Lowest_cost_route_id[s][0]]]
                                    ] -= rt_plant_demand

                rt_plant_demand = 0

                if remaining_MBR_Stakeholders[s] == 0:
                    break
                else:
                    Lowest_cost_route_id[s].pop(0)

    # STEP-3 : assigning remaining quantity greedily from lowest cost route to highest cost route

    if rt_plant_demand > 0:

        for i in df.index:

            if True:

                if df['Grower'][i] != '-' and df['HIT'][i] != '-' and df['LLE'][i] != '-' and df['TR'][i] != '-':

                    x = min(rt_capacity[df['Grower'][i]], rt_capacity[df['HIT'][i]],
                            rt_capacity[df['LLE'][i]], rt_capacity[df['TR'][i]], rt_plant_demand)

                    rt_capacity[df['Grower'][i]] -= x
                    rt_capacity[df['HIT'][i]] -= x
                    rt_capacity[df['LLE'][i]] -= x
                    rt_capacity[df['TR'][i]] -= x
                    rt_plant_demand -= x
                    df['Qty'][i] += x
                    allocation[df['Grower'][i]] += x
                    allocation[df['HIT'][i]] += x
                    allocation[df['LLE'][i]] += x
                    allocation[df['TR'][i]] += x

                elif df['Grower'][i] != '-' and df['HIT'][i] != '-':

                    x = min(rt_capacity[df['Grower'][i]],
                            rt_capacity[df['HIT'][i]], rt_plant_demand)

                    rt_capacity[df['Grower'][i]] -= x
                    rt_capacity[df['HIT'][i]] -= x
                    rt_plant_demand -= x
                    df['Qty'][i] += x

                    allocation[df['Grower'][i]] += x
                    allocation[df['HIT'][i]] += x

    # STEP-4.5
    for j in range(1):
        for i in reversed(df.index):

            if True:

                if df['Grower'][i] != '-' and df['HIT'][i] != '-' and df['LLE'][i] != '-' and df['TR'][i] != '-':

                    if allocation[df['Grower'][i]] - MBR[df['Grower'][i]] >= 0:
                        x1 = allocation[df['Grower'][i]] - MBR[df['Grower'][i]]
                    else:
                        x1 = 0

                    if allocation[df['HIT'][i]] - MBR[df['HIT'][i]] >= 0:
                        x2 = allocation[df['HIT'][i]] - MBR[df['HIT'][i]]
                    else:
                        x2 = 0

                    if allocation[df['LLE'][i]] - MBR[df['LLE'][i]] >= 0:
                        x3 = allocation[df['LLE'][i]] - MBR[df['LLE'][i]]
                    else:
                        x3 = 0

                    if allocation[df['TR'][i]] - MBR[df['TR'][i]] >= 0:
                        x4 =  \
                            allocation[df['TR'][i]] - \
                            MBR[df['TR'][i]]
                    else:
                        x4 = 0

                    x = min(x1, x2, x3, x4, df['Qty'][i])

                    df['Qty'][i] -= x
                    allocation[df['HIT'][i]] -= x
                    allocation[df['LLE'][i]] -= x
                    allocation[df['Grower'][i]] -= x
                    allocation[df['TR'][i]] -= x
                    rt_plant_demand += x
                    rt_capacity[df['HIT'][i]] += x
                    rt_capacity[df['LLE'][i]] += x
                    rt_capacity[df['Grower'][i]] += x
                    rt_capacity[df['TR'][i]] += x

                elif df['Grower'][i] != '-' and df['HIT'][i] != '-':

                    if allocation[df['Grower'][i]] - MBR[df['Grower'][i]] >= 0:
                        x1 = allocation[df['Grower'][i]] - MBR[df['Grower'][i]]
                    else:
                        x1 = 0
                    if allocation[df['HIT'][i]] - MBR[df['HIT'][i]] >= 0:
                        x2 = allocation[df['HIT'][i]] - MBR[df['HIT'][i]]
                    else:
                        x2 = 0

                    x = min(x1, x2, df['Qty'][i])

                    df['Qty'][i] -= x
                    allocation[df['HIT'][i]] -= x
                    allocation[df['Grower'][i]] -= x
                    rt_plant_demand += x
                    rt_capacity[df['HIT'][i]] += x
                    rt_capacity[df['Grower'][i]] += x

        for i in df.index:

            if True:

                if df['Grower'][i] != '-' and df['HIT'][i] != '-' and df['LLE'][i] != '-' and df['TR'][i] != '-':

                    x = min(rt_capacity[df['Grower'][i]], rt_capacity[df['HIT'][i]],
                            rt_capacity[df['LLE'][i]], rt_capacity[df['TR'][i]], rt_plant_demand)

                    df['Qty'][i] += x
                    rt_plant_demand -= x

                    rt_capacity[df['Grower'][i]] -= x
                    rt_capacity[df['HIT'][i]] -= x
                    rt_capacity[df['LLE'][i]] -= x
                    rt_capacity[df['TR'][i]] -= x

                    allocation[df['Grower'][i]] += x
                    allocation[df['HIT'][i]] += x
                    allocation[df['LLE'][i]] += x
                    allocation[df['TR'][i]] += x

                elif df['Grower'][i] != '-' and df['HIT'][i] != '-':

                    x = min(rt_capacity[df['Grower'][i]],
                            rt_capacity[df['HIT'][i]], rt_plant_demand)

                    df['Qty'][i] += x
                    rt_plant_demand -= x

                    rt_capacity[df['Grower'][i]] -= x
                    rt_capacity[df['HIT'][i]] -= x

                    allocation[df['Grower'][i]] += x
                    allocation[df['HIT'][i]] += x

    # STEP-6 : Recalculate required RB according to remaining CB demand

    # remaining_CB_demand = Plant_demand - df['CB Qty'].sum()
    # print(remaining_CB_demand)
    # f = True
    # while remaining_CB_demand > 0 and f == True:
    #     c = 0
    #     RB_required = round(remaining_CB_demand * RB_CB_Ratio)

    #     for i in df.index:

    #         if df['IS'][i] == '-':

    #             if df['Grower'][i] != '-' and df['HIT'][i] != '-' and df['LLE'][i] != '-' and df['TR'][i] != '-':

    #                 x = min(rt_capacity[df['Grower'][i]], rt_capacity[df['HIT'][i]], rt_capacity[df['LLE'][i]], round(RB_CB_Ratio*rt_capacity[df['TR'][i]]), RB_required)

    #                 x -= (x + df['RB Qty'][i]) % 2

    #                 if x + df['RB Qty'][i] < MOQ[df['HIT'][i]]:

    #                     df['RB Qty'][i] = 0
    #                     continue

    #                 rt_capacity[df['Grower'][i]] -= x
    #                 rt_capacity[df['HIT'][i]] -= x
    #                 rt_capacity[df['LLE'][i]] -= x
    #                 rt_capacity[df['TR'][i]] -= round(x/RB_CB_Ratio)
    #                 RB_required -= x
    #                 df['RB Qty'][i] += x
    #                 y = round(x / RB_CB_Ratio) - round(x/RB_CB_Ratio)%2
    #                 df['CB Qty'][i] += y
    #                 remaining_CB_demand -= y

    #                 if y != 0:

    #                     c+=1

    #             elif df['Grower'][i] != '-' and df['HIT'][i] != '-':

    #                 x = min(rt_capacity[df['Grower'][i]], rt_capacity[df['HIT'][i]], RB_required)

    #                 x -= (x + df['RB Qty'][i]) % 2

    #                 if x + df['RB Qty'][i] < MOQ[df['HIT'][i]]:

    #                     df['RB Qty'][i] = 0
    #                     continue

    #                 rt_capacity[df['Grower'][i]] -= x
    #                 rt_capacity[df['HIT'][i]] -= x
    #                 RB_required -= x
    #                 df['RB Qty'][i] += x
    #                 y = round(x / RB_CB_Ratio) - round(x/RB_CB_Ratio)%2
    #                 df['CB Qty'][i] += y
    #                 remaining_CB_demand -= y

    #                 if y != 0:

    #                     c+=1

    #     if c == 0:

    #         f = False
    # print(rt_plant_demand, remaining_CB_demand, rt_IS_demand)

    # # return [df, rt_MBR, rt_capacity, rt_plant_demand, rt_IS_demand, rt_capacity]

    # df = df.sort_values(by='S.No.')
    return [df, rt_MBR, rt_capacity, rt_plant_demand]


def Route_Optimization(file, Plant_demand):

    # reading excel file
    df = pd.read_excel(file, sheet_name='Combinations_Data')
    g_con = pd.read_excel(file, sheet_name='Grower_Constraints')
    h_con = pd.read_excel(file, sheet_name='HIT_Constraints')
    l_con = pd.read_excel(file, sheet_name='LLE_Constraints')
    t_con = pd.read_excel(file, sheet_name='Transporter_Constraints')

    df['Qty'] = 0

    # creating dictionaries to store constraints
    capacity = {}

    MBR = {}

    # calculating MBR for each stakeholder
    # total_grower_capacity = g_con['Capacity'].sum()
    # total_hit_capacity = h_con['Capacity'].sum()
    # total_lle_capacity = l_con['capacity'].sum()
    # total_tr_capacity = t_con['Capacity'].sum()

    for i in g_con.index:
        # g_con['MBR'][i] = round ( (total_MBR * g_con['Capacity'][i]) / total_grower_capacity )
        capacity[g_con['Grower'][i]] = g_con['Capacity'][i]
        MBR[g_con['Grower'][i]] = g_con['MBR'][i]

    for i in h_con.index:
        # h_con['MBR'][i] = round ( (total_MBR * h_con['Capacity'][i]) / total_hit_capacity )
        MBR[h_con['HIT'][i]] = h_con['MBR'][i]
        capacity[h_con['HIT'][i]] = h_con['Capacity'][i]

    for i in l_con.index:
        # l_con['MBR'][i] = round ( (total_MBR * l_con['capacity'][i]) / total_lle_capacity )
        MBR[l_con['LLE'][i]] = l_con['MBR'][i]
        capacity[l_con['LLE'][i]] = l_con['Capacity'][i]

    for i in t_con.index:
        # t_con['MBR'][i] = round ( (total_MBR * t_con['Capacity'][i]) / total_tr_capacity )
        MBR[t_con['Transporter'][i]] = t_con['MBR'][i]
        capacity[t_con['Transporter'][i]] = t_con['Capacity'][i]

    # calculating total per ton cost for each route
    for i in df.index:

        df['Landed Cost'][i] = (df['TR cost/ton'][i] + df['Plant Chippin cost/ton'][i]) + (
            df['RB cost /ton'][i] + df['HIT cost/ton'][i] + df['LLE cost/ton'][i])

    result_df = Route_optimization_logic(MBR, capacity, Plant_demand, df)
    df = result_df[0]
    rt_MBR = result_df[1]
    rt_capacity = result_df[2]
    rt_plant_demand = result_df[3]

    df = df.drop(columns=['RB cost /ton', 'HIT cost/ton', 'LLE cost/ton',
                 'TR cost/ton', 'Plant Chippin cost/ton'])

    df.to_excel('result.xlsx')

    alloc = {}

    for i in df.index:

        df['Total cost'][i] = df['Landed Cost'][i] * df['Qty'][i]

        if df['Grower'][i] != '-':
            if df['Grower'][i] not in alloc:
                alloc[df['Grower'][i]] = int(df['Qty'][i])
            else:
                alloc[df['Grower'][i]] += int(df['Qty'][i])

        if df['HIT'][i] != '-':
            if df['HIT'][i] not in alloc:
                alloc[df['HIT'][i]] = int(df['Qty'][i])
            else:
                alloc[df['HIT'][i]] += int(df['Qty'][i])

        if df['LLE'][i] != '-':
            if df['LLE'][i] not in alloc:
                alloc[df['LLE'][i]] = int(df['Qty'][i])
            else:
                alloc[df['LLE'][i]] += int(df['Qty'][i])

        if df['TR'][i] != '-':
            if df['TR'][i] not in alloc:
                alloc[df['TR'][i]] = int(df['Qty'][i])
            else:
                alloc[df['TR'][i]] += int(df['Qty'][i])
    remaining_plant_demand = Plant_demand - df['Qty'].sum()

    return [df, alloc, MBR, remaining_plant_demand]


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


def Allocation(df, alloc, MBR):

    RA_MBR = {}
    remaining_MBR = dict()

    for i in alloc:
        RA_MBR[i] = str(MBR[i]).split('.')[0]

        if int(alloc[i]) >= int(RA_MBR[i]):
            remaining_MBR[i] = 0
        else:
            remaining_MBR[i] = str(
                int(RA_MBR[i]) - int(alloc[i])).split('.')[0]

    data = {'Stakeholders': alloc.keys(), 'Allocation': alloc.values(
    ), 'MBR': RA_MBR.values(), 'Remaining_MBR': remaining_MBR.values()}

    df2 = pd.DataFrame(data)

    for i in df2.index:
        df2['Allocation'][i] = str(df2['Allocation'][i]).split('.')[0]

    return df2


def dashboard(file, df, remaining_plant_demand):

    g_con = pd.read_excel(file, sheet_name='Grower_Constraints')
    h_con = pd.read_excel(file, sheet_name='HIT_Constraints')
    l_con = pd.read_excel(file, sheet_name='LLE_Constraints')
    t_con = pd.read_excel(file, sheet_name='Transporter_Constraints')

    total_growers = len(g_con)
    total_hits = len(h_con)
    total_lles = len(l_con)
    total_trs = len(t_con)

    total_cost = sum(list(map(int, (df['Total cost']))))

    total_cost = str(total_cost).split('.')[0]
    total_growers = str(total_growers).split('.')[0]
    total_hits = str(total_hits).split('.')[0]
    total_lles = str(total_lles).split('.')[0]
    total_trs = str(total_trs).split('.')[0]

    data = {'Growers': total_growers, 'HITs': total_hits, 'LLEs': total_lles, 'TRs': total_trs, 'Total cost': total_cost,
            'Remaining Plant Demand': remaining_plant_demand}
    df2 = pd.DataFrame(columns=['Growers', 'HITs', 'LLEs', 'TRs', 'Total cost',
                       'Remaining Plant Demand'])
    df2 = df2.append(data, ignore_index=True)

    df2.to_excel('result.xlsx')

    return df2
