# Data-Scraper-V2

Data entry bot for Driggs title company. 

## What it does

This program transfers agent market share data into the driggs title company website.

(It completes data entry between two sites fully autonomously)

The process requires no human interaction/help, which is a big step up from the once manual and very tedious work done by myself and a few others at the company. Yay passive income! 

The program utilizes selenium webdriver to create and navigate a browser window, which is used in tandem with beautifulsoup4 to parse html and isolate only the data we need. The data is then post processed if needed and entered into the correct agent and time slot section associated with the retrieved data.
