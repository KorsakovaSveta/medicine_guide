from django.shortcuts import render, redirect, get_object_or_404
from website.models import *
from neomodel import db
from neo4j import GraphDatabase
from django.db.models import Q
from .forms import *
from math import sqrt, erf, log
from uuid import UUID
# Create your views here.
def diseasesClasses(request):
    # all_nodes = []
    # diseases_classes = DiseasesClass.nodes.all()
    # diseases = Disease.nodes.all()
    # symptoms = Symptom.nodes.all()  
    # models = [diseases_classes, diseases,symptoms]
    # all_nodes = set(item.name for items in models for item in items)
    # all_nodes = sorted(all_nodes)
    
    # # unique_nodes = {}
    # # for node in all_nodes:
    # #     node_attributes = [node.description, node.text]
    # #     unique_nodes[node.name] = node_attributes
    # all_nodes = grouped_terms(all_nodes)
   

    return render(request, 'index.html', {'all_nodes': allNodes()})

def allNodes():
    all_nodes = []
    diseases_classes = DiseasesClass.nodes.all()
    diseases = Disease.nodes.all()
    symptoms = Symptom.nodes.all()  
    models = [diseases_classes, diseases,symptoms]
    all_nodes = set(item.name for items in models for item in items)
    all_nodes = sorted(all_nodes)
    
    # unique_nodes = {}
    # for node in all_nodes:
    #     node_attributes = [node.description, node.text]
    #     unique_nodes[node.name] = node_attributes
    all_nodes = grouped_terms(all_nodes)
    return all_nodes

def grouped_terms(all_nodes):
    grouped_terms = {}
    for node in all_nodes:
        first_letter = node[0].upper()
        if first_letter not in grouped_terms:
            grouped_terms[first_letter] = []
        grouped_terms[first_letter].append(node)
    return grouped_terms

def term_detail_view(request, term_name):
    try:
        term = DiseasesClass.nodes.filter(name=term_name).first()
        term.name = term.name.capitalize()
        if term.description == None and term.text == None:
                term.description = 'Term not found'
                term.text = None
    except DiseasesClass.DoesNotExist:
        try:
            term = Disease.nodes.filter(name=term_name).first()
            term.name = term.name.capitalize()
            if term.description == None and term.text == None:
                term.description = 'Term not found'
                term.text = None
        except Disease.DoesNotExist:
            try:
                term = Symptom.nodes.filter(name=term_name).first()
                term.name = term.name.capitalize()
                if term.description == None:
                    
                    term.description = 'Term not found'
            except Symptom.DoesNotExist:
                return render(request, 'terms.html', {'term': 'Term not found'})

    return render(request, 'terms.html', {'term': term, 'all_nodes': allNodes()})

def search(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = 'Term not found'
        text = None
        try:
            medical_term = DiseasesClass.nodes.filter(name=name.capitalize()).first() 
            medical_term_name = medical_term.name
            description = medical_term.description
            text = medical_term.text
            if description == None and text == None:
                medical_term = name
                description = 'Term not found'
                text = None
        except DiseasesClass.DoesNotExist:
            try:
                medical_term = Disease.nodes.filter(name=name.capitalize()).first() 
                medical_term_name = medical_term.name
                description = medical_term.description
                text = medical_term.text
                if description == None and text == None:
                    medical_term_name = name
                    description = 'Term not found'
                    text = None
            except Disease.DoesNotExist:
                try:
                    medical_term = Symptom.nodes.filter(name=name.lower()).first()
                    medical_term_name = medical_term.name.capitalize()
                    description = medical_term.description
                    if description == None:
                        medical_term_name = name
                        description = 'Term not found'
                       
                except Symptom.DoesNotExist:
                    medical_term_name = name
                    description = 'Term not found'
                    
        return render(request, 'search.html', {'name': medical_term_name,'description': description, "text": text, 'all_nodes': allNodes()})
    else:
        return render(request, 'search.html')
    

def search_disease_by_symptoms(request):

    all_symptoms = Symptom.nodes.all()
    all_symptoms = sorted(list(set(symptom.name for symptom in all_symptoms)))
    all_symptoms = grouped_terms(all_symptoms)
    selected_symptoms, diseases, other_symptoms, probable_diseases = [], [], [], []
    
    if request.method == 'POST':
        selected_symptoms = request.POST.getlist('symptoms')
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "keW3z48dcPHG8Au"))
        with driver.session() as session:
            if selected_symptoms:
               
                cypher_query = """
                MATCH (d:Disease)-[:симптом]->(s:Symptom)
                    WHERE s.name IN $selected_symptoms
                    WITH d, COLLECT(s.name) AS allSymptoms, COUNT(DISTINCT s) AS numSymptoms
                    WHERE numSymptoms = SIZE($selected_symptoms)
                    RETURN DISTINCT d.name AS disease
                """

                result = session.run(cypher_query, {"selected_symptoms": selected_symptoms})
                

                diseases = [record['disease'] for record in result]

                cypher_query = """
                    MATCH (d:Disease)-[:симптом]->(s:Symptom)
                    WHERE d.name = $disease
                    RETURN DISTINCT s.name AS symptoms
                    """

                for disease in diseases:
                    
                    result = session.run(cypher_query, {"disease": disease})
                    symptoms = [record["symptoms"] for record in result if record["symptoms"] not in selected_symptoms]
                    other_symptoms.append(symptoms)
                    symptoms = []

                other_symptoms = list(set([item for sublist in other_symptoms for item in sublist]))
                #probable_diseases = additional_search(request, other_symptoms, selected_symptoms, diseases)
     
    return render(request, 'search_by_symptoms.html', {
        'all_symptoms': all_symptoms,
        'selected_symptoms': selected_symptoms,
        'diseases': diseases,
        "other_symptoms": other_symptoms,
        
    })


