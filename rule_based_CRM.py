import numpy as np
import pandas as pd
import seaborn as sns
pd.pandas.set_option('display.max_columns', None)

#Import
dff= pd.read_csv("github/persona.csv",sep=",")

def check_df(dataframe, head=5):
    """
    Task: Gives a brief explanation for the data
    Params:
    dataframe: dataframe
    head= The number of rows to return.Default is 5.
    """
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
check_df(dff)

###############Understanding Data############################

dff["SOURCE"].nunique() # number of unique source
dff["SOURCE"].value_counts() #source frequencies
dff["PRICE"].nunique() #number of unique prices
dff["PRICE"].value_counts() #price frequencies
dff.groupby("COUNTRY")["SOURCE"].count() #number of sales for each country
dff.groupby("COUNTRY")["PRICE"].sum() #total sales for each country
dff.groupby("SOURCE")["PRICE"].count() # number of sales for each source
dff["SOURCE"].value_counts() #source frequencies
dff.groupby("COUNTRY")["PRICE"].mean() #price means for each country
dff.groupby("SOURCE").agg({"PRICE":"mean"}) #price means for each source
dff.groupby(["COUNTRY","SOURCE"])["PRICE"].mean()  #PRICE averages in the COUNTRY-SOURCE breakdown?

####################CRM Step By Step ########################
#Total earning in COUNTRY, SOURCE, SEX, AGE breakdown,
agg_df=dff.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE":"sum"}).sort_values("PRICE")
agg_df=agg_df.reset_index()  # give  new indexes for teh new data
agg_df.head()

#Creating age ranges and adding to data
agg_df["NEW_AGE"] = pd.cut(agg_df["AGE"], [0, 19, 24, 31, 41, 70],labels=["0_19", "19_24", "24_31", "31_41", "41_70"])

#Creating  customer_level_based column by combining country& source& sex& new_age
agg_df["customers_level_based"]=[str(agg_df.iloc[i, 0]) + "_" + str(agg_df.iloc[i, 1]) + "_" + str(agg_df.iloc[i, 2]) + "_" + str(agg_df.iloc[i, 5]) for i, row in agg_df.iterrows()]
agg_df=agg_df.groupby("customers_level_based").agg({"PRICE":"mean"}) #group data according to customer_level_based  and calulate the mean of the earnings
agg_df=agg_df.reset_index()

#Segmentation according to price
agg_df["SEGMENT"] =pd.qcut(agg_df["PRICE"],4,labels=["D","C","B","A"])

#Description for the segmentation
agg_df[["SEGMENT","PRICE"]].groupby("SEGMENT").agg(["min","max","mean","sum"])

#Analysis of C segment
c_segment=agg_df[agg_df["SEGMENT"]=="C"]
c_segment[["SEGMENT","PRICE"]].groupby("SEGMENT").agg(["min","max","mean","sum"])

# Age:33 Source: ANDROID Country:TUR , find the segment and average earning from this user
new_user="TUR_ANDROID_FEMALE_31_41"
agg_df[agg_df["customers_level_based"] == new_user]["SEGMENT"].item()
agg_df[agg_df["customers_level_based"] == new_user]["PRICE"].item()

# Age:35 Source: IOS  Country: FRA , find the segment  and average earning from this user.
new_user="FRA_IOS_FEMALE_31_41"
agg_df[agg_df["customers_level_based"] == new_user]["SEGMENT"].item()
agg_df[agg_df["customers_level_based"] == new_user]["PRICE"].item()
