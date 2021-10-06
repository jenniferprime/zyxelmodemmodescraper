import asyncio
from pyppeteer import element_handle, launch

async def main():
    browser = await launch(options={'args': ['--no-sandbox']})
    page = await browser.newPage()
    await page.setViewport({ 'width': 1920, 'height': 1080 })

    #navigate digitbox
    await page.goto('http://192.168.2.1', {'waitUntil' : 'domcontentloaded'})
    print("navigated")
    
    #debug screenshot
    #await page.screenshot({'path':"fpbeforelogin.png", 'fullPage': 'true'})
    
    #wait for load
    element = await page.querySelector('#device_name')
    print(await page.evaluate('(element) => element.textContent', element))

    element = await page.querySelector('#idButtonSave')
    elementin = await page.evaluate('(element) => element.value', element)

    #check if loggedin, then login/eval   
    if elementin == "Login":
        print("login")
        #fill in details
        await page.evaluate('''() => [ document.getElementById('LoginName').value = "zyxel" ]''')
        await page.evaluate('''() => [ document.getElementById('LoginPass').value = "passpass" ]''')
        #press login button
        await page.evaluate('(element) => element.click()', element)
        await page.waitForSelector('#device_name')
    else:
        print("eval")

    
    print(page.url)

    #debug screenshot
    #await page.screenshot({'path':"fpafterlogin.png", 'fullPage': 'true'})

    await page.waitForSelector('#title1')
    element = await page.querySelector('#OverviewContent')

    #write Overviewpage to disk
    ov = open("zyxel_ov.html", "w")
    ov.write(await page.evaluate('(element) => element.innerHTML', element))
    ov.close()
    print("saved overview")

    #nav to DSL Status
    element = await page.querySelector('#DSL')
    await page.evaluate('(element) => element.childNodes[0].click()', element)
    await page.waitForSelector('#title1')
    #debug screenschot
    #await page.screenshot({'path':"dsl.png", 'fullPage': 'true'})

    #write DSL page to disk
    element = await page.querySelector('#main_container')
    dsl = open("zyxel_dsl.html", "w")
    dsl.write(await page.evaluate('(element) => element.innerHTML', element))
    dsl.close()
    print("saved DSL")

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
