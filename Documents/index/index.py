from django.shortcuts import render
from Documents.index.generate import generate
import os

generated_path, fname, _ = __file__.rsplit(os.sep, 2)

html_path = os.path.join(generated_path, fname)
html_fname = f"{fname}.html"
async def view(request):
    await generate(html_path, html_fname)
    return render(request, html_fname)