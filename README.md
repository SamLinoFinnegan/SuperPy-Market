 
# **SuperPy**
 
### A super lightweight, easy to use, practical supermarket administrative back-end tool in Python.
 
# Table of contents
1. [Description](#description)
2. [Why use SuperPy](#why_use)
    1. [Who can use SuperPy](#why_use_subparagraph1)
3. [Getting started with SuperPy](#getting_started)
    1. [How to install and run SuperPy](#getting_started_subparagraph1)
    2. [Installing python](#getting_started_subparagraph2)
    3. [Installing the Gooey decarator](#getting_started_subparagraph3)
    4. [Installing the Rich library](#getting_started_subparagraph4)
3. [How to use the SuperPy GUI](#how_gui)
3. [Now about how to use the SuperPy in the CLI version](#how_cli)
 
 
 
 
 
## **Description** <a name="description"></a>
 
SuperPy is a tool that was designed with the intention of helping small businesses be able to control their store in a simple and easy manner.
Giving the store owner/manager all the tools he would need in just one single place.
With SuperPy you will see that you will be able to easily:
Add products to your inventory.
Control the products you have in your store, as well as automatically know if you have products that have passed their expiration dates.
Sell products to your customers, knowing that the system will automatically sell the first products that have closest expiration dates.
Create reports from any specific set of dates.
Check your store history to see your expenses/waste/revenue/profit from any given time.
 
At SuperPy we believe in providing the simplest and most efficient solution to our clients, we plan constantly improving our APP and  we are open to innovation and suggestions.  
 
## **Why use SuperPy** <a name="why_use"><a>
 
SuperPy is simple and straight forward, it is very light weight, but it can still give you all the tools you need to help you run your store, and it can be used both as a back-end application, running on your server for your online store as well as, instore administrative tool running on your local PC.
 
### **Who can use SuperPy** <a name="why_use_subparagraph1"><a>
 
SuperPy was originally created as a school project, but it can also be used in real live aplications.
If you are a developer looking for a CLI, back-end application for you online store, or you are a local small business owner that is looking for an application that can help you control your store, SuperPy might be right for you.
 
``note: This is a work in progress and we are always looking for ways to improove``
 
 
## **Getting started with SuperPy** <a name="getting_started"><a>
 
To get started the first thing to do is clone this repository onto your machine
 
>git clone https://github.com/SamLinoFinnegan/SuperPy-.git
 
Once you have the SuperPy, on your machine you can run it from your command line
 
 
### **How to Install and Run SuperPy** <a name="getting_started_subparagraph1"><a>
 
1 First you must have python installed on your machine.
 
If you already have python 3 installed on your machine you can skip to: [Installing the Gooey decorator](#getting_started_subparagraph3)
If not this will guide you on how to setup python on your computer:
 
There are three installation methods on Windows:
 <br>
The Microsoft Store
 </br>
The full installer
 br
Windows Subsystem for Linux
 br
In this section, you’ll learn how to check which version of Python, if any, is installed on your Windows computer. You’ll also learn which of the three installation methods you should use.
To check if you already have Python on your Windows machine, first open a command-line application, such as PowerShell.
With the command line open, type in the following command and press Enter:
 
>C:\> python --version
 
If you see a version less than 3.8.4, which was the most recent version at the time of writing, then you’ll want to upgrade your installation.
For this program we want the full version
How to Install From the Full Installer
For professional developers who need a full-featured Python development environment, installing from the full installer is the right choice. It offers more customization and control over the installation than installing from the Microsoft Store.
You can install from the full installer in two steps.
 
### **Installing python** <a name="getting_started_subparagraph2"><a>
 
 
Step 1: Download the Full Installer
Follow these steps to download the full installer:
Open a browser window and navigate to the Python.org Downloads page for Windows.
Under the “Python Releases for Windows” heading, click the link for the Latest Python 3 Release - Python 3.x.x. As of this writing, the latest version was Python 3.8.4.
Scroll to the bottom and select either Windows x86-64 executable installer for 64-bit or Windows x86 executable installer for 32-bit.
 
Step 2: Run the Installer
 
Once you’ve chosen and downloaded an installer, run it by double-clicking on the downloaded file. A dialog box like the one below will appear:
There are four things to notice about this dialog box:
The default install path is in the AppData/ directory of the current Windows user.
The Customize installation button can be used to customize the installation location and which additional features get installed, including pip and IDLE.
The Install launcher for all users (recommended) checkbox is checked default. This means every user on the machine will have access to the py.exe launcher. You can uncheck this box to restrict Python to the current Windows user.
The Add Python 3.8 to PATH checkbox is unchecked by default. There are several reasons that you might not want Python on PATH, so make sure you understand the implications before you check this box.
The full installer gives you total control over the installation process.
 
Now you should have python installed on your computer and we are ready to run our program.
 
 
### **Installing the Gooey decarator**  <a name="getting_started_subparagraph3"><a>
 
2 Second you will need to install the ```Gooey``` decorator
 
Installation instructions
 
The easiest way to install Gooey is with pip
Just write on your terminal in your code editor:
 
>pip install Gooey
 
Alternatively, you can install Gooey by cloning the project to your local directory.
 
>git clone https://github.com/chriskiehl/Gooey.git
 
Then write:
> python setup.py install
 
 
If you need further support with downloading and installing the Gooey decorator, feel free to read the docs
[Gooey github](https://github.com/chriskiehl/Gooey)
 
**Note: wxtools is one of the main tools used by the Gooey decorator, and is not yet supported by python 3.10, the Gooey GUI can only run on python <= 3.9.**
 
### **Installing the Rich decorator**  <a name="getting_started_subparagraph4"><a>
 
3 Third we will install ```rich``` library
 
Rich is a Python library for rich text and beautiful formatting in the terminal.
 
The Rich API makes it easy to add color and style to terminal output. Rich can also render pretty tables, progress bars, markdown, syntax highlighted source code, tracebacks, and more — out of the box.
 
To install with pip:
Just write on your terminal in your code editor:
 
>python -m pip install rich
Run the following to test Rich output on your terminal:
 
>python -m rich
 
Once you have python, Gooey and rich on your machine we can run our program.
 
**To run the SuperPy file:**
 
Open your command line tool (cmd)
Navigate to the folder where you have placed the SuperPy.py file. Ex: cd/folder_where_you_put_the/SuperPy.py file
Type: python SuperPy.py
Hit: enter
Note: If you wish to use the CLI (Command Line Interface)  version of the program instead of the GUI (Global User Interface) version, just add --ignore-gooey on 3.
Like this:
>python SuperPy.py --ignore-gooey Buy -p Bread -b 1.6 -e 2022-04-29
 
## **How to use the SuperPy GUI**<a name="how_gui"><a>
 
**First lets see how to use the GUI version:**
 
As soon as you follow the instructions on: ```To run the SuperPy file```.
The program will open and you will have a window where you can start using your SuperPy app.
As soon as you open the app, you will see 4 different tabs (Buy, Sell, Stock, Search_Report)
Each tab represents the different areas where you can use the app.
 
### Buy tab:
 
You will have 4 different input fields: ```Product``` (this is where you will type in the product you would like to add to your inventory), ```Bought``` (this is the price you paid for the product), ```Quantity``` (this is where you will put how many you bought), ```Expiration``` (this is where you put the expiration date of your product)
 
### Sell tab:
 
You will have 2 different input fields: ```Product``` (this is where you will type in the product you would like sell at your store), ```Sell``` (this is the price you sold your product for), ```Quantity``` (this is where you will put how many you sold)
 
### Stock tab:
 
Here you will have a ```print``` check button that you can click if you would like to see what you currently have in your inventory.
 
Just check the print box and run the program.
 
### Search_Report tab:
 
You will have 2 date input fields, and 1 dropdown list at the bottom of the program: ```Start``` (this is the starting point of your search), ```End``` (this is till when you want the search) and the dropdown will give you the different ```Departments``` you can choose from.
 
>Ex: Start = 2022-03-15 End = 2022-03-30 Department = Revenue (this will return all the revenue that came into your store from 2022-03-15 till 2022-03-30)
 
Note: ```End``` is not mandatory, if you wish to just see 1 specific date you can type into Start, and it will give you the specific date you have asked for.
Further, Start accepts: dates (ex: 2022-05-15), day (ex: now, yesterday) or a give time ago (2+days, weeks, months)
 
Whichever you choose, the Search_Report will accept and give you the requested date.
 
Just put in the time frame you would like to see, and the department (Inventory, Revenue, Profit, Waste)
 
 
 
## **Now about how to use the app in the CLI version:**<a name="how_cli"><a>
 
Open your cmd, and go to the folder where your SuperPy.py file is.
Once there you can type:
 
**Buy**:
To use the Buy functionality, we start by using the Buy keyword, followed the -p flag and then the product, then the -q flag and the quantity, -b flag and the bought price, and last the -e flag and the expiration date.
 
To add a product to your store you can simply type:
 
ex. python SuperPy.py --ignore-gooey Buy -p Bread -q 5 -b 1.6 -e 2022-04-29
And hit:  
> enter
 
Bread, 5, 1.6,  2022-04-29. is just an example that I've added to show you the syntax of how to add a product to your store.
 
**Sell**:
To use the Sell functionality, we start by using the Sell keyword, followed the -p flag and then the product, then the -q flag and the quantity, -s flag and the sell price.
 
To sell a product from your inventory you can simply type:
 
> python SuperPy.py --ignore-gooey Sell -p Bread -q 5 -s 3.0
 
Again Bread, 5, 3.0. Is just an example, **However** you must make sure that the product that you are trying to sell, is in fact in your store.
 
``hint: you can alsways use the print stock``
 
**Stock**:
Stock will let you check to see what you have available in your store, simply type:
 
>python SuperPy.py  --ignore-gooey Stock -p
 
And hit:
> enter
 
**Search_Report**:
 
To use the search report functionality, we satrt by using the Search_Report keyword, followed by the -from flag, and then the -till flag, followed by the department keyword you would like to see, you can pick between: Inventory ,  Revenue ,  Profit ,  Waste .
 
>Ex: SuperPy.py --ignore-gooey Search_Report -from 2022-05-25 -till now
 
You can use the Search_Report to get reports from your inventory, waste, profit or revenue from any given time frame.
 
And its as simple as that.
 
I hope you found this useful and i'm ready to help in case of any bugs
 
Sam Finnegan


