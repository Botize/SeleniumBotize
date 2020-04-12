# SeleniumBotize
Controlling selenium from botize

Authorize Botize to use your Selenium WebDriver installation
By providing your access data, you declare that you accept
and you allow Botize to connect to your account. 


## What is Selenium and what is it for?

Selenium is open source software to automate tests carried out in web browsers, automating navigation and interacting with HTML elements.


## How does it work?

Through the Botize Selenium software that you will install on your computer (Windows, Linux or MacOS) you can connect Botize with Selenium and automate all kinds of tasks in combination with any of the Botize integrations to test, navigate, extract and even interact with sites Web.


## Previous requirements

Para la comunicación entre Botize y Selenium necesitarás una base de datos MySQL, un equipo Windows, Linux o Mac con Python 3 o superior previamente instalado y conocimientos de este lenguaje para programar las acciones que requieras automatizar.

In this guide you will learn how to install the software and create your first automatic task with Selenium from Botize.


## SeleniumBotize App Download

If you have Git you can clone the repository of our Github with the following command:

$ git clone https://github.com/Botize/SeleniumBotize.git

Or download the software in ZIP format from the following URL and unzip it in the directory you decide on your computer:

https://github.com/Botize/SeleniumBotize/archive/master.zip

In the directory where you are, you will now have a new folder named SeleniumBotize.


## Chrome driver download

Selenium requires the download of a Chrome driver to control the browser, which you can download by accessing the following link:

https://sites.google.com/a/chromium.org/chromedriver/downloads

Among the available options, download the one that corresponds to the operating system and version of Chrome that you have installed on your computer, for example ChromeDriver 81.0.4044.69.

Once downloaded, unzip the ZIP file and save the "chromedriver" file that it contains inside the SeleniumBotize folder.


## Installing the virtual environment

Create a virtual environment for the SeleniumBotize folder.

$ virtualenv -p python3 SeleniumBotize

If you do not have the virtualenv tool, you can install it previously with the following command: pip install virtualenv

Activate the virtual environment with the following command:

$ . SeleniumBotize/bin/activate


## Selenium WebDriver installation

The first step is to install Selenium WebDriver. You can do it with the following command:

(SeleniumBotize)$ pip install selenium


## pyMySQL installation

Communication between Selenium and Botize requires that you have a MySQL database. To be able to work with it, the pyMySQL module must be installed. You can do it with the following command:

(SeleniumBotize)$ pip install pymysql


## SeleniumBotize Installation

Access the SeleniumBotize folder and run the installer with the following command:

(SeleniumBotize)$ cd SeleniumBotize
(SeleniumBotize)$ python install.py

Then the installer will guide you to indicate the connection data to a MySQL database that you must provide:

Welcome to BotizeSelenium!

This is an application for running Python snippets from Botize inside Selenium.

This 'install' program will help you configure your Selenium environment

Let's get starter!

For communication with Botize this application requires that you have a database.

Please enter the access data to your database.

Enter Database Host: mydatabase.com
Enter Database User: username
Enter Database Password: mypassword

Now enter the name of an existing or new database to use with this application

Name (default 'selenium_botize'): 
Installation completed successfully.


## Run SeleniumBotize

Run the SeleniumBotize application with the following command:

(SeleniumBotize)$ python app.py
Browser Ready! Waiting for jobs.

## Connect Selenium to Botize

Once the application is installed and configured, connect it to Botize. To do this, go to the Botize Applications section and enter the Selenium Webdriver application. You can do it from this link:

https://botize.com/service/selenium/Automate+tasks+with+Selenium+WebDriver

Once inside, click on Start using it now and then on Connect to Selenium. You will see a form like the following where you will have to indicate the access data to your database.

It is important that you indicate the same values ​​that you set when installing the SeleniumBotize application.


## Create your first task
Finally you can now get your Selenium connection up and running, for example with this example formula:

http://botize.com/task/5399

This formula uses Selenium to connect to themoviedb.org, access the new releases section and post on Twitter the name and cover of one of the upcoming movies to come.

Congratulations!! You've already set up your first task with Selenium!

