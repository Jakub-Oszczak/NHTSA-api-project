import requests
import json
from tkinter import *
import tkinter.font as tkFont
from PIL import ImageTk, Image
from urllib.request import urlopen
from io import BytesIO

num_of_clicks = 0

def make_request(suffix, key):
    content_table = []
    r = requests.get('https://api.nhtsa.gov/SafetyRatings' + suffix)
    dictionary = json.loads(r.text)
    results = dictionary['Results']
    for i in results:
        data = str(i[key])
        content_table.append(data)
    return content_table

def submit():
    global num_of_clicks
    global make
    global model
    global variant
    global make_table
    global model_table
    global variant_table
    global variant_label
    global make_label
    global model_label

    if num_of_clicks == 0:
        year_table['state'] = DISABLED
        suffix = '/modelyear/' + year.get()
        make_content_table = make_request(suffix = suffix, key = 'Make')
        make_label = Label(win, text = 'Select make:')
        make_label.grid(row = 2, column = 0)
        make = StringVar()
        make.set(make_content_table[0])
        make_table = OptionMenu(win, make, *make_content_table)
        make_table.grid(row = 3, column = 0)
        num_of_clicks += 1
        return True
    
    elif num_of_clicks == 1:
        make_table['state'] = DISABLED
        suffix = '/modelyear/' + year.get() + '/make/' + make.get()
        model_content_table = make_request(suffix = suffix, key = 'Model')
        model_label = Label(win, text = 'Select model:')
        model_label.grid(row = 4, column = 0)
        model = StringVar()
        model.set(model_content_table[0])
        model_table = OptionMenu(win, model, *model_content_table)
        model_table.grid(row = 5, column = 0)
        num_of_clicks += 1
        return True

    elif num_of_clicks == 2:
        model_table['state'] = DISABLED
        suffix = '/modelyear/' + year.get() + '/make/' + make.get() + '/model/' + model.get()
        variant_content_table = make_request(suffix = suffix, key = 'VehicleDescription')
        variant_label = Label(win, text = 'Select variant:')
        variant_label.grid(row = 6, column = 0)
        variant = StringVar()
        variant.set(variant_content_table[0])
        variant_table = OptionMenu(win, variant, *variant_content_table)
        variant_table.grid(row = 7, column = 0)
        num_of_clicks += 1
        return True

    elif num_of_clicks == 3:
        suffix = '/modelyear/' + year.get() + '/make/' + make.get() + '/model/' + model.get()
        r = requests.get('https://api.nhtsa.gov/SafetyRatings' + suffix)
        dictionary = json.loads(r.text)
        results = dictionary['Results']
        for i in results:
            if i['VehicleDescription'] == variant.get():
                VehicleId = i['VehicleId']
        show_results_window(VehicleId)

