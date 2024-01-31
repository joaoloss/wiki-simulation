from django.shortcuts import render, redirect
from . import util
import markdown
from django.contrib import messages
import random
from urllib.parse import quote

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def load_entry(request, title):
    """
    Loads an entry with its title or an error page 
    if the page is not found.
    """

    content = util.get_entry(title)

    if not content: # content == None --> no entry with 'title'
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    
    html_body = markdown.markdown(content) # this function converts an str in md pattern to a str in html pattern
    
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_body
    })

def search_entry(request):
    url = "/wiki" 
    """
    Obs.: the slash ("/") at the beginning of a URL indicates 
    that it is an absolute path, starting from the root of the domain.
    """
    
    try:
        page_title = request.POST['title']
        if page_title != '': # checks if a title was actually entered by the user

            content = util.get_entry(page_title)
            if not content: # no entry with 'page_title'
                similar_strings = [] # stores all titles that contain 'page_title' as substring
                all_titles = util.list_entries()

                for title in all_titles:
                    if page_title in title:
                        similar_strings.append(title)

                return render(request, "encyclopedia/index.html", {
                    "entries": similar_strings
                })
            else:
                url = f"wiki/{page_title}"                
    except:
        pass

    return redirect(url)

def new_page(request):
    """
    Renders the html page with a from to create a new encyclopedia entry
    """
    return render(request, "encyclopedia/new_page.html")

def handle_empty_data(request, path):
    """
    Handles cases of empty title or content when 
    the user is try to submit a new page or a change 
    to an existing encyclopedia entry.
    """
    
    page_title = request.POST["title"]
    page_content = request.POST["content"]
    page_content_encoded = quote(page_content)
    
    url = f"/{path}?title={page_title}&content={page_content_encoded}"

    if page_title == "": # check if the user typed a title
        msg_error = "You forgot the title of your page"
        if page_content == "": # check if the user typed a content
            msg_error = "Type a title and a content for your page"
        messages.error(request, msg_error)
        return False, redirect(url)
        
    elif page_content == "":
        msg_error = "Type a content for your page"
        messages.error(request, msg_error)
        return False, redirect(url)
    
    return True, request

def validating_data(request):
    """
    Makes the necessary validations when the 
    user submits data to create a new page.
    """
    try:
        success, request = handle_empty_data(request, "newPage")

        if not success:
            return request

        new_page_title = request.POST["title"]
        new_page_content = request.POST["content"]
        database_titles = util.list_entries() 
        new_page_content_encoded = quote(new_page_content)
        url = f"/newPage?title={new_page_title}&content={new_page_content_encoded}"

        if new_page_title in database_titles: # check if the user's title is already in use
            messages.error(request, "This title already exists. Type a new one!")
            return redirect(url)
        
        else: # valid title and content
            util.save_entry(new_page_title, new_page_content)
            return redirect(f"wiki/{new_page_title}")
    except:
        pass

def random_page(request):
    """
    Loads a random page.
    """

    titles = util.list_entries()
    random_index = random.randint(0, (len(titles)-1))
    return redirect(f"wiki/{titles[random_index]}")

def edit_page_display(request):
    """
    Just renders the html page for user edit an 
    existing encyclopedia page
    """
    return render(request, "encyclopedia/edit_page.html")

def edit_page(request, title):
    """
    Creates a url passing the title and content of a page 
    as query parameters and redirects to actually display 
    the page for editing with the form fields filled with 
    the current page data.
    """

    content = quote(util.get_entry(title))
    url = f"/edition?title={title}&content={content}"
    return redirect(url)

def save_changes(request):
    """
    Saves changes made by the user to the database. 
    It also handles sending empty form fields.
    """
    
    try:
        page_title = request.POST["title"]
        page_content = request.POST["content"]
        page_content_encoded = quote(page_content)

        success, request = handle_empty_data(request, f"edit/{page_title}")

        if not success:
            return redirect(f"/edition?title={page_title}&content={page_content_encoded}")
        
        util.save_entry(page_title, page_content)
        return redirect(f"wiki/{page_title}")

    except:
        pass

def delete_page(request, title):
    """
    Deletes a page from the database given its title.
    """
    
    util.delete_entry(title)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })