def getPage(url): #Everything comes from this code. Once you entered an url, it will give you an html code for that url that means a string.
  try:
    import urllib.request
    page = urllib.request.urlopen(url).read()
    return page.decode("utf-8")
  except:
    return ""

def linkExtracter(htmlContent):
  firstHref = htmlContent.find('a href')
  firstQuote = htmlContent.find('"',firstHref)+1
  secondQuote = htmlContent.find('"',firstQuote)
  urlLink = htmlContent[firstQuote:secondQuote]
  return urlLink , secondQuote

def allLinkExtracter(url):
  htmlContent = getPage(url)

  urlList = []
  while htmlContent.find('a href') != -1 :
    urlLink , secondQuote = linkExtracter(htmlContent)
    if urlLink.find('http') == -1:
      urlList.append(url + urlLink)
    else:
      urlList.append(urlLink)
    htmlContent = htmlContent[secondQuote:]
  return urlList

def keyWordExtractor(url):
  content = getPage(url).split()
  return content

def fullAutomaticIndexAdder(anyList) :
  anIndex = {}
  for links in anyList:
    keywordList = keyWordExtractor(links)
    for words in keywordList:
      if words not in anIndex:
        anIndex[words] = [links]
      else:
        if links not in anIndex[words]:
          anIndex[words].append(links)
  return anIndex

def graphDesigner(anyList):
  myGraph = {}
  for elements in anyList:
    myGraph[elements] = allLinkExtracter(elements)
  return myGraph

def urlRanker(anyGraph):
  d = 0.8
  N = len(anyGraph)
  repetitionCount = 10
  ranks = {}

  for element in anyGraph:
    ranks[element] = 1/N
  for i in range(repetitionCount):
    newranks = {}
    for element in anyGraph:
      newrank = (1-d)/N
      for node in anyGraph:
        if node in anyGraph[node]:
          newrank = newrank + d*(ranks[node]/(len(anyGraph[element])+1))
      newranks[element] = newrank
    ranks = newranks
  return ranks


def Crawler(url):
  toCrawl = [url]
  crawled = []
  while len(toCrawl) > 0 :
    processingUrl = toCrawl.pop()
    if processingUrl not in crawled:
      for links in allLinkExtracter(processingUrl):
        if links not in toCrawl:
          toCrawl.append(links)
      crawled.append(processingUrl)
      if len(crawled) > 100:
        break

  myIndex = fullAutomaticIndexAdder(crawled)
  myGraph = graphDesigner(crawled)
  myRanksIndex = urlRanker(myGraph)
  return myRanksIndex , myIndex


def lookUp(index , keyword ,rankindex):
  if keyword in index:
    return sorted(index[keyword],key= rankindex.get ,reverse = True)


