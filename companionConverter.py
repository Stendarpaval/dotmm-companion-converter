import codecs
import json
from bs4 import BeautifulSoup

remove_attributes = ['name','lang','language','onmouseover','script','style',
					'font','dir','face','size','color','style','class',
					'width','height','hspace','border','valign','background',
					'bgcolor','text','link','vlink','alink','cellpadding',
					'cellspacing', 'data-content-chunk-id','alt','src',
					'data-tooltip-href','href','id','title','data-href',
					'data-layout','data-next-link','data-prev-link',
					'data-next-title','content']

# htmlName = 'Companion_Wyllowwood.html'
# htmlName = 'Companion_MuiralsGauntlet.html'
# htmlName = 'Companion_TroglodyteWarrens.html'
# htmlName = 'Companion_MazeLevel.html'
# htmlName = 'Companion_TrobriandsGraveyard.html'
# htmlName = 'Companion_Arcturiadoom.html'
# htmlName = 'Companion_ObstacleCourse.html'
# htmlName = 'Companion_CrystalLabyrinth.html'
# htmlName = 'Companion_Seadeeps.html'
# htmlName = 'Companion_Vanrakdoom.html'
# htmlName = 'Companion_CavernsOfOoze.html'
# htmlName = 'Companion_RunestoneCaverns.html'
# htmlName = 'Companion_TerminusLevel.html'
# htmlName = 'Companion_ShadowduskHold.html'
# htmlName = 'Companion_MadWizardsLair.html'
htmlName = 'Companion_ArcaneChambers.html'
# htmlName = 'Companion_LostLevel.html'
# htmlName = 'Companion_MaddgothsCastle.html'
# htmlName = 'Companion_Slitherswamp.html'
# htmlName = 'Companion_Dweomercore.html'
# htmlName = 'Companion_TwistedCaverns.html'
htmlFile = codecs.open(htmlName,'r')
htmlData = htmlFile.read()
htmlStr = str(htmlData)


soup = BeautifulSoup(htmlStr, features="html.parser")


def RepresentsInt(string):
    """Checks if string is an integer."""
    try:
        int(string)
        return True
    except ValueError:
        return False


for tag in soup.find_all(['span','header','article']):
	tag.unwrap()

for blockquote in soup.find_all('blockquote'):
	blockquote.wrap(soup.new_tag('ul'))
	for tag in blockquote.find_all('p'):
		tag.wrap(soup.new_tag('li'))
		tag.unwrap()
	blockquote.unwrap()

for attribute in remove_attributes:
	for tag in soup.find_all(attrs={attribute: True}):
		del tag[attribute]

for script in soup(["script", "style", "select","img","head","a","br"]):
	script.extract()

for div in soup.find_all(['div']):
	if "Page" in "".join(div.contents):
		div.extract()
	if RepresentsInt("".join(div.contents)):
		div.extract()
	if str(div.string).isspace() or "".join(div.contents) == "" or str(div.string) == None:
		div.extract()


i = 0
n = 0
for div in soup.find_all(['div']):
	if "\n" in div:
		
		newContent = [0] * len(div.contents)
		for ii in range(len(div.contents)):
			if len(div.contents[ii]) > 2 and ('\n' in div.contents[ii]):
				newContent[ii] = div.contents[ii].replace('\n','')
			else:
				newContent[ii] = div.contents[ii]

		newContent = "".join(newContent)
		div.smooth()

		titles = []
		div.string.replace_with(newContent)
		# print(div.prettify())
		for line in div.string.splitlines():
			if line.isupper():
				titles.append(line)
			
		newDivTag = soup.new_tag("div")
		newDivTag.string = ""
		newDivTag.string.replace_with(newContent)

		updatedContent = [0] * len(titles)
		for titleNum in range(len(titles)):
			titlePos = newContent.find(titles[titleNum])
			firstNewline = newContent[titlePos:].find("\n") + titlePos
			potentialTitle = newContent[titlePos:firstNewline]
			
			if potentialTitle.isupper():
				if titleNum > 0:
					if potentialTitle in "".join(updatedContent[titleNum - 1].contents[1]):
						duplicateStartIndex = updatedContent[titleNum - 1].contents[1].find(potentialTitle)
						fixedText = [updatedContent[titleNum - 1].contents[0],updatedContent[titleNum - 1].contents[1][:duplicateStartIndex]]
						updatedContent[titleNum - 1] = fixedText				

				titleTag = soup.new_tag("h3")
				titleTag.string = potentialTitle
				

				newDivTag.string = newContent[(titlePos + len(potentialTitle)):]
				newDivTag.string.insert_before(titleTag)				
				updatedContent[titleNum] = newDivTag

		tails = []
		if len(titles) > 0:
			div.clear()
			newContentStart = newContent.find(titles[0])
			tailOfPreviousDiv = newContent[:newContentStart]
			tails.append(tailOfPreviousDiv)
			div.insert(0,tailOfPreviousDiv)

		for titleNum in range(len(titles)):
			titlePos = newContent.find(titles[titleNum])
			firstNewline = newContent[titlePos:].find("\n") + titlePos
			potentialTitle = newContent[titlePos:firstNewline]
			
			if potentialTitle.isupper():				
				if isinstance(updatedContent[titleNum],list):
					contentList = []
					for i in (range(len(updatedContent[titleNum]))):
						div.insert(len(div.contents)+1,updatedContent[titleNum][i])
				else:
					div.insert(len(div.contents),updatedContent[titleNum])
					div.div.unwrap()
				if n == 0:
					actualTitle = potentialTitle
					div.h3.unwrap()
					# print(div)
					div.wrap(soup.new_tag("h2"))
					div.unwrap()
					n += 1
	i += 1


