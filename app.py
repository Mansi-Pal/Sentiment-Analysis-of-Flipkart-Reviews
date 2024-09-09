import streamlit as st 
import base64
import SentimentAnalysisFlipkart

def add_bg(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: wide
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

def main():
    st.set_page_config(page_title="FLIPKART",page_icon=":tada:",layout="wide")
    st.title("Sentimental Analysis of Products")
    add_bg("E:\code_workspace\MiniProject6\img.jpg")
    
    url = st.text_input("Enter the URL:")
    
    if st.button("Analyze"):
        try:
            # Step 1: Scraping reviews
            data = SentimentAnalysisFlipkart.webScrapingReviews(url)

            # Step 2: Performing sentiment analysis and saving results
            SentimentAnalysisFlipkart.sentimentAnalysis(data)

            # Step 3: Visualizing sentiment analysis results
            st.markdown(
                '<div style="background-color: #FFD700; padding: 10px; border-radius: 10px;">'
                '<h3 style="color: black; text-align: center;">Overall Sentiment Analysis:</h3>'
                '</div>',
                unsafe_allow_html=True
            )
            SentimentAnalysisFlipkart.visualization()

        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
   
if __name__=='__main__':
    main()

# streamlit run "E:\code_workspace\MiniProject6\app.py"
# streamlit run e:\code_workspace\MiniProject6\app.py 


#samples:
#   
#https://www.flipkart.com/eureka-forbes-bold-wet-dry-vacuum-cleaner/p/itm5a1c0501fa6e0?pid=VCLFHW6AYCE6GRST&lid=LSTVCLFHW6AYCE6GRSTHROKPE&marketplace=FLIPKART&store=j9e%2Fabm%2Ful2&srno=b_1_1&otracker=browse&fm=organic&iid=en_g1W-X2d22as92EvbfdPft8Kkfm9vhxsGx0mi4P5WzNva6SMSIHMObZYP-W0oXJF6xsknhEKhASMD6v_cUm2TcQ%3D%3D&ppt=None&ppn=None&ssid=n0kpyge61s0000001689450624994

