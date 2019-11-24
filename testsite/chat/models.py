from django.db import models

import re

# Create your models here.


class Chat(models.Model):
    user_id = models.IntegerField(null=False)
    question_text = models.CharField(max_length=512, null=False)
    question_response = models.CharField(max_length=512, null=False)
    sequence_id = models.IntegerField(null=False)
    next_sequence_id = models.IntegerField(null=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def process_response(self, i_id, txt_response, dct_questions):
        dct = dct_questions[i_id]
        txt_question = dct['question']
        validation = dct['validation']
        paths = dct['paths']

        txt_error = ''
        # questions 1, 2 and 7 follow the same logic
        if 1 == i_id or 2 == i_id or 7 == i_id:
            b_valid, txt_result = Chat.validate_from_list(txt_response, validation)
            if not b_valid:
                # we stay here until we receive input that we can process
                i_next_id = i_id
                txt_error = Chat.error_msg_from_step(i_id)
            else:
                if 7 == i_id:
                    i_next_id = paths
                else:
                    i_next_id = paths[txt_result]

        if 3 == i_id or 5 == i_id or 6 == i_id:
            b_valid = Chat.validate_regexp(txt_response, validation)
            if b_valid:
                i_next_id = paths
            else:
                txt_error = Chat.error_msg_from_step(i_id)
                i_next_id = i_id

        if 4 == i_id:
            b_valid = Chat.validate_name(txt_response, validation)
            if b_valid:
                i_next_id = paths
            else:
                txt_error = Chat.error_msg_from_step(i_id)
                i_next_id = i_id

        if 8 == i_id:
            i_next_id = 9

        self.save_data(txt_question, txt_response, i_id, i_next_id)
        return i_next_id, txt_error

    def save_data(self, txt_question, txt_response, i_id, i_next_id):
        self.user_id = 1
        self.question_text = txt_question
        self.question_response = txt_response
        self.sequence_id = i_id
        self.next_sequence_id = i_next_id

        self.save()

    # static methods
    @staticmethod
    def validate_from_list(txt_response, lst_validation):
        # we know the validation is a list of yes/no
        if txt_response in lst_validation:
            i_index = lst_validation.index(txt_response)
            return True, lst_validation[i_index]

        return False, None

    @staticmethod
    def validate_regexp(txt_response, txt_re):
        result = re.match(txt_re, txt_response)
        if result:
            return True

        return False

    @staticmethod
    def validate_name(txt_response, validation):
        if 0 < len(txt_response):
            return True

        return False

    @staticmethod
    def error_msg_from_step(i_id):
        switcher = {
            1: "Please respond with either 'yes' or 'no'.",
            2: "Please respond with either 'yes' or 'no'.",
            3: "Please provide a valid email address.",
            4: "Please enter your name.",
            5: "Please enter a valid password of six or more characters.",
            6: "Please enter your birth date in the form (mm/dd/yyyy).",
            7: "Please respond with: 'past week', 'past month', or 'longer'?",
        }
        return switcher.get(i_id, "")


