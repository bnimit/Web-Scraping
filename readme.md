# Web Scraping Demo Application
This is a demo application to showcase a basic web scraping setup using the python `Scrapy` framework.

### System Requirements and setup instructions
- You need to have `Python3.x` installed on your machine to be able run this demo.
- You would also require `pip` python package manager to install the `scrapy` binaries to be able to execute this app.
- On MacOs, `pip` can be installed using the command on the terminal `python3 -m ensurepip`
- Next we need `scrapy`, to install `scrapy` with `pip` from the terminal use command `pip install scrapy`. It's highly recommended to install `scrapy` in a virtual environment so it does not create an issue with any other system packages. If you wish to do that please following the setup for `virtualenv` and then install scrapy inside a virtual environment. 
- If you are using `Python3.x` the virtualenv package comes pre-installed with it and can be easily activated using the command `virtualenv <some/directory>`

### How to run this locally ?
Once you have cloned this repository, you can populate the `urls.txt` file with a list of web addresses that you wish to scrape using this setup. A few hundred web-links should not be an issue as long as your local machine has decent processing power and connected to the internet.

1. To run, open the `terminal` application and `cd` into the `folder/webscraper` after cloning the repo.
2. Then, to start the scraping process - `scrapy crawl web-spider -a filename='../urls.txt'`
3. The `urls.txt` file is provided as a command line input to the program so it can start processing those links.
4. The `web-spider` is the name of the crawler that I have defined for this demo but can be renamed.
5. Once the scraping application is done running in the terminal the output is stored in the `folder/output` as json files.

### Current Limitations and Solutions
This section would describe the current limitations and possible solutions to develop a production ready version of this demo application:
    
##### <u>Input Limitations</u>
- The `urls.txt` file has to be provided to the setup manually. For a production application this could be automated with a batch process that picks up this input file from a network storage location automatically.

- The list of `urls` could also be stored as in a nosql database periodically and fetched programmatically using a batch job setup. That way we can isolate the 

##### <u>Output Limitations</u>
- Currently, the system stores the results in `json` files but it can be improved to store these directly in a database using the `pipelines` capabilities of the `scrapy` framework.

##### <u>Capability Limitations</u>
- The current system would only scrape the list of `urls` from the input file provided and has been restricted to not extract more `url addresses` from the page it's currently scraping. This can also be improved to continue fetching more `url` addresses from the ones that are provided.
- The `classification` logic is also limited and basic to the `meta` information from the page which sometimes is limited in identifying the main theme of the page. The `meta` tags are not populated correctly at times and you can see that while running this demonstration locally and reviewing the json results.
- A better approach would be to build another service that can create a `classification model`, for e.g. like a `word-cloud` that can be more robust in identifying the main theme of the page being scraped.

##### <u>Throughput Limitations</u>
- The current system is also limited in its processing power in the terms of compute that is available to it to process thousands or billions of urls. In its current form it can only process as much as the hardware of the machine would allow it to.
- To scale this system we can use the inbuilt concurrency capabilities of the `scrapy` framework which can run hundreds of `spiders` in parallel based on the business requirements and available compute. The processing capabilities of a server / cloud environment could help run this application on a much higher number of target addresses and allow us to run it round the clock for fetching better results.

### Database Design
We can setup the following tables for this application that can be used to visualize the results better using reporting / analytic applications. These are thematic based on a few assumptions from the main theme of the target URL address :

##### <u>E-commerce Data</u>
<i>When we are scraping shopping, e-commerce websites we could use the following schema to store such information for further analysis:</i>

| Field Name    |   Type  |
|---------------|:-------:|
| ID            |   ID    |
| Description   | Varchar |
| Category      | Varchar |
| Main Category | Varchar |
| Rating        | Number  |
| Price         | Number  |
| Website Name  | Varchar |
| Date Added    | DateTime|

##### <u>News / Blog Page Data</u>
<i>While for target addresses that are news or blogs the following schema could be used:</i>

| Field Name      |   Type  |
|-----------------|:-------:|
| ID              |   ID    |
| Description     | Varchar |
| Theme           | Varchar |
| Author          | Varchar |
| Website Name    | Varchar |
| Date Published  | DateTime|

The current demo application only targets these two areas but can be further expanded to more themes as we identify requirements for other kinds of data.

Currently we only the above themes identified as our target sectors. As more themes like educational, legal, government, utility companies etc. are identified the database schema could further be expanded.

### Estimation & Production Rollout Plan
- This needs to be planned in phases where we identify our target businesses incrementally and the write specific `crawlers` for each thematic area separately.
- Start with testing these on a smaller sets using in-built python language benchmarking to time the running of a few crawlers in parallel including the time they take storing the results in the database and then we can slowly scale them to crawl more addresses automatically.
- With the efforts employed in the current demo a single thematic crawler for e.g. for e-commerce platform could be written, tested and deployed to a production environment in around 3 weeks time. Ideally spending a week on development and tests and the remaining two on benchmarking and tweaking the code based on the business requirements.

### Performance Monitoring & Benchmarking
- Bechmarking could be done iteratively at each crawler level and then over all timing the system during its test run on UAT environment which is closer in processing power to its production setup. As mentioned earlier there are benchmarking capabilities in python that could be done to achieve that.
- Integrated benchmarking on UAT and peformance monitoring could be achieved by using `APM` such as `New Relic` or `Data Dog` that can be configured to identify any errors that can be seen in the logs as the different `spiders` are running on the server. The application monitoring platforms can easily detect outages, fatal errors and any delays while isolating the root cause as well in certain cases.

### Legal Challenges
Web scraping is subjected to legal challenges as well based on the laws of where the target URL is hosted. But the `scrapy` framework has some inbuilt support for such a challenge. for e.g. `scrapy` framework can automatically honor the `robots.txt` file for a target web address without requiring any configuration. The `settings.py` has the `ROBOTSTXT_OBEY` set to `TRUE` by default. 
