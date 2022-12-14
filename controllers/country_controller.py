from flask import Flask, render_template, request, redirect
from models.country import Country 
from repositories import country_repository, memory_repository, user_repository

from app import app

@app.route('/countries')
def countries():
    countries = country_repository.select_all()
    return render_template('countries/index.html', countries=countries)


@app.route('/countries/new')
def new_country():
    return render_template('countries/new_country.html')


@app.route('/countries', methods=['POST'])
def save_country():
    visited = False
    form_data = request.form
    country_name = form_data['country_name']
    cities = form_data['cities']
    
 
    visited = 'visited' in form_data

    new_country = Country(country_name, cities, visited)
    country_repository.save(new_country)

    return redirect('/countries')


@app.route('/countries/delete/<id>', methods=['POST'])
def delete_country(id):
    country_repository.delete(id)

    return redirect('/countries')


@app.route('/countries/<id>')
def show(id):
    memories = memory_repository.select_country_id(id)
    country = country_repository.select_country_by_id(id)
    # users = user_repository.select_user_by_id(id)
    return render_template('countries/country.html', country=country, memories=memories) #users=users


@app.route('/countries/edit/<id>', methods=['GET'])
def edit_country(id):
    country = country_repository.select_country_by_id(id)
    return render_template('countries/edit.html', country=country)


@app.route('/countries/<id>', methods=['POST'])
def update_country(id):
    form_data = request.form
    country_name = form_data['country_name']
    cities = form_data['cities']
    visited = 'visited' in form_data

    country = Country(country_name, cities, visited, id)
    country_repository.update_country(country)
    return redirect('/countries')