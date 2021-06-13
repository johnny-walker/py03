import tkinter as tk
import requests
from bs4 import BeautifulSoup
import webbrowser

# import root window
import Root as rt


class NewsViewer(rt.ProgramBase):
    sports_all = []
    links = []
    divData = None
    lblMsg = None

    def __init__(self, root, width=640, height=480):
        super().__init__(root, width, height)
        self.root.resizable(False, False)
        self.root.title("Yahoo Sports News")

    def loadNews(self):
        # 定義網址
        base_url = "https://tw.news.yahoo.com"
        url = "https://tw.news.yahoo.com/sports/archive/"

        # 向網址要回網頁原始碼，並透過 BeautifulSoup 解析
        '''
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        '''

        start = 0
        pages = range(start, start+1)

        for page in pages:
            print(url + str(page) + ".html")
            yahoo_r = requests.get(url + str(page) + ".html")
            yahoo_soup = BeautifulSoup(yahoo_r.text, 'html.parser')
            sports = yahoo_soup.findAll('h3')
            self.sports_all.append(sports)

        len(self.sports_all)
        for sports in self.sports_all:
            for info in sports:
                link = ""
                try:
                    link = info.findAll('a', href=True)[0]
                    title = link.get_text()
                    #print(title)
                    # filter out 一覽表
                    if link.get('href') != '#':
                        full_url = base_url + link.get("href")
                        self.links.append((title, full_url))
                        #print(full_url)
                except:
                    print("exception")
                    link = None
        print(len(self.links))

        # save index file
        '''
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
        index_file = 'index-{0:s}.txt'.format(dt_string)
        self.check_dir(index_file)         
        '''

    def defineLayout(self, widgets, cols=1, rows=1):
        def method(widget):
            for c in range(cols):    
                widget.columnconfigure(c, weight=1)
            for r in range(rows):
                widget.rowconfigure(r, weight=1)
            return

        if type(widgets)==list:        
            [ method(wgt) for wgt in widgets ]
        else:
            wgt = widgets
            method(wgt) 

    def loadLayout(self):
        align_mode = 'nswe'
        padding= 3
        msgHeight = 40

        self.imgWidth = self.root.width
        self.imgHeight = self.root.height - msgHeight

        divData = tk.Frame(self.root,  width=self.imgWidth , height=self.imgHeight , bg='white')
        divMsg = tk.Frame(self.root,  width=self.imgWidth , height=msgHeight , bg='black')

        self.root.update()

        divData.grid(row=0, column=0, padx=padding, pady=padding, sticky=align_mode)
        divMsg.grid(row=1, column=0, padx=padding, pady=padding, sticky=align_mode)

        self.defineLayout(self.root)
        self.defineLayout(divData, 20, 1)
        self.defineLayout(divMsg, 1, 1)

        # label as container of image
        self.divData = divData

        # label as message
        self.lblMsg = tk.Label(divMsg, text='show message here', bg='black', fg='white')
        self.lblMsg.grid(row=0, column=0, sticky='w')

    def showMessage(self, msg):
        self.lblMsg['text'] = msg


    def feedNews(self):
        self.loadLayout()
        if len(self.links):
            self.createPage()
            self.showMessage('{0} news found'.format(len(self.links)))
        else:
            self.showMessage('No news found')

    def createPage(self):
        for i in range(0, len(self.links)):
            self.createItem(i, self.links[i])

    def createItem(self, no, data):
        color = '#ceddf0' #if (no % 2 == 0) else '#d7f7df'

        lblItem = tk.Label(self.divData,                     
                             bg=color,  
                             font=('Arial', 12),           
                             width=self.root.width,
                             text=data[0] )
        lblItem.grid(row=no+1, sticky='w')
        lblItem.bind("<Enter>", self.onEnter)
        lblItem.bind("<Leave>", self.onLeave)
        lblItem.bind("<Button-1>", self.onClick)

    def onEnter(self, event):
        event.widget.config(bg='#defdff')

    def onLeave(self, event):
        event.widget.config(bg='#ceddf0')

    def onClick(self, event):
        print(event.widget['text'])
        for i in range(0, len(self.links)):
            if self.links[i][0] == event.widget['text']:
                webbrowser.open_new(self.links[i][1])

if __name__ == '__main__':
    program = NewsViewer(tk.Tk())

    program.loadNews()
    program.feedNews()

    program.run()
    print("quit, bye bye ...")
