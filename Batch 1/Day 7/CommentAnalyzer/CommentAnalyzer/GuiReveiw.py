import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import nltk
nltk.download('vader_lexicon')

analyzer=SentimentIntensityAnalyzer()


def get_sentiment_score(score):
    if(score>=0.05):
        return 1
    elif(score<=-0.05):
        return -1
    else:
        return 0


def statistical_analyzer(reviews,details=False):
    posCount,negCount,neuCount=0,0,0
    responseList=[]
    for review in reviews:
        result=analyzer.polarity_scores(review)
        response=get_sentiment_score(result['compound'])
        responseList.append(response)
        if(details):
            print(result)
            print(f"Text: {review}\nResult:{response}\n\n")

    for response in responseList:
        if response==1:
            posCount+=1
        elif response==-1:
            negCount+=1
        else:
            neuCount+=1
    # print(responseList,"\n\n\n",len(responseList))
    return posCount,negCount,neuCount

def graphical(pos,neg,neu):
    context=["Positive","Negative","Neutral"]
    percentage=[pos,neg,neu]
    colors = ['#4CAF50', '#F44336', '#9E9E9E']
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(percentage, labels=context, autopct="%.1f%%", colors=colors, startangle=90)
    ax.set_title("Sentiment Distribution")

    for widget in chart_frame.winfo_children():
        widget.destroy()  # Clear previous chart

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    



#------------------tkinter part--------------------------------------------

def analyze_review():
    input_text=text_area.get("1.0",tk.END).strip()

    if(not input_text):
        messagebox.showwarning("Warning!","Please enter reviews for analyzed Report")
        return
    reviews=input_text.split("\n")
    pos,neg,neu=statistical_analyzer(reviews)


    #updating
    result_text.config(state=tk.NORMAL) if 'tk' in globals() else print("Tk not defined!")

    result_text.delete("1.0",tk.END)
    result_text.insert(tk.END, f"Positive Reviews: {pos}\n")
    result_text.insert(tk.END, f"Negative Reviews: {neg}\n")
    result_text.insert(tk.END, f"Neutral Reviews: {neu}\n")
    result_text.config(state=tk.DISABLED)

    graphical(pos,neg,neu)


commentsSample1 = [
    "This app is absolutely amazing! So smooth and easy to use.",  # Positive 😊
    "I hate the latest update. It ruined everything!",  # Negative 😡
    "The UI is decent, but nothing special.",  # Neutral 😐
    "Great features, but some bugs make it frustrating to use.",  # Mixed (Positive + Negative)
    "It’s okay, but I wouldn’t recommend it over other apps.",  # Neutral 😐
    "I love how intuitive the design is!",  # Positive 😊
    "Too many ads! It’s annoying and ruins the experience.",  # Negative 😡
    "The app works fine, but it lacks innovation.",  # Neutral 😐
    "This has potential, but it needs serious improvements.",  # Mixed (Neutral + Negative)
    "Best app I’ve used in a long time! 10/10 would recommend!",  # Positive 😊
]
commentsSample2=[
    # Positive Reviews 😊
    "This app is absolutely amazing! So smooth and easy to use.",  
    "I love how intuitive the design is!",  
    "Best app I’ve used in a long time! 10/10 would recommend!",  
    "Great features, and the customer support is excellent!",  
    "The latest update fixed all the bugs. Works perfectly now!",  
    "Super fast and reliable. Exactly what I needed.",  
    "Fantastic user experience. Highly recommended!",  

    # Negative Reviews 😡
    "I hate the latest update. It ruined everything!",  
    "Too many ads! It’s annoying and ruins the experience.",  
    "The app crashes every time I try to open it. Useless!",  
    "Terrible UI. Hard to navigate and confusing.",  
    "Customer support is completely unresponsive!",  
    "I regret downloading this. Waste of time.",  
    "So many bugs! It’s frustrating to use.",  

    # Neutral Reviews 😐
    "The UI is decent, but nothing special.",  
    "It’s okay, but I wouldn’t recommend it over other apps.",  
    "The app works fine, but it lacks innovation.",  
    "Nothing extraordinary, just an average app.",  
    "This has potential, but it needs serious improvements.",  
    "Some features are good, but others are pointless."  
]


#------------------------------setting up Tkinter---------------------------------------
    
root=tk.Tk()
root.title("Review Analysis")
root.geometry("900x600")
try:
    #image
    image = Image.open("./Day 7/CommentAnalyzer/CommentAnalyzer/back.jpeg")  
    image = image.resize((900, 600), Image.LANCZOS)  # Resize to match window size
    bg_image = ImageTk.PhotoImage(image)

    #Set Background Label
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)  # Stretch to full window size
except:
    print("Image not found")
# Place widgets on top of the background
frame = tk.Frame(root, bg="white", bd=5)  # A frame to hold widgets (improves visibility)
frame.place(relx=0.5, rely=0.05, anchor="n")  # Centered at top

tk.Label(root,text="Enter Set of Reviews",font=("Times New Roman",25,"bold"),fg="white",bg="black").pack(pady=10)
text_area=scrolledtext.ScrolledText(root,width=70,height=8,font=("Helvetica", 18, "italic"))
text_area.pack(pady=20,padx=20)

#Analyze and show result button
analyze_button=tk.Button(root,text="Submit",font=("Helvetica", 18, "italic"),command=analyze_review)
analyze_button.pack(pady=10)



# Frame for Result & Chart Side by Side
result_chart_frame = tk.Frame(root, bg="black")
result_chart_frame.pack(fill="both", expand=True)


# Results Section (Left Side) without Scroll
result_text = tk.Text(result_chart_frame, width=5, height=1, font=("Arial", 12), state=tk.DISABLED)
result_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Expand with window


# Make it expand with window
#chart
chart_frame = tk.Frame(result_chart_frame, bg="pink")
chart_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Adjust column weights so they resize proportionally
result_chart_frame.columnconfigure(0, weight=1)
result_chart_frame.columnconfigure(1, weight=1)
result_chart_frame.rowconfigure(0, weight=1)

root.mainloop()