"""Dump all shape names per slide using PowerPoint COM with retry.
用於診斷：當模板更換後 shape 名稱變了，跑此腳本抓取 COM 實際名稱。
"""
import win32com.client, time, sys

TEMPLATE = sys.argv[1] if len(sys.argv) > 1 else r"G:\示例项目\模板\月報模板.pptx"

ppt = win32com.client.Dispatch("PowerPoint.Application")
try:
    ppt.Visible = True
except:
    pass

prs = ppt.Presentations.Open(TEMPLATE)
time.sleep(4)

def get_slide_count(prs, retries=10):
    for attempt in range(retries):
        try:
            return prs.Slides.Count
        except Exception:
            if attempt < retries - 1:
                time.sleep(2.0)
            else:
                raise

def get_slide_shapes(slide, retries=10):
    for attempt in range(retries):
        try:
            count = slide.Shapes.Count
            shapes = []
            for j in range(1, count + 1):
                sh = slide.Shapes(j)
                name = sh.Name
                ttype = sh.Type
                text = ""
                if sh.HasTextFrame:
                    try:
                        text = sh.TextFrame.TextRange.Text.replace('\r', ' ').replace('\n', ' ')[:80]
                    except:
                        text = "(text error)"
                elif sh.HasTable:
                    text = f"[TABLE {sh.Table.Rows.Count}r x {sh.Table.Columns.Count}c]"
                else:
                    text = "(no text)"
                type_map = {1:"AutoShape", 14:"Picture", 17:"TextBox", 19:"Table", 13:"Group"}
                tname = type_map.get(ttype, f"T{ttype}")
                shapes.append((tname, name, text))
            return shapes
        except Exception:
            if attempt < retries - 1:
                time.sleep(1.5)
            else:
                raise

total = get_slide_count(prs)
for i in range(1, total + 1):
    slide = prs.Slides(i)
    time.sleep(0.5)
    shapes = get_slide_shapes(slide)
    print(f"=== Slide {i} ===")
    for tname, name, text in shapes:
        print(f"  [{tname}] name='{name}' | text='{text}'")

prs.Close()
ppt.Quit()
print("\nDONE")
