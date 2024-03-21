import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import json
import requests
from PIL import Image
import sys
sys.setrecursionlimit(10000)



#Dataframe creation

#Sql connection
myconnection=psycopg2.connect(host="localhost",
                              user="postgres",
                              password="0726",
                              database="phonepe_data",
                              port="5432")

cursor=myconnection.cursor()

#aggre_insus_df
cursor.execute("SELECT * FROM aggregated_insurance")
myconnection.commit()
table_1 = cursor.fetchall()

Aggre_insurance = pd.DataFrame(table_1, columns=("State", "Year", "Quarter", "Transaction_type",
                                                 "Transaction_count", "Transaction_amount"))

#aggre_trans_df
cursor.execute("SELECT * FROM aggregated_transaction")
myconnection.commit()
table_2 = cursor.fetchall()

Aggre_transaction = pd.DataFrame(table_2, columns=("State", "Year", "Quarter", "Transaction_type",
                                                 "Transaction_count", "Transaction_amount"))

#aggre_users_df
cursor.execute("SELECT * FROM aggregated_users")
myconnection.commit()
table_3 = cursor.fetchall()

Aggre_users = pd.DataFrame(table_3, columns=("State", "Year", "Quarter", "Brands",
                                                 "User_Count", "User_Percentage"))

#map_insus
cursor.execute("SELECT * FROM map_insurance")
myconnection.commit()
table_4 = cursor.fetchall()

map_insurance = pd.DataFrame(table_4, columns=("State", "Year", "Quarter",  "District",
                                                 "Transaction_count", "Transaction_amount"))

#map_trans
cursor.execute("SELECT * FROM map_transaction")
myconnection.commit()
table_5 = cursor.fetchall()

map_transaction = pd.DataFrame(table_5, columns=("State", "Year", "Quarter",  "District",
                                                 "Transaction_count", "Transaction_amount"))

#map_users
cursor.execute("SELECT * FROM map_users")
myconnection.commit()
table_6 = cursor.fetchall()

map_users = pd.DataFrame(table_6, columns=("State", "Year", "Quarter",  "District",
                                                 "Registered_User","AppOpens"))

#top_insus
cursor.execute("SELECT * FROM top_insurance")
myconnection.commit()
table_7 = cursor.fetchall()

top_insurance = pd.DataFrame(table_7, columns=("State", "Year", "Quarter", "pincodes",
                                                 "Transaction_count","Transaction_amount"))

#top_trans
cursor.execute("SELECT * FROM top_transaction")
myconnection.commit()
table_8 = cursor.fetchall()

top_transaction = pd.DataFrame(table_8, columns=("State", "Year", "Quarter", "pincodes",
                                                 "Transaction_count","Transaction_amount"))

#top_user
cursor.execute("SELECT * FROM top_users")
myconnection.commit()
table_9 = cursor.fetchall()

top_users = pd.DataFrame(table_9, columns=("State", "Year", "Quarter", "pincodes",
                                                 "Registered_Userst"))


#Functions

