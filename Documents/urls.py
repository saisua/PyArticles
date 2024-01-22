"""
URL configuration for Documents project.

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

import os
import importlib.util

from Documents.index.index import view as index_view

urlpatterns = [
	path("admin/", admin.site.urls),
	path("", index_view),
]

folder: str
for folder in os.listdir('Documents/generated'):
	generated_folder = os.path.join('Documents/generated', folder)
	if os.path.isdir(generated_folder):
		generated_document = os.path.join(generated_folder, 'document.py')
		spec = importlib.util.spec_from_file_location(folder, generated_document)

		# Create the module
		module = importlib.util.module_from_spec(spec)

		# Load the module
		spec.loader.exec_module(module)

		# Import the function
		view = getattr(module, 'document')
				
		urlpatterns.append(
			path(f'{folder}/', view)
		)

		urlpatterns.extend(static(
			f'{folder}/static/', 
			document_root=os.path.join(generated_folder, 'static')
		))
