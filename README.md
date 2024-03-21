Introduction:

PhonePe has become one of the most popular digital payment platforms in India, with millions of users relying on it for their day-to-day transactions. The app is known for its simplicity, user-friendly interface, and fast and secure payment processing. It has also won several awards and accolades for its innovative features and contributions to the digital payments industry.

We create a web app to analyse the Phonepe transaction and users depending on various Years, Quarters, States, and Types of transaction and give a Geographical and Geo visualization output based on given requirements.

About PhonePe-Pulse Data:

This data has been structured to provide details of following three sections with data cuts on Transactions, Users and Insurance of PhonePe Pulse - Explore tab.

Aggregated - Aggregated values of various payment categories as shown under Categories section
Map - Total values at the State and District levels.
Top - Totals of top States / Districts /Pin Codes
All the data provided in these folders is of JSON format.

Requisites:

Python -- Programming Language
plotly -- Python Module that is used for data visualization and supports various graphs
pandas -- Python Library for Data Visualization
streamlit -- Python framework to rapidly build and share beautiful machine learning and data science web apps
git.repo.base -- Python Module that helps to clone the github Repository and the store the data locally
mysql.connector -- Python Library that enables Python programs to access MySQL databases
json -- Python Library that helps parse JSON into a Python dictionary/list, in short open JSON files using Python
os -- Python Module that provides functions for interacting with the operating system

Installation:

To run this project, you need to install the following packages:

git - https://git-scm.com/downloads

 pip install pandas
 pip install psycopg2
 pip install requests
 pip install streamlit
 pip install plotly

Installing and Importing the required Libraries:
  
Firstly install all the required extensions/libraries/modules given above, if not installed

pip install (name of the library/module)

After installing the required libraries one need to import them in the program before one can use them.

import streamlit as st
import psycopg2
import requests
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import os
import json

Features:

Data Collection: 
Clone PhonePe Pulse data from the GitHub repository to your local directory for seamless access. Streamline your data collection process effortlessly. Explore a rich variety of insightful metrics and analytics, empowering you with comprehensive information. Make informed decisions with up-to-date data, ensuring precision in your analyses and strategies.

Data Overview:
Immerse yourself in a detailed exploration of the collected data. Gain comprehensive insights with breakdowns by states, years, quarters, transaction types, and user devices. This thorough analysis empowers you to make informed decisions based on a nuanced understanding of the dataset. Uncover trends, patterns, and correlations that drive strategic planning. Elevate your data-driven approach with a wealth of information at your fingertips.

Migrating Data to SQL Database: 
Simplify your workflow by seamlessly converting PhonePe Pulse data from JSON to a structured DataFrame. Effortlessly store the organized data in a PostgreSQL Database, ensuring optimal accessibility and efficiency. This streamlined process facilitates easier querying and analysis. Take advantage of a robust foundation for your data-driven applications and insights.

Interactive Streamlit Interface:
Unleash the power of data exploration through our Streamlit app. The intuitive interface facilitates seamless interaction with dynamic charts, allowing users to customize visualizations and apply filters. Effortlessly zoom in or out to delve into specific nuances of your analysis. Empower your data-driven decisions with a user-friendly and adaptable platform.

Dynamic Visualizations with Plotly:
Unlock the potential of Plotly to generate an array of charts, from dynamic line charts to insightful bar charts, and pie charts. Dive into your data with these visualizations, gaining a deeper understanding and effortlessly identifying patterns, trends, and correlations. Plotly's robust features empower users to create compelling visuals that enhance data exploration and analysis.

Data Exploration:
Embark on a dynamic analytical journey with our interactive Plotly charts and maps. Delve into nuanced insights across states, years, quarters, districts, transaction types, and user brands. Navigate seamlessly through a wealth of information, gaining a comprehensive understanding of your data landscape. Uncover patterns and trends that empower informed decision-making, making your exploration both insightful and user-friendly.

Live Geo Visualization Dashboard:
Elevate your data exploration with a dynamic geo-visualization dashboard crafted using Streamlit and Plotly. Interact seamlessly with live maps, gaining real-time insights and unlocking the full potential of your geographical data. Effortlessly navigate through the interactive features to enhance your understanding and make informed decisions based on the latest information.

Top Performers Highlight:
Effortlessly discern the top 10 states, districts, and pincodes through user-friendly visualizations. Engage with ease using our intuitive Streamlit dashboard, designed for seamless exploration. Navigate through insightful charts and graphs to glean actionable insights, empowering you to make informed decisions. Simplify your data-driven strategy by focusing on key performance indicators, ensuring a comprehensive understanding of top performers.

Data-Driven Decision Making:
Elevate your decision-making prowess by leveraging insights from PhonePe Pulse data uncover valuable trends, patterns, and statistics. Navigate confidently through a sea of information, ensuring each decision is fortified with robust, data-driven analysis. Empower your strategies with actionable intelligence, transforming raw data into a powerful tool for informed and impactful choices. Make every decision count with the precision and confidence derived from a data-rich foundation.

Conclusion:

Phonepe Pulse Data based on the provided functions and data visualization capabilities, the conclusion of the project could involve insights derived from the data analysis. These insights could include patterns in transaction behavior, user demographics, geographical trends, and exploration, top-performing regions or transaction types.
