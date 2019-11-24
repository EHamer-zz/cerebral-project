from django.shortcuts import render

# Create your views here.
import websockets

import json
from chat.models import Chat


dct_questions = None


def index(request):
    global dct_questions

    if 'dct_questions' not in globals():
        dct_questions = load_default_json()
    else:
        dct_questions = globals()['dct_questions']
        if not dct_questions:
            dct_questions = load_default_json()

    if 'GET' == request.method:
        # assume the page is being loaded for the first time, so delete any previous chat data
        Chat.objects.all().delete()

    if 0 < len(request.POST):
        # data has been posted
        my_chat = Chat()
        i_id = int(request.POST['place'])
        txt_response = request.POST['response']
        i_new_id, txt_error = my_chat.process_response(i_id, txt_response, dct_questions)

        dct = dct_questions[i_new_id]
        txt_question = dct['question']
    else:
        # we are assuming the page is just being loaded
        # delete any previous chat data
        Chat.objects.all().delete()

        i_new_id = 1
        dct = dct_questions[1]
        txt_question = dct['question']
        txt_error = ''

    dct_response = {'place': i_new_id, 'question': txt_question, 'error': txt_error}
    return render(request, 'chat/index.html', dct_response)


def view(request):
    lst_chat = Chat.objects.all().order_by('id')
    dct_response = {}

    lst_dialog = []
    for i in range(0, len(lst_chat)):
        dct = {}

        dct['question'] = lst_chat[i].question_text
        dct['answer'] = lst_chat[i].question_response

        lst_dialog.append(dct)

    dct_response['dialog'] = lst_dialog
    return render(request, 'chat/view.html', dct_response)


def connect(request):
    dct_response = {}
    return render(request, 'chat/connect.html', dct_response)


def load_default_json():
    # turn the list of questions into a data dict where the key is the id
    fp = open('./testsite/input.json', 'r')
    lst = json.load(fp)
    fp.close()

    dct_full = {}
    for dct in lst:
        id = dct['id']
        dct_full[id] = dct

    return dct_full