def calculate_bmi(request):
    if request.method == 'POST':
        form = BMIForm(request.POST)
        if form.is_valid():
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            
            # Вычисление индекса массы тела
          
            bmi = weight / (height**2) * 10000
            bmi = round(bmi, 2)
            # Возвращение результата
            return render(request, 'bmi.html', {'form': form, 'bmi': bmi})
    else:
        form = BMIForm()
    
    return render(request, 'bmi.html', {'form': form})


def calculator_child_height(request):
    def z_to_percentile(z_score):
        return round((1 + erf(z_score / sqrt(2))) * 50, 2)
    if request.method == 'POST':
        form=ChildHeightForm(request.POST)
        if form.is_valid():
            sex = form.cleaned_data['sex']
            mothers_height = form.cleaned_data['mothers_height']
            fathers_height = form.cleaned_data['fathers_height']
            if sex == "ж":
                target_height = ((fathers_height - 13) + mothers_height) / 2
            elif sex == "м":
                target_height = ((mothers_height + 13) + fathers_height) / 2
            else:
                return "Invalid sex"

            if sex == "ж":
                L = 1.108046193
                M = 163.338251
                S = 0.039636316
            elif sex == "м":
                L = 1.167279219
                M = 176.8492322
                S = 0.040369574
            else:
                return "Invalid sex"

            z_score = ((target_height / M) ** L - 1) / (L * S)
            z_score = round(z_score, 2)
            height_percentile = z_to_percentile(z_score)


            target_height = round(target_height, 2)
            return render(request, 'child_height.html', {'form': form, 'target_height': target_height, "z_score": z_score, "height_percentile": height_percentile})
    else:
        form = ChildHeightForm()
    
    return render(request, 'child_height.html', {'form': form})


def calculate_meldna(request):
    if request.method == 'POST':
        form = ParamsForMeldnaForm(request.POST)
        if form.is_valid():
            creatinine = form.cleaned_data['creatinine']
            bilirubin = form.cleaned_data['bilirubin']
            serum_na = form.cleaned_data['serum_na']
            inr = form.cleaned_data['inr']
            hemodialysis_twice_in_week_prior = form.cleaned_data['hemodialysis_twice_in_week_prior']
            
            creatinine = creatinine *0.0113
            bilirubin = bilirubin * 0.05848


            creatinine = max(1.0, min(creatinine, 4.0))
            bilirubin = max(1.0, bilirubin)
            inr = max(1.0, inr)
            serum_na = max(125, min(serum_na, 137))

            if hemodialysis_twice_in_week_prior == "да":
                creatinine = 4.0

            meld_na_i = (
                0.957 * log(creatinine) + 0.378 * log(bilirubin) + 1.120 * log(inr) + 0.643
            )
            meld_na_i = round(meld_na_i * 10, 1)
            meld = meld_na_i

            if meld_na_i > 11:
                meld_na = (
                    meld_na_i + 1.32 * (137 - serum_na) - (0.033 * meld_na_i * (137 - serum_na))
                )
                meld_na = min(40, meld_na)
            else:
                meld_na = meld_na_i

            return render(request, 'meldna.html', {'form': form, "MELD": round(meld)})
    else:
        form = ParamsForMeldnaForm()
    
    return render(request, 'meldna.html', {'form': form})


