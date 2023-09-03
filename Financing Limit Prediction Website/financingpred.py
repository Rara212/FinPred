import pandas as pd  
import numpy as nmp  
import pickle as pkl  
import streamlit as st  
from PIL import Image as img
from streamlit_option_menu import option_menu
import pygwalker as pyg
from streamlit_extras.app_logo import add_logo

import mysql.connector

# Set page configuration
st.set_page_config(
    layout="wide",
)

# Establish a connection to MySQL Server

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="finpred"
)

mycursor=mydb.cursor()
print("Connection Established")

# loading in the model to predict on the data  
pickle_in1 = open('rfclassifier.pkl', 'rb')  
classifier1 = pkl.load(pickle_in1)

def prediction1(sektor_ekonomi, pby_bank, kode_produk, jangka_waktu_bulan, nilai_agunan, golongan_pemilik, kategori_usaha, uang_muka, kategori_nasabah, kategori_produk, kategori_segmen, kode_bisnis, jenis_piutang, kategori_portofolio, omset_xbrl, ratio_rbh, equivalen_rate_kontrak):
    prediction1 = classifier1.predict(
    [[sektor_ekonomi, pby_bank, kode_produk, jangka_waktu_bulan, nilai_agunan, golongan_pemilik, kategori_usaha, uang_muka, kategori_nasabah, kategori_produk, kategori_segmen, kode_bisnis, jenis_piutang, kategori_portofolio, omset_xbrl, ratio_rbh, equivalen_rate_kontrak]])  
    print(prediction1)  
    return prediction1


def main():  
    # Now, we will give the title to out web page  
    st.write("")

# Create Streamlit App
if 'login' not in st.session_state:
    st.session_state.login = False


#making horizontal menu
selected = option_menu(
    menu_title=None,
    options=["Home", "About Us", "Prediction"],
    icons=["bank", 'info', 'calculator', 'bar-chart'],
    menu_icon= "cast",
    default_index=0,
    orientation="horizontal",
)


#home
if selected == "Home":
    st.title("Welcome to Finpred")
    add_logo("finpredlogo.png", height=300)
    # Display Options for CRUD Operations
    option=st.sidebar.selectbox("Select an Operation",("Create Account","Login","Update","Delete"))
    if st.sidebar.button("Logout", key="logout"): 
        st.session_state.login = False
        st.success('Thank you for using this app!')

    if option=="Create Account":
        st.subheader("Create a new account")
        name=st.text_input("Enter Name")
        email=st.text_input("Enter Email")
        if st.button("Create"):
            sql= "insert into users(name,email) values(%s,%s)"
            val= (name,email)
            mycursor.execute(sql,val)
            mydb.commit()
            st.success("Record Created Successfully!!!")
        
    
    if option=="Login":
        st.subheader("Login to your account")
        name=st.text_input("Enter Name")
        email=st.text_input("Enter Email")
        if st.button("Login"):
            sql="select * from users where name =%s"
            val=(name,)
            result = mycursor.execute(sql, val)
            result = mycursor.fetchall()
            #st.write(result)
            # iterating over the data
            flat_list = []
            for item in result:
                # appending elements to the flat_list
                flat_list += item
            # printing the resultantn flat_list
            #st.write(flat_list)
            st.session_state['user'] = flat_list
            #st.write(st.session_state.user)
            if name == st.session_state.user[1]:
                if email == st.session_state.user[2]:
                    st.session_state.login = True
                    sql2= "insert into login_log(name) values(%s)"
                    val2= (st.session_state.user[1],)
                    mycursor.execute(sql2,val2)
                    mydb.commit()
                    st.success("You are successfully logged in!!")
                else:
                    st.error('Login Failed')
            if name != st.session_state.user[1]:
                st.error('Login Failed')
        
    elif option=="Update":
        if st.session_state['login'] == True:
            st.subheader("Update a Record")
            id=st.number_input("Enter ID",min_value=1)
            name=st.text_input("Enter New Name")
            email=st.text_input("Enter New Email")
            if st.button("Update"):
                sql="update users set name=%s, email=%s where id =%s"
                val=(name,email,id)
                mycursor.execute(sql,val)
                mydb.commit()
                st.success("Record Updated Successfully!!!")
        else:
            st.write('Please login first')

    elif option=="Delete":
        if st.session_state['login'] == True:
            st.subheader("Delete a User")
            id=st.number_input("Enter ID",min_value=1)
            if st.button("Delete"):
                sql="delete from users where id =%s"
                val=(id,)
                mycursor.execute(sql,val)
                mydb.commit()
                st.success("Record Deleted Successfully!!!")
        else:
            st.write('Please login first')