def show_results_window(VehicleId):
    global var, var1, var2, var3, var4, var5, var6, var7
    var = StringVar()
    var1 = StringVar()
    var2 = StringVar()
    var3 = StringVar()
    var4 = StringVar()
    var5 = StringVar()
    var6 = StringVar()
    var7 = StringVar()
    var.set('a')
    var1.set('b')
    var2.set('c')
    var3.set('d')
    var4.set('e')
    var5.set('f')
    var6.set('g')
    var7.set('h')
    win2 = Toplevel()
    car_label = Label(win2, text = 'Chosen car: ' + variant.get()).grid(row = 0, column = 0, columnspan = 6)
    overall_label = Label(win2, text = 'Overall rating:  ').grid(row = 4, column = 0)
    front_label = Label(win2, text = 'Front crash:  ').grid(row = 5, column = 0)
    side_label = Label(win2, text = 'Side crash:  ').grid(row = 6, column = 0)
    rollover_label = Label(win2, text = 'Rollover:  ').grid(row = 7, column = 0)

    r = requests.get('https://api.nhtsa.gov/SafetyRatings/VehicleId/' + str(VehicleId))
    dictionary = json.loads(r.text)
    results = dictionary['Results']
    dictionary = results[0]
    try:
        overall_rating = int(dictionary['OverallRating'])
        x = 5 - overall_rating
        for i in range(overall_rating):
            rb = Radiobutton(win2, variable=var, value='1', fg='red')
            rb.grid(row = 4, column=i+1)
            rb.select()
        for i in range(x):
            rb1 = Radiobutton(win2, variable=var1, value='2', state=DISABLED)
            rb1.grid(row = 4, column=overall_rating+1+i)
            rb1.deselect()
    except ValueError:
        error_label = Label(win2, text='Not rated').grid(row = 4, column = 1, columnspan = 5)

    try:
        front_rating = int(dictionary['OverallFrontCrashRating'])
        x = 5 - front_rating
        for i in range(front_rating):
            rb2 = Radiobutton(win2, variable=var2, value='3', fg='red')
            rb2.grid(row = 5, column=i+1)
            rb2.select()
        for i in range(x):
            rb3 = Radiobutton(win2, variable=var3, value='4', state=DISABLED)
            rb3.grid(row = 5, column=front_rating+1+i)
            rb3.deselect()
    except ValueError:
        error_label = Label(win2, text='Not rated').grid(row = 5, column = 1, columnspan = 5)

    try:
        side_rating = int(dictionary['OverallSideCrashRating'])
        x = 5 - side_rating
        for i in range(side_rating):
            rb4 = Radiobutton(win2, variable=var4, value='5', fg='red')
            rb4.grid(row = 6, column=i+1)
            rb4.select()
        for i in range(x):
            rb5 = Radiobutton(win2, variable=var5, value='6', state=DISABLED)
            rb5.grid(row = 6, column=side_rating+1+i)
            rb5.deselect()
    except ValueError:
        error_label = Label(win2, text='Not rated').grid(row = 6, column = 1, columnspan = 5)
    
    try:
        rollover_rating = int(dictionary['RolloverRating'])
        x = 5 - rollover_rating
        for i in range(rollover_rating):
            rb6 = Radiobutton(win2, variable=var6, value='7', fg='red')
            rb6.grid(row = 7, column=i+1)
            rb6.select()
        for i in range(x):
            rb7 = Radiobutton(win2, variable=var7, value='8', state=DISABLED)
            rb7.grid(row = 7, column=rollover_rating+1+i)
            rb7.deselect()
    except ValueError:
        error_label = Label(win2, text='Not rated').grid(row = 7, column = 1, columnspan = 5)

    img_url_front = dictionary['FrontCrashPicture']
    img_url_side = dictionary['SideCrashPicture']
    empty_col = Label(win2, text='           ').grid(row=2 , column=6)
    image_data_front = urlopen(img_url_front).read()
    image_front = Image.open(BytesIO(image_data_front))
    image_front = ImageTk.PhotoImage(image_front)
    front_img_label = Label(win2, image=image_front, relief = 'sunken', bd=7)
    front_img_label.image = image_front
    front_img_label.grid(row=1, column=12,rowspan=10)

    image_data_side = urlopen(img_url_side).read()
    image_side = Image.open(BytesIO(image_data_side))
    image_side = ImageTk.PhotoImage(image_side)
    side_img_label = Label(win2, image=image_side, relief = 'sunken', bd=7)
    side_img_label.image = image_side
    side_img_label.grid(row=12, column=12, rowspan=5)    

def center_window(width=400, height=350):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    win.geometry('%dx%d+%d+%d' % (width, height, x, y))
    win.geometry("")

def clear():
    global num_of_clicks
    num_of_clicks = 0
    make_table.grid_remove()
    model_table.grid_remove()
    variant_table.grid_remove()
    make_label.grid_forget()
    model_label.grid_forget()
    variant_label.grid_forget()
    year_table['state'] = NORMAL

win = Tk()
center_window()

default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(family = "Comic Sans MS", size=13)

year_table_content = make_request("","ModelYear")

year_label = Label(win, text = 'Select production year:')
year = StringVar()
year.set(year_table_content[0])
year_table = OptionMenu(win, year, *year_table_content)
submit_button = Button(win, text = "Submit", command = submit)
clear_button = Button(win, text='Clear', command=clear)

year_label.grid(row = 0, column = 0)
year_table.grid(row = 1, column = 0)
empty_col = Label(win, text='        ').grid(row=0, column=1)
submit_button.grid(row = 0, column = 2)
clear_button.grid(row = 1, column = 2)

win.mainloop()