This project is my first project outside of University. It was made after my fist year as soon as I learned how to 
program so it was filled with bugs and bad practices. I decided to keep it as a reminder of how far I've come.

I have made some changes to the code so I could check all of this bad practices and learn from them. 

I list them here so I can remember them for educational purposes.


1. Use of import *.
    Importing everything from a module can cause name conflicts and makes the code less clear.
2. Lack of exception handling.
    Critical operations did not handle possible exceptions.
3. Repetitive code.
    Blocks of code are repeated a lot and could be refactored into functions.
4. Hardcoded credentials.
    Credentials are hardcoded in the code, which is not secure.
5. Long and fragile CSS selectors.
    CSS selectors are very specific and can easily break.
6. Functions without exception handling
    Critical functions do not handle exceptions.
7. Lack of modular structure.
    All code is in a single file instead of being divided into modules.
8. Direct Access to Raw URL File (urls_disposiciones.txt) Without Checks.
    URLs were read directly from a text file without any data cleaning or error handling, which 
    could lead to unexpected issues if the file contained empty lines or unwanted whitespace.
9. Lack of Error Handling in the URL Processing Loop.
    If a URL failed during processing (e.g., due to network issues), the entire loop could terminate, 
    and other URLs wouldn’t be processed
10. Hardcoded Paths with Redundant Directory Strings.
    Multiple places used hardcoded directory paths 
    (e.g., "C:\\Users\\DickVater\\PycharmProjects\\AutoMagislex\\magislex\\urls&pdfs"), which made the code harder 
    to maintain and change
11. No Log for Crawler Execution Completion.
    There was no way to know when the crawler completed its task or if the script ran without issues.
12. There was no venv used in the project.

Probably there are more bad practices in the code, but these are the ones I could identify. It's worth noting that I 
don't think this code is perfect now, I just took some time to improve it, and this is what I've done with the time 
I've allocated to this project. I'm open to suggestions and feedback to improve it even more, but most of all to learn 
from other people's experience. 

I hope this list helps someone else to identify bad practices in their code and improve it.
