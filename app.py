import streamlit as st 
import pandas as pd 
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt 
import plotly.graph_objects as go
#import seaborn as sns 
#import altair as alt 
#import folium 
#from folium.plugins import HeatMap 


### Custom CSS for the sidebar background
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background: url("https://wallpapercave.com/wp/DM6hvet.jpg");
        background-size: cover    
    }
</style>
""", unsafe_allow_html=True)

#st.title('20th LIVESTOCK CENSUS - 2019')
new_title = '<p style="font-family:Berlin Sans FB;text-align: center; color:white; font-size: 80px;">20th LIVESTOCK CENSUS - 2019</p>'
st.markdown(new_title, unsafe_allow_html=True)
st.divider()

my_dataset = "C:/Users/91932/OneDrive/Desktop/dashboard/data/DATA_2019.csv"
df = pd.read_csv(my_dataset)

tab1, tab2, tab3, tab4 =st.tabs(['ABOUT DATA','VISUALIZATION','DASHBOARD','ANALYSIS'])

with tab1:
    c=st.container()
    c.header('DESCRIPTION')
    st.divider()
    c.write(' Livestock Census conducted in every five years in India. India has largest livestock numbers in the world.')
    c.write('data on details of Cattle, Buffalo, Sheep, Goat, Horse, Pony, Mule, Donkey, Camel and Pig in Rural and Urban combined at State and District level. 20th Livestock census covers the census of livestock, poultry, implements and machinery used for livestock rearing.')
    c.write('This dataset released under NATIONAL DATA SHARING & ACCESSIBILITY POLICY (NDSAP). \n contributed by Department of Animal Husbandry and Dairying & Ministry of Fisheries, Animal Husbandry and Dairying.')
    c.write('Domain : Open Government Data (OGD) Platform India')
    
    if st.checkbox('Show all column names'):
        st.text('COLUMNS :')
        st.write(df.columns)
    if st.checkbox('Preview Dataframe'):
        if st.button('Head'):
            st.write(df.head())
        if st.button('Tail'):
            st.write(df.tail())  
    if st.checkbox('Show all Dataframe'):
        st.dataframe(df)    
    if st.checkbox('SUMMARY OF DATA'):
        st.text('SUMMARY :') 
        st.write(df.describe())
        st.divider()
    if st.checkbox('INFORMATION OF DATA'):
        st.text('INFORMATION :') 
        st.write(df.info())    
    st.divider()
    #st.image('SURVEY ANIMAL.png')
   
with tab2:
    #1
    state=st.sidebar.selectbox('SELECT ONE STATE :',df['state_name'].unique())   
    st.title('STATE WISE TOTAL POULTRY OF EVERY DISTRICT')   
    df1 = df[df['state_name'] == state][['district_name','Total_poultry']]
    bar = px.bar(data_frame=df1, x='district_name', y='Total_poultry',
                 color_discrete_sequence=['indianred'])
    col1, col2 =st.columns(2)
    with col1:
        st.subheader('BAR PLOT')
        st.plotly_chart(bar , use_container_width=True) 
    with col2:    
        df1
    st.divider()
    #2
    st.title('DISTRICT WISE TOTAL COUNTS OF EACH ANIMALS IN SELECTED STATE')
    district = st.sidebar.selectbox('CHOOSE ONE DISTRICT :',df1['district_name'])
    df2 = df[df['district_name']==district][['cattle','buffalo','sheep','goat','horse','pony','mule','donkey','camel','pig']]
    df21=pd.DataFrame.transpose(df2)
    df21.columns=['counts']
    df21['animals']=['cattle','buffalo','sheep','goat','horse','pony','mule','donkey','camel','pig']
    pie1 = px.pie(df21,labels=['cattle','buffalo','sheep','goat','horse','pony','mule','donkey','camel','pig'],names='animals',
                   values='counts',color_discrete_sequence=px.colors.qualitative.Pastel)
    col1, col2 =st.columns(2)
    with col1:
         st.subheader('PIE CHART')
         st.plotly_chart(pie1,use_container_width=True) 
    with col2:   
         df21[['counts']]
    st.divider()     
    #3
    st.title('SELECTED ANIMAL COUNT IN EACH DISTRICT OF CHOOSEN STATE')
    Animals = st.sidebar.selectbox('CHOOSE ONE ANIMAL :',['cattle','buffalo','sheep','goat','horse','pony','mule','donkey','camel','pig'])
    df3 = df[df['state_name'] == state][['district_name',Animals]]
    pie = px.pie(names=df3['district_name'].value_counts().index,values=df3[Animals].values,
                  hole=0.3, color_discrete_sequence=px.colors.qualitative.Pastel)
    col1, col2 =st.columns(2)
    with col1:
        st.subheader('DONUT CHART')
        st.plotly_chart(pie,use_container_width=True)
    with col2:
         df3
    st.divider()
    #4
    st.title('SELECTED ANIMAL COUNT IN EACH DISTRICT OF EVERY STATE')
    fig5= px.sunburst(df, path=['state_name','district_name'], values=Animals)
    st.subheader('SUNBURST CHART')
    st.plotly_chart(fig5, use_container_width=True)
    st.divider()
    #5
    st.title('TOTAL POULTRY OF EVERY STATE')
    st.subheader('HORIZONTAL BAR PLOT')
    fig7 = px.bar(df, x="Total_poultry", y="state_name", orientation='h',color_discrete_sequence=px.colors.qualitative.Antique)
    st.plotly_chart(fig7, use_container_width=True)
    st.divider() 
    #6
    st.title('DATA OF TOTAL POULTRY OVER MAP USING MAPBOX PLOT')
    st.text("size represents Total Poultry")
    st.text("color represents State Name")
    map = px.scatter_mapbox(df, lat='lat', lon='lon', size='Total_poultry', color='state_name',
                             hover_name='district_name',size_max=40, zoom=3, mapbox_style="carto-positron",
                             height=600, width=1000)
    st.plotly_chart(map, use_container_width=True)
    st.divider()
    #7
    st.title('TOTAL POULTRY OF EVERY STATE & DISTRICT USING SUNBURST PLOT')
    fig6= px.sunburst(df, path=['state_name','district_name'], values='Total_poultry')
    st.plotly_chart(fig6, use_container_width=True)
    st.divider() 
    #8
    st.title('SCATTER PLOT OF SELECTED TWO ANIMALS IN STATES')
    S1=st.selectbox('CHOOSE FIRST ANIMAL :',['cattle','buffalo','sheep','goat','horse','pony','mule','donkey','camel','pig'])
    S2=st.selectbox('CHOOSE SECOND ANIMAL :',['cattle','buffalo','sheep','goat','horse','pony','mule','donkey','camel','pig'])
    scatter_plot = px.scatter(df, x=S1, y=S2, title='Simple Scatter Plot',color='state_name')
    st.plotly_chart(scatter_plot,use_container_width=True)
    st.divider()
    #9
    st.title('TOTAL COUNT OF EVERY ANIMAL SURVEYED')
    animals_survey=['cattle','buffalo','sheep','goat','horse','pony','mule','donkey','camel','pig']
    sum=[df['cattle'].sum(),df['buffalo'].sum(),df['sheep'].sum(),df['goat'].sum(),df['horse'].sum(),df['pony'].sum(),df['mule'].sum(),df['donkey'].sum(),df['camel'].sum(),df['pig'].sum()]
    data={'animal_survey':['cattle','buffalo','sheep','goat','horse','pony','mule','donkey','camel','pig'],'sum':[df['cattle'].sum(),df['buffalo'].sum(),df['sheep'].sum(),df['goat'].sum(),df['horse'].sum(),df['pony'].sum(),df['mule'].sum(),df['donkey'].sum(),df['camel'].sum(),df['pig'].sum()]}
    df9=pd.DataFrame(data)
    col1, col2 =st.columns(2)
    with col1:
        st.subheader(' BY HORIZONTAL BAR PLOT')
        bar9 = px.bar(x=sum, y=animals_survey, orientation='h',color_discrete_sequence=px.colors.qualitative.Dark2)
        st.plotly_chart(bar9, use_container_width=True)
    with col2:
        df9    
    st.subheader('BY PIE PLOT')
    #or
    pie9 = px.pie(labels=animals_survey,names=df21['animals'],
                   values=sum,color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(pie9,use_container_width=True) 
    #or
    #fig9 = go.Figure([go.Bar(x=animals_survey, y=[df['cattle'].sum(),df['buffalo'].sum(),df['sheep'].sum(),df['goat'].sum(),df['horse'].sum(),df['pony'].sum(),df['mule'].sum(),df['donkey'].sum(),df['camel'].sum(),df['pig'].sum()])])
    #st.plotly_chart(fig9,use_container_width=True)
    
with tab3:
    col1, col2, col3 =st.columns(3)
    with col1:
        st.write('TOTAL POULTRY OF EVERY STATE')
        st.plotly_chart(fig7, use_container_width=True)
    with col2:
        st.write('STATE WISE TOTAL POULTRY OF EVERY DISTRICT')
        st.plotly_chart(bar , use_container_width=True)
    with col3:
        st.write('DISTRICT WISE TOTAL COUNTS OF EACH ANIMALS IN SELECTED STATE')
        st.plotly_chart(pie1,use_container_width=True) 
    st.divider()
    col1, col2, col3 =st.columns(3)   
    with col1:
        st.write('SELECTED ANIMAL COUNT IN EACH DISTRICT OF CHOOSEN STATE')
        st.plotly_chart(pie,use_container_width=True)
    with col2:    
        st.write('SELECTED ANIMAL COUNT IN EACH DISTRICT OF EVERY STATE')
        st.plotly_chart(fig5, use_container_width=True)
    with col3:
        st.write('TOTAL COUNT OF EVERY ANIMAL SURVEYED')   
        st.plotly_chart(bar9, use_container_width=True) 
    st.divider()
    col1, col2, col3 =st.columns(3)  
    with col1:
        st.write('DATA OF TOTAL POULTRY OVER MAP USING MAPBOX PLOT')
        st.text("size represents Total Poultry")
        st.text("color represents State Name")
        st.plotly_chart(map, use_container_width=True)
    with col2:    
        st.write('TOTAL POULTRY OF EVERY STATE & DISTRICT USING SUNBURST PLOT')
        st.plotly_chart(fig6, use_container_width=True)
    with col3:
        st.write('SCATTER PLOT OF SELECTED TWO ANIMALS IN STATES')   
        S11=st.selectbox('CHOOSE 1st ANIMAL :',['cattle','buffalo','sheep','goat','horse','pony','mule','donkey','camel','pig'])
        S21=st.selectbox('CHOOSE 2nd ANIMAL :',['cattle','buffalo','sheep','goat','horse','pony','mule','donkey','camel','pig'])
        scatter_plot1 = px.scatter(df, x=S11, y=S21, title='Simple Scatter Plot',color='state_name')
        st.plotly_chart(scatter_plot1,use_container_width=True) 

with tab4:
    st.write('Tamil Nadu had highest total poultry with count 16.72739 Million and Daman & Diu had lowest total poultry with count 5074.')
    st.write('common species is Cattle & rarest one is Pony , total 193.3764 Million cattle surveyed while only 44.042 K pony surveyed.')
    st.write('in north-west area of india,about no amount of poultry had & in middle part, very less poultry had.')
    st.write('Gujrat is state where more poultry of Cattle & Buffalo both.')
    st.write('Rajasthan is state where more poultry of Cammel & Goat both')
    st.write('Bihar is state where, more poultry of Donkey & Pig both')
    st.write('Jammu & Kashmir is state where, more poultry of Mule & Pony both')

with st.sidebar:
     st.subheader('ANIMALS SURVEYED')
     st.image('https://environment.co/wp-content/uploads/sites/4/2023/05/A-Comprehensive-Guide-to-Raising-Cattle-for-Beginners.jpg.webp')
     st.image('https://www.foodnavigator-asia.com/var/wrbm_gb_food_pharma/storage/images/_aliases/wrbm_large/7/0/6/1/1771607-1-eng-GB/Mumbai-region-buffalo-meat-strike-launched-over-police-harassment.jpg')    
     st.image('https://upload.wikimedia.org/wikipedia/commons/f/f1/Sheep_eating_grass_edit02.jpg')       
     st.image('https://th-thumbnailer.cdn-si-edu.com/ZPFEN2-I60kglB6skBuTZ0xoFi8=/1072x720/filters:no_upscale()/https://tf-cmsv2-smithsonianmag-media.s3.amazonaws.com/filer/95/e0/95e04fb5-8608-463a-967d-a8d7fe957abf/istock-135157828.jpg')          
     st.image('https://www.cavaletticollection.co.uk/media/wysiwyg/Horse_Behaviour_-_blog.png')  
     st.image('https://www.thesprucepets.com/thmb/jyXTRBwAVx83M1d4v71E-n0hfh8=/2121x0/filters:no_upscale():strip_icc()/GettyImages-882448822-a6c9d488e32b4c76b94dd7a5de6c19b4.jpg')  
     st.image('https://spana.org/wp-content/uploads/2019/01/mules-on-mountain-1.jpg')  
     st.image('https://cdn.britannica.com/68/143568-050-5246474F/Donkey.jpg')  
     st.image('https://rajras.in/wp-content/uploads/2016/12/Rajasthan-Camel.jpg')  
     st.image('https://static.vecteezy.com/system/resources/previews/006/898/389/original/pig-writing-design-on-white-background-free-vector.jpg')      
    




            



    
    

   

    

    

   

   
    


    

