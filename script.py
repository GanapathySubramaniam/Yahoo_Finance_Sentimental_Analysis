# Importing necessary modules for subprocess management and system-specific parameters.
import subprocess
import sys

# Defining the Setup class to manage package installations.
class Setup:
    def __init__(self):
        '''
        Initializes the Setup object, preparing a list of essential Python packages for installation.
        This setup ensures that all required libraries are available for the application to function properly.
        
        Args:
            None
        
        Returns:
            None
        '''
        # List of Python packages that are necessary for the application.
        self.packages = ['pandas', 'nltk', 'requests', 'yahoo_fin', 'textblob', 'xlsxwriter']
        print('🚀 Setup Initiated!!')

    def check_library_exists(self, package):
        '''
        Checks if a specified Python package is already installed in the environment.
        
        Args:
            package (str): The name of the package to check.
        
        Returns:
            Boolean: True if the package is installed, False otherwise.
        '''
        try:
            # Executes 'pip show' command to check for the package's existence.
            result = subprocess.run(['pip', 'show', package], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Returns True if the command's output indicates the package is installed.
            return bool(result.stdout)
        except subprocess.CalledProcessError:
            # Prints an error message if 'pip show' command fails.
            print(f"⚠️ An error occurred while checking for {package}.")
            return False

    def install_packages(self, package):
        '''
        Installs a specified Python package using pip, if it is not already installed.
        
        Args:
            package (str): The name of the package to install.
        
        Returns:
            None
        '''
        if self.check_library_exists(package):
            # Notifies the user if the package is already installed.
            print(f'✅ {package} already exists!')
        else:
            # Installs the package using pip and notifies the user.
            print(f'📦 Installing {package}...')
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    def run(self):
        '''
        Executes the setup process by iterating through the list of packages and installing them.
        
        Args:
            None
        
        Returns:
            None
        '''
        # Iterates through each package in the list and attempts to install it.
        for package in self.packages:
            self.install_packages(package)
        # Notifies the user once all packages have been processed.
        print('🌟 Setup Completed!!')

if __name__=='__main__':
  # Instantiates the Setup class and starts the package installation process.
    setup_instance = Setup()
    setup_instance.run()
    print('Setup completed successfully. Proceeding with analysis...')



# Importing the required libraries 📚
import pandas as pd  # For data wrangling 🛠
import requests  # For fetching the top companies in the specified country 🌍
from yahoo_fin import news  # For fetching the company news 📰
from textblob import TextBlob  # For sentimental analysis 😊😠
import nltk  # For text preprocessing 📝
from nltk.corpus import stopwords  # For removing stopwords 🚫📖
import string  # For punctuation removal 🚫❗

class CompanyNewsSentimentalAnalysis:
    def __init__(self, country):
        '''
        Initializes the CompanyNewsSentimentalAnalysis object with a specified country. 🌐
        
        Args:
            country (str): The country for which to perform the sentimental analysis on companies' news.
        
        Returns:
            None
        '''
        self.country = country
        self.company_news_dict = {}  # Initializes a dictionary to store company news data 🗃
        print('🚀 Process Initiated!')
    
    def get_companies_data(self):
        '''
        Fetches companies data from the specified country using the NASDAQ screener API. 📈
        
        Returns:
            pd.DataFrame: A DataFrame containing the companies data.
        '''
        print(f'🔍 Fetching {self.country} companies data...')
        headers = {
            'authority': 'api.nasdaq.com',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0',
            'origin': 'https://www.nasdaq.com',
        }
        params = {
            'tableonly': 'true',
            'limit': '25',
            'offset': '0',
            'download': 'true',
            'country': self.country
        }
        response = requests.get('https://api.nasdaq.com/api/screener/stocks/', headers=headers, params=params)
        json_data = response.json()['data']
        data= pd.DataFrame(json_data['rows'], columns=json_data['headers'])
        print(f'✅ {self.country} companies data downloaded successfully!')
        return data

    def get_company_news(self, company_ticker_symbol):
        '''
        Fetches news for a given company using the company's ticker symbol. 📊
        
        Args:
            company_ticker_symbol (str): The ticker symbol of the company.
        
        Returns:
            pd.DataFrame: A DataFrame containing the titles and summaries of the news articles.
        '''
        print(f'🔍 Fetching news for {company_ticker_symbol}...')
        company_news_list = news.get_yf_rss(company_ticker_symbol)
        print(f'📰 {company_ticker_symbol} news gathered successfully!')
        return pd.DataFrame({
            'titles': [article.get('title') for article in company_news_list],
            'summaries': [article.get('summary') for article in company_news_list]
        })

    def preprocess_setup(self):
        '''
        Prepares the text preprocessing setup by downloading the necessary NLTK resources. 📚
        
        Returns:
            None
        '''
        print('🛠 Text Preprocessing Setup initiated...')
        nltk.download('stopwords')
        nltk.download('punkt')
        self.stop_words = set(stopwords.words('english'))
        print('✅ Text Preprocessing Setup completed successfully!')

    def preprocess_text(self, text):
        '''
        Removes punctuation and stopwords from a given text. 🧹
        
        Args:
            text (str): The text to preprocess.
        
        Returns:
            list: A list of tokenized text without stopwords and punctuation.
        '''
        no_punctuation = text.translate(str.maketrans('', '', string.punctuation))
        tokens = nltk.word_tokenize(no_punctuation)
        return [word for word in tokens if word.lower() not in self.stop_words]

    def analyze_sentiment(self, text):
        '''
        Analyzes the sentiment of a given text. 😊😠
        
        Args:
            text (str): The text to analyze.
        
        Returns:
            tuple: A tuple containing the polarity of the text and its sentiment classification.
        '''
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        sentiment = 'Positive' if polarity > 0 else 'Negative' if polarity < 0 else 'Neutral'
        return polarity, f'{sentiment}' if sentiment == 'Positive' else f'{sentiment}' if sentiment == 'Negative' else f'{sentiment}'

    def gather_companies_info(self):
      '''
      Gathers the data for companies within {self.country}, preparing for analysis. 🌍
      This method fetches companies' information and initializes columns for sentiment analysis.

      Args:
          None

      Returns:
          None
      '''
      # Print statement to indicate the beginning of the data gathering process
      print(f'🔎 Gathering {self.country} company information...')
      # Call get_companies_data to fetch company data from the specified country
      self.companies_df = self.get_companies_data()
      # Initialize columns in the DataFrame for storing average polarities of news titles and summaries
      self.companies_df['title average polarity'] = None  # For average polarity of news titles
      self.companies_df['summary average polarity'] = None  # For average polarity of news summaries
      self.companies_df['overall average polarity'] = None  # For overall average polarity combining titles and summaries

    def gather_company_info(self, company_name, company_ticker_symbol):
        '''
        Gathers and stores news data for a specific company using its ticker symbol. 📈
        This information is later used for sentiment analysis.
        
        Args:
            company_name (str): Name of the company.
            company_ticker_symbol (str): Ticker symbol of the company.
        
        Returns:
            None
        '''
        # Print statement indicating the start of news data gathering for a specific company
        print(f'📰 Fetching news for {company_name}...')
        # Call get_company_news to fetch news articles for the company and store it in company_news_dict
        self.company_news_dict[company_name] = self.get_company_news(company_ticker_symbol)
        # Assign the company's name to the fetched news data for identification
        self.company_news_dict[company_name]['name'] = company_name

    def run_sentimental_analysis(self, company_name):
        '''
        Performs sentiment analysis on the gathered news titles and summaries for a specific company. 😊
        Analyzes sentiment to classify as Positive, Negative, or Neutral.
        
        Args:
            company_name (str): Name of the company for which to perform sentiment analysis.
        
        Returns:
            None
        '''
        # Analyzing sentiment of news titles and storing the polarity and sentiment
        self.company_news_dict[company_name]['title polarity'], self.company_news_dict[company_name]['title sentiment'] = \
            zip(*self.company_news_dict[company_name]['titles'].apply(self.analyze_sentiment))
        # Analyzing sentiment of news summaries and storing the polarity and sentiment
        self.company_news_dict[company_name]['summary polarity'], self.company_news_dict[company_name]['summary sentiment'] = \
            zip(*self.company_news_dict[company_name]['summaries'].apply(self.analyze_sentiment))

    def calculate_average_polarity(self, company_name):
        '''
        Calculates the average polarity of news titles and summaries for a given company. 📊
        Determines the overall sentiment towards the company based on the news articles.
        
        Args:
            company_name (str): Name of the company.
        
        Returns:
            None
        '''
        # Calculate the mean polarity for news titles
        title_average_polarity = self.company_news_dict[company_name]['title polarity'].mean()
        # Calculate the mean polarity for news summaries
        summary_average_polarity = self.company_news_dict[company_name]['summary polarity'].mean()
        # Filter the main DataFrame for the current company
        filt = self.companies_df['name'] == company_name
        # Assign calculated average polarities to the company's row in the main DataFrame
        self.companies_df.loc[filt, 'title average polarity'] = title_average_polarity
        self.companies_df.loc[filt, 'summary average polarity'] = summary_average_polarity
        # Calculate and assign the overall average polarity combining titles and summaries
        self.companies_df.loc[filt, 'overall average polarity'] = (title_average_polarity + summary_average_polarity) / 2

    def combine_company_news(self):
        '''
        Combines all fetched company news into a single DataFrame for further analysis. 📚
        Facilitates the analysis of news data across all companies.
        
        Args:
            None
        
        Returns:
            None
        '''
        # Combining all company news DataFrames into a single DataFrame
        self.company_news_df = pd.concat(list(self.company_news_dict.values()))

    def save_data(self):
        '''
        Saves the analyzed data and formatted results as .xlsx files for reporting and archiving. 💾
        Creates an Excel file with separate sheets for company information and sentiment analysis results.
        
        Args:
            None
        
        Returns:
            None
        '''
        # Print statement indicating the start of the data saving process
        print('💾 Saving Analysis...')
        # Using ExcelWriter to save DataFrames to an Excel file with specified sheets
        with pd.ExcelWriter(f'{self.country}_companies_news_sentimental_info.xlsx', engine='xlsxwriter') as writer:
            self.companies_df.to_excel(writer, sheet_name='Company_info', index=False)  # Saving company info
            self.company_news_df.to_excel(writer, sheet_name='Companies_News_Sentimental_info', index=False)  # Saving sentiment analysis results
        # Confirmation message after saving the data
        print(f'✅ {self.country} companies Analysis Saved as Excel!')

    def run(self):
        '''
        Orchestrates the entire process flow for information retrieval and sentimental analysis of company news. 🌐🔍
        This method acts as the central controller, invoking all necessary steps in sequence to gather data,
        analyze sentiment, and save the results.

        Args:
            None

        Returns:
            None
        '''
        # 🚀 Start by gathering company information for the specified country.
        self.gather_companies_info()
        
        # 📚 Initialize a dictionary to store news articles for each company.
        self.company_news_dict = dict()
        
        # 🔑 Create a mapping of company names to their ticker symbols for easy access.
        self.company_dict = dict(zip(self.companies_df['name'], self.companies_df['symbol']))

        # 🛠 Prepare the text analysis environment (e.g., download necessary NLTK resources).
        self.preprocess_setup()
        
        # 🔄 Iterate over each company, performing a series of analyses.
        for company_name, company_ticker_symbol in self.company_dict.items():
            # 🗞 Fetch and store news data for each company.
            self.gather_company_info(company_name, company_ticker_symbol)

            # 💡 Conduct sentiment analysis on the collected news articles.
            self.run_sentimental_analysis(company_name)
            
            # 📊 Calculate the average sentiment polarity from the collected news articles.
            self.calculate_average_polarity(company_name)
        
        # 📈 Combine all collected news data into a single DataFrame for analysis or reporting.
        self.combine_company_news()
        
        # 💾 Finally, save the analyzed data to Excel files for reporting or archival purposes.
        self.save_data()
        
        # ✅ Signal the completion of the analysis process.
        print(f'🎉 Sentimental analysis process completed for {self.country}!')


# Entry point of the script. This block is executed when the script is run directly.
if __name__ == '__main__':
    
    # 🌍 Specify the target country for analysis. In this case, it's Ireland.
    country = 'Ireland'
    
    # 🏗️ Create an instance of CompanyNewsSentimentalAnalysis for the specified country.
    # This object will be used to orchestrate the sentiment analysis process.
    obj = CompanyNewsSentimentalAnalysis(country)
    
    # 🚀 Trigger the sentiment analysis process by calling the run method on the created object.
    # This will start the sequence of operations defined in the run method of the CompanyNewsSentimentalAnalysis class.
    obj.run()
    
    # ✅ The script concludes its execution here, after the sentiment analysis process has been completed.
    print(f'🎉 Sentimental analysis for companies in {country} has been successfully completed!')
