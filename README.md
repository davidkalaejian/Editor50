# Journey50
#### Video Demo:  <URL https://youtu.be/uwVgiOAkZSs>
#### Description:
# Journey50 Photo editor
I have created a very simple photo editing app where you can apply different tools and filters to your photos, like sharpness, blur, brightness, etc. You can access the editor only by logging in, each user receives 15 tokens upon registration, each successfully uploaded image then costs 1 token to edit, you can also purchase additional tokens to refill your balance, all of which is kept in an SQL data base for storage.

## Main logic
The main app.py file contains most of the logic for checking and veryfing uploads, user registration and login, token refills.
Each time the user uploads a file a directory in the static/uploads folder gets created with that user's id, so that each user can only access the content they have uploaded.
Registration creates a database entry in the users table of project.db, with the user's information, and automatically gives each user 15 tokens, every time the user refills their tokens this field gets updated.
When the user clicks on upload the previous uploads directory of that user is wiped, similarly when the user clicks on Log Out the directory is wiped again, this is also when the user's token balance gets updated (-1 token), if the user does not have enough tokens they will see an apology instead of the editor.
### Why save the uploads in a separate directory
I decided to save each uploaded photo in a directory instead of using it as a variable in code in order to make the project more scalable, so it would be easy to add a previous projects gallery, go back to previous editing sessions, etc.
### filtering
app.py is also responsible for calling filter functions from filters.py each time the user clicks on one of the filtering options with a verified photo.
Whenever the user clicks on a photo a copy gets made, the vopy is sent to filters.py, where it is filtered and replaces the copied image. The original is still intact to be able to get it back by clicking on the "Original" button.

## Filters
filters.py contains all of the filters that are being applied to the image, these functions are being called each time the user clicks on one of the filter options in the /edit page of the app, and are called from app.py which handles the routing logic.
Each of the filters have hard coded parameters at the moment, but this can also be easily change to a slider, or multiple buttons with preset values.

## Helpers
helpers.py contains just the require login function and apology function from the finance project as these were not very important for the photo editing project, and serve their purpose.
The first function is a decorator that is called before specific functions to check that the user is logged in, as only logged in users can access the editor, and only logged in users have tokens.

## Front-end
Most of the front-end is done with templating code with HTML and Jinja, dynamically adding to the layout.html for every other page.