def Transaction_amount_count_Y(df, year):
    tacy = df[df ["Year"]== year]
    tacy.reset_index(drop = True, inplace = True)

    tacyg = tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1,col2 =st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x="State", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                            height= 650, width= 600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x="State", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650, width= 600)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1 = json.loads(response.content)
        states_name =[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations= "State", featureidkey= "properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale = "Reds",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="State", title=f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600, width= 600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    
    with col2:
        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations= "State", featureidkey= "properties.ST_NM",
                                color="Transaction_count", color_continuous_scale = "Reds",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name="State", title=f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height= 600, width= 600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

def Transaction_amount_count_Y_Q(df, quarter):
    tacy = df[df["Quarter"]==quarter]
    tacy.reset_index(drop = True, inplace = True)

    tacyg = tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1,col2 =st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x="State", y="Transaction_amount", title=f"{tacy['Year'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        height= 650, width= 600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x="State", y="Transaction_count", title=f"{tacy['Year'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650, width= 600)
        st.plotly_chart(fig_count)
    
    col1,col2 =st.columns(2)
    with col1:
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1 = json.loads(response.content)
        states_name =[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations= "State", featureidkey= "properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale = "pinkyl",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="State", title=f"{tacy['Year'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600, width= 600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    
    with col2:
        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations= "State", featureidkey= "properties.ST_NM",
                                color="Transaction_count", color_continuous_scale = "pinkyl",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name="State", title=f"{tacy['Year'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                height= 600, width= 600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy
    

def Aggre_Tran_Transaction_type(df,state):
    
    tacy = df[df["State"]==state]
    tacy.reset_index(drop = True, inplace = True)

    tacyg = tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1,col2 =st.columns(2)
    with col1:
        fig_pie_1 = px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount",
                        width= 600, title= f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2 = px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count",
                        width= 600, title=f"{state.upper()} TRANSACTION COUNT", hole= 0.5)
        st.plotly_chart(fig_pie_2)    

def Aggre_user_plot_1(df,year):
    aguy = df[df["Year"]== year]
    aguy.reset_index(drop = True, inplace = True)

    aguyg = aguy.groupby("Brands")[["User_Count"]].sum()
    aguyg.reset_index(inplace = True)

    fig_bar_1 = px.bar(aguyg, x="Brands", y="User_Count", title = f"{year} Brands And User Count",
                      width = 800, color_discrete_sequence= px.colors.sequential.haline, hover_name ="Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguy


#Aggre_user_Quarter
def Aggre_user_plot_2(df, quarter):
    aguyq = df[df["Quarter"]== quarter]
    aguyq.reset_index(drop = True, inplace = True)

    aguyqg= aguyq.groupby("Brands")[["User_Count"]].sum()
    aguyqg.reset_index(inplace = True)

    fig_bar_1 = px.bar(aguyqg, x="Brands", y="User_Count", title = f"{quarter} Quarter Brands And User Count",
                          width = 800, color_discrete_sequence= px.colors.sequential.Pinkyl_r, hover_name ="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq

#Aggre_user_state
def Aggre_user_plot_3(df, state):
    auyqs = df[df["State"] ==state]
    auyqs.reset_index(drop =True, inplace = True)

    fig_line_1 = px.line(auyqs, x= "Brands", y= "User_Count", hover_data= "User_Percentage",
                        title = f"{state} BRANDS, USER COUNT, PERCENTAGE", width=800, markers = True)
    st.plotly_chart(fig_line_1)

#map_insus_district
def Map_insus_District(df,state):
    
    tacy = df[df["State"]==state]
    tacy.reset_index(drop = True, inplace = True)

    tacyg = tacy.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1,col2 =st.columns(2)
    with col1:
        fig_bar_1 = px.bar(tacyg, x="Transaction_amount", y= "District", orientation="h", height=600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT",color_discrete_sequence= px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2 =px.bar(tacyg, x="Transaction_count", y= "District", orientation="h", height=600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT",color_discrete_sequence= px.colors.sequential.Purples_r)
        st.plotly_chart(fig_bar_2)


#map user plot 1
def map_user_plot_1(df, year):
    muy = df[df["Year"]== year]
    muy.reset_index(drop = True, inplace = True)

    muyg = muy.groupby("State")[["Registered_User","AppOpens"]].sum()
    muyg.reset_index(inplace = True)

    fig_line_1 = px.line(muyg, x= "State", y= ["Registered_User","AppOpens"],color_discrete_map={"Registered_User": "blue", "AppOpens": "green"},
                        title = f"{year} REGISTERED USER AND APPOPENS", width=800,height=800, markers= True)
    st.plotly_chart(fig_line_1)
    
    return muy


#map_user_plot_2
def map_user_plot_2(df, quarter):
    muyq = df[df["Quarter"]== quarter]
    muyq.reset_index(drop = True, inplace = True)

    muyqg = muyq.groupby("State")[["Registered_User","AppOpens"]].sum()
    muyqg.reset_index(inplace = True)

    fig_line_1 = px.line(muyqg, x= "State", y= ["Registered_User","AppOpens"], color_discrete_map={"Registered_User": "red", "AppOpens": "blue"},
                        title = f"{df['Year'].min()} yr {quarter} QUARTER REGISTERED USER AND APPOPENS", width=800,height=800, markers= True)
    st.plotly_chart(fig_line_1)
    
    return muyq


#map_user_plot_3
def map_user_plot_3(df, state):
    muyqs = df[df["State"]== state]
    muyqs.reset_index(drop = True, inplace = True)
    
    col1,col2 =st.columns(2)
    with col1:
        fig_map_user_bar_1 = px.bar(muyqs, x="Registered_User", y="District", orientation="h",
                                    title = f"{state.upper()} REGISTERED USER",height = 700,width=650,
                                color_discrete_sequence= px.colors.sequential.Magenta_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2 = px.bar(muyqs, x="AppOpens", y="District", orientation="h",
                                    title = f"{state.upper()} APPOPENS",height = 700,width=650,
                                color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)

#top_insus_plot_1
def top_insus_plot_1(df,state):
    tiy = df[df["State"]== state]
    tiy.reset_index(drop = True, inplace = True)

    tiyg = tiy.groupby("pincodes")[["Transaction_count","Transaction_amount"]].sum()
    tiyg.reset_index(inplace = True)

    col1,col2 =st.columns(2)
    with col1:
        fig_top_insus_bar_1 = px.bar(tiy, x="Quarter", y="Transaction_amount", hover_data="pincodes",
                                        title = f"{state.upper()} TRANSACTION AMOUNT",height = 650,width=600,
                                    color_discrete_sequence= px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insus_bar_1)    

    with col2:
        fig_top_insus_bar_2 = px.bar(tiy, x="Quarter", y="Transaction_count", hover_data="pincodes",
                                        title = f"{state.upper()} TRANSACTION COUNT",height = 650,width=600,
                                    color_discrete_sequence= px.colors.sequential.Agsunset)
        st.plotly_chart(fig_top_insus_bar_2)

#top_user_plot-1
def top_user_plot_1(df, year):
    tuy = df[df["Year"] == year]
    tuy.reset_index(drop=True, inplace=True)

    tuyg = pd.DataFrame(tuy.groupby(["State", "Quarter"])["Registered_Userst"].sum())
    tuyg.reset_index(inplace=True)
    
    fig_top_plot_1 = px.bar(tuyg, x="State",  y="Registered_Userst", color="Quarter",
                            width=800,  height=800, color_discrete_sequence=px.colors.sequential.Burgyl_r, 
                            hover_name="State", title=f"{year} REGISTERED USER")
    st.plotly_chart(fig_top_plot_1)
    return tuy


#top_user_plot_2
def top_user_plot_2(df, state):
    tuys=df[df["State"]== state]
    tuys.reset_index(drop = True, inplace = True)

    fig_top_plot_2 = px.bar(tuys, x= "Quarter", y= "Registered_Userst", title="REGISTERED USER PINCODES QUARTER",
                           width= 1000, height=800, color="Registered_Userst", hover_data= "pincodes",
                           color_continuous_scale = px.colors.sequential.Pinkyl)
    st.plotly_chart(fig_top_plot_2)


#sql plot1 
def top_chart_trans_amount(table_name):
    myconnection=psycopg2.connect(host="localhost",
                                  user="postgres",
                                  password="0726",
                                  database="phonepe_data",
                                  port="5432")

    cursor=myconnection.cursor()
    #plot1
    query1 =f'''select state, SUM(transaction_amount) AS transaction_amount 
                FROM {table_name}
                GROUP BY state
                ORDER BY transaction_amount DESC
                limit 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    myconnection.commit()

    df_1 = pd.DataFrame(table_1, columns=("state", "transaction_amount"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount_1 = px.bar(df_1, x="state", y="transaction_amount", title="TOP 10 OF TRANSACTION AMOUNT",hover_name ="state",
                            height= 650, width= 600, color_discrete_sequence=px.colors.sequential.Sunset_r)
        st.plotly_chart(fig_amount_1)

    #plot2
    query2 =f'''select state, SUM(transaction_amount) AS transaction_amount 
                FROM {table_name}
                GROUP BY state
                ORDER BY transaction_amount
                limit 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    myconnection.commit()

    df_2 = pd.DataFrame(table_2, columns=("state", "transaction_amount"))

    with col2:
        fig_amount_2 = px.bar(df_2, x="state", y="transaction_amount", title="BELOW 10 OF TRANSACTION AMOUNT",hover_name ="state",
                            height= 650, width= 600, color_discrete_sequence=px.colors.sequential.Sunset_r)
        st.plotly_chart(fig_amount_2)

    #plot3
    query3 =f'''select state, AVG(transaction_amount) AS transaction_amount 
                FROM {table_name}
                GROUP BY state
                ORDER BY transaction_amount;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    myconnection.commit()

    df_3 = pd.DataFrame(table_3, columns=("state", "transaction_amount"))

    fig_amount_3 = px.bar(df_3, y="state", x="transaction_amount", title="AVERAGE OF TRANSACTION AMOUNT",hover_name ="state",orientation="h",
                           height= 800, width= 800, color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(fig_amount_3)


#sql plot2
def top_chart_trans_count(table_name):
    myconnection=psycopg2.connect(host="localhost",
                                  user="postgres",
                                  password="0726",
                                  database="phonepe_data",
                                  port="5432")

    cursor=myconnection.cursor()
    #plot1
    query1 =f'''select state, SUM(transaction_count) AS transaction_count 
                FROM {table_name}
                GROUP BY state
                ORDER BY transaction_count DESC
                limit 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    myconnection.commit()

    df_1 = pd.DataFrame(table_1, columns=("state", "transaction_count"))

    col1,col2 = st.columns(2)
    with col1:
        fig_count_1 = px.bar(df_1, x="state", y="transaction_count", title="TOP 10 OF TRANSACTION COUNT",hover_name ="state",
                            height= 650, width= 600, color_discrete_sequence=px.colors.sequential.Sunset_r)
        st.plotly_chart(fig_count_1)

    #plot2
    query2 =f'''select state, SUM(transaction_count) AS transaction_count 
                FROM {table_name}
                GROUP BY state
                ORDER BY transaction_count
                limit 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    myconnection.commit()

    df_2 = pd.DataFrame(table_2, columns=("state", "transaction_count"))

    with col2:
        fig_count_2 = px.bar(df_2, x="state", y="transaction_count", title="BELOW 10 OF TRANSACTION COUNT",hover_name ="state",
                            height= 650, width= 600, color_discrete_sequence=px.colors.sequential.Sunset_r)
        st.plotly_chart(fig_count_2)

    #plot3
    query3 =f'''select state, AVG(transaction_count) AS transaction_count 
                FROM {table_name}
                GROUP BY state
                ORDER BY transaction_count;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    myconnection.commit()

    df_3 = pd.DataFrame(table_3, columns=("state", "transaction_count"))

    fig_count_3 = px.bar(df_3, y="state", x="transaction_count", title="AVERAGE OF TRANSACTION COUNT",hover_name ="state",orientation="h",
                           height= 800, width= 800, color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(fig_count_3)


#sql plot3
def top_chart_top_trans_count(table_name):
    myconnection=psycopg2.connect(host="localhost",
                                  user="postgres",
                                  password="0726",
                                  database="phonepe_data",
                                  port="5432")

    cursor=myconnection.cursor()
    #plot1
    query1 =f'''select state, SUM(user_count) AS user_count 
                FROM {table_name}
                GROUP BY state
                ORDER BY user_count DESC
                limit 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    myconnection.commit()

    df_1 = pd.DataFrame(table_1, columns=("state", "user_count"))

    col1,col2 = st.columns(2)
    with col1:
        fig_count_1 = px.bar(df_1, x="state", y="user_count", title="TOP 10 OF USER COUNT",hover_name ="state",
                            height= 650, width= 600, color_discrete_sequence=px.colors.sequential.Sunset_r)
        st.plotly_chart(fig_count_1)

    #plot2
    query2 =f'''select state, SUM(user_count) AS user_count 
                FROM {table_name}
                GROUP BY state
                ORDER BY user_count
                limit 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    myconnection.commit()

    df_2 = pd.DataFrame(table_2, columns=("state", "user_count"))

    with col2:
        fig_count_2 = px.bar(df_2, x="state", y="user_count", title="BELOW 10 OF USER COUNT",hover_name ="state",
                            height= 650, width= 600, color_discrete_sequence=px.colors.sequential.Sunset_r)
        st.plotly_chart(fig_count_2)

    #plot3
    query3 =f'''select state, AVG(user_count) AS user_count 
                FROM {table_name}
                GROUP BY state
                ORDER BY user_count;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    myconnection.commit()

    df_3 = pd.DataFrame(table_3, columns=("state", "user_count"))

    fig_count_3 = px.bar(df_3, y="state", x="user_count", title="AVERAGE OF USER COUNT",hover_name ="state",orientation="h",
                           height= 800, width= 800, color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(fig_count_3)

#sql 
def top_chart_registered_user(table_name,state):
    myconnection=psycopg2.connect(host="localhost",
                                  user="postgres",
                                  password="0726",
                                  database="phonepe_data",
                                  port="5432")

    cursor=myconnection.cursor()
    #plot1
    query1 =f'''select district, sum(registered_user) as registered_user
                from  {table_name}
                where state = '{state}'
                group by district
                order by registered_user DESC
                limit 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    myconnection.commit()

    df_1 = pd.DataFrame(table_1, columns=("district", "registered_user"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount_1 = px.bar(df_1, x="district", y="registered_user", title="TOP 10 OF REGISTERED USER",hover_name ="district",
                            height= 650, width= 600, color_discrete_sequence=px.colors.sequential.Sunset_r)
        st.plotly_chart(fig_amount_1)

    #plot2
    query2 =f'''select district, sum(registered_user) as registered_user
                from  {table_name}
                where state = '{state}'
                group by district
                order by registered_user 
                limit 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    myconnection.commit()

    df_2 = pd.DataFrame(table_2, columns=("district", "registered_user"))

    with col2:
        fig_amount_2 = px.bar(df_2, x="district", y="registered_user", title="BELOW 10 OF REGISTERED USER",hover_name ="district",
                            height= 650, width= 600, color_discrete_sequence=px.colors.sequential.Sunset_r)
        st.plotly_chart(fig_amount_2)

    #plot3
    query3 =f'''select district, AVG (registered_user) as registered_user
                from  {table_name}
                where state = '{state}'
                group by district
                order by registered_user;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    myconnection.commit()

    df_3 = pd.DataFrame(table_3, columns=("district", "registered_user"))

    fig_amount_3 = px.bar(df_3, y="district", x="registered_user", title="AVERAGE OF REGISTERED USER",hover_name ="district",orientation="h",
                           height= 800, width= 600, color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(fig_amount_3)


#sql 
def top_chart_appopens(table_name,state):
    myconnection=psycopg2.connect(host="localhost",
                                  user="postgres",
                                  password="0726",
                                  database="phonepe_data",
                                  port="5432")

    cursor=myconnection.cursor()
    #plot1
    query1 =f'''select district, sum(appopens) as appopens
                from  {table_name}
                where state = '{state}'
                group by district
                order by appopens DESC
                limit 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    myconnection.commit()

    df_1 = pd.DataFrame(table_1, columns=("district", "appopens"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount_1 = px.bar(df_1, x="district", y="appopens", title="TOP 10 OF APP OPENS",hover_name ="district",
                            height= 650, width= 600, color_discrete_sequence=px.colors.sequential.Sunset_r)
        st.plotly_chart(fig_amount_1)

    #plot2
    query2 =f'''select district, sum(appopens) as appopens
                from  {table_name}
                where state = '{state}'
                group by district
                order by appopens 
                limit 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    myconnection.commit()

    df_2 = pd.DataFrame(table_2, columns=("district", "appopens"))
    
    with col2:
        fig_amount_2 = px.bar(df_2, x="district", y="appopens", title="BELOW 10 OF APP OPENS",hover_name ="district",
                            height= 650, width= 600, color_discrete_sequence=px.colors.sequential.Sunset_r)
        st.plotly_chart(fig_amount_2)

    #plot3
    query3 =f'''select district, AVG (appopens) as appopens
                from  {table_name}
                where state = '{state}'
                group by district
                order by appopens;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    myconnection.commit()

    df_3 = pd.DataFrame(table_3, columns=("district", "appopens"))

    fig_amount_3 = px.bar(df_3, y="district", x="appopens", title="AVERAGE OF APP OPENS",hover_name ="district",orientation="h",
                           height= 800, width= 600, color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(fig_amount_3)


#sql 
def top_chart_registered_userst(table_name):
    myconnection=psycopg2.connect(host="localhost",
                                  user="postgres",
                                  password="0726",
                                  database="phonepe_data",
                                  port="5432")

    cursor=myconnection.cursor()
    #plot1
    query1 =f'''select state, sum(registered_user) as registered_user
                from {table_name}
                group by state
                order by registered_user DESC
                limit 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    myconnection.commit()

    df_1 = pd.DataFrame(table_1, columns=("state", "registered_user"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount_1 = px.bar(df_1, x="state", y="registered_user", title="TOP 10 OF REGISTERED USER",hover_name ="state",
                            height= 650, width= 600, color_discrete_sequence=px.colors.sequential.Sunset_r)
        st.plotly_chart(fig_amount_1)

    #plot2
    query2 =f'''select state, sum(registered_user) as registered_user
                from {table_name}
                group by state
                order by registered_user
                limit 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    myconnection.commit()

    df_2 = pd.DataFrame(table_2, columns=("state", "registered_user"))

    with col2:
        fig_amount_2 = px.bar(df_2, x="state", y="registered_user", title="BELOW 10 OF REGISTERED USER",hover_name ="state",
                            height= 650, width= 600, color_discrete_sequence=px.colors.sequential.Sunset_r)
        st.plotly_chart(fig_amount_2)

    #plot3
    query3 =f'''select state, AVG (registered_user) as registered_user
                from {table_name}
                group by state
                order by registered_user;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    myconnection.commit()

    df_3 = pd.DataFrame(table_3, columns=("state", "registered_user"))

    fig_amount_3 = px.bar(df_3, y="state", x="registered_user", title="AVERAGE OF REGISTERED USER",hover_name ="state",orientation="h",
                           height= 800, width= 600, color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(fig_amount_3)




#Streamlit

st.set_page_config(layout="wide")
st.title ('Phonepe Pulse Data Visualization And Exploration')

st.sidebar.header(":wave: :violet[**Hello! Welcome to the dashboard**]")

with st.sidebar:

    selected = option_menu("Menu", ["Home","Explore Data","Top Charts"])

if selected =="Home":
    
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:\Users\ELCOT\Desktop\Phonepe\download.jpg"))
        st.image(Image.open(r"C:\Users\ELCOT\Desktop\Phonepe\download 1.png"))

    col3,col4= st.columns(2)
    
    with col3:
        st.video("C:\\Users\\ELCOT\\Desktop\\Phonepe\\bs-advertise.mp4")

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"C:\Users\ELCOT\Desktop\Phonepe\download 2.webp"),width=300)



elif selected =="Explore Data":

    tab1, tab2, tab3 =st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:
        method =st.radio("Select The Method",["Insurance Analysis","Transaction Analysis","User Analysis"])

        if method == "Insurance Analysis":

            col1,col2= st.columns(2)
            with col1:

                years =st.slider("Select The Year",Aggre_insurance["Year"].min(),Aggre_insurance["Year"].max(),Aggre_insurance["Year"].min())
            tac_Y = Transaction_amount_count_Y(Aggre_insurance, years)

            col1,col2 =st.columns(2)
            with col1:

                quarters =st.slider("Select The Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y, quarters)

        elif method == "Transaction Analysis":
            
            col1,col2= st.columns(2)
            with col1:

                years =st.slider("Select The Year",Aggre_transaction["Year"].min(),Aggre_transaction["Year"].max(),Aggre_transaction["Year"].min())
            Aggre_tran_tac_Y= Transaction_amount_count_Y(Aggre_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State", Aggre_tran_tac_Y["State"].unique())
            
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y,states)

            col1,col2 =st.columns(2)
            with col1:

                quarters =st.slider("Select The Quarter",Aggre_tran_tac_Y["Quarter"].min(),Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Aggre_tran_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Ty", Aggre_tran_tac_Y_Q["State"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q,states)

        elif method == "User Analysis":

            col1,col2= st.columns(2)
            with col1:

                years =st.slider("Select The Year",Aggre_users["Year"].min(),Aggre_users["Year"].max(),Aggre_users["Year"].min())
            Aggre_user_Y= Aggre_user_plot_1(Aggre_users, years)

            col1,col2 =st.columns(2)
            with col1:

                quarters =st.slider("Select The Quarter",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q = Aggre_user_plot_2(Aggre_user_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State", Aggre_user_Y_Q["State"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q, states)

    
    with tab2:

        method_2 = st.radio("Select The Method",["Map Insurance","Map Transaction","Map User"])

        if method_2 == "Map Insurance":
            
            col1,col2= st.columns(2)
            with col1:

                years =st.slider("Select The Year_mi",map_insurance["Year"].min(),map_insurance["Year"].max(),map_insurance["Year"].min())
            Map_insus_tac_Y= Transaction_amount_count_Y(map_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_mi", Map_insus_tac_Y["State"].unique())
            
            Map_insus_District(Map_insus_tac_Y,states)

            col1,col2 =st.columns(2)
            with col1:

                quarters =st.slider("Select The Quarter_mi",Map_insus_tac_Y["Quarter"].min(),Map_insus_tac_Y["Quarter"].max(),Map_insus_tac_Y["Quarter"].min())
            Map_insus_tac_Y_Q = Transaction_amount_count_Y_Q(Map_insus_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Mi", Map_insus_tac_Y_Q["State"].unique())

            Map_insus_District(Map_insus_tac_Y_Q,states)


        elif method_2 == "Map Transaction":
            
            col1,col2= st.columns(2)
            with col1:

                years =st.slider("Select The Year_mt",map_transaction["Year"].min(),map_transaction["Year"].max(),map_transaction["Year"].min())
            Map_trans_tac_Y= Transaction_amount_count_Y(map_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_mt", Map_trans_tac_Y["State"].unique())
            
            Map_insus_District(Map_trans_tac_Y,states)

            col1,col2 =st.columns(2)
            with col1:

                quarters =st.slider("Select The Quarter_mt",Map_trans_tac_Y["Quarter"].min(),Map_trans_tac_Y["Quarter"].max(),Map_trans_tac_Y["Quarter"].min())
            Map_trans_tac_Y_Q = Transaction_amount_count_Y_Q(Map_trans_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Mt", Map_trans_tac_Y_Q["State"].unique())

            Map_insus_District(Map_trans_tac_Y_Q,states)

        elif method_2 == "Map User":
            
            col1,col2= st.columns(2)
            with col1:

                years =st.slider("Select The Year_mu",map_users["Year"].min(),map_users["Year"].max(),map_users["Year"].min())
            Map_user_Y= map_user_plot_1(map_users, years)

            col1,col2 =st.columns(2)
            with col1:

                quarters =st.slider("Select The Quarter_mu",Map_user_Y["Quarter"].min(),Map_user_Y["Quarter"].max(),Map_user_Y["Quarter"].min())
            Map_user_Y_Q = map_user_plot_2(Map_user_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Mu", Map_user_Y_Q ["State"].unique())

            map_user_plot_3(Map_user_Y_Q ,states)

    
    with tab3:

        method_3 = st.radio("Select The Method",["Top Insurance","Top Transaction","Top User"])

        if method_3 == "Top Insurance":
            
            col1,col2= st.columns(2)
            with col1:

                years =st.slider("Select The Year_ti",top_insurance["Year"].min(),top_insurance["Year"].max(),top_insurance["Year"].min())
            Top_insus_tac_Y = Transaction_amount_count_Y(top_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_ti", Top_insus_tac_Y ["State"].unique())

            top_insus_plot_1(Top_insus_tac_Y ,states)

            col1,col2 =st.columns(2)
            with col1:

                quarters =st.slider("Select The Quarter_ti",Top_insus_tac_Y["Quarter"].min(),Top_insus_tac_Y["Quarter"].max(),Top_insus_tac_Y["Quarter"].min())
            top_insus_tac_Y_Q = Transaction_amount_count_Y_Q(Top_insus_tac_Y, quarters)

        elif method_3 == "Top Transaction":

            col1,col2= st.columns(2)
            with col1:

                years =st.slider("Select The Year_tt",top_transaction["Year"].min(),top_transaction["Year"].max(),top_transaction["Year"].min())
            Top_trans_tac_Y = Transaction_amount_count_Y(top_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_tt", Top_trans_tac_Y ["State"].unique())
            top_insus_plot_1(Top_trans_tac_Y ,states)

            col1,col2 =st.columns(2)
            with col1:

                quarters =st.slider("Select The Quarter_tt",Top_trans_tac_Y["Quarter"].min(),Top_trans_tac_Y["Quarter"].max(),Top_trans_tac_Y["Quarter"].min())
            top_trans_tac_Y_Q = Transaction_amount_count_Y_Q(Top_trans_tac_Y, quarters)

        elif method_3 == "Top User":

            col1,col2= st.columns(2)
            with col1:
                years =st.slider("Select The Year_tu",top_users["Year"].min(),top_users["Year"].max(),top_users["Year"].min())
            Top_user_Y= top_user_plot_1(top_users, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_tu", Top_user_Y ["State"].unique())
            top_user_plot_2(Top_user_Y ,states)

            

elif selected =="Top Charts":

    questions =st.selectbox("Select The Question",["1.Transaction Amount and Count of Aggregated Insurance",
                                                   "2.Transaction Amount and Count of Map Insurance",
                                                   "3.Transaction Amount and Count of Top Insurance",
                                                   "4.Transaction Amount and Count of Aggregated Transaction",
                                                   "5.Transaction Amount and Count of Map Transaction",
                                                   "6.Transaction Amount and Count of Top Transaction",
                                                   "7.Transaction Count of Aggregated User",
                                                   "8.Registered User of Map User",
                                                   "9.App Opens of Map User",
                                                   "10.Registered User of Top User",
                                                   ])
    
    if questions =="1.Transaction Amount and Count of Aggregated Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("aggregated_insurance")


    elif questions =="2.Transaction Amount and Count of Map Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("map_insurance")

    
    elif questions =="3.Transaction Amount and Count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("top_insurance")


    elif questions =="4.Transaction Amount and Count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("aggregated_transaction")


    elif questions =="5.Transaction Amount and Count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("map_transaction")


    elif questions =="6.Transaction Amount and Count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("top_transaction")


    elif questions =="7.Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        top_chart_top_trans_count("aggregated_users")

    
    elif questions =="8.Registered User of Map User":
        
        state = st.selectbox("Select The State", map_users["State"].unique())
        st.subheader("REGISTERED USER")
        top_chart_registered_user("map_users",state)


    elif questions =="9.App Opens of Map User":
        
        state = st.selectbox("Select The State", map_users["State"].unique())
        st.subheader("APP OPENS")
        top_chart_appopens("map_users",state)


    elif questions =="10.Registered User of Top User":
        
        st.subheader("REGISTERED USER")
        top_chart_registered_userst("map_users")