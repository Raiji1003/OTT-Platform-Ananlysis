from tkinter import *
from tkinter import messagebox
import pywinstyles
from PIL import ImageTk
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

# Create the main Tkinter window
root = Tk()
root.geometry("1270x640+0+0")

pywinstyles.change_header_color(root, color="black")

# Connect to SQLite database
conn = sqlite3.connect('users.db')

def create_tables():
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            Fname TEXT NOT NULL,
            Lname TEXT NOT NULL,
            Age INTEGER NOT NULL,
            Interested_in TEXT NOT NULL,
            Username TEXT PRIMARY KEY,
            Password TEXT NOT NULL
        )
    ''')
    conn.commit()

create_tables()

def show_registration_form():
    clear_frame()
    
    root.title("Login/Registration Form")
    
    fname=StringVar()
    lname=StringVar()
    age=IntVar()
    interested=StringVar()
    usern=StringVar()
    passw=StringVar()
    
    # Function to change button color on hover
    def on_enter(e):
        submit_button.config(bg="light pink")

    # Function to change button color back when mouse leaves
    def on_leave(e):
        submit_button.config(bg="sky blue")

    background_image = ImageTk.PhotoImage(file="C:/Users/Admin/OneDrive/Desktop/mini project/DVP/BG.png")

    canvas = Canvas(root)
    canvas.pack(fill="both", expand=True)

    canvas.create_image(0 ,0 , image=background_image, anchor="nw")

    canvas.create_text(290, 80, text="Registration form", fill="white", font=('times', 20 , 'bold'))

    canvas.create_text(210,140,text="First name :-", fill="white", font=('times', 20 , 'bold'))
    fname_en=Entry(root,textvariable=fname,font=("times",12,"bold")).place(x=300,y=130,width=130)

    canvas.create_text(210,200,text="Last name :-", fill="white", font=('times', 20 , 'bold'))
    lname_en=Entry(root,textvariable=lname,font=("times",12,"bold")).place(x=300,y=190,width=130)

    canvas.create_text(250,260,text="Age :-", fill="white", font=('times', 20 , 'bold'))
    age_en=Entry(root,textvariable=age,font=("times",12,"bold")).place(x=300,y=250,width=130)

    canvas.create_text(200,320,text="Interested in :-", fill="white", font=('times', 20 , 'bold'))
    interest_en=Entry(root,textvariable=interested,font=("times",12,"bold")).place(x=300,y=310,width=130)
    
    canvas.create_text(210,380,text="Username :-" ,fill="White",font=('times', 20 , 'bold'))
    usern_en=Entry(root,textvariable=usern,font=('times', 12 , 'bold')).place(x=300,y=370,width=130)
    
    canvas.create_text(215,440,text="Password :-",fill="white",font=('times', 20 , 'bold'))
    pass_en=Entry(root,textvariable=passw,font=('times', 12 , 'bold'), show="*").place(x=300,y=430,width=130)

    submit_button = Button(root, text="Sign up",command=lambda:complete_registration(fname.get(),lname.get(),age.get(),interested.get(),usern.get(),passw.get()), relief="raised", font=("times", 12, "bold"), bg="sky blue")
    submit_button.place(x=250, y=480, width=80)

    # Bind events to button for hover effect
    submit_button.bind("<Enter>", on_enter)
    submit_button.bind("<Leave>", on_leave)
    
    # Create text "Sign in" and bind the event to the text
    sign_in_text = canvas.create_text(290, 530, text="Already have an account : Log in", fill="white", font=('times', 15 , 'bold'))
    canvas.tag_bind(sign_in_text, "<Button-1>", lambda event: show_login_form())
    
    root.mainloop()
    
def complete_registration(fname,lname,age,interested,usern,passw):
    if fname and lname and age and interested and usern and passw:
        cursor=conn.cursor()
        cursor.execute("SELECT Username FROM Users WHERE Username=?", (usern,))
        existing_user = cursor.fetchone()
        if existing_user:
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        else:
            # Insert the new user if the username is unique
            cursor.execute('INSERT INTO Users(Fname, Lname, Age, Interested_in, Username, Password) VALUES(?, ?, ?, ?, ?, ?)', (fname, lname, age, interested, usern, passw))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful. Log in to continue.")
            show_login_form()
    
    else:
        messagebox.showerror("Error","Please fill all data")     
    
    
def clear_frame():                  #to destroy all the inputs
    for widget in root.winfo_children():
        widget.destroy()

def show_login_form():
    
    clear_frame()
    root.title("Login/Registration Form")
    
    usern=StringVar()
    passw=StringVar()
    
    def on_enter(e):
        submit_button.config(bg="light pink")

    def on_leave(e):
        submit_button.config(bg="sky blue")

    background_image = ImageTk.PhotoImage(file="C:/Users/Admin/OneDrive/Desktop/mini project/DVP/BG.png")
    
    canvas = Canvas(root)               #creating a transparent page (canvas)
    canvas.pack(fill="both", expand=True)
    
    canvas.create_image(0 ,0 , image=background_image, anchor="nw")
    
    canvas.create_text(290, 80, text="Login form", fill="white", font=('times', 20 , 'bold'))
    
    canvas.create_text(210,140,text="Username :-", fill="white", font=('times', 20 , 'bold'))
    user_en=Entry(root,textvariable=usern, font=('times', 12 , 'bold')).place(x=300,y=130,width=130)
    
    canvas.create_text(210,200,text="Password :-", fill="white", font=('times', 20 , 'bold'))
    pass_en=Entry(root,textvariable=passw, font=('times', 12 , 'bold'), show="*").place(x=300,y=190,width=130)
    
    submit_button = Button(root, text="Login in", command=lambda: complete_login(usern.get(), passw.get()), relief="raised", font=("times", 12, "bold"), bg="sky blue")
    submit_button.place(x=250, y=240, width=80)
    
    submit_button.bind("<Enter>", on_enter)
    submit_button.bind("<Leave>", on_leave)
    
    sign_in_text = canvas.create_text(290, 290, text="Don't have an account : Sign up", fill="white", font=('times', 15 , 'bold'))
    canvas.tag_bind(sign_in_text, "<Button-1>", lambda event: show_registration_form())

    root.mainloop()
    
def complete_login(usern,passw):
    if usern and passw:
        cursor = conn.cursor()
        cursor.execute("SELECT Username,Password FROM Users WHERE Username=?", ((usern),))
        data = cursor.fetchone()
        if data:
            username , password = data
            if usern==username and passw==password:
                messagebox.showinfo("Login Successful", "Welcome, Admin!")
                show_main_menu()
                
            else:
                messagebox.showerror("Login Failed", "Invalid password")
            
        else:
            messagebox.showerror("Error","Username doesn't exist")    
        
    else:
        messagebox.showerror("Error","Please fill all data")    
        
def abt_us():
    clear_frame()
    
    root.title("About us")
    
    menubar=Menu(root)
    root.config(menu=menubar)
    
    menubar.add_command(label="About Us", command=abt_us)
    menubar.add_command(label="Home", command=show_main_menu)
    
    background_image=ImageTk.PhotoImage(file="C:/Users/Admin/OneDrive/Desktop/mini project/DVP/main bg.png")
    canvas = Canvas(root)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0 ,0 , image=background_image, anchor="nw")
    canvas.create_text(650,50,text="TEAM MEMBERS",fill="white", font=('times', 25 , 'bold'))
    
    
    root.mainloop()
    
def show_main_menu():
    clear_frame()
    
    root.title("Main Page")
    
    background_image = ImageTk.PhotoImage(file="C:/Users/Admin/OneDrive/Desktop/mini project/DVP/main bg.png")
    
    menubar = Menu(root)
    root.config(menu=menubar)
    
    menubar.add_command(label="About Us", command=abt_us)
    menubar.add_command(label="Home", command=show_main_menu)
    
    search = StringVar()
    
    canvas = Canvas(root)
    canvas.pack(fill="both", expand=True)

    canvas.create_image(0 ,0 , image=background_image, anchor="nw")
    
    def on_entry_click(event):
        if search_en.get() == "Search here...":
            search_en.delete(0, "end") # delete all the text in the entry
            search_en.insert(0, '') #Insert blank for user input
            search_en.config(fg = 'black')

    def on_focusout(event):
        if search_en.get() == '':
            search_en.insert(0, "Search here...")
            search_en.config(fg = 'grey')

    def on_key_release(event):
        suggestions = ["Netflix vs other OTT platforms","Ratings Distribution of Web Series","Number of web series on each OTT Platform"]
        search_text = search_en.get().lower()
        suggested_options = [option for option in suggestions if search_text in option.lower()]
        update_suggestions(suggested_options)
        
    def update_suggestions(suggestions):
        suggestion_listbox.delete(0, END)
        for suggestion in suggestions:
            suggestion_listbox.insert(END, suggestion)
        
        if suggestions:
            suggestion_listbox.place(x=420, y=search_en.winfo_y() + search_en.winfo_height(), width=280)
        else:
            suggestion_listbox.place_forget()
            
    def on_suggestion_click(event):
        if suggestion_listbox.curselection():  # Check if selection is not empty
            index = suggestion_listbox.curselection()[0]
            selected_option = suggestion_listbox.get(index)
            search_en.delete(0, END)
            search_en.insert(0, selected_option)
        
    #search for the any analysis based on ott platforms
    canvas.create_text(600,210,text="Search for any", fill="white", font=('times', 35 , 'bold'))
    canvas.create_text(600,260,text="analysis based on ", fill="white", font=('times', 35 , 'bold'))
    canvas.create_text(600,310,text="ott platforms", fill="white", font=('times', 35 , 'bold'))
    
    search_en=Entry(root,textvariable=search,font=('times', 22 ))
    search_en.insert(0, "Search here...")
    search_en.bind('<FocusIn>', on_entry_click)
    search_en.bind('<FocusOut>', on_focusout)
    search_en.bind('<KeyRelease>', on_key_release)
    search_en.place(x=420, y=360, width=280)
    
    suggestion_listbox = Listbox(root, font=('times', 16))
    suggestion_listbox.bind('<Button-1>', on_suggestion_click)
    
    search_button=Button(root,text="Search",bg="red",font=('times', 14 , 'bold'),command=lambda:error_handling_in_analysis(search.get()),relief="raised")
    search_button.place(x=700,y=360,width=150)
    
    root.mainloop()
    
        
def error_handling_in_analysis(search):
    if search:
        if search=='Netflix vs other OTT platforms' or search=='Ratings Distribution of Web Series' or search=='Number of web series on each OTT Platform':
            analysis(search)
        else :
            messagebox.showerror("Error","Enter the valid input")
    else:
        messagebox.showerror("Error","Please enter what you want to search")


def analysis(search):
    clear_frame()
    
    global plot_canvas  # Declare plot_canvas as global variable
    
    root.title("Analysis( Visualizattion )")
    
    data = pd.read_csv("webseries (2).csv")

    menubar=Menu(root)
    root.config(menu=menubar)
    
    menubar.add_command(label="About Us", command=abt_us)
    menubar.add_command(label="Home", command=show_main_menu)
    
    def decision():
        if search=="Netflix vs other OTT platforms":
            plot1()
        elif search=="Ratings Distribution of Web Series":
            plot2()
        elif search=="Number of web series on each OTT Platform":
            plot3()
        else :
            messagebox.showerror("Error","Enter the valid input")

    def plot1():
        global plot_canvas  # Access plot_canvas from global scope
        netflix_series = data[data['ott_platform'] == 'Netflix']

        # Filter the DataFrame to include TV series not available on Netflix
        other_series = data[data['ott_platform'] != 'Netflix']

        # Plotting the distribution of ratings for Netflix series and other series
        plt.figure(figsize=(10, 6))

        # Plotting Netflix series ratings
        plt.hist(netflix_series['ratings'], bins=10, color='red', alpha=0.5, label='Netflix')

        # Plotting ratings of series on other platforms
        plt.hist(other_series['ratings'], bins=10, color='blue', alpha=0.5, label='Other Platforms')

        plt.title('Distribution of Ratings for TV Series on Netflix vs Other Platforms')
        plt.xlabel('Ratings')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        if plot_canvas:
            plot_canvas.get_tk_widget().destroy()
        
        plot_canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().pack()
        
    def plot2():
        global plot_canvas  # Access plot_canvas from global scope
        plt.figure(figsize=(7, 5))
        plt.hist(data['ratings'], bins=10, color='skyblue', edgecolor='black')
        plt.title('Ratings Distribution of Web Series')
        plt.xlabel('Ratings')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.tight_layout()
        
        if plot_canvas:
            plot_canvas.get_tk_widget().destroy()
        
        plot_canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().pack()
        
    def plot3():
        global plot_canvas  # Access plot_canvas from global scope
        # Count the number of TV series on each OTT platform
        platform_counts = data['ott_platform'].value_counts()

        # Plotting the bar chart
        plt.figure(figsize=(10, 6))
        platform_counts.plot(kind='bar', color='skyblue')
        plt.title('Number of web series on each OTT Platform')
        plt.xlabel('OTT Platform')
        plt.ylabel('Number of TV Series')
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.grid(axis='y')  # Show gridlines on the y-axis
        plt.tight_layout()
        
        if plot_canvas:
            plot_canvas.get_tk_widget().destroy()
        
        plot_canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().pack()
        
    def exit_plot():    
        root.quit()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    plot_canvas = None

    plot_button = Button(root, text="Plot graph", command=decision)
    plot_button.pack(pady=20)

    plot_exit=Button(root,text="Exit",command=exit_plot)
    plot_exit.place(x=730,y=20,width=50)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()
    
    
show_login_form()

