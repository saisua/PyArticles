from django.shortcuts import render
import os
import sys

generated_path, fname, _ = __file__.rsplit(os.sep, 2)
folder_path = os.path.join(generated_path, fname)

sys.path.append(folder_path)

from generate import generate

html_fname = f"{fname}.html"
async def document(request):
    await generate(folder_path, html_fname)
    return render(request, html_fname)