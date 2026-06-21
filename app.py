import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

url='OLA_Cleaned_Data.csv'
df=pd.read_csv(url)
engine = create_engine("sqlite:///ola.db")
load_data=df.to_sql('OLA_Cleaned_Data',con=engine,if_exists='replace',index=False)


# Page Config
st.set_page_config(
    page_title="OLA Dashboard",
    page_icon="🚕",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #0f1117;
}
.metric-card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}
.big-font {
    font-size: 30px;
    font-weight: bold;
    color: white;
}
.small-font {
    color: gray;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🚕 OLA Analytics")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    ["Overview", "Successful Bookings", "Incomplete Rides"]
)

if menu =="Successful Bookings":
        st.title("Successful Bookings Analysis")


        query = """SELECT * FROM OLA_Cleaned_Data
                    WHERE Booking_Status = 'Success'"""
        df1=pd.read_sql_query(query, engine)
        

        st.table(df1.head())

if menu == "Overview":
        st.title("OLA Ride Analytics Dashboard")

        col1,col2,col3=st.columns(3)

        with col1:
            st.metric(
                label= "Customer Cancelled Rides",
                value='10499',
                delta="10.19%"
        )

        with col2:
            st.metric(
                label="Rides Cancelled by Drivers",
                value='6542',
                delta="6.35%"
            )

        with col3:
            st.metric(
                label="Total booking value",
                value="3,50,80,467",
                delta="+35M"
            )

        st.markdown("---")

        st.subheader("Prime Sedan")
        col20,col30=st.columns(2)
        with col20:
            st.metric(
                label='Maximum Driver Rating ',
                value='3.0'
            )
        with col30:
             st.metric(
                  label='Maximum Customer Rating',
                  value='5.0'
             )

        st.markdown("---")

        ##2. Find the average ride distance for each vehicle type:

        query2 = '''select Vehicle_Type,avg(Ride_Distance) as avg_distance from OLA_Cleaned_Data 
                    group by vehicle_type
                    '''

        df2=pd.read_sql_query(query2, engine)





        col4,col5=st.columns(2)
        with col4:
            st.subheader("Average Ride Distance by Vehicle Type")
            st.bar_chart(df2.set_index('Vehicle_Type')['avg_distance'])


        query4 = '''
        SELECT Customer_ID,
            COUNT(*) AS Total_Bookings
        FROM OLA_Cleaned_Data
        GROUP BY Customer_ID
        ORDER BY Total_Bookings DESC
        LIMIT 5
        '''
        df4=pd.read_sql_query(query4,engine)


        
        with col5:
            st.subheader("Top 5 Customers by Number of Bookings")
            st.bar_chart(df4.set_index('Customer_ID')['Total_Bookings'])
        st.markdown("---")

        query7='''
        select * from OLA_Cleaned_Data 
        where Payment_Method = 'UPI'
        '''
        query8='''
        select Vehicle_Type,avg(Customer_Rating) Avg_Customer_Rating from OLA_Cleaned_Data
        where Customer_Rating!=0
        group by Vehicle_Type
        order by Avg_Customer_Rating desc
        '''
        df8=pd.read_sql_query(query8,engine)
        df7=pd.read_sql_query(query7,engine)
        

            
        col6,col7=st.columns(2)
        with col7:
             st.table(df7.head(5))


        with col6:
             st.table(df8.head())
        st.markdown("---")

if menu == "Incomplete Rides":
    st.title("Incomplete Rides and Resons")
    query10='''
    select Booking_ID,Incomplete_Rides,Incomplete_Rides_Reason from OLA_Cleaned_Data
    where Incomplete_Rides in ('Yes','Not Completed') and
    Incomplete_Rides_Reason != 'Not applicable'
    '''
    df10=pd.read_sql_query(query10,engine)
    st.dataframe(df10.head(100))





