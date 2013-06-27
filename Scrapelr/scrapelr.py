#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# I know, there's an api for this kind of stuff.
#

from bs4 import BeautifulSoup as bs4
import requests, os

# colored output, if possible
try:
    from termcolor import colored,cprint
except:
    def colored(text,color=None):
        return text
    def cprint(text,color=None):
        print(text)

SIZES           = [1280,500,400,250,100,75] # <-- tumblr sizes
OVERWRITE       = False # <-- overwrite existing images
BRUTEFORCELIMIT = 3 # <-- tries next N pages, if one has no valid images
HTML_PARSER     = 'html.parser' # <-- html.parser seems to be the best for this job

#HTTP Headers
HEADERS   = {
'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0"
}

VERBOSE = False
DEBUG   = False

def safe_filename(fn):
    #removes path seperator and NULL, everything else is a valid filename
    fn = fn.replace(os.path.sep,'')
    fn = fn.replace('\0','')
    #avoid leading and tailing dots
    fn = fn.strip('.') 
    #remove some anoying chars
    fn = fn.replace('\n','')
    if fn == '':
        return None
    else:
        return fn
    

# ==============================================================================
# FIXME:
#        [ ] Catch all exception.
#        [ ] Improve verbose output
#        [ ] Improve debug output
# ==============================================================================

class Scrapelr():

    def __init__(self,url,path = './',verbose = True, debug = False):
        self.path = path
        self.url = url
        self.verbose = verbose
        self.debug = debug
        self.image_urls = []

        self.pl();self.p("Fetching: %s" % self.url,'yellow')
        self.__SetupPage()
        self.pl()

        if self.page is None:
            self.p("Error while fetching: %s" % self.err,'red')
            raise ValueError #FIXME: Throw the right exception
        else:
            self.__XImages()

    def __SetupPage(self):
        """Inits the bs4 property"""
        page = bs4(self.__FetchPage(self.url),HTML_PARSER) 
        # put iframes into the page object, some blog themes require this
        for frame in page.find_all('iframe'):
            try:
                frame_content = bs4(self.__FetchPage(frame['src']),HTML_PARSER)
                frame.replace_with(frame_content.body)
            except KeyError:
                pass
        self.page = page
        

    def __FetchPage(self,url):
        """fetches the content of a page
        returns the content as a string, or none on error
        """
        r = requests.get(url,headers=HEADERS)
        if r.status_code == 200:
            return r.text
        else:
            self.err = r.status_code
            return None

    def __XImages(self):
        """Extract image URLs from page"""
        for x in self.page.find_all('img'):
            if self.__NoskipURL(x['src']):
                self.d("%s"%x['src'])
                self.image_urls.append(x['src'])        

    def Rip(self):
        """Downloads the images of a specific blog page"""
        self.pl()
        for img in self.image_urls:
            img = str(img)
            self.FetchImage(img)
            self.pl()

    def Fetch(self, url):
        """returns the (binary) content of some url,
        or None, on error (i.e. 404, 403, …)
        """
        r = requests.get(url, headers=HEADERS)
        self.p("fetching: %s" % colored(url,'yellow'),'green')
        if r.status_code == 200:
            return r.content
        else:
            self.p("Failed: %s" % r.status_code,'red')
            return None

    def __FetchImage(self,u):
        """do the actual fetching and saving of an image
        True: if image could be fetched or the local file exists
        False: if image could not be fetched and no local file exits
        """
        fn = safe_filename(u.split('/')[-1]) # <-- only the filename
        if fn is None:
            raise ValueError('Filename could not be <None>')
        fqfn = os.path.join(self.path,fn) # <-- "Full Qualified Filename"
        if not OVERWRITE and os.path.exists(fqfn):
            self.p("%s exists, skipping"%fqfn,'green')
            return True
        img = self.Fetch(u)
        if img is not None:
            f = open(fqfn,'wb')
            f.write(img)
            f.close()
            self.p("%s saved."%fqfn,'green')
            return True
        return False


    def FetchImage(self,image_url):
        """Fetch a specific image from url"""
        url = image_url
        ext = '.' + url.split('.')[-1]
        url = url.rstrip(ext)    
        size = url.split('_')[-1]
        url = url.rstrip(size)
        
        try:
            size = int(size)
        except:
            self.p("Image URL has no size part (%s)"%image_url,'red')
            self.__FetchImage(image_url)
            return
        
        for s in SIZES:
            if self.__FetchImage(url + str(s) + ext):            
                break
            


    def IsValid(self):
        "returns False if image list is empty"
        if len(self.image_urls) == 0:
            return False
        else:
            return True

    def __NoskipURL(self,url):
        """
        False: if image url points to an unwanted image
        True: if image url semms good
        """
        #FIXME: following code is unmaintainable
        try:
            url.index('media.tumblr.com/')
        except ValueError:
            self.d("Skipping %s" % url)
            return False
        try: 
            url.index('media.tumblr.com/avatar')
            self.d("Skipping %s"%url)
            return False
        except ValueError:
            pass
        return True



    def d(self,text):
        """prints debug message"""
        if self.debug:
            print(text)

    def p(self, text, color = ''):
        """prints verbose message"""
        if self.verbose:
            print(colored(text,color))


    def pl(self,char = '-', color='blue'):
        """prints a silly line on screen"""
        if self.verbose:
            print(colored(80*char,color))


def FetchPages(path, blog, pages):
    """params:
        path: Path where the images are saved
        blog: blog url e.g. foo.tumblr.com
        pages: array of pages
    """
    #if not present, put 'http://' at the beginning…
    if blog[:7] != 'http://':
        blog = 'http://'+blog
    for p in pages:
        url = '/'.join([blog,'page',str(p)])
        Page = Scrapelr(url,path,verbose=VERBOSE,debug=DEBUG)
        Page.Rip()

def FetchAllPages(path, blog):
    """params:
        path: Path where the images are saved
        blog: blog url e.g. foo.tumblr.com
    """
    #if not present, put 'http://' at the beginning…
    if blog[:7] != 'http://':
        blog = 'http://'+blog
    i = 1
    t = 0
    while True:
        url = '/'.join([blog,'page',str(i)])
        Page = Scrapelr(url,path,verbose=VERBOSE,debug=DEBUG)
        if Page.IsValid():
            t = 0
            Page.Rip()
        else:
            t += 1
            cprint("Page has no valid images, try next page (%d of %d tries)" % (t,BRUTEFORCELIMIT),'red')
            if t > BRUTEFORCELIMIT:
                break
        i = i + 1