for tag in soup.find_all(['h3','h4']):
	tag.insert_before(soup.new_tag('br'))
	tag.insert_before(soup.new_tag('hr'))
	tag.insert_before(soup.new_tag('br'))

for div in soup.find_all(['div']):
	div.wrap(soup.new_tag('p'))
	div.unwrap()	

output = str(soup.html).replace("•","<li>").replace("—"," - ").replace("…","...").replace("’","'").replace("–"," - ").replace("“",'"').replace("”",'"')
soup = BeautifulSoup(output, features="html.parser")
output = str(soup.html)
splitOutput = output.splitlines()
titleIndices = []
i = 0
for line in splitOutput:
	if "<h3>" in line:
		titleIndices.append(i)
	i += 1

linesDone = []
for i in range(len(titleIndices)):
	if i != len(titleIndices) - 1:
		for j in range(titleIndices[i],titleIndices[i+1]):
			if "<li>" in splitOutput[j]:
				if j in linesDone:
					break
				listStartIndex = splitOutput[j].find("<li>")
				
				splitOutput[j] = splitOutput[j][:listStartIndex] + "<ul>" + splitOutput[j][listStartIndex:]
				linesDone.append(j)
				for k in reversed(range(j,titleIndices[i+1]+1)):
					if "<br/><hr/><br/>" in splitOutput[k]:
						listEndIndex = splitOutput[k].rfind("<br/><hr/><br/>")
						splitOutput[k] = splitOutput[k][:(listEndIndex)] + "</ul>" + splitOutput[k][(listEndIndex):]
						break
				break

for i in reversed(range(len(splitOutput))):
	if i > 0:
		if "</p><p><li>" in splitOutput[i]:
			lineBreakIndex = splitOutput[i].find("</p><p>")
			splitOutput[i] = splitOutput[i][:(lineBreakIndex)] + splitOutput[i][(lineBreakIndex + 7):]
		if "</li></p><p>" in splitOutput[i]:
			lineBreakIndex = splitOutput[i].find("</li></p><p>")
			splitOutput[i] = splitOutput[i][:(lineBreakIndex)] + splitOutput[i][(lineBreakIndex + 12):]
		if "<h3>" not in splitOutput[i] and "<h3>" not in splitOutput[i-1] and splitOutput[i][0:1] not in [" ",""]:
			if "<li>" in splitOutput[i-1] and "</li></p><p>" in splitOutput[i]:
				lineBreakIndex = splitOutput[i].find("</li></p><p>")
				splitOutput[i] = splitOutput[i][:(lineBreakIndex)] + splitOutput[i][(lineBreakIndex + 12):]
			
			if not splitOutput[i-1].rstrip().endswith((".","!",'"',":")):
				if "<p>" in splitOutput[i-1] and "</p><p>" in splitOutput[i]:
					lineBreakIndex = splitOutput[i].find("</p><p>")
					if lineBreakIndex != -1:
						splitOutput[i] = splitOutput[i][:(lineBreakIndex)] + splitOutput[i][(lineBreakIndex + 7):]
			if splitOutput[i][0:1].islower():
				splitOutput[i-1] = splitOutput[i-1] + splitOutput[i]
				splitOutput.pop(i)
			elif not splitOutput[i-1].rstrip().endswith((".","!",'"',":")):
				splitOutput[i-1] = splitOutput[i-1] + splitOutput[i]
				splitOutput.pop(i)

testOutput = " ".join(splitOutput)

output = testOutput

# if not actualTitle:
if htmlName[0:1] != "C":
	actualTitle = htmlName[:-5]
print("json title:",actualTitle)

jsonFormat = {	"name": actualTitle,
				"sort": 260000, 
				"flags": {
					"exportSource": {
						"world": "companion-dotmm", 
						"system": "dnd5e", 
						"coreVersion": 
						"0.7.9", 
						"systemVersion": "1.2.0"
						}
					}, 
				"content": output,
				"_id": "JKs46PwKkpTZamrS"
			}
with open(actualTitle.replace(':','') + '.json','w') as jsonFile:
	json.dump(jsonFormat, jsonFile)

text_file = open("output.txt","w")
text_file.write(output)
text_file.close()

html_file = open("output.html","w")
html_file.write(output)
html_file.close()
