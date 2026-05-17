
from matplotlib.pyplot import ylabel
from streamlit.elements import deck_gl_json_chart
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#Setting page layout
st.set_page_config(
    layout = 'wide',
    initial_sidebar_state = 'collapsed',
    page_title = "Indian Startup Funding Analysis",
    page_icon = "📊"
)

df = pd.read_csv('D:\Startup_dashboard\Data\processed\clean_startup_data.csv',parse_dates=['Date'])


#Making sidebar
st.sidebar.title('Indian Startup Funding Analysis')

option = st.sidebar.selectbox("Select one", ['Overall Analysis','Startup Analysis','Investor Analysis'])

def load_investor_details(investor):
    st.title(investor)
    #Load the recent 5 investments of the investor
    last_5 = df[df['Investors'].str.contains(investor)].head()[['Date','StartUp','Vertical','Location','Round','Amount']]
    st.subheader('Recent Investments')
    st.dataframe(last_5)
    
    col1,col2 = st.columns(2)
    with col1:
        #Biggest Investments
        big_series = df[df['Investors'].str.contains(investor)].groupby('StartUp')['Amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        plt.ylabel('Amount(in Crores)', fontsize =12)
        plt.xlabel('Startup', fontsize =12)
        plt.title('Biggest Investments', fontsize=12)
        st.pyplot(fig)
    
    with col2:
        #Sector Wise Investments
        sector_series= df[df['Investors'].str.contains(investor)].groupby('Vertical')['Amount'].sum().head()
        st.subheader('Top Investment Sectors')
        fig1, ax1 = plt.subplots()
        wedges, texts, autotexts = ax1.pie(sector_series.values,autopct='%1.1f%%')
        # Separate legend
        ax1.legend(wedges,sector_series.index,title="Sectors",loc="center left",bbox_to_anchor=(1, 0.5))
        plt.title('Sector Wise Investments')
        st.pyplot(fig1)
    
    col3,col4 = st.columns(2)
    with col3:
        #Stage wise analysis
        stage_series = df[df['Investors'].str.contains(investor)].groupby('Round')['Amount'].sum()
        st.subheader('Stage Wise Investments')
        fig3, ax3 = plt.subplots()
        wedges, texts = ax3.pie(stage_series)

        # Calculate percentages
        total = stage_series.sum()
        labels = [
            f"{label} ({value/total*100:.1f}%)"
            for label, value in zip(stage_series.index, stage_series)
        ]
        
        # Separate legend
        ax3.legend(wedges,labels,title="Stages",loc="center left",bbox_to_anchor=(1, 0.5))
        st.pyplot(fig3)
    
    with col4:
        city_series= df[df['Investors'].str.contains(investor)].groupby('Location')['Amount'].sum()
        st.subheader('Top Investment Cities')
        fig4,ax4 = plt.subplots()
        wedges,texts= ax4.pie(city_series)

        # Calculate percentages
        total_city = city_series.sum()
        labels=[
            f"{label} ({value/total_city*100:.1f}%)"
            for label,value in zip(city_series.index,city_series)
        ]

        #Seprate legend
        ax4.legend(wedges,labels,title="Cities",loc="center left",bbox_to_anchor=(1, 0.5))
        plt.title('City Wise Investments')
        st.pyplot(fig4)
    
    

    #Investment trend over Time
    df['Year']=df['Date'].dt.year   #Extracting year from Date column

    yearly_investment = df[df['Investors'].str.contains(investor)].groupby('Year')['Amount'].sum().reset_index()
    st.subheader('Investment trend over Time')

    #Line plots to show YOY trend
    fig5,ax5 = plt.subplots(figsize=(12, 4))
    ax5.plot(yearly_investment['Year'],yearly_investment['Amount'],markersize=10,linestyle='-')
    plt.ylabel('Amount(in Crores)',fontsize=12)
    plt.xlabel('Year',fontsize=12)
    plt.title('Year On Year Investments',fontsize=12)
    plt.xticks(yearly_investment['Year'])
    st.pyplot(fig5)
    

#Overall Analysis
if option ==  'Overall Analysis':
    st.title('Overall Analysis')

#Startup Analysis
elif option == 'Startup Analysis':
    st.sidebar.selectbox('Select startup', sorted(df['StartUp'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')

#Investor Analysis
else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['Investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor details')
    st.title('Investor Analysis')

    if btn2:
        load_investor_details(selected_investor)
        
    






