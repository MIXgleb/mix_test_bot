# Telegram Bot that shows the weather in the entered city
This bot provides information about the temperature and cloudiness in the city. The city is entered directly in the messages and after sending it, the bot processes it and either gives out information about the weather, or says that there is no such city. Also in its functionality there is a memorization of your city where you live. After pressing a special button or entering a special command, the bot immediately shows the weather in the city that you have assigned by default. The bot contains a bottom menu in the form of 3 buttons, as well as an auxiliary menu with hints about the bot commands (from **FatherBot** settings).

### Requirements.txt
***pyTelegramBotAPI*** module is used to interact with Telegram. For API request ***requests*** module is used. To encrypt the token ***python-decouple*** is used.

### Weather_bot.py
The main file in which all commands used in the bot, all messages entered by the user, as well as all responses from buttons **(markups.py)** are processed.

Commands:
**/start** - a command that is called when the bot starts. She greets the user by his nickname or first name, describes how the bot works, and also offers to set the default city (initially, it is *Москва*). The user can agree to change the default city or refuse and just continue to use the bot.
**/help** - a command that tells about the bot, how it works and shows all commands.
**/mycity** - a command that will show the weather in your default city.
**/change_mycity** - a command will tell you your current default city and offer to change it. To change, you need to enter a new city in the message line, after sending a message to the bot, the changes will be saved. Also, the user can cancel the changes by clicking on the corresponding button.

### Commands.py
This file contains all entries that will be displayed to the user when calling bot commands.

### Markups.py
This file contains the constructor of all buttons in the bot.

**Plates menu:**
+ button *"Погода в моем городе"* corresponds to command /mycity;
+ button *"Изменить мой город"* corresponds to command /change_mycity;
+ button *"Помощь"* corresponds to command /help.

**Starting button** - inline buttons when starting the bot:
+ button *Да* - allow the user to immediately change the default city;
+ button *Нет* - just continue to use the bot without changes.

**Cancel button** - inline button when user wants to change default city
+ button *Отменить изменение* - cancels the default city change and continues working with the bot.

### Get_city_info.py
This file processes the name of the city from the user and receives information about the weather ***(requests)***. If the city is found, then the user is shown full information about the weather, otherwise it is reported that the city was not found.

### Change_mycity_operation.py
This is the file in which the default city is changed, checked and saved.
When calling the corresponding command **(/change_mycity)**, the bot offers to change the default city or cancel the changes by pressing the **cancel** button. The next city entered in the message line will become a candidate for the new default city. If the city does not exist or the entered city matches the one already assigned by default, the bot will not change the default city to a new one and will offer to try again or cancel the changes. Otherwise, the new city will become the new default city.
Pressing the **cancel** button terminates the change process.
