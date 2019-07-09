import re
import pandas as pd
import numpy as np
import json


def readData():
	colnames_airbnb = ['activity_type','activity_name','location','duration','includes','language','host_name','host_intro','price','cancel_policy','min_age','No_Ppl','rating','noRev','longtitude_al','links']
	airbnb1 = pd.read_csv("testrun_1.csv",header = None,names = colnames_airbnb)
	airbnb2 = pd.read_csv("testrun_2.csv",header = None,names = colnames_airbnb)
	airbnb3 = pd.read_csv("testrun_3.csv",header = None,names = colnames_airbnb)
	airbnb4 = pd.read_csv("testrun_4.csv",header = None,names = colnames_airbnb)
	airbnb5 = pd.read_csv("testrun_5.csv",header = None,names = colnames_airbnb)
	airbnb6 = pd.read_csv("testrun_6.csv",header = None,names = colnames_airbnb)
	airbnb7 = pd.read_csv("testrun_7.csv",header = None,names = colnames_airbnb)
	df = pd.concat([airbnb1,airbnb2,airbnb3,airbnb4,airbnb5,airbnb6,airbnb7])
	return df.drop_duplicates(subset='links', keep='first')


def str_int(x):
	return int(x)

def str_float(x):
	return float(x)

def cleanPrice(x):
	out = re.sub("\D", "", x)
	if (out == ""):
		return np.nan
	else:
		return float(out)


def cleanLanguage(x):
	txt = re.sub("(Offered\sin\s)|(\swelcome.*)","",x)
	txt = re.sub("\sand\s",",",txt)
	txt = re.sub(",\s",",",txt)
	return txt

def cleanIncludes(x):
	try:
		txt = re.sub("\sand\s",",",x)
		txt = re.sub(",\s",",",txt)
		return txt
	except:
		return x


def count_languages(x):
	if re.match("^All.*") is None:
		return len(x.split(','))
	else:
		return 0


def cleanNoRev(x):
	try:
		out = re.sub("\D", "", x)
		try:
			return float(out)
		except:
			print(f"second try failed: {out}")
			return np.nan
	except:
		return np.nan


def clean_calPolicy(x):
	out = re.sub("\D", "", x)
	if (out == ""):
		return np.nan
	else:
		return int(out)

def lat_creation(df,new_colname):
	temp = df.longtitude_al.apply(lambda x: x.split('=')[1])
	df[new_colname] = temp.apply(lambda x: float(re.findall("([-.0-9]+)",x)[0]))
	

	
def long_creation(df,new_colname):
	temp = df.longtitude_al.apply(lambda x: x.split('=')[1])
	df[new_colname] = temp.apply(lambda x: float(re.findall("([-.0-9]+)",x)[1]))


def language_count(df,new_colname):
	def helper(x):
		try:
			if re.match("^All.*",x) is None:
				return len(x.split(','))
			else:
				return 0
		except:
			print(x)
			return 0
	df[new_colname] = df.language.apply(lambda x: helper(x))


def includes_count(df,new_colname):
	def helper(x):
		if pd.isnull(x) == True:
			return 0
		else:
			return len(x.split(','))
	df[new_colname] = df.includes.apply(lambda x: helper(x))


def country_creation(df,new_colname):
    def country_finder(lat,long):
        geolocator = Nominatim()
        location = geolocator.reverse([lat, long], language="en")
        return location.raw['address'].get('country', np.nan)
    df[new_colname] = df.apply(lambda x: country_finder(x.latitude,x.longtitude), axis = 1)



def cleanDF(in_df):
	df = in_df.copy(deep=True)
	df.duration = df.duration.apply(lambda x: str_int(x))
	df.min_age = df.min_age.apply(lambda x: str_int(x))
	df.No_Ppl = df.No_Ppl.apply(lambda x: str_int(x))
	df.language = df.language.apply(lambda x: cleanLanguage(x))
	df.price = df.price.apply(lambda x: cleanPrice(x))
	df.cancel_policy = df.cancel_policy.apply(lambda x: clean_calPolicy(x))
	df.noRev = df.noRev.apply(lambda x: cleanNoRev(x))
	df.includes = df.includes.apply(lambda x: cleanIncludes(x))
	lat_creation(df,'latitude')
	long_creation(df,'longtitude')
	language_count(df,'language_count')
	includes_count(df,'includes_count')
	country_creation(df,"country")
	df['noRev'] = df['noRev'].fillna(0)
	df['rating'] = df['rating'].fillna(0)
	df = df.drop('longtitude_al', 1)
	df.rating = df.rating.apply(lambda x: str_float(x))
	df.noRev = df.noRev.apply(lambda x: str_float(x))
	return df