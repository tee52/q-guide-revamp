# Revamping the Q Guide

A look at what a redesign of Harvard College's Q Guide could look like if it was more visually appealing, user-friendly, and fun to use.

## Background

I'm a freshman at Harvard College, and when registering for courses, almost all students are pointed to the Q Guide for assistance - the website where course evaluations are found. However, when I logged onto the website for the first time, my first thought was "wow, this website is ugly." While the newer iteration of the Q Guide is certainly a step up from the older version, there are still a lot of issues with the website. For this final project, I henceforth set out to start to rebuild the Q Guide into a site that I would actually enjoy using.

## The Project Itself

For my implementation of the CS50 final project, I used primarily Flask with HTML, CSS, and Python. I utilized some components and classes from the Bootstrap version 5.2 library (modals, cards, navbar, table, etc.), as well as reused some of the basic functionality from the Finance pset (login, register, basic setup). Also, I used SQLite for creating and managing the database.

You can access the site at this link: [https://q-guide-revamp-dwc7.onrender.com/](https://q-guide-revamp-dwc7.onrender.com/)

Alternatively, you can run the website locally. In order to run the project, you need to have Python and Flask installed on your computer. You can install Flask using pip, which is downloaded along with Python, using this command:
```
pip3 install flask
```

Once you've done that, you can clone my repository onto your computer or download the files from Github, cd into the q-guide-revamp folder, and run 
```
python -m flask run
```
, which should launch the website on the server. 

You can access a demo account using the following username and password:
- username: demo1
- password: 1234

Feel free to also make your own account! For the sake of anonymity, please do not use your real name or enter any sensitive information/passwords.

There are comments within the code itself explaining what my code does and the purpose of each function, as well as sources. You can also refer to the DESIGN.md document, which has more information about the design of the project.

## Challenges and Limitations

This is the first time that we were really taken off the training wheels of the CS50 codespace, so transferring and setting up features that CS50 had previously set up for us was a little confusing. I ran into challenges with using Flask and SQLite in my local VS Code. As well, (as expected) bugs were frequent in my code. Limited by time constraints, I ultimately could not implement all of the features that I had originally planned to, but I did do my best to offer at least a prototype of what a new Q Guide could look like.

## Where to Go From Here?

To my knowledge, the data on every Harvard undergraduate course is not publicly available, and I obviously could not manually input thousands of courses, so in the future, it would be helpful to have access already to a database containing all of the course information. Given more time, I would add more courses to the database.

As well, I would add the following features:
- verify Harvard emails/student IDs
- link to my.harvard entry and/or full q-report for courses
- favorite courses
- personalized recommendations (not just completely randomized)
- more detailed course cards
- delete and edit posts
- make posting more specific and limited (implementing tags, topics, etc.)
- give each post its own page
- comment on posts
- filter search results by q scores