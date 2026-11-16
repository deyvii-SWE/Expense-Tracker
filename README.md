# Expense Tracker 0.5

## How It Works

This is a program designed to help you manage your personal finances. You can register your expenses, check the total and average spending, change the currency, and more.

The program supports a wide range of currencies, which you can select through the settings. When a new month begins, a new file is created for it. Don't worry, you can still access previous months and their statistics through the settings (this feature is not implemented yet).

## About the Code

This time, the project was a little more complex, so I decided to separate some classes from the main code. We now have three classes: `Config`, `Storage`, and `Interface`, each with its own responsibilities.

I also tried my best to make sure that if a folder or file gets deleted somehow, the program can recreate it. That's why it already starts with some verification routines.

For the `match` statement, I decided to create separate functions for each option, keeping the code blocks organized and independent.

In the interface and other functions, I also tried to make everything more flexible and reusable, keeping efficiency and maintainability in mind.

One of the funniest parts was creating the Page Interface! We have pages in the settings when changing currencies, and in the expense list, where you can browse everything. Each page has 10 items, and you can go forward or back, edit expenses, and more.

At least the data is persistent!

You can make changes, add expenses, edit settings, and when you open the program again, everything is still there, saved in JSON.

I could have reduced a lot of things and made them work better, but I decided to keep the code more straightforward and simple so I could better understand how things work.

Overall, this was a great opportunity to learn how many things work behind the scenes, improve my organization and logic, and expand my library of knowledge. I also learned about Babel, JSON, datetime, and several other libraries.

This is currently my biggest programming project, and I'm really proud of how it turned out!
