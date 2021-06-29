import requests
from bs4 import BeautifulSoup
import webbrowser

import tkinter as tk
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
    def __init__(self, root, width=640, height=480):
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
        def defineLayout(widget, cols=1, rows=1):
            #https://stackoverflow.com/questions/45847313/what-does-weight-do-in-tkinter
            for c in range(cols):    
                widget.columnconfigure(c, weight=1)
            for r in range(rows):
                widget.rowconfigure(r, weight=1)

        align_mode = 'nswe'
        padding= 2
        msgHeight = 40

        self.imgWidth = self.root.width
        self.imgHeight = self.root.height - msgHeight

        self.divData = tk.Frame(self.root,  width=self.imgWidth , height=self.imgHeight , bg='white')
        self.divData.grid(row=0, padx=padding, pady=padding, sticky=align_mode)
        divMsg = tk.Frame(self.root,  width=self.imgWidth , height=msgHeight , bg='black')
        divMsg.grid(row=1, columnspan=4, padx=padding, pady=padding, sticky=align_mode)

        defineLayout(self.root)
        self.divData.columnconfigure(0, weight=1)
        self.divData.columnconfigure(1, weight=20)
        self.divData.columnconfigure(2, weight=2)
        self.divData.columnconfigure(3, weight=4)

        # label as message
        self.lblMsg = tk.Label(divMsg, text='show message here', bg='black', fg='white')
        self.lblMsg.grid(row=0, column=0, sticky='w')

    def showPosts(self, posts):
        for row in range(len(posts)):
            color = 'black'
            print(posts[row]['push'], posts[row]['title'], posts[row]['date'], posts[row]['author'])
            tk.Label(self.divData, fg=color, text=posts[row]['push']).grid(row=row, column=0, padx=5, pady=5, sticky='e')
            title = tk.Label(self.divData, fg=color, text=posts[row]['title'])
            title.grid(row=row, column=1, padx=5, pady=5, sticky='w')
            tk.Label(self.divData, fg=color, text=posts[row]['date']).grid(row=row, column=2, padx=5, pady=5, sticky='w')
            tk.Label(self.divData, fg=color, text=posts[row]['author']).grid(row=row, column=3, padx=5, pady=5, sticky='w')
        
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
    program.showPage('movie')
    program.run()


