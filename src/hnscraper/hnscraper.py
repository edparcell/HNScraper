'''
Created on Sep 15, 2010

@author: edparcell
'''

import mechanize
from BeautifulSoup import BeautifulSoup
        
def get_unique(g):
    l=list(g)
    assert(len(l)==1)
    return l[0]

class HNScraper:
    def __init__(self):
        self.br = mechanize.Browser()
        self.nav_home()
        
    def nav_home(self):
        """Go to Hacker News home page"""
        self.br.open("http://news.ycombinator.com/")
        
    def nav_user_page(self):
        """Go to HN user page"""
        self.nav_home()
        L = list(self.br.links())
        logout_index = get_unique([i for i,l in enumerate(L) if l.text=='logout'])
        self.br.follow_link(L[logout_index-1])
        
    def nav_saved_stories(self):
        """Go to HN user's saved story page - list of contributed stories, plus upvoted stories"""
        self.nav_user_page()
        saved_stories_link = get_unique(self.br.links(text_regex='saved stories'))
        self.br.follow_link(saved_stories_link)
           
    def nav_more(self):
        """Go to next page of stories"""
        more_link = get_unique(self.br.links(text='More'))
        self.br.follow_link(more_link)
        
    def more_available(self):
        """Returns true if there is a next page"""
        more_links = self.br.links(text='More')
        return len(list(more_links))==1
        
    def login_with_google(self, username, password):
        """Login using clickpass and a google account"""
        self.nav_home()        
        br = self.br
        
        login_link = get_unique(br.links(text='login'))
        br.follow_link(login_link)

        clickpass_link = get_unique(br.links(url_regex=r'clickpass\.com'))
        br.follow_link(clickpass_link)

        br.select_form(predicate=lambda f: f.attrs.get('id') =='clickpassForm')
        br.submit()

        google_link = get_unique(br.links(url_regex="googlestart"))
        br.follow_link(google_link)

        br.select_form(predicate=lambda f: f.attrs.get('id') =='gaia_loginform')
        br["Email"] = username
        br["Passwd"] = password
        br.submit()
        
        br.select_form(nr=0)
        br.submit(name='allow')
        
        br.select_form(nr=0)
        br.submit()

    def get_current_page_text(self):
        """Get the text of the current page"""
        return self.br.response().read()
    
    def get_current_page_stories(self):
        """Pull the stories from the current page into a list of dictionaries, one per story."""
        text = self.get_current_page_text()
        soup = BeautifulSoup(text)
        s = {}
        for tr in soup.findAll('tr'):
            if len(tr) == 3:
                tds = tr('td')
                if len(tds) == 3:
                    if (tds[0].get('class') == 'title' and 
                            tds[0].get('align') == 'right' and
                            tds[0].get('valign') == 'top' and 
                            tds[2].get('class') == 'title'):
                        ord = tds[0].string
                        if ord.endswith('.'):
                            ord = int(ord[:-1])
                        a_s = tds[2]('a')
                        spans = tds[2]('span')
                        if len(a_s) >= 1 and len(spans) <= 1:
                            a = a_s[0]
                            link =  a['href']
                            title = a.string
                            s = {'ord': ord ,'link': link, 'title': title}
                            if len(spans)==1:
                                span = spans[0]
                                comhead = span.string
                                s.update(comhead=comhead)
                            continue
            if len(tr) == 2:
                tds = tr('td')
                if len(tds) == 2:
                    if (tds[0].get('colspan') == '2' and
                            tds[1].get('class') == 'subtext'):
                        score = tds[1].span.string
                        if score.endswith(' points'):
                            score = int(score[:-7])
                        user = tds[1].a.string
                        s.update(score=score, user=user)
                        yield s
                        s={}
            s = {}