import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from .models import User
from .client import generate_questions, parse_message, process_diagnosis
from .inference import consult
from utils.io import read_file
import time

@require_http_methods(["GET"])
def details(request):
    try:
        data = json.loads(request.body)
        client_id = data.get('client_id')
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    if not all([client_id]):
        return HttpResponseBadRequest("Missing required fields")

    try:
        user = User.objects.filter(client_id=client_id).get()
    except:
        user = User(client_id=client_id)
        user.save()

    details_ = {
        "gender": user.gender,
        "age": user.age,
        "symptoms": user.symptoms,
    }

    response_data = {
        'details': details_,
        'complete': bool(all(details_.values())),
        'status': 'success'
    }
    return JsonResponse(response_data)

@require_http_methods(["POST"])
def update(request):
    try:
        data = json.loads(request.body)
        details_ = data.get('details')
        client_id = data.get('client_id')
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    if not all([details_, client_id]):
        return HttpResponseBadRequest("Missing required fields")

    try:
        user = User.objects.filter(client_id=client_id).get()
    except:
        user = User(client_id=client_id)
        user.save()

    current = {
        "gender": user.gender,
        "age": user.age,
        "symptoms": user.symptoms,
        "preferred_language": user.preferred_language
    }

    try:
        for key in current:
            if details_.get(key):
                current[key] = details_[key]
    except Exception as e:
        print(f"Unable to match keys from user data: {e}")
        return JsonResponse({
            'details': {
                "gender": str(user.gender),
                "age": str(user.age),
            "symptoms": user.symptoms,
            },
            'complete': False,
            'status': 'failure'
        })

    user.gender = current["gender"]
    user.age = current["age"]
    user.symptoms = current["symptoms"]
    user.preferred_language = current["preferred_language"]

    try:
        user.save()
    except Exception as e:
        print(f"Unable to save user details: {e}")
        return JsonResponse({
            'details': {
                "gender": str(user.gender),
                "age": str(user.age),
                "symptoms": str(user.symptoms),
            },
            'complete': False,
            'status': 'failure'
        })

    details_ = {
        "gender": user.gender,
        "age": user.age,
        "symptoms": user.symptoms,
        "preferred_language": user.preferred_language
    }

    response_data = {
        'details': details_,
        'complete': bool(all(details_.values())),
        'status': 'success'
    }
    return JsonResponse(response_data)

@require_http_methods(["POST"])
def process(request):
    try:
        data = json.loads(request.body)
        message = data.get('message')
        client_id = data.get('client_id')
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    if not all([message, client_id]):
        return HttpResponseBadRequest("Missing required fields")

    try:
        user = User.objects.filter(client_id=client_id).get()
    except:
        user = User(client_id=client_id)
        user.save()

    current = {
        "gender": user.gender,
        "age": user.age,
        "symptoms": user.symptoms,
    }

    try:
        update = parse_message(message, user.preferred_language)
    except Exception as e:
        print(f"Unable to parse message: {e}")
        return JsonResponse({
            'details': {
                "gender": str(user.gender),
                "age": str(user.age),
                "symptoms": user.symptoms,
            },
            'complete': False,
            'status': 'failure'
        })

    try:
        for key in current.keys():
            if key in update.keys():
                current[key] = update[key]
    except Exception as e:
        print(f"Unable to match keys from LLM response: {e}")
        return JsonResponse({
            'details': {
                "gender": str(user.gender),
                "age": str(user.age),
                "symptoms": user.symptoms,
            },
            'complete': False,
            'status': 'failure'
        })

    user.gender = current["gender"]
    user.age = current["age"]
    user.symptoms = current["symptoms"]

    try:
        user.save()
    except Exception as e:
        print(f"Unable to save user details: {e}")
        return JsonResponse({
            'details': {
                "gender": str(user.gender),
                "age": str(user.age),
                "symptoms": user.symptoms,
            },
            'complete': False,
            'status': 'failure'
        })

    details_ = {
        "gender": str(user.gender),
        "age": str(user.age),
        "symptoms": user.symptoms,
    }
    response_data = {
        'details': details_,
        'complete': bool(all(details_.values())),
        'status': 'success'
    }
    return JsonResponse(response_data)

@require_http_methods(["GET"])
def converse(request):
    try:
        data = json.loads(request.body)
        client_id = data.get('client_id')
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    if not all([client_id]):
        return HttpResponseBadRequest("Missing required fields")

    try:
        user = User.objects.filter(client_id=client_id).get()
    except:
        user = User(client_id=client_id)
        user.save()

    details_ = {
        "gender": user.gender,
        "age": user.age,
        "symptoms": user.symptoms
    }

    if all(details_.values()) and user.diagnosis is not None:
        reply = read_file("static/chat/complete.txt").replace('#####', "\n".join([
            "Gender: " + str(user.gender),
            "Age: " + str(user.age),
            "Symptoms: " + str(user.symptoms),
            "Diagnosis: " + str(user.diagnosis),
        ]))
    elif all(details_.values()):
        diagnosis = consult(f"I am a {user.gender} of age {user.age}. {user.symptoms}")
        reply = process_diagnosis(diagnosis) + read_file("static/chat/complete.txt").replace('#####', "\n".join([
            "Gender: " + str(user.gender),
            "Age: " + str(user.age),
            "Symptoms: " + str(user.symptoms),
            "Diagnosis: " + str(user.diagnosis),
        ]))
    else:
        missing_field = None
        for field in details_: 
            if not details_[field]:
                missing_field = field
                break
        try:
            questions = generate_questions({missing_field: None},user_language=user.preferred_language)
        except Exception as e:
            print(f"Unable to generate question: {e}")
            return JsonResponse({
                'reply': read_file("static/chat/error.txt"),
                'status': 'failure'
            })
        reply = '\n'.join(list(questions.values()))

    response_data = {
        'reply': reply,
        'status': 'success'
    }
    return JsonResponse(response_data)
