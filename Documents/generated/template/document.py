from django.shortcuts import render
import os
import sys
from multiprocessing import Process
import importlib

generated_path, fname, _ = __file__.rsplit(os.sep, 2)
folder_path = os.path.join(generated_path, fname)

sys.path.append(folder_path)

generate = importlib.import_module(f"Documents.generated.{fname}.generate").generate
#from print import _print

printing_process: Process = False

html_fname = f"{fname}.html"
pdf_name = f"{fname}.pdf"
async def document(request):
    global printing_process

    doc = await generate(folder_path, html_fname)

    # if(printing_process is None or not printing_process.is_alive()):
    #     printing_process = Process(target=_print, args=(doc, folder_path, html_fname, pdf_name))
    #     printing_process.start()

    return render(request, html_fname)
