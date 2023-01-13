# Design Document

## Problems with the Original Q Guide

There are several issues with the current Q Guide that I wanted to fix:
- clunky layout
- inconsistent visual identity
- lack of information on courses
- scores reported on separate pages from courses
- search by only two criteria (course and instructor)
- irrelevant information presented on pages with scores

## Functional Design

In terms of functionality, I wanted to address some of those issues I found in the original Q Guide. I wanted to create a website with more pages with clearly defined functions. As well, I wanted to add a way for people to post comments and questions relating to courses, i.e. the forum page. The different pages are as such:
- start/homepage: If you are logged in, you see the homepage, which displays a welcome message with your username and three randomized course recommendations. I used the Bootstrap card component, with some modifications, to display the cards. If you are logged out, you see the start page, which says "welcome to the q guide" in big text. From there, you can click the arrow to access the login page or use the link at the bottom to register for an account. Both the login and register pages are made to display error alerts if certain conditions are or are not met. 
- search: The search page enables you to search courses by name, course code (abbreviation), term (spring or fall), year, instructor, department, subject, or all criteria. You can choose which criteria to search by using the dropdown on the left of the search bar. The results are displayed as cards, which once again are a modified Bootstrap component.
- forum: The forum page allows you to make a post to and view the "forum," which shows posts made by all users displayed as a table. Each row of the table shows the username of the user who made the post, the post title, the post content, and the timestamp of when the post was submitted, organized with the newest posts first. The "make a post" element can also be collapsed to make more room for the table.
- profile: The profile button reveals a dropdown when clicked that displays two links - profile and logout. The profile page shows the profile information for your account. There, you can change your username and/or password, displayed with a button-triggered modal, as well as your graduation year, current class (freshman, sophomore, etc.), and intended concentration. Options are presented as select dropdowns. Obviously, the logout link logs you out, and you are redirected to the start page.
I used SQLite to make the database containing the information for the courses, scores, users, and posts, and Flask with Python/HTML/CSS for the actual webpage.

## Aesthetics and User Interface

For aesthetics and UI, I personally find the current Q Guide to be thematically inconsistent and harsh on the eyes (the main color is just bright white). To contrast this, I went with a color theme that stays true to the Harvard crimson but minimizes the jarring brightness of the pages. As such, I made the background color for the pages a dark crimson red with white text, with contrasting elements being either a darker red or white. For the cards with the course information as well as the posts table, I used a dark red header with white text, and the body was the inverse of this. For fonts, I chose a bolder, more eye-catching and visually interesting font for buttons, titles, and some subtitles, while I chose a simple, more basic font for paragraphs, body text, and other less important text. In general, I wanted a more simplified, minimal look, so I went with icons rather than text in the navigation bar and used dropdowns to hide other text elements. These visual design changes involved overriding many of Bootstrap's existing CSS rules. I used Figma to make the wireframe concepts for the UI/UX design ([https://www.figma.com/file/u1isYDrFRgU41qMqKwC6ic/q-guide?node-id=0%3A1&t=0ackEfp92k8ZqfrZ-1]https://tinyurl.com/q-guide-wireframes).