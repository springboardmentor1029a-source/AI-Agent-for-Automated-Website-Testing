def get_dom_snapshot(page):
    return page.evaluate("""
    () => Array.from(document.querySelectorAll(
      "input, button, textarea, select, a"
    )).map(el => ({
      tag: el.tagName.toLowerCase(),
      type: el.type || "",
      text: el.innerText || "",
      name: el.name || "",
      id: el.id || "",
      placeholder: el.placeholder || "",
      aria: el.getAttribute("aria-label") || ""
    }))
    """)
