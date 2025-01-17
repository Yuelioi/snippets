
from PIL import Image
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import os
from pathlib import Path
from shutil import rmtree


from Snippets.sub_progress.translator import *

from selenium.webdriver.chrome.service import Service


def getGraph(path, imgPath):
    driver = webdriver.Chrome(
        executable_path=r"H:\Snippets\Program-Learning\Python\chromedriver.exe")
    driver.get(path)
    try:
        element = driver.find_element(by=By.CLASS_NAME, value="graph")
    except:
        return 0

    location = element.location
    size = element.size

    driver.save_screenshot(imgPath)

    x = location['x']
    y = location['y']
    width = location['x']+size['width']
    height = location['y']+size['height']

    im = Image.open(imgPath, mode='r')
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save(imgPath)
    return 1


def content_progress(i, current_line, no_tran, to_tran):

    if current_line.startswith("#"):
        no_tran.append([i, current_line])
    elif len(current_line) < 3:
        no_tran.append([i, current_line])
    elif current_line.startswith("!"):
        no_tran.append([i, current_line])
    else:
        to_tran.append([i, current_line])


def tran_file(path, loop, driver):

    no_tran = []
    to_tran = []
    traned = []
    final_list = []

    with open(path, "r+", encoding='utf-8') as f:
        print("正在翻译:" + str(loop) + path)
        content = f.readlines()
        for i in range(len(content)):
            current_line = content[i].replace("\n", "")
            content_progress(i, current_line, no_tran, to_tran)

        to_tran_src = [ele[1] for ele in to_tran]

        print("共计:" + str(len(to_tran_src)) + "行")
        # to_tran_trg = tran_deepl_pro_auto(to_tran_src)
        try:
            to_tran_trg = tran_deepl_pro_auto(to_tran_src)
            # to_tran_trg = tran_deepl_auto(to_tran_src, driver)
            if len(to_tran_trg) < 2:
                print("______错误1" + path)
                return

            traned = [[to_tran[i][0], to_tran_trg[i]]
                      for i in range(len(to_tran))]
        except:
            print("______错误2" + path)
            time.sleep(4)
            return

        final_list.extend(traned)
        final_list.extend(no_tran)
        final_list.sort(key=lambda a: a[0])

        final_text = "\n".join([ele[1] for ele in final_list])

        f.seek(0)
        f.truncate()
        f.write(final_text)


def html2md(content):
    import html2text as ht

    text_maker = ht.HTML2Text()
    text_maker.bypass_tables = False
    text_maker.body_width = 0
    text_maker.protect_links = True
    text_maker.single_line_break = 1

    text = text_maker.handle(content)
    return text


def rebuild_ue_blueprint(root_dir):

    for root, dirs, files in os.walk(root_dir):
        # 如果当前目录没有文件夹 则爬虫 并删除当前目录

        if not dirs:
            file_path = Path(root, files[0])
            parent = Path(file_path).parent
            print(file_path)
            if (file_path.suffix == ".html"):
                with open(file_path, "r+", encoding='utf-8') as file:

                    now_time = datetime.datetime.now()
                    imgPath = now_time.strftime(
                        "%Y%m%d-%H%M%S%f")[:-4] + ".png"
                    dataPath = Path(Path.cwd(), "./Python/Snippets/data")

                    hasGraph = getGraph(file_path.as_uri(), Path(
                        dataPath, Path(dataPath, imgPath)))

                    file_content = file.read()
                    soup = BeautifulSoup(file_content, "html.parser")
                    main = soup.select_one("#maincol")

                    # 删除window/linux切换 以及 图标
                    [i.decompose() for i in main.select("#osContainer")]
                    [i.decompose() for i in main.select(".icon-cell")]

                    # 处理段落
                    for p in main.select("p"):
                        p.string = p.get_text(
                            " ", strip=True).replace("\n", ". ")

                    # 处理图表
                    if hasGraph:
                        graph = main.select_one(".graph")
                        g2 = soup.new_tag("h2")
                        g2.string = "图示"
                        graph.insert_before(g2)
                        new_img = soup.new_tag("img")
                        new_img["src"] = "$-" + imgPath
                        graph.replace_with(new_img)

                    # 处理表格
                    for tb in main.select("table"):
                        for tr in tb.select("tr"):
                            res = ""
                            for td in tr.find_all("td"):
                                res += td.get_text(": ", strip=True) + ". "
                                td.decompose()
                            p = soup.new_tag("p")
                            p.string = res.replace(" . ", "").strip()
                            tb.insert_before(p)

                    md = html2md(str(main))
                    md = md.replace("\n", "\n\n")
                    md = md.replace("Inputs", "## Inputs").replace(
                        "Outputs", "## Outputs")

                    with open(str(parent) + ".md", "w+", encoding='utf-8') as file:
                        file.seek(0)
                        file.truncate()
                        file.write("# " + parent.name + "\n\n" + md)

                rmtree(parent)


test_file = r"H:\Scripting\Vue Projects\docs_ue\测试"


def readFolder(root_dir):
    loop = 0
    driver = get_driver()
    # driver =""
    back = False
    for parent, dir_names, file_names in os.walk(root_dir):

        for file in file_names:
            loop += 1

            current = "BreakGeometryScriptCopyMeshToAss-.md"

            if file == current:
                back = True
            if back:
                tran_file(parent + "/" + file, loop, driver)


def get_summary(root_dir):
    for item in os.listdir(root_dir):
        full_path = os.path.join(root_dir, item)
        if os.path.isdir(full_path):
            get_summary(root_dir)
        else:
            print(item)


def ue_combine_en_zh(root_dir):
    for root, dirs, files in os.walk(root_dir + "\\final"):
        for file in files:
            print(file)
            enRoot = root.replace(r"H:\Scripting\Vue Projects\docs_ue\docs\final",
                                  r"H:\Scripting\Vue Projects\docs_ue\docs\en")
            with open(enRoot + "\\" + file, "r+", encoding='utf-8') as f:
                enContent = f.readlines()[1:]

            with open(root + "\\" + file, "r+", encoding='utf-8') as f2:
                file_content = f2.read()
                f2.seek(0)
                f2.truncate()
                f2.write((file_content + "\n<hr>\n" + "".join(enContent)
                          ).replace("$-", "/uploads/projects/ue-bluprint/"))


summary = ""


def print_folder_tree(folder_path, parent="", indent=0):
    # 遍历文件夹中的所有文件和子文件夹
    global summary
    for entry in os.scandir(folder_path):

        if parent == "":
            root = ""
        else:
            root = (parent + "-").lstrip("-")
        tab = "\t" * indent

        # 清除父目录的孤立文件
        if not (parent == "" and entry.is_file()):
            summary += f'{tab}- [{entry.name}](${root}{entry.name})' + "\n"
        if entry.is_dir():
            print_folder_tree(entry.path, parent+"-"+entry.name, indent + 1)


root_dir = r"H:\Scripting\Vue Projects\docs_ue\docs\final"
# root_dir= r"H:\Scripting\Vue Projects\docs_ue\测试"
root_dir = r'H:\Scripting\Vue Projects\docs2_yuelili_com\UE\BlueprintAPI-HTML\en-US\BlueprintAPIHtml'
root_dir = r'H:\Scripting\Vue Projects\docs_ue\docs\final'

print_folder_tree(root_dir)
# with open(root_dir+"\\summary.md", "w+", encoding="utf-8") as f:
#     f.write(summary)
