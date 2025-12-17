from playwright.sync_api import sync_playwright, TimeoutError
def run_test():
    out = {"steps": []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("login page")




        page.fill("#username", "admin")
        out["steps"].append({"action":"fill","target":"#username","value":"admin"})



        page.fill("#password", "pass")
        out["steps"].append({"action":"fill","target":"#password","value":"pass"})



        page.click("#loginBtn")
        out["steps"].append({"action":"click","target":"#loginBtn"})


        browser.close()
    return out

if __name__ == '__main__':
    print(run_test())