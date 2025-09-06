FramesDirect Web Scraping Project

This project focused on extracting product information from the FramesDirect Eyeglasses page using Python, Selenium, and BeautifulSoup. The scraper collects the brand, product name, former price, current price, and discount from each eyeglass product, cleans the price values by removing dollar signs, and saves the results in both CSV and JSON formats.

During development, I encountered key challenges such as handling JavaScript-loaded content, identifying the correct HTML classes for product details, ensuring consistent variable naming, and performing price data cleaning. These were resolved by leveraging Selenium’s ability to wait for elements, carefully inspecting the site’s HTML, defining a helper function to clean prices, and maintaining proper coding conventions.

The final solution provides a structured dataset of FramesDirect eyeglasses, suitable for analysis, reporting, or integration into a larger data pipeline.
This scrips is reusable and can be extented to scrape multiple pages if needed.
