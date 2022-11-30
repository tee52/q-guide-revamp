# Revamping the Q Guide

A look at what a redesign of Harvard College's Q Guide could look like if it was more visually appealing, user-friendly, and fun to use.

## Background

I'm a freshman at Harvard College, and when registering for courses, almost all students are pointed to the Q Guide for assistance - the website where course evaluations are found. However, when I logged onto the website for the first time, my first thought was "wow, this website is ugly." While the newer iteration of the Q Guide is certainly a step up from the older version, there are still a lot of issues with the website. For this final project, I henceforth set out to start to rebuild the Q Guide into a site that I would actually enjoy using.

## The Project Itself

For my implementation of the CS50 final project, I used primarily Flask with HTML, CSS, and Python. I utilized some components from the Bootstrap library, as well as reused some of the basic functionality from the Finance pset (login, register, basic setup). To run the project, you would need to download the files, cd into the q-guide-revamp folder, and run 
```
python -m flask run
```
, which should launch the website on the server.

You can access a demo account using the following username and password:
- username: demo1
- password: 1234

There are comments within the code itself explaining what my code does and the purpose of each function, as well as sources.

## Challenges

This is the first time that we were really taken off the training wheels of the CS50 codespace, so transferring and setting up features that CS50 had previously set up for us was a little confusing.

## Where to Go From Here?

I could not figure out how to upload the data for every single Harvard undergraduate course and could not manually input thousands of courses, so in the future, it would be helpful to have access already to a database containing all of the course information. As well, considering that this site is for Harvard students, realistically, it would be beneficial to add a way to confirm students' Harvard emails or student IDs.