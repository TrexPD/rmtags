from re import compile

def removedor_tags_html(html: str):
    print(compile(r"<[^>]*>").sub(" ", html).strip())
     

if __name__ == "__main__":
    html = ""
    
    removedor_tags_html(html=html)
