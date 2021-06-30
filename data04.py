import requests
from bs4 import BeautifulSoup
import webbrowser

import tkinter as tk
import tkinter.ttk as ttk
from Root import ProgramBase

class PTTCrawler():
    def __init__(self, board = 'movie'):
        self.domain = 'https://www.ptt.cc'
        self.page = self.domain + '/bbs/movie/index.html'

    def getPosts(self, board):
        self.page = self.domain + '/bbs/{0:s}/index.html'.format(board)
        response = requests.get(self.page)
        soup = BeautifulSoup(response.text, 'lxml')

        articles = soup.find_all('div', 'r-ent')
        posts = list() 
        for article in articles:
            meta = article.find('div', 'title').find('a') 
            if not meta:  # skip 刪文
                continue 
            posts.append({
                'title': meta.getText().strip(),
                'link': meta.get('href'),
                'push': article.find('div', 'nrec').getText(),
                'date': article.find('div', 'date').getText(),
                'author': article.find('div', 'author').getText(),
            })
        return posts

    def getDomain(self):
        return self.domain

    def getPage(self):
        return self.page

class PTTViewer(ProgramBase):
    postbg = '#ddeedd'

    def __init__(self, root, width=800, height=600):
        super().__init__(root, width, height)
        self.root.title("PTT Posts")
        self.crawer = PTTCrawler()
        self.posts = list()
        self.loadLayout()
    
    def showPage(self, board):
        self.posts = self.crawer.getPosts(board)
        self.root.title("PTT BOARD - " + board.upper())
        self.showMessage(self.crawer.getPage())
        self.showPosts(self.posts)
    
    def loadLayout(self):
        align_mode = 'nswe'
        padding= 2
        msgHeight = 40
        optHeight = 40
        self.dataWidth = self.root.width
        self.dataHeight = self.root.height - optHeight - msgHeight

        self.divOptions = tk.Frame(self.root,  width=self.dataWidth , height=optHeight)
        self.divOptions.grid(row=0, columnspan=4, padx=padding, pady=padding, sticky=align_mode)
        
        self.divData = tk.Frame(self.root,  width=self.dataWidth , height=self.dataHeight , bg=self.postbg)
        self.divData.grid(row=1, padx=padding, pady=padding, sticky=align_mode)
        
        self.divMsg = tk.Frame(self.root,  width=self.dataWidth , height=msgHeight , bg='black')
        self.divMsg.grid(row=2, columnspan=4, padx=padding, pady=padding, sticky=align_mode)

        #define widgets' relative ratio )
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.divData.columnconfigure(0, weight=1)
        self.divData.columnconfigure(1, weight=10)
        self.divData.columnconfigure(2, weight=1)
        self.divData.columnconfigure(3, weight=2)

        # label as message
        self.lblMsg = tk.Label(self.divMsg, text='show message here', bg='black', fg='white')
        self.lblMsg.grid(row=0, column=0, sticky='w')

    def showOptions(self, boards):
        padding = 1
        label = tk.Label( self.divOptions,  text=" PTT Board Selection: ")
        label.grid(row=0, column=0, sticky='nswe')

        combobox = ttk.Combobox(self.divOptions, values=boards, width=20, height=1)
        combobox.current(0)   # select first one
        combobox.grid(row=0, column=1, columnspan=3, padx=padding, pady=padding) 

        combobox.bind('<<ComboboxSelected>>', self.optSelected)

    def optSelected(self, event):
        print(event.widget.get())
        self.showPage(event.widget.get())

    def showPosts(self, posts):
        padding =2
        for child in self.divData.winfo_children():
            child.destroy()

        for row in range(len(posts)):
            color = 'black'
            tk.Label(self.divData, fg=color, bg=self.postbg, text=posts[row]['push']).grid(row=row, column=0, padx=padding, pady=padding, sticky='e')
            title = tk.Label(self.divData, fg=color, bg=self.postbg, text=posts[row]['title'])
            title.grid(row=row, column=1, padx=padding, pady=padding, sticky='w')
            tk.Label(self.divData, fg=color, bg=self.postbg, text=posts[row]['date']).grid(row=row, column=2, padx=padding, pady=padding, sticky='w')
            tk.Label(self.divData, fg=color, bg=self.postbg, text=posts[row]['author']).grid(row=row, column=3, padx=padding, pady=padding, sticky='w')
        
            # bind mouse events
            title.bind("<Enter>", self.onEnter)
            title.bind("<Leave>", self.onLeave)
            title.bind("<Button-1>", self.onClick)

    def onEnter(self, event):
        event.widget.config(fg='blue')

    def onLeave(self, event):
        event.widget.config(fg='black')

    def onClick(self, event):
        print(event.widget['text'])
        for i in range(0, len(self.posts)):
            if self.posts[i]['title'] == event.widget['text']:
                link = self.crawer.getDomain() +  self.posts[i]['link']
                webbrowser.open_new(link)

    def showMessage(self, msg):
        self.lblMsg['text'] = msg

if __name__ == '__main__':
    program = PTTViewer(tk.Tk())
    boards = ['NBA', 'MLB', 'Baseball', 'Music', 'Movie', 'Stock', 'Joke', 'KoreaStar','Boy-Girl', 'NSwitch','Car']
    program.showOptions(boards)
    program.showPage('NBA')
    program.run()