#about us                   
if selected == "About Us":
    # ---- HEADER SECTION ----
    with st.container():
        st.title("FinPred")
        st.subheader("A Machine Learning tool for Financing-analysis :dollar:")
       
    
    # ---- WHAT I DO ----
    image = img.open('finpredlogo.png')
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.write(
            "FinPred provides a tool to predict financing limit for potential recurring customer in Islamic Bank. Using historical financing data of customers, this tool will predict a range of facility limit that could be given to a current customer if they prolong their business partnership with your institution. "
            )
            st.write(
            "Fetch your data and let's get started!"
            )
            st.write("[Contact Me >](https://twitter.com/MutyaQurratu)")
        with right_column:
            st.image(image)

#prediction
if selected == "Prediction":
    if st.session_state['login'] == True:
        # Display Options for CRUD Operations
        option=st.sidebar.selectbox("Select an Operation",("Predict","Data Record","Delete", "Input Reference"))
        # Perform Selected CRUD Operations
        if option=="Predict":
            st.subheader("Predict a Customer")
            # # Now, we will be defining some of the frontend elements of our webpage like the colour of background and fonts and font size, the padding and the text to be displayed  
            # html_temp = """  
            #     <div style = "background-colour: #FFFF00; padding: 16px">  
            #     <h1 style = "color: #000000; text-align: centre; "> Potential Financing Limit Prediction   
            #     </h1>  
            #     </div>  
            #     """

            # # # Now, this line will allow us to display the front-end aspects we have defined in the earlier  
            # smt.markdown(html_temp, unsafe_allow_html = True)

            #getting input from user
            pby_bank = st.number_input('Financing Amount')
            uang_muka = st.number_input('Front Payment Amount')
            omset_xbrl = st.number_input('Company Revenue')
            ratio_rbh = st.number_input('Profit Sharing Ratio')
            jangka_waktu_bulan = st.number_input('Financing Terms - in month')
            nilai_agunan = st.number_input('Collateral Value')
            equivalen_rate_kontrak = st.number_input('Equivalent Rate Contract')
            #getting input for categorical values
            sektor_ekonomi = st.selectbox('Economy Sector', ('851000', '649900', '661009', '14600', '410190', '620200', '410149', '610009', '472009', '466990', '960009', '471100', '853000', '106300', '465000', '360000', '649100', '854000', '870000', '14110', '472001', '869000', '464190', '352000',
                                                             '453000', '421102', '454001', '852000', '478400', '475900', '478200', '522000', '181000', '201200', '451000', '478300', '410114', '107100', '862000', '639900', '320000', '4190', '475200', '263000', '422190', '11200', '422139', '466309',
                                                             '351001', '681107', '432000', '410130', '561009', '501100', '466200', '861000', '466920', '471900', '494300', '561001', '107900', '477200', '681102', '31119', '722000', '210000', '478920', '463309', '141000', '610001', '429190', '473000',
                                                             '780000', '463141', '771000', '463209', '421101', '466930', '681105', '462060', '681108', '681109', '521000'))
            sektor_ekonomi = int(sektor_ekonomi)
            #kode bisnis
            kode_bisnis = st.selectbox('Business Code', ('101', '102', '106', '110', '112', '113', '118', '126', '128', '129'))
            kode_bisnis = int(kode_bisnis)
            #golongan pemilik
            golongan_pemilik = st.selectbox('Owner Category', ('601','4140','4513','4599','5599','7130','7140','7173', '7172','7174', '7190','8115', '8139','8152', '8159','9000', ))
            golongan_pemilik = int(golongan_pemilik)
            #kode Produk
            kode_produk = st.selectbox('Product Type', ('902', '903', '904', '905', '911', '913', '916'))
            kode_produk =int(kode_produk)
            #kategori usaha
            kategori_usaha = st.selectbox('Business Category', ('10', '20', '30', '40', '50', '60', '70', '80', '90', '99'))
            kategori_usaha = int(kategori_usaha)
            #kategori nasabah
            kategori_nasabah = st.selectbox('Customer Category', ('Yayasan', 'Koperasi', 'Perorangan Produktif', 'Kontraktor', 'Perusahaan', 'BMT (Baitul Maal Wattamwil)', 'BPRS (Bank Pembiayaan Rakyat Syariah)', 'Developer'))
            if kategori_nasabah == 'Yayasan':
                kategori_nasabah = 0
            elif kategori_nasabah == 'Koperasi':
                kategori_nasabah = 1
            elif kategori_nasabah == 'Perorangan Produktif':
                kategori_nasabah = 2
            elif kategori_nasabah == 'Kontraktor':
                kategori_nasabah = 3
            elif kategori_nasabah == 'Perusahaan':
                kategori_nasabah = 4
            elif kategori_nasabah == 'BMT (Baitul Maal Wattamwil)':
                kategori_nasabah = 5
            elif kategori_nasabah == 'BPRS (Bank Pembiayaan Rakyat Syariah)':
                kategori_nasabah = 6
            elif kategori_nasabah == 'Developer':
                kategori_nasabah = 7
            #kategori produk
            kategori_produk = st.selectbox('Product Category', ('Investasi', 'Modal Kerja'))
            if kategori_produk == 'Investasi':
                kategori_produk = 0
            elif kategori_produk == 'Modal Kerja':
                kategori_produk = 1
            #kategori segmen
            kategori_segmen = st.selectbox('Segment Category', ('1', '2', '3', '4', '5', '9', '11'))
            kategori_segmen = int(kategori_segmen)
            #jenis piutang
            jenis_piutang = st.selectbox('Receivables Type', ('P01', 'P03','P99'))
            if jenis_piutang == 'P01':
                jenis_piutang = 0
            elif jenis_piutang == 'P03':
                jenis_piutang = 1
            elif jenis_piutang == 'P99':
                jenis_piutang = 2
            #kategori portofolio
            kategori_portofolio = st.selectbox('Portfolio Category', ('15', '16', '35', '36', '39','42', '52', '70'))
            kategori_portofolio = int(kategori_portofolio)
            result = ''

            if st.button ("Predict"):
                result = prediction1 (sektor_ekonomi, pby_bank, kode_produk, jangka_waktu_bulan, nilai_agunan, golongan_pemilik, kategori_usaha, uang_muka, kategori_nasabah, kategori_produk, kategori_segmen, kode_bisnis, jenis_piutang, kategori_portofolio, omset_xbrl, ratio_rbh, equivalen_rate_kontrak)
                if result[0] == 1:
                    st.success ('The customer above can be given facility in between 500 million - 2 billion rupiah')
                if result[0] == 2:
                    st.success ('The customer above can be given facility in between 2 billion - 5 billion rupiah')
                if result[0] == 3:
                    st.success ('The customer above can be given facility in between 5 billion - 10 billion rupiah')
                if result[0] == 4:
                    st.success ('The customer above can be given facility in between 10 billion - 30 billion or more (on special case) rupiah')

                pby_bank = str(pby_bank)
                uang_muka = str(uang_muka)
                omset_xbrl = str(omset_xbrl)
                ratio_rbh = str(ratio_rbh)
                jangka_waktu_bulan = str(jangka_waktu_bulan)
                nilai_agunan = str(nilai_agunan)
                equivalen_rate_kontrak = str(equivalen_rate_kontrak)
                sektor_ekonomi = str(sektor_ekonomi)
                golongan_pemilik = str(golongan_pemilik)
                kode_produk = str(kode_produk)
                kategori_usaha = str(kategori_usaha)
                kategori_nasabah = str(kategori_nasabah)
                kategori_produk = str(kategori_produk)
                kategori_segmen = str(kategori_segmen)
                kode_bisnis = str(kode_bisnis)
                jenis_piutang = str(jenis_piutang)
                kategori_portofolio = str(kategori_portofolio)
                ao_id = st.session_state.user[0]
                result = str(result)

                sql= "insert into customerpred(pby_bank, uang_muka, omset_xbrl, ratio_rbh, jangka_waktu_bulan, nilai_agunan, equivalen_rate_kontrak, sektor_ekonomi, golongan_pemilik, kode_produk, kategori_usaha, kategori_nasabah, kategori_produk, kategori_segmen, kode_bisnis, jenis_piutang, kategori_portofolio, ao_id, result) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val= (pby_bank, uang_muka, omset_xbrl, ratio_rbh, jangka_waktu_bulan, nilai_agunan, equivalen_rate_kontrak, sektor_ekonomi, golongan_pemilik, kode_produk, kategori_usaha, kategori_nasabah, kategori_produk, kategori_segmen, kode_bisnis, jenis_piutang, kategori_portofolio, ao_id, result)
                mycursor.execute(sql,val)
                mydb.commit()
                st.success("Data has been recorded Successfully!!!")
                st.balloons()

        elif option=="Data Record":
            st.subheader("Read Records")
            mycursor.execute("select * from customerpred")
            result = mycursor.fetchall()
            df = pd.DataFrame(data= result, columns=['Current Financing','Front Payment','Profit', 'Profit-Sharing Ratio', 'Financing Term (In Month)', 'Collateral', 'Equivalent Rate Contract', 'Economic Sector', 'Owner Category', 'Product Code', 'Business Category', 'Customer Category', 'Product Category', 'Segment Category', 'Business Code', 'Receivables Type', 'Portfolio Category', 'Result', 'id', 'AO_id'])
            table = st.data_editor(df, num_rows='dynamic')
            #st.write(table)

        elif option=="Delete":
            st.subheader("Delete a Record")
            id=st.number_input("Enter ID",min_value=1)
            if st.button("Delete"):
                sql="delete from customerpred where id =%s"
                val=(id,)
                mycursor.execute(sql,val)
                mydb.commit()
                st.success("Record Deleted Successfully!!!")
        
        elif option=="Input Reference":
            st.subheader("This is the code reference for input form")
            econ_sector_type = ['Elementary Education', 'Financial services activity (exclude insurance and retirement fund)', 'Other supportive financial services industry', 'Poultry', 'Other construction activities', 'Other telecommunications activity', 'Management and computer consulting activity', 'Other shopping building construction activities', 'Car spare parts and accessories trading', 'Road construction (non-highway)', 'Motorcycle trading', 'Secondary education', 'Chemical retail industry', 'Furniture retail industry', 'Food retail industry', 'Transportation activity', 'Village electricity', 'Office building real estate', 'Construction and electricity system installation', 'Food and beverages industry', 'Marine vehicles for passengers', 'Metal and metal ore industry', 'Hospital activity', 'Employment activity', 'Coffee industry', 'Leasing without option', 'Trading']
            econ_sector_code = [851000, 649900, 661009, 14600, 410149, 610009, 620200, 410149, 453000, 421102, 454001, 852000, 478400, 475900, 478400, 475900, 478200, 522000, 351001, 681107, 432000, 561009, 501100, 466200, 861000, 780000, 463141, 771000, 463209]
            businesscode_type = ['Capital financing', 'Investment', 'BPRS Executing', 'Multi-finance Executing', 'Syndication', 'Club deal', 'Multifunction consumer financing', 'Cooperation financing executing', 'BMT', 'Venture capital']
            businesscode_code = [101, 102, 106, 110, 112, 113, 118, 126, 128, 129]
            productcode_type = ['Mudaraba capital financing', 'Musharaka investment', 'General Musharaka', 'Musharaka Mutanaqishah', 'Musharaka Allocation']
            productcode_code = [902, 903, 904, 913, 916]
            businesscategory_type = ['SME debtor - with certain micro guarantor', 'Small enterprise - with certain micro guarantor', 'Medium enterprise - with certain micro guarantor', 'SME debtor - with other micro guarantors', 'Small enterprise - with other micro guarantors', 'Medium enterprise - with other micro gurantors', 'Other SME micro debtors', 'Other small enterprise with micro debtors', 'Other medium enterprise with micro debtors', 'Not micro, small, or medium enterprise debtors']
            businesscategory_code = [10, 20, 30, 40, 50, 60, 70, 80, 90, 99]
            receivablestype_type = ['Syndication financing', 'SME executing financing for re-financing purposes', 'Other financing']
            receivablestype_code = ['P01', 'P03', 'P99']
            portfoliocategory_type = ['Long term bank receivables', "Entity's invoice", 'Corporate invoice', 'Retail and SME invoice', 'Credit with house as collateral', 'Credit with commercial property as collateral', 'Securitization exposure']
            portfoliocategory_code = [15, 16, 35, 36, 39, 42,52]

            df = pd.DataFrame(list(zip(econ_sector_type, econ_sector_code)),
               columns =['Type', 'Code'])
            df2 = pd.DataFrame(list(zip(businesscode_type, businesscode_code)),
               columns =['Type', 'Code'])
            df3 = pd.DataFrame(list(zip(productcode_type, productcode_code)),
               columns =['Type', 'Code'])
            df4 = pd.DataFrame(list(zip(businesscategory_type, businesscategory_code)),
               columns =['Type', 'Code'])
            df5 = pd.DataFrame(list(zip(receivablestype_type, receivablestype_code)),
               columns =['Type', 'Code'])
            df6 = pd.DataFrame(list(zip(portfoliocategory_type, portfoliocategory_code)),
               columns =['Type', 'Code'])
            st.write("Economics Sector Type")
            st.table(df)
            st.write("Business Code")
            st.table(df2)
            st.write("Product Code")
            st.table(df3)
            st.write("Business Category")
            st.table(df4)
            st.write("Receivables Type")
            st.table(df5)
            st.write("Portfolio Category")
            st.table(df6)


    else:
        st.subheader("Please Login First")


if __name__== '__main__':  
    main()